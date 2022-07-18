from Core.Decorator import OTCommand
from Core.Fonctions.Embeds import createEmbed
from Stats.SQL.ConnectSQL import connectSQL

from Titres.Outils import createAccount

dictReverse={300:1,600:2,1000:3,2500:5}
dictValue={1:300,2:600,3:1000,5:2500}

@OTCommand
async def achatTitre(interaction,bot,idtitre,gift):
    nom,valeur,coins=verifAchat(interaction,idtitre,gift)

    connexion,curseur=connectSQL("OT","Titres","Titres",None,None)
    connexionUser,curseurUser=connectSQL("OT",interaction.user.id,"Titres",None,None)
    curseur.execute("UPDATE marketplace SET Stock=Stock-1 WHERE ID={0}".format(idtitre))
    curseurUser.execute("UPDATE coins SET Coins=Coins-{0}".format(valeur))

    if gift!=None:
        assert not gift.bot, "Vous ne pouvez pas offrir de titres à un bot !"
        connexionGift,curseurGift=connectSQL("OT",gift.id,"Titres",None,None)
        curseurGift.execute("INSERT INTO titresUser VALUES({0},'{1}',{2})".format(idtitre,nom,dictReverse[valeur]))
        connexionGift.commit()
    else:
        curseurUser.execute("INSERT INTO titresUser VALUES({0},'{1}',{2})".format(idtitre,nom,dictReverse[valeur]))

    connexion.commit()
    connexionUser.commit()

    if gift!=None:
        embed=createEmbed("Cadeau de Titre","Titre offert avec succès !\n<@{0}> peut équiper **{1}** avec la commande **OT!titre set {2}**.".format(gift.id,nom,idtitre),0xf58d1d,interaction.command.qualified_name,interaction.user)
    else:
        embed=createEmbed("Achat de Titre","Titre acheté avec succès !\nVous pouvez équiper **{0}** avec la commande **OT!titre set {1}**.".format(nom,idtitre),0xf58d1d,interaction.command.qualified_name,interaction.user)

    await interaction.response.send_message(embed=embed)


def verifAchat(interaction,idtitre,gift):
    connexion,curseur=connectSQL("OT","Titres","Titres",None,None)
    titre=curseur.execute("SELECT marketplace.ID,marketplace.Stock,titres.Rareté,titres.Nom FROM marketplace JOIN titres ON marketplace.ID=titres.ID WHERE marketplace.ID={0}".format(idtitre)).fetchone()
    assert titre!=None, "Ce titre n'est actuellement pas en vente !"
    assert titre["Stock"]!=0, "Ce titre n'est plus en stock sur le MarketPlace !"

    connexionUser,curseurUser=connectSQL("OT",interaction.user.id,"Titres",None,None)
    createAccount(connexionUser,curseurUser)
    coins=curseurUser.execute("SELECT * FROM coins").fetchone()["Coins"]
    assert coins>=dictValue[titre["Rareté"]], "Vous n'avez pas assez d'OT Coins pour acheter ce titre !"

    if gift!=None:
        connexionGift,curseurGift=connectSQL("OT",gift.id,"Titres",None,None)
        createAccount(connexionGift,curseurGift)
        assert curseurGift.execute("SELECT * FROM titresUser WHERE ID={0}".format(idtitre)).fetchone()==None, "La personne à qui vous voulez offrir ce titre le possède déjà !"
        if titre["Rareté"]==5:
            assert curseurGift.execute("SELECT COUNT() AS Count FROM titresUser WHERE Rareté=5").fetchone()["Count"]==0, "La personne à qui vous voulez offrir ce titre a déjà un titre de type Unique."
        connexionGift.close()
    else:
        assert curseurUser.execute("SELECT * FROM titresUser WHERE ID={0}".format(idtitre)).fetchone()==None, "Vous possèdez déjà ce titre !"
        if titre["Rareté"]==5:
            assert curseurUser.execute("SELECT COUNT() AS Count FROM titresUser WHERE Rareté=5").fetchone()["Count"]==0, "Vous possèdez déjà un titre Unique, vous ne pouvez donc pas en acheter."

    connexionUser.close()
    connexion.close()
    return titre["Nom"], dictValue[titre["Rareté"]], coins
