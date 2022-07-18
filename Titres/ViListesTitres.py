from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.SendView import sendView
from Core.Fonctions.setMaxPage import setMax, setPage
from Titres.Outils import getColorJeux
from Stats.SQL.ConnectSQL import connectSQL

from Titres.ListesEmbed import embedTMP, embedTUser, getTableTitres

dictStatut={0:"Spécial",1:"Basique",2:"Rare",3:"Légendaire",4:"Haut-Fait",5:"Unique",6:"Fabuleux"}
dictSell={0:"Inestimable",1:150,2:300,3:500,4:"Inestimable",5:"Inestimable",6:"Inestimable"}
dictValue={0:"Inestimable",1:300,2:600,3:1000,4:"Inestimable",5:2500,6:"Inestimable"}

async def listesTitresView(interaction,ligne,connexionCMD,curseurCMD,turn):
    connexion,curseur=connectSQL("OT","Titres","Titres",None,None)
    option=ligne["Option"]
    
    table=getTableTitres(curseur,option,ligne["AuthorID"])
    pagemax=setMax(len(table))

    page=setPage(ligne["Page"],pagemax,turn)
    if option=="user":
        embed=embedTUser(table,page,ligne["Mobile"])
        user=interaction.guild.get_member(ligne["AuthorID"])
        embed=auteur(user.name,user.avatar,embed,"user")
    else:
        embed=embedTMP(table,page,ligne["Mobile"])
        embed=auteur("Olbor Track Bot",interaction.guild.get_member(699728606493933650).display_avatar,embed,"user")
    
    if option=="marketplace":
        embed.title="Titres en vente aujourd'hui"
        embed.color=0xf58d1d
    elif option=="user":
        embed.title="Titres en votre possession"
        embed.color=getColorJeux(ligne["AuthorID"])
    else:
        embed.title="Liste des titres existants"
        embed.color=0xf58d1d

    if option=="user":
        connexionUser,curseurUser=connectSQL("OT",ligne["AuthorID"],"Titres",None,None)
        embed.set_footer(text="Page {0}/{1} - Vous avez {2} OT Coins".format(page,pagemax,int(curseurUser.execute("SELECT * FROM coins").fetchone()["Coins"])))
    else:
        embed.set_footer(text="Page {0}/{1}".format(page,pagemax))
    
    await sendView(interaction,embed,curseurCMD,connexionCMD,page,pagemax)
    