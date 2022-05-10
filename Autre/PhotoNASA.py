import discord
from Core.Fonctions.Embeds import createEmbed
from Core.Fonctions.WebRequest import webRequest
from Core.OS.Keys3 import NASAKey
from Core.Decorator import OTCommand


async def embedNasaPhoto() -> discord.Embed:
    """Se sert de l'API de la NASA et de APOD pour obtenir la 'photo du jour'.
    
    Se sert de l'image donné en URL pour la mettre dans un embed, avec la description donnée.
    
    Renvoie l'embed en question."""
    table=await webRequest("https://api.nasa.gov/planetary/apod?api_key="+NASAKey+"&hd=True")
    assert table!=False, "Une erreur est survenue lors du chargement de l'image... Veuillez réessayer plus tard..."
    embed=createEmbed("Photo du jour : "+table["title"],table["explanation"],0xa83e32,"nasaphoto",None)
    embed.set_author(name="NASA",icon_url="https://media.discordapp.net/attachments/726034739550486618/769603075282305044/nasa-vector-logo-small.png",url="https://apod.nasa.gov/apod/astropix.html")
    embed.set_image(url=table["url"])
    return embed

@OTCommand
async def exeNASA(ctx,bot):
    """Cette fonction génère les embeds des commandes de type Geo en fonction de quelle commande est invoquée."""
    await ctx.send(embed=await embedNasaPhoto())
