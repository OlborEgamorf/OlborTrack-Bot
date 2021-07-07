import discord
from Core.OS.Keys3 import NASAKey
from Core.Fonctions.WebRequest import webRequest
from Core.Fonctions.AuteurIcon import auteur

async def embedMeteoMars() -> discord.Embed:
    """Se sert de l'API de la NASA pour obtenir la météo sur Mars.
    
    Met les informations en forme dans un embed.
    
    Renvoie l'embed en question."""
    table=await webRequest("https://api.nasa.gov/insight_weather/?api_key="+NASAKey+"&feedtype=json&ver=1.0")
    key=table["sol_keys"][len(table["sol_keys"])-1]
    embedP=discord.Embed(title="Météo sur Mars - Sol "+key,color=0xa83e32)
    embedP.set_footer(text="OT!meteomars")
    try:
        embedP.add_field(name="Température",value="Minimale : "+str(table[key]["AT"]["mn"])+"°C\nMaximale : "+str(table[key]["AT"]["mx"])+"°C\nMoyenne : "+str(table[key]["AT"]["av"])+"°C",inline=True)
    except:
        pass
    try:
        embedP.add_field(name="Pression atmosphérique",value="Minimale : "+str(table[key]["PRE"]["mn"])+"Pa\nMaximale : "+str(table[key]["PRE"]["mx"])+"Pa\nMoyenne : "+str(table[key]["PRE"]["av"])+"Pa",inline=True)
    except:
        pass
    try:
        embedP.add_field(name="Vitesse du vent",value="Minimal : "+str(round(table[key]["HWS"]["mn"]*3.6,2))+"km/h\nMaximal : "+str(round(table[key]["HWS"]["mx"]*3.6,2))+"km/h\nMoyenne : "+str(round(table[key]["HWS"]["av"]*3.6,2))+"km/h",inline=True)
    except:
        pass
    embedP=auteur("https://mars.nasa.gov/insight/weather",0,0,embedP,"nasa")
    return embedP