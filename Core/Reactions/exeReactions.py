from Core.Reactions.ChangePage import reactStats
from Core.Reactions.Compare import reactCompare
from Core.Reactions.Plus import reactPlus
from Core.Reactions.Tri import changeTri
from Core.Reactions.Mobile import changeMobile
from Core.Reactions.Graphiques import reactGraph
import discord
from discord.ext import commands
from Core.OTGuild import OTGuild

async def exeReactOT(emoji:discord.Reaction, message:discord.Message, user:discord.Member, bot:commands.Bot, guildOT:OTGuild):
    """En fonction de la réaction utilisée, dispatche vers quelle fonction se servir pour effectuer l'action."""
    
    if emoji.id in (772766034376523776,772766034335236127,772766034356076584,835930140571729941,835928773718835260,835928773740199936,835928773705990154,835928773726699520,835929144579326003,836947337808314389):
        await reactStats(message,emoji,user,bot,guildOT)
    elif emoji.id==772766034558058506:
        await reactGraph(message,bot,guildOT)
        await message.clear_reaction(emoji)
    elif emoji.id==772766033996021761:
        await reactCompare(message,user)
    elif emoji.id==772766034163400715:
        await reactPlus(message,user)
        await message.clear_reaction(emoji)
    elif emoji.id==833666016491864114:
        await changeTri(message,emoji,user,bot,guildOT)
    elif emoji.id==833736320919797780:
        await changeMobile(message,emoji,user,bot,guildOT)
    else:
        return