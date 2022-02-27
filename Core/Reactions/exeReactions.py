import discord
from Admin.DeleteStats import confirmDel
from Core.Fonctions.Embeds import embedAssertClassic
from Core.OTGuild import OTGuild
from Core.Reactions.ChangePage import reactStats
from Core.Reactions.ChoixPage import choosePage
from Core.Reactions.Graphiques import reactGraph
from Core.Reactions.Mobile import changeMobile
from Core.Reactions.Tri import changeTri
from discord.ext import commands
from Sondages.exePolls import petition, vote


async def exeReactOT(emoji:discord.Reaction, message:int, bot:commands.Bot, guildOT:OTGuild, payload, user):
    """En fonction de la réaction utilisée, dispatche vers quelle fonction se servir pour effectuer l'action."""
    try:
        if emoji.id in (772766034376523776,772766034335236127,772766034356076584,835930140571729941,835928773718835260,835928773740199936,835928773705990154,835928773726699520,835929144579326003,836947337808314389):
            await reactStats(message,emoji,bot,guildOT,payload)
        elif emoji.id==772766034558058506:
            await reactGraph(message,bot,guildOT,payload,emoji)
        elif emoji.id==833666016491864114:
            await changeTri(message,emoji,bot,guildOT,payload)
        elif emoji.id==833736320919797780:
            await changeMobile(message,emoji,bot,guildOT,payload)
        elif emoji.id==866705696505200691:
            ctx=await bot.get_context(message)
            await confirmDel(ctx,user,bot)
        elif emoji.id==887022335578767420:
            await choosePage(message,emoji,bot,guildOT,payload)
        elif emoji.id in (705766186909958185,705766186989912154,705766186930929685,705766186947706934,705766186713088042,705766187182850148,705766187115741246,705766187132256308,705766187145101363,705766186909958206):
            await vote(message,user,emoji)
        elif emoji.id==662410363219738636:
            await petition(message,user)
        else:
            return
    except discord.errors.Forbidden:
        await message.channel.send(embed=embedAssertClassic("Je ne peux pas retirer automatiquement votre réaction ! Donnez moi la permission 'gestion des messages' pour que je puisse le faire et ne plus voir ce message."),delete_after=10)
