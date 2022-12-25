from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.GetTable import getTableSV
from Core.Fonctions.SendView import sendView
from Core.Fonctions.setMaxPage import setMax
from Core.Fonctions.setMaxPage import setPage
from Stats.SQL.ConnectSQL import connectSQL

from Savezvous.ListModoEmbed import embedSV

async def svPersoModoView(interaction,bot,ligne,connexionCMD,curseurCMD,turn):
    connexion,curseur=connectSQL(interaction.guild_id)

    option=ligne["Option"]
    table=getTableSV(curseur,option,ligne["AuthorID"])
    pagemax=setMax(len(table))

    page=setPage(ligne["Page"],pagemax,turn)
    option=ligne["Option"]

    embed=embedSV(table,page,pagemax)
    if option=="perso":
        user=interaction.guild.get_member(ligne["AuthorID"])
        embed=auteur(user.name,user.avatar,embed,"user")
    else:
        embed=auteur(interaction.guild.name,interaction.guild.icon,embed,"guild")

    await sendView(interaction,embed,curseurCMD,connexionCMD,page,pagemax)