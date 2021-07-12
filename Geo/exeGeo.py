import asyncio

import discord
from Core.Fonctions.Embeds import embedAssert, exeErrorExcept
from Core.Fonctions.Phrase import createPhrase

from Geo.MapISS import embedISS
from Geo.PhotoNASA import embedNasaPhoto


async def exeGeo(ctx,bot,args):
    """Cette fonction génère les embeds des commandes de type Geo en fonction de quelle commande est invoquée."""
    try:
        if ctx.command.name=="iss":
            await embedISS(ctx)
        elif ctx.command.name=="nasaphoto":
            embed=await embedNasaPhoto()
            await ctx.send(embed=embed)
    except AssertionError as er:
        await ctx.send(embed=embedAssert(str(er)))
    except asyncio.exceptions.TimeoutError:
        await ctx.send(embed=embedAssert("Temps de requête écoulé, veuillez réessayer."))
    except:
        await ctx.send(embed=await exeErrorExcept(ctx,bot,args))