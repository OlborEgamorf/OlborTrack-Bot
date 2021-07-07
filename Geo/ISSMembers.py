import discord
from Core.Fonctions.WebRequest import webRequest
from Core.Fonctions.AuteurIcon import auteur


async def embedISSMembers() -> discord.Embed :
    """Se sert de l'API de Open Notify pour obtenir la liste des personnes actuellement dans l'ISS.
    
    Renvoie la liste dans un embed"""
    table=await webRequest("http://api.open-notify.org/astros.json")
    descip=""
    for i in table["people"]:
        descip+=i["name"]+"\n"
    embedP=discord.Embed(title="Il y a "+str(table["number"])+" personnes dans l'ISS :",description=descip,color=0xa83e32)
    embedP.set_footer(text="OT!issmembers")
    embedP=auteur("http://api.open-notify.org/astros.json",0,0,embedP,"nasa")
    return embedP