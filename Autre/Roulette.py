from random import choice

from Core.Fonctions.Embeds import createEmbed
from Core.Decorator import OTCommand

@OTCommand
async def exeRoulette(ctx,bot,args):
    """Cette fonction permet d'exécuter une roulette, qui choisit de manière aléatoire une proposition parmi plusieurs.
    
    En argument avec la commande est donné les propositions."""
    assert len(args)>0, "La roulette est vide !"
    assert len(args)>1, "Mettez deux propositions dans la roulette !"
    await ctx.reply(embed=createEmbed("Roulette !",choice(args),0x2ba195,ctx.invoked_with.lower(),ctx.author))
