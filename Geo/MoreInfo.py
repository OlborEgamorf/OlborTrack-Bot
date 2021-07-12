import json
import discord
from Core.Fonctions.AuteurIcon import auteur

async def embedMoreGeo(arg) -> discord.Embed:
    """Donne plus d'informations sur une localisation observée avec la commande iss ou geosearch.
    
    Mis en forme dans un embed qui est renvoyé."""
    with open("JSON/"+str(arg[0])+str(arg[1])+".json") as json_file:
        table=json.load(json_file)
    embedP=discord.Embed(title=table["results"][0]["formatted"],color=0xa83e32)
    descip=""
    listeDetails=["state","county","suburb"]
    for i in listeDetails:
        try:
            descip+=table["results"][0]["components"][i]+"\n"
        except:
            pass
    if descip!="":
        embedP.add_field(name="Détails lieu",value=descip,inline=True)
    try:
        embedP.add_field(name="Union politique",value=table["results"][0]["components"]["political_union"],inline=True)
    except:
        pass
    try:
        embedP.add_field(name="Drapeau",value=table["results"][0]["annotations"]["flag"],inline=True)
    except:
        pass
    try:
        embedP.add_field(name="Monnaie",value=table["results"][0]["annotations"]["currency"]["name"]+" ("+table["results"][0]["annotations"]["currency"]["symbol"]+")",inline=True)
    except:
        pass
    try:
        embedP.add_field(name="Fuseau horaire",value=table["results"][0]["annotations"]["timezone"]["name"]+" ("+table["results"][0]["annotations"]["timezone"]["offset_string"]+")",inline=True)
    except:
        pass
    try:
        embedP.add_field(name="Circulation",value=table["results"][0]["annotations"]["roadinfo"]["drive_on"]+" - "+table["results"][0]["annotations"]["roadinfo"]["speed_in"],inline=True)
    except:
        pass
    embedP.set_footer(text="OT!iss / OT!geosearch")
    embedP=auteur(0,0,0,embedP,"map")
    return embedP