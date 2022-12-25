from Core.Fonctions.AuteurIcon import auteur

from Core.Fonctions.Embeds import newDescip
from Core.OTGuild import OTGuild
from FocusTest.EmbedStatus import (embedFocusDevice, embedFocusFreq,
                                   embedFocusGame, embedFocusStatus)
from Stats.Embeds.Divers import embedDivers
from Stats.Embeds.Emotes import embedEmote
from Stats.Embeds.First import embedFirst
from Stats.Embeds.Freq import embedFreq
from Stats.Embeds.Jeux import embedJeux
from Stats.Embeds.Membres import embedMembre
from Stats.Embeds.Mois import embedMois
from Stats.Embeds.Salons import embedSalon
from Stats.Embeds.Serveur import embedServeurs
from Stats.Embeds.Trivialperso import embedTrivialPerso

import discord

dictTriArg={"countAsc":"Count","rankAsc":"Rank","countDesc":"Count","rankDesc":"Rank","dateAsc":"DateID","dateDesc":"DateID","periodAsc":"None","periodDesc":"None","moyDesc":"Moyenne","nombreDesc":"Nombre","winAsc":"W","winDesc":"W","loseAsc":"L","loseDesc":"L","expDesc":"Exp","expAsc":"Exp"}
dictTriSens={"countAsc":"ASC","rankAsc":"ASC","countDesc":"DESC","rankDesc":"DESC","dateAsc":"ASC","dateDesc":"DESC","periodAsc":"None","periodDesc":"None","moyDesc":"DESC","nombreDesc":"DESC","winAsc":"ASC","winDesc":"DESC","loseAsc":"ASC","loseDesc":"DESC","expDesc":"DESC","expAsc":"ASC"}

dictTriField={"countAsc":"Compteur croissant","rankAsc":"Rang croissant","countDesc":"Compteur décroissant","rankDesc":"Rang décroissant","dateAsc":"Date croissante","dateDesc":"Date décroissante","periodAsc":"Date croissante","periodDesc":"Date décroissante","moyDesc":"Moyenne décroissante","nombreDesc":"Compteur décroissant","winAsc":"Victoires croissant","winDesc":"Victoires décroissant","loseAsc":"Défaites croissant","loseDesc":"Défaites décroissant","expDesc":"Expérience décroissant","expAsc":"Expérience croissant"}

liste=["Créé avec amour par OlborEgamorf <3",
"/credits montre la liste de mes contributeurs",
"Invitez moi sur votre serveur avec /invite !",
"Vous avez déjà essayé le /tortues ?",
"Besoin d'aide : /help",
"Vous pouvez me suivre sur Twitter et Instagram !",
"Essayez les graphiques !",
"Si vous aimez mes commandes, parlez de moi autour de vous !",
"Les graphiques ont un Dark Mode !",
"Utilisez '/help jeux' pour voir les jeux dont je dispose !",
"Merci de soutenir le projet <3",
"Regardez comment soutenir le projet avec /support",
"Vous pouvez soumettre des questions pour le /trivial",
"Mon anniversaire est le 15/04/2020",
"Un affichage spécial téléphone existe !"]

async def statsEmbed(interaction:discord.Interaction,guildOT:OTGuild,bot,table:list[dict],ligne:dict,iconAuth:str,title:str,option:str,optionFormat:str,evol=False,obj=None) -> discord.Embed:
    author=ligne["AuthorID"]
    mobile=ligne["Mobile"]
    tri=ligne["Tri"]
    page=ligne["Page"]
    pagemax=ligne["PageMax"]

    if optionFormat == "User":
        embed=embedMembre(table,guildOT,mobile,author,evol,option)
    elif optionFormat == "Salon":
        embed=embedSalon(table,guildOT,mobile,evol,option)
    elif optionFormat == "Freq":
        embed=embedFreq(table,mobile,evol)
    elif optionFormat == "Emote":
        embed=embedEmote(table,bot,mobile,evol)
    elif optionFormat=="Divers":
        embed=embedDivers(table,mobile,evol)
    elif optionFormat=="Mois":
        embed=embedMois(table,mobile,option)
    elif optionFormat == "Jeux":
        embed=embedJeux(table,guildOT,mobile,author,evol,option)
    elif optionFormat=="TrivialPerso":
        embed=embedTrivialPerso(table,mobile)
    elif optionFormat=="Cross":
        embed=embedServeurs(table,guildOT,mobile,evol)
    elif optionFormat=="Status":
        embed=embedFocusStatus(table,mobile,evol)
    elif optionFormat=="Device":
        embed=embedFocusDevice(table,mobile,evol)
    elif optionFormat=="Game":
        embed=embedFocusGame(table,mobile,evol)
    elif optionFormat=="FreqFocus":
        embed=embedFocusFreq(table,mobile)
    elif optionFormat=="First":
        embed=embedFirst(table,ligne["Option"],guildOT,bot,mobile)
    
    embed.add_field(name="Tri <:otTRI:833666016491864114>",value=dictTriField[tri],inline=True)
    embed.set_footer(text="Page {0}/{1} | {2}".format(page,pagemax,"OT Companion Bêta : OT!companion"))

    if obj!=None:
        embed.description=newDescip(embed.description,option,obj,guildOT,bot)

    if iconAuth == "guild":
        embed=auteur(interaction.guild.name,interaction.guild.icon,embed,"guild")
        embed.colour=0x3498db
    else:
        user=interaction.guild.get_member(author)
        if user!=None:
            embed=auteur(user.name,user.avatar,embed,"user")
            embed.colour=user.color.value
        else:
            embed=auteur("Ancien membre",bot.user.avatar,embed,"user")
            embed.colour=0x3498d

    embed.title = title

    return embed
