from Core.Decorator import OTCommand
from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.GetTable import getTableSV
from Core.Fonctions.SendSlash import sendSlash
from Core.Fonctions.setMaxPage import setMax
from Core.Reactions.exeReactions import ViewControls
from Stats.SQL.ConnectSQL import connectSQL

from Savezvous.ListModoEmbed import embedSV


@OTCommand
async def svPersoModoSlash(interaction,bot,option):
    connexionCMD,curseurCMD=connectSQL(interaction.guild_id,"Commandes","Guild",None,None)
    connexion,curseur=connectSQL(interaction.guild_id,"Guild","Guild",None,None)

    table=getTableSV(curseur,option,interaction.user.id)
    assert table!=[], "Vous devez commencer par ajouter une phrase avec `OT!savezvous add` !"
    pagemax=setMax(len(table))
    curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'savezvous','{2}','None','None','None','None',1,{3},'countDesc',False)".format(interaction.id,interaction.user.id,option,pagemax))
    ligne=curseurCMD.execute("SELECT * FROM commandes WHERE MessageID={0}".format(interaction.id)).fetchone()

    embed=embedSV(table,1,pagemax)
    if option=="perso":
        user=interaction.guild.get_member(ligne["AuthorID"])
        embed=auteur(user.name,user.avatar,embed,"user")
    else:
        embed=auteur(interaction.guild.name,interaction.guild.icon,embed,"guild")

    if pagemax>1:
        await sendSlash(interaction,embed,curseurCMD,connexionCMD,1,pagemax,customView=ViewControls(mobile=False,tri=False,graph=False))
    else:
        await sendSlash(interaction,embed,curseurCMD,connexionCMD,1,pagemax,customView=ViewControls(mobile=False,tri=False,graph=False,droite=False,gauche=False,page=False))
    