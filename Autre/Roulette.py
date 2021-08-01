import discord
from random import choice
from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.Embeds import exeErrorExcept, embedAssert


async def exeRoulette(ctx,bot,args):
    """Cette fonction permet d'exécuter une roulette, qui choisit de manière aléatoire une proposition parmi plusieurs.
    
    En argument avec la commande est donné les propositions."""
    try:
        assert len(args)>0, "La roulette est vide !"
        assert len(args)>1, "Mettez deux propositions dans la roulette !"
        embedTable=discord.Embed(title="Roulette !", description=choice(args), color=0x2ba195)
        embedTable.set_footer(text="OT!roulette")
        embedTable=auteur(ctx.author.id,ctx.author.name,ctx.author.avatar,embedTable,"user")
    except AssertionError as er:
        embedTable=embedAssert(str(er))
    except:
        embedTable=await exeErrorExcept(ctx,bot,args)
    await ctx.send(embed=embedTable)