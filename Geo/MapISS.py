from Core.Fonctions.WebRequest import webRequest
from Stats.Graphiques.Carte import graphMap
import json
from Core.OS.Keys3 import opencageKey
import discord


async def embedISS(ctx):
    tableLieu=await webRequest("http://api.open-notify.org/iss-now.json")
    arg="{0} {1}".format(tableLieu["iss_position"]["latitude"],tableLieu["iss_position"]["longitude"])
    table=await webRequest("https://api.opencagedata.com/geocode/v1/json?key="+opencageKey+"&language=fr&limit=1&q="+arg)
    with open("JSON/{0}{1}.json".format(table["results"][0]["geometry"]["lat"],table["results"][0]["geometry"]["lng"]),"w") as outfile:
        json.dump(table,outfile)
    
    geojson={"type": "FeatureCollection","features": [{"type": "Feature","properties": {},"geometry": {"type": "Point","coordinates": [float(tableLieu["iss_position"]["longitude"]),float(tableLieu["iss_position"]["latitude"])]}}]}

    with open("GeoJson/iss.geo.json".format(table["results"][0]["geometry"]["lat"],table["results"][0]["geometry"]["lng"]),"w") as outfile:
        json.dump(geojson,outfile)

    graphMap(table)
    try:
        contenu=table["results"][0]["annotations"]["flag"]+" "+str(table["results"][0]["geometry"]["lat"])+" "+str(table["results"][0]["geometry"]["lng"])
    except:
        contenu=":map: "+str(table["results"][0]["geometry"]["lat"])+" "+str(table["results"][0]["geometry"]["lng"])
    
    message=await ctx.send(content=contenu, file=discord.File("Graphs/map.png"))
    await message.add_reaction("<:otPLUS:772766034163400715>")