import asyncio

import discord
from Core.Fonctions.Embeds import embedAssert, exeErrorExcept
from Core.Fonctions.Phrase import createPhrase

from Geo.ISSMembers import embedISSMembers
from Geo.MapSearch import embedGeoSearch
from Geo.MeteoMars import embedMeteoMars
from Geo.PhotoNASA import embedNasaPhoto


async def exeGeo(ctx,bot,args):
    """Cette fonction génère les embeds des commandes de type Geo en fonction de quelle commande est invoquée."""
    try:
        if ctx.command.name=="iss" or ctx.command.name=="geosearch":
            arg=createPhrase(args)
            link=await embedGeoSearch(arg,ctx.command.name)
            message=await ctx.send(content=link[1], file=discord.File(link[0]))
        else:
            if ctx.command.name=="issmembers":
                embed=await embedISSMembers()
            elif ctx.command.name=="meteomars":
                embed=await embedMeteoMars()
            elif ctx.command.name=="nasaphoto":
                embed=await embedNasaPhoto()
            await ctx.send(embed=embed)
            return
    except AssertionError as er:
        await ctx.send(embed=embedAssert(str(er)))
        return  
    except asyncio.exceptions.TimeoutError:
        await ctx.send(embed=embedAssert("Temps de requête écoulé, veuillez réessayer."))
        return
    except:
        await ctx.send(embed=await exeErrorExcept(ctx,bot,args))
        return
    await message.add_reaction("<:otPLUS:772766034163400715>")