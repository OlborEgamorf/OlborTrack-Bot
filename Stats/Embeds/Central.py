from Core.Fonctions.DichoTri import triPeriod
from Stats.Embeds.Salons import embedSalon
from Stats.Embeds.Freq import embedFreq
from Stats.Embeds.Emotes import embedEmote
from Stats.Embeds.Divers import embedDivers
from Stats.Embeds.Moyennes import embedMoy
from Stats.Embeds.Membres import embedMembre
from Stats.Embeds.Mois import embedMois
from Stats.Embeds.Evol import embedEvol
from Stats.Embeds.Jeux import embedJeux
dictTriArg={"countAsc":"Count","rankAsc":"Rank","countDesc":"Count","rankDesc":"Rank","dateAsc":"DateID","dateDesc":"DateID","periodAsc":"None","periodDesc":"None","moyDesc":"Moyenne","nombreDesc":"Nombre","winAsc":"W","winDesc":"W","loseAsc":"L","loseDesc":"L"}
dictTriSens={"countAsc":"ASC","rankAsc":"ASC","countDesc":"DESC","rankDesc":"DESC","dateAsc":"ASC","dateDesc":"DESC","periodAsc":"None","periodDesc":"None","moyDesc":"DESC","nombreDesc":"DESC","winAsc":"ASC","winDesc":"DESC","loseAsc":"ASC","loseDesc":"DESC"}

async def statsEmbed(nom,ligne,page,pagemax,option,guildOT,bot,evol,collapse,curseur):
    author=ligne["AuthorID"]
    mobile=ligne["Mobile"]
    tri=ligne["Tri"]

    if tri in ("periodAsc","periodDesc"):
        table=triPeriod(curseur,nom,tri)
    else:
        table=curseur.execute("SELECT * FROM {0} ORDER BY {1} {2}".format(nom,dictTriArg[tri],dictTriSens[tri])).fetchall()

    if option in ("Voice","Messages","Mots","Mentions","Mentionne"):
        embed=embedMembre(table,guildOT,page,mobile,author,evol,option)
    elif option in ("Salons","Voicechan"):
        embed=embedSalon(table,guildOT,page,mobile,evol,option)
    elif option=="Freq":
        embed=embedFreq(table,page,mobile,evol)
    elif option in ("Emotes","Reactions"):
        embed=embedEmote(table,bot,page,mobile,evol)
    elif option=="Divers":
        embed=embedDivers(table,page,mobile,evol)
    elif option=="Mois":
        embed=embedMois(table,page,mobile,ligne["Option"])
    elif option=="Evol":
        embed=embedEvol(table,page,mobile,collapse,evol,ligne["Option"])
    elif option=="Moy":
        embed=embedMoy(table,page,mobile)
    elif option in ("tortues","tortuesduo","p4","bn","trivialversus","trivialbr","trivialparty"):
        embed=embedJeux(table,guildOT,page,mobile,author,evol,option)
    
    embed.set_footer(text="Page {0}/{1}".format(page,pagemax))
    return embed