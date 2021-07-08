from Core.Fonctions.setMaxPage import setPage
from Core.Reactions.Outils import getTurn, removeReact
from MAL.exeMAL import exeMAL
from Savezvous.ListModo import commandeSV
from Stats.Commandes.Classements import statsRank
from Stats.Commandes.Evol import statsEvol
from Stats.Commandes.Jeux import statsJeux
from Stats.Commandes.Jours import statsJours
from Stats.Commandes.Moyennes import statsMoy
from Stats.Commandes.Periods import statsPeriods
from Stats.Commandes.PeriodsInter import statsPeriodsInter
from Stats.Commandes.Perso import statsPerso
from Stats.Commandes.Random import commandeRandom
from Stats.Commandes.Roles import statsRoles
from Stats.Rapports.exeRapports import changePage, switchRapport
from Stats.RapportsUsers.exeRapports import changePageUser, switchRapportUser
from Stats.SQL.ConnectSQL import connectSQL
from Wikipedia.exeWikipedia import exeWikipedia
import discord
from discord.ext import commands
from Core.OTGuild import OTGuild
from Stats.Commandes.Trivial import statsTrivial

async def reactStats(message:discord.Message,reaction:discord.Reaction,user:discord.Member,bot:commands.Bot,guildOT:OTGuild):
    """Effectue le changement de page pour toutes les commandes du Bot.
    
    Regarde dans la base de données des commandes du serveur si le message est valide et regarde les informations enregistrées.
    
    Ensuite, appelle la fonction adaptée à la commande."""
    connexionCMD,curseurCMD=connectSQL(message.guild.id,"Commandes","Guild",None,None)
    ligne=curseurCMD.execute("SELECT * FROM commandes WHERE MessageID={0}".format(message.id)).fetchone()
    if ligne!=None:
        ctx=await bot.get_context(message)
        if ligne["Commande"]=="rank":
            await statsRank(ctx,ligne["Option"],getTurn(reaction),True,ligne,guildOT,bot)
        elif ligne["Commande"]=="periods":
            await statsPeriods(ctx,ligne["Option"],getTurn(reaction),True,ligne,guildOT,bot)
        elif ligne["Commande"]=="periodsInter":
            await statsPeriodsInter(ctx,ligne["Option"],getTurn(reaction),True,ligne,guildOT,bot)
        elif ligne["Commande"]=="evol":
            await statsEvol(ctx,ligne["Option"],getTurn(reaction),True,ligne,guildOT,bot)
        elif ligne["Commande"]=="perso":
            await statsPerso(ctx,ligne["Option"],getTurn(reaction),True,ligne,guildOT,bot)
        elif ligne["Commande"]=="wikipedia":
            await exeWikipedia(ctx,bot,ligne["Option"],getTurn(reaction),ligne)
        elif ligne["Commande"]=="mal":
            await exeMAL(ctx,bot,ligne["Option"],getTurn(reaction),ligne)
        elif ligne["Commande"]=="moy":
            await statsMoy(ctx,ligne["Option"],getTurn(reaction),True,ligne,guildOT,bot)
        elif ligne["Commande"]=="day":
            await statsJours(ctx,ligne["Option"],getTurn(reaction),True,ligne,guildOT,bot)
        elif ligne["Commande"]=="savezvous":
            await commandeSV(ctx,ligne["Option"],getTurn(reaction),True,ligne,bot)
        elif ligne["Commande"]=="roles":
            await statsRoles(ctx,ligne["Option"],getTurn(reaction),True,ligne,guildOT,bot)
        elif ligne["Commande"]=="jeux":
            await statsJeux(ctx,getTurn(reaction),True,ligne,guildOT,bot,ligne["Args3"])
        elif ligne["Commande"]=="trivial":
            await statsTrivial(ctx,getTurn(reaction),True,ligne,guildOT,bot,ligne["Option"])
        elif ligne["Commande"]=="rapport":
            if reaction.id in (835930140571729941,835928773718835260,835928773740199936,835928773705990154,835928773726699520,835929144579326003,836947337808314389):
                await switchRapport(ctx,reaction.id,ligne,guildOT,bot)
            else:
                await changePage(ctx,getTurn(reaction),ligne,guildOT,bot)
        elif ligne["Commande"]=="rapportUser":
            if reaction.id in (835930140571729941,835928773718835260,835928773740199936,835928773705990154,835928773726699520,835929144579326003,836947337808314389):
                await switchRapportUser(ctx,reaction.id,ligne,guildOT,bot)
            else:
                await changePageUser(ctx,getTurn(reaction),ligne,guildOT,bot)
        elif ligne["Commande"]=="random":
            await commandeRandom(ctx,ligne,True,guildOT,bot)
        await removeReact(message,reaction.id,user)
    else:
        ligne=curseurCMD.execute("SELECT * FROM graphs WHERE MessageID={0}".format(message.id)).fetchone()
        if ligne!=None:
            page=setPage(ligne["Page"],ligne["PageMax"],getTurn(reaction))
            embed=message.embeds[0]
            embed.set_image(url=ligne["Graph{0}".format(page)])
            embed.set_footer(text="Page {0}/{1}".format(page,ligne["PageMax"]))
            curseurCMD.execute("UPDATE graphs SET Page={0} WHERE MessageID={1}".format(page,message.id))
            connexionCMD.commit()
            await message.edit(embed=embed)
            await removeReact(message,reaction.id,user)