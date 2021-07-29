from Stats.SQL.ConnectSQL import connectSQL
from Core.Reactions.ChangePage import reactStats
import discord
from discord.ext import commands
from Core.OTGuild import OTGuild

async def changeMobile(message:int,reaction:discord.Reaction,bot:commands.Bot,guildOT:OTGuild,payload):
    """Chnage l'affichage d'une commande pour le passer en version mobile"""
    connexionCMD,curseurCMD=connectSQL(guildOT.id,"Commandes","Guild",None,None)
    ligne=curseurCMD.execute("SELECT * FROM commandes WHERE MessageID={0}".format(message)).fetchone()
    if ligne!=None:
        curseurCMD.execute("UPDATE commandes SET Mobile={0} WHERE MessageID={1}".format(bool(int(ligne["Mobile"])-1),message))
        connexionCMD.commit()
        await reactStats(message,reaction,bot,guildOT,payload)