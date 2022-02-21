import discord
from Autre.Events import exeWikipedia
from Autre.Help import commandeHelp
from Core.Fonctions.SeekMessage import seekMessage
from Core.Fonctions.setMaxPage import setPage
from Core.OTGuild import OTGuild
from Core.Reactions.Outils import getTurn, removeReact
from discord.ext import commands
from Savezvous.ListModo import commandeSV
from Sondages.GAReroll import commandeGAR
from Stats.Commandes.Classements import statsRank
from Stats.Commandes.Evol import statsEvol
from Stats.Commandes.First import statsFirstPeriods
from Stats.Commandes.Jeux import statsJeux
from Stats.Commandes.Jours import statsJours
from Stats.Commandes.Moyennes import statsMoy
from Stats.Commandes.Periods import statsPeriods
from Stats.Commandes.PeriodsInter import statsPeriodsInter
from Stats.Commandes.Perso import statsPerso
from Stats.Commandes.Random import commandeRandom
from Stats.Commandes.Roles import statsRoles
from Stats.Commandes.Trivial import statsTrivial
from Stats.Rapports.exeRapports import changePage, switchRapport
from Stats.RapportsUsers.exeRapports import changePageUser, switchRapportUser
from Stats.SQL.ConnectSQL import connectSQL
from Titres.Listes import commandeTMP

from Outils.Bienvenue.Listes import commandeImageBV, commandeMessBV
from Outils.Tableaux.EmbedsTab import commandeSB
from Outils.Twitch.ExeTwitch import commandeTwitch


async def reactStats(message:int,reaction:discord.Reaction,bot:commands.Bot,guildOT:OTGuild,payload):
    """Effectue le changement de page pour toutes les commandes du Bot.
    
    Regarde dans la base de données des commandes du serveur si le message est valide et regarde les informations enregistrées.
    
    Ensuite, appelle la fonction adaptée à la commande."""
    connexionCMD,curseurCMD=connectSQL(guildOT.id,"Commandes","Guild",None,None)
    ligne=curseurCMD.execute("SELECT * FROM commandes WHERE MessageID={0}".format(message)).fetchone()
    if ligne!=None:
        message,user=await seekMessage(bot,payload)
        if message==None:
            return
        ctx=await bot.get_context(message)

        if ligne["Commande"] in ("rank","periods","periodsInter","evol","perso","moy","day","roles","compareUser","comparePerso","compareRank","compareServ","first"):
            dictFonction={
                "rank":statsRank,"periods":statsPeriods,"periodsInter":statsPeriodsInter,"evol":statsEvol,"perso":statsPerso,"moy":statsMoy,
                "day":statsJours,"roles":statsRoles,"first":statsFirstPeriods
                }
            await dictFonction[ligne["Commande"]](ctx,ligne["Option"],getTurn(reaction),True,ligne,guildOT,bot)

        elif ligne["Commande"] in ("savezvous","imagesBV","messagesBV"):
            dictFonction={"savezvous":commandeSV,"imagesBV":commandeImageBV,"messagesBV":commandeMessBV}
            await dictFonction[ligne["Commande"]](ctx,ligne["Option"],getTurn(reaction),True,ligne,bot)

        elif ligne["Commande"] in ("tableau","twitch"):
            dictFonction={"tableau":commandeSB,"twitch":commandeTwitch}
            await dictFonction[ligne["Commande"]](ctx,getTurn(reaction),True,ligne,bot,guildOT,None)

        elif ligne["Commande"]=="wikipedia":
            await exeWikipedia(ctx,bot,ligne["Args1"],ligne)
        elif ligne["Commande"]=="jeux":
            await statsJeux(ctx,getTurn(reaction),True,ligne,guildOT,bot,ligne["Args3"])
        elif ligne["Commande"]=="trivial":
            await statsTrivial(ctx,getTurn(reaction),True,ligne,bot,ligne["Option"])
        elif ligne["Commande"]=="gareroll":
            await commandeGAR(ctx,getTurn(reaction),True,ligne)
        elif ligne["Commande"]=="help":
            await commandeHelp(ctx,getTurn(reaction),True,ligne,bot,guildOT)
        elif ligne["Commande"]=="titres":
            await commandeTMP(ctx,getTurn(reaction),True,ligne,ligne["Option"])
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
        ligne=curseurCMD.execute("SELECT * FROM graphs WHERE MessageID={0}".format(message)).fetchone()
        if ligne!=None:
            message,user=await seekMessage(bot,payload)
            page=setPage(ligne["Page"],ligne["PageMax"],getTurn(reaction))
            embed=message.embeds[0]
            embed.set_image(url=ligne["Graph{0}".format(page)])
            embed.set_footer(text="Page {0}/{1}".format(page,ligne["PageMax"]))
            curseurCMD.execute("UPDATE graphs SET Page={0} WHERE MessageID={1}".format(page,message.id))
            connexionCMD.commit()
            await message.edit(embed=embed)
            await removeReact(message,reaction.id,user)
