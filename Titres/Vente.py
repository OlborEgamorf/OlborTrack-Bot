from Core.Decorator import OTCommand
from Core.Fonctions.Embeds import createEmbed
from Stats.SQL.ConnectSQL import connectSQL

from Titres.Outils import createAccount

dictSell={0:"Inestimable",1:150,2:300,3:500,4:"Inestimable",5:"Inestimable",6:"Inestimable"}

@OTCommand
async def venteTitre(interaction,bot,idtitre):
    nom,valeur,coins=verifVente(interaction.user.id,idtitre)

    connexion,curseur=connectSQL("OT","Titres","Titres",None,None)
    connexionUser,curseurUser=connectSQL("OT",interaction.user.id,"Titres",None,None)
    if curseur.execute("SELECT * FROM marketplace WHERE ID={0}".format(idtitre)).fetchone()==None:
        curseur.execute("INSERT INTO marketplace VALUES({0},0,1)".format(idtitre))
    curseur.execute("UPDATE marketplace SET Stock=Stock+1 WHERE ID={0}".format(idtitre))
    curseurUser.execute("UPDATE coins SET Coins=Coins+{0}".format(valeur))
    curseurUser.execute("DELETE FROM titresUser WHERE ID={0}".format(idtitre))

    connexion.commit()
    connexionUser.commit()

    embed=createEmbed("Vente de Titre","Titre **{0}** vendu avec succès !\nVous possèdez désormais **{1} <:otCOINS:873226814527520809>**.".format(nom,int(coins+valeur)),0xf58d1d,interaction.command.qualified_name,interaction.user)
    await interaction.response.send_message(embed=embed)

def verifVente(user,idtitre):
    connexion,curseur=connectSQL("OT","Titres","Titres",None,None)
    connexionUser,curseurUser=connectSQL("OT",user,"Titres",None,None)
    createAccount(connexionUser,curseurUser)

    titre=curseurUser.execute("SELECT * FROM titresUser WHERE ID={0}".format(idtitre)).fetchone()
    assert titre!=None, "Vous ne possèdez pas ce titre."
    assert titre["Rareté"] not in (0,4,5,6), "Vous ne pouvez vendre ou échanger ce titre."
    membre=curseur.execute("SELECT * FROM active WHERE MembreID={0}".format(user)).fetchone()
    if membre!=None:
        assert membre["TitreID"]!=int(idtitre), "Le titre que vous voulez vendre est celui qui est actuellement équipé pour vous."

    coins=curseurUser.execute("SELECT * FROM coins").fetchone()["Coins"]

    connexionUser.close()
    connexion.close()
    return titre["Nom"], dictSell[titre["Rareté"]], coins
