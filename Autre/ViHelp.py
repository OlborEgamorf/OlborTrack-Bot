from Core.Fonctions.SendView import sendView
from Core.Fonctions.setMaxPage import setPage

from Autre.EmbedHelp import embedHelp


async def commandeHelpView(interaction,curseurCMD,connexionCMD,turn,ligne,guildOT,bot):
    option=ligne["Option"]
    page=setPage(ligne["Page"],ligne["PageMax"],turn)
    embed,pagemax=embedHelp(option,guildOT,page,bot)
    await sendView(interaction,embed,curseurCMD,connexionCMD,page,pagemax)
