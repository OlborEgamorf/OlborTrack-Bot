import asyncio

from Core.Fonctions.Embeds import createEmbed, embedAssert
from Stats.SQL.ConnectSQL import connectSQL

from Titres.Outils import createAccount

dictReverse={300:1,600:2,1000:3,2500:5}
dictValue={1:300,2:600,3:1000,5:2500}

async def achatTitre(ctx,idtitre,bot,gift):
    try:
        def checkValid(reaction,user):
            if type(reaction.emoji)==str:
                return False
            return reaction.emoji.id==772766033996021761 and reaction.message.id==message.id and user.id==ctx.author.id

        if gift:
            assert len(ctx.message.mentions)!=0, "Si vous voulez offrir un titre à quelqu'un, vous devez le mentionner."
        nom,valeur,coins=verifAchat(ctx,idtitre,gift)

        if gift:
            embed=createEmbed("Cadeau de Titre","Vous êtes sur le point d'offrir **{0}** pour *{1} <:otCOINS:873226814527520809>* à <@{2}>.\nVous possèdez {3} <:otCOINS:873226814527520809> au total et en aurez {4} <:otCOINS:873226814527520809> après la transaction.\nAppuyez sur <:otVALIDER:772766033996021761> pour confirmer l'achat.".format(nom,valeur,ctx.message.mentions[0].id,int(coins),int(coins-valeur)),0xf58d1d,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.author)
        else:
            embed=createEmbed("Achat de Titre","Vous êtes sur le point d'acheter **{0}** pour *{1} <:otCOINS:873226814527520809>*.\nVous possèdez {2} <:otCOINS:873226814527520809> au total et en aurez {3} <:otCOINS:873226814527520809> après la transaction.\nAppuyez sur <:otVALIDER:772766033996021761> pour confirmer l'achat.".format(nom,valeur,int(coins),int(coins-valeur)),0xf58d1d,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.author)

        message=await ctx.reply(embed=embed)
        await message.add_reaction("<:otVALIDER:772766033996021761>")

        reaction,user=await bot.wait_for('reaction_add', check=checkValid, timeout=60)
        await message.clear_reactions()
        nom,valeur,coins=verifAchat(ctx,idtitre,gift)

        connexion,curseur=connectSQL("OT","Titres","Titres",None,None)
        connexionUser,curseurUser=connectSQL("OT",ctx.author.id,"Titres",None,None)
        curseur.execute("UPDATE marketplace SET Stock=Stock-1 WHERE ID={0}".format(idtitre))
        curseurUser.execute("UPDATE coins SET Coins=Coins-{0}".format(valeur))

        if gift:
            connexionGift,curseurGift=connectSQL("OT",ctx.message.mentions[0].id,"Titres",None,None)
            curseurGift.execute("INSERT INTO titresUser VALUES({0},'{1}',{2})".format(idtitre,nom,dictReverse[valeur]))
            connexionGift.commit()
        else:
            curseurUser.execute("INSERT INTO titresUser VALUES({0},'{1}',{2})".format(idtitre,nom,dictReverse[valeur]))

        connexion.commit()
        connexionUser.commit()

        if gift:
            embed=createEmbed("Cadeau de Titre","Titre offert avec succès !\n<@{0}> peut équiper **{1}** avec la commande **OT!titre set {2}**.".format(ctx.message.mentions[0].id,nom,idtitre),0xf58d1d,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.author)
        else:
            embed=createEmbed("Achat de Titre","Titre acheté avec succès !\nVous pouvez équiper **{0}** avec la commande **OT!titre set {1}**.".format(nom,idtitre),0xf58d1d,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.author)

        await message.reply(embed=embed)
    except asyncio.exceptions.TimeoutError:
        await embedAssert(ctx,"Une minute s'est écoulée et vous n'avez pas confirmé l'activation. L'opération a été annulée",True)
        await message.clear_reactions()


def verifAchat(ctx,idtitre,gift):
    connexion,curseur=connectSQL("OT","Titres","Titres",None,None)
    titre=curseur.execute("SELECT marketplace.ID,marketplace.Stock,titres.Rareté,titres.Nom FROM marketplace JOIN titres ON marketplace.ID=titres.ID WHERE marketplace.ID={0}".format(idtitre)).fetchone()
    assert titre!=None, "Ce titre n'est actuellement pas en vente !"
    assert titre["Stock"]!=0, "Ce titre n'est plus en stock sur le MarketPlace !"

    connexionUser,curseurUser=connectSQL("OT",ctx.author.id,"Titres",None,None)
    createAccount(connexionUser,curseurUser)
    coins=curseurUser.execute("SELECT * FROM coins").fetchone()["Coins"]
    assert coins>=dictValue[titre["Rareté"]], "Vous n'avez pas assez d'OT Coins pour acheter ce titre !"

    if gift:
        connexionGift,curseurGift=connectSQL("OT",ctx.message.mentions[0].id,"Titres",None,None)
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
