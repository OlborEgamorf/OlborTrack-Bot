import asyncio
from Core.Fonctions.Embeds import embedAssert, exeErrorExcept
from Core.Fonctions.Unpin import unpin
import discord


def OTCommand(func):
    async def wrapper(*args,**kwargs):
        ctx,bot=args[0],args[1]
        try:
            await func(*args,**kwargs)
        except AssertionError as er:
            await embedAssert(ctx,er,True)
        except asyncio.exceptions.TimeoutError:
            await embedAssert(ctx,"Temps de requête écoulé, veuillez réessayer.",True)
        except discord.errors.Forbidden:
            await embedAssert(ctx,"Je n'ai pas pu envoyer les réactions de cette commande, qui servent à naviguer dedans. Donnez moi les permissions 'utiliser emojis externes' et 'ajouter des réactions' si vous ne voulez plus voir ce message, et profiter à fond de mes possibilités.",True)
        except:
            await exeErrorExcept(ctx,bot,True)
        
    return wrapper

def OTJeux(func):
    async def wrapper(*args,**kwargs):
        ctx,bot=args[0],args[1]
        try:
            await func(*args,**kwargs)
        except AssertionError as er:
            await embedAssert(ctx,er,True)
        except:
            await exeErrorExcept(ctx,bot,True)
            # AJOUT UNPIN ! METTRE MESSAGE DANS GAME ET DEL AUSSI
        if ctx.cog.qualified_name=="Jeux":
            game,inGame=args[2],args[3]
            try:
                await game.delEmotes()
            except:
                pass
            for i in game.ids:
                inGame.remove(i)
        
    return wrapper

def OTCross(func):
    async def wrapper(*args,**kwargs):
        ctx,bot,game,inGame,listeGames=args
        try:
            await func(*args,**kwargs)
        except AssertionError as er:
            await embedAssert(ctx,er,True)
        except:
            for i in game.messages:
                await i.channel.send(embed=await exeErrorExcept(ctx,bot,None))
                await unpin(i)
        
        if ctx.cog.qualified_name=="Jeux":
            try:
                await game.delEmotes()
            except:
                pass
            for i in game.ids:
                inGame.remove(i)
            for i in game.messages:
                del listeGames[i.id]
        
    return wrapper