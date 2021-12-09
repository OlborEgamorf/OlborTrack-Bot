import discord
from Core.OS.Keys3 import NASAKey
from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.WebRequest import webRequest
from Core.Fonctions.Embeds import embedAssert, exeErrorExcept
import asyncio

async def embedNasaPhoto() -> discord.Embed:
    """Se sert de l'API de la NASA et de APOD pour obtenir la 'photo du jour'.
    
    Se sert de l'image donné en URL pour la mettre dans un embed, avec la description donnée.
    
    Renvoie l'embed en question."""
    table=await webRequest("https://api.nasa.gov/planetary/apod?api_key="+NASAKey+"&hd=True")
    assert table!=False, "Une erreur est survenue lors du chargement de l'image... Veuillez réessayer plus tard..."
    embedP=discord.Embed(title="Photo du jour : "+table["title"],description=table["explanation"],color=0xa83e32)
    embedP=auteur("https://apod.nasa.gov/apod/astropix.html",0,0,embedP,"nasa")
    embedP.set_image(url=table["url"])
    embedP.set_footer(text="OT!nasaphoto")
    return embedP

async def exeNASA(ctx,bot,args):
    """Cette fonction génère les embeds des commandes de type Geo en fonction de quelle commande est invoquée."""
    try:
        embed=await embedNasaPhoto()
        await ctx.send(embed=embed)
    except AssertionError as er:
        await ctx.send(embed=embedAssert(str(er)))
    except asyncio.exceptions.TimeoutError:
        await ctx.send(embed=embedAssert("Temps de requête écoulé, veuillez réessayer."))
    except:
        await ctx.send(embed=await exeErrorExcept(ctx,bot,args))