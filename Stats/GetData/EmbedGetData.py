from time import time

from Core.Fonctions.Embeds import createEmbed
from Core.Fonctions.TempsVoice import tempsVoice

def embedStatut(embedOri,texte,tempsI,tempsT,guild):
    etape,temps,total="","",""
    embed=createEmbed("OlborTrack GetData - Statut","L'opération est en cours. Aucun message envoyé pendant ne sera compté dans les stats. Votre serveur a été placé sous maintenance.",0x220cc9,"getdata",guild)
    if embedOri!=None:
        etape=embedOri.fields[0].value
        temps=embedOri.fields[1].value
        total=embedOri.fields[2].value
    if len(texte)>25:
        etape+="\n{0}...".format(texte[0:25])
    else:
        etape+="\n{0}".format(texte)
    temps+="\n"+tempsVoice(int(time()-tempsI))
    total+="\n"+tempsVoice(int(time()-tempsT))
    embed.add_field(name="Etapes",value=etape)
    embed.add_field(name="Temps",value=temps)
    embed.add_field(name="Total",value=total)
    if len(embed.fields[0])>=1024:
        embed=embedOri
    return embed
