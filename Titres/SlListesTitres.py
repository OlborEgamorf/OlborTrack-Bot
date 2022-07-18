from Core.Decorator import OTCommand
from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.SendSlash import sendSlash
from Core.Fonctions.setMaxPage import setMax
from Core.Reactions.exeReactions import ViewControls
from Stats.SQL.ConnectSQL import connectSQL

from Titres.ListesEmbed import embedTMP, embedTUser, getTableTitres
from Titres.Outils import getColorJeux


@OTCommand
async def listesTitresSlash(interaction,bot,option):
    connexionCMD,curseurCMD=connectSQL(interaction.guild_id,"Commandes","Guild",None,None)
    connexion,curseur=connectSQL("OT","Titres","Titres",None,None)

    table=getTableTitres(curseur,option,interaction.user.id)
    assert table!=[], "Cette liste est vide."
    pagemax=setMax(len(table))
    curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'titres','{2}','None','None','None','None',1,{3},'countDesc',False)".format(interaction.id,interaction.user.id,option,pagemax))
    ligne=curseurCMD.execute("SELECT * FROM commandes WHERE MessageID={0}".format(interaction.id)).fetchone()

    page=1

    if option=="user":
        embed=embedTUser(table,page,ligne["Mobile"])
        embed=auteur(interaction.user.name,interaction.user.display_avatar,embed,"user")
    else:
        embed=embedTMP(table,page,ligne["Mobile"])
        embed=auteur("Olbor Track Bot",interaction.guild.get_member(699728606493933650).display_avatar,embed,"user")
    
    if option=="marketplace":
        embed.title="Titres en vente aujourd'hui"
        embed.color=0xf58d1d
    elif option=="user":
        embed.title="Titres en votre possession"
        embed.color=getColorJeux(interaction.user.id)
    else:
        embed.title="Liste des titres existants"
        embed.color=0xf58d1d
    

    if option=="user":
        connexionUser,curseurUser=connectSQL("OT",ligne["AuthorID"],"Titres",None,None)
        embed.set_footer(text="Page {0}/{1} - Vous avez {2} OT Coins".format(page,pagemax,int(curseurUser.execute("SELECT * FROM coins").fetchone()["Coins"])))
    else:
        embed.set_footer(text="Page {0}/{1}".format(page,pagemax))
    
    if pagemax>1:
        await sendSlash(interaction,embed,curseurCMD,connexionCMD,1,pagemax,customView=ViewControls(tri=False,graph=False))
    else:
        await sendSlash(interaction,embed,curseurCMD,connexionCMD,1,pagemax,customView=ViewControls(tri=False,graph=False,droite=False,gauche=False,page=False))

    
