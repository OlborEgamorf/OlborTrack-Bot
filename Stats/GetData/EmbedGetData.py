import discord
from time import time
from Core.Fonctions.TempsVoice import tempsVoice
from Core.Fonctions.AuteurIcon import auteur

def embedCreate(embedOri,texte,tempsI,tempsT,guild):
    etape,temps,total="","",""
    embedT=discord.Embed(title="OlborTrack GetData - Statut", description="L'opération est en cours. Aucun message envoyé pendant ne sera compté dans les stats. Votre serveur a été placé sous maintenance.", color=0x220cc9)
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
    embedT.add_field(name="Etapes",value=etape)
    embedT.add_field(name="Temps",value=temps)
    embedT.add_field(name="Total",value=total)
    embedT.set_footer(text="OT!getdata")
    embedT=auteur(guild.id,guild.name,guild.icon,embedT,"guild")
    if len(embedT.fields[0])>=1024:
        embedT=embedOri
    return embedT