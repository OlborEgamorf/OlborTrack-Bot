import asyncio

import discord

from Core.Fonctions.Embeds import embedAssert, exeErrorExcept


def OTCommand(func):
    async def wrapper(*args,**kwargs):
        ctx,bot=args[0],args[1]
        try:
            ret=await func(*args,**kwargs)
            return ret
        except AssertionError as er:
            await embedAssert(ctx,er,True)
        except asyncio.exceptions.TimeoutError:
            await embedAssert(ctx,"Temps de requête écoulé, veuillez réessayer.",True)
        except discord.errors.Forbidden:
            await embedAssert(ctx,"Je n'ai pas pu envoyer les réactions de cette commande, qui servent à naviguer dedans. Donnez moi les permissions 'utiliser emojis externes' et 'ajouter des réactions' si vous ne voulez plus voir ce message, et profiter à fond de mes possibilités.",True)
        except:
            await exeErrorExcept(ctx,bot,True)
        
    return wrapper
