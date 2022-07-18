from random import choice

from Core.Fonctions.DichoTri import triPeriod
from FocusTest.EmbedStatus import (embedFocusDevice, embedFocusFreq,
                                   embedFocusGame, embedFocusStatus)
from Stats.Embeds.Divers import embedDivers
from Stats.Embeds.Emotes import embedEmote
from Stats.Embeds.Evol import embedEvol
from Stats.Embeds.First import embedFirst
from Stats.Embeds.Freq import embedFreq
from Stats.Embeds.Jeux import embedJeux
from Stats.Embeds.Membres import embedMembre
from Stats.Embeds.Mois import embedMois
from Stats.Embeds.Moyennes import embedMoy
from Stats.Embeds.Salons import embedSalon
from Stats.Embeds.Serveur import embedServeurs
from Stats.Embeds.Trivialperso import embedTrivialPerso

dictTriArg={"countAsc":"Count","rankAsc":"Rank","countDesc":"Count","rankDesc":"Rank","dateAsc":"DateID","dateDesc":"DateID","periodAsc":"None","periodDesc":"None","moyDesc":"Moyenne","nombreDesc":"Nombre","winAsc":"W","winDesc":"W","loseAsc":"L","loseDesc":"L","expDesc":"Exp","expAsc":"Exp"}
dictTriSens={"countAsc":"ASC","rankAsc":"ASC","countDesc":"DESC","rankDesc":"DESC","dateAsc":"ASC","dateDesc":"DESC","periodAsc":"None","periodDesc":"None","moyDesc":"DESC","nombreDesc":"DESC","winAsc":"ASC","winDesc":"DESC","loseAsc":"ASC","loseDesc":"DESC","expDesc":"DESC","expAsc":"ASC"}

dictTriField={"countAsc":"Compteur croissant","rankAsc":"Rang croissant","countDesc":"Compteur décroissant","rankDesc":"Rang décroissant","dateAsc":"Date croissante","dateDesc":"Date décroissante","periodAsc":"Date croissante","periodDesc":"Date décroissante","moyDesc":"Moyenne décroissante","nombreDesc":"Compteur décroissant","winAsc":"Victoires croissant","winDesc":"Victoires décroissant","loseAsc":"Défaites croissant","loseDesc":"Défaites décroissant","expDesc":"Expérience décroissant","expAsc":"Expérience croissant"}

liste=["Créé avec amour par OlborEgamorf <3",
"OT!credits montre la liste de mes contributeurs",
"Invitez moi sur votre serveur avec OT!invite !",
"Vous avez déjà essayé le OT!tortues ?",
"Besoin d'aide : OT!help",
"Un commentaire à faire ? Utilisez OT!feedback",
"Vous pouvez me suivre sur Twitter et Instagram !",
"Essayez les graphiques !",
"Si vous aimez mes commandes, parlez de moi autour de vous !",
"On vous a déjà parlé des graphiques animés ?",
"Les graphiques ont un Dark Mode !",
"Utilisez 'OT!help jeux' pour voir les jeux dont je dispose !",
"Merci de soutenir le projet <3",
"Regardez comment soutenir le projet avec OT!support",
"Vous pouvez soumettre des questions pour le OT!trivial",
"Mon anniversaire est le 15/04/2020",
"Je possède des commandes de comparaison de stats !",
"Les commandes d'évolutions sont intéressantes...",
"Un affichage spécial téléphone existe !"]

async def statsEmbed(nom,ligne,page,pagemax,option,guildOT,bot,evol,collapse,curseur):
    author=ligne["AuthorID"]
    mobile=ligne["Mobile"]
    tri=ligne["Tri"]

    if tri in ("periodAsc","periodDesc"):
        table=triPeriod(curseur,nom,tri)
    else:
        table=curseur.execute("SELECT * FROM {0} ORDER BY {1} {2} LIMIT 15 OFFSET {3}".format(nom,dictTriArg[tri],dictTriSens[tri],15*(page-1))).fetchall()

    if option in ("Voice","Messages","Mots","Mentions","Mentionne"):
        embed=embedMembre(table,guildOT,mobile,author,evol,option)
    elif option in ("Salons","Voicechan"):
        embed=embedSalon(table,guildOT,mobile,evol,option)
    elif option=="Freq":
        embed=embedFreq(table,mobile,evol)
    elif option in ("Emotes","Reactions"):
        embed=embedEmote(table,bot,mobile,evol)
    elif option=="Divers":
        embed=embedDivers(table,mobile,evol)
    elif option=="Mois":
        embed=embedMois(table,mobile,ligne["Option"])
    elif option=="Evol":
        embed=embedEvol(table,mobile,collapse,evol,ligne["Option"])
    elif option=="Moy":
        embed=embedMoy(table,mobile)
    elif option in ("Tortues","TortuesDuo","P4","TrivialVersus","TrivialBR","TrivialParty","trivial","CodeNames","Morpion","BatailleNavale"):
        embed=embedJeux(table,guildOT,mobile,author,evol,option)
    elif option=="trivialperso":
        embed=embedTrivialPerso(table,mobile)
    elif option=="cross":
        embed=embedServeurs(table,guildOT,mobile,evol)
    elif option=="Status":
        embed=embedFocusStatus(table,mobile,evol)
    elif option=="Device":
        embed=embedFocusDevice(table,mobile,evol)
    elif option=="Game":
        embed=embedFocusGame(table,mobile,evol)
    elif option=="FreqFocus":
        embed=embedFocusFreq(table,mobile)
    elif option=="First":
        embed=embedFirst(table,ligne["Option"],guildOT,bot,mobile)
    
    embed.add_field(name="Tri <:otTRI:833666016491864114>",value=dictTriField[tri],inline=True)
    embed.set_footer(text="Page {0}/{1} | {2}".format(page,pagemax,"OT Companion Bêta : OT!companion"))
    return embed
