from Core.Decorator import OTCommand
from Core.Fonctions.SendSlash import sendSlash
from Core.Reactions.exeReactions import ViewControls
from Stats.SQL.ConnectSQL import connectSQL

from Autre.EmbedHelp import embedHelp


@OTCommand
async def commandeHelpSlash(interaction,bot,option,guildOT):
    connexionCMD,curseurCMD=connectSQL(guildOT.id)

    if option==None:
        option="home"
    else:
        option=option.value

    curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'help','{2}','None','None','None','None',1,99,'countDesc',False)".format(interaction.id,interaction.user.id,option))

    embed,pagemax=embedHelp(option,guildOT,1,bot)

    if pagemax>1:
        await sendSlash(interaction,embed,curseurCMD,connexionCMD,1,pagemax,customView=ViewControls(tri=False,graph=False,mobile=False))
    else:
        await sendSlash(interaction,embed,curseurCMD,connexionCMD,1,pagemax,customView=ViewControls(tri=False,graph=False,droite=False,gauche=False,page=False,mobile=None))

