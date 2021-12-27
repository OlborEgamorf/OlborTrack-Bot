import asyncio

import discord
from Core.Fonctions.Phrase import createPhrase


async def exeSay(ctx,bot,args):
    """Cette fonction fait réécrire au bot un message donné par un utilisateur.
    
    Avant d'envoyer, le bot simule une écriture sur un temps qui dépend de la longueur du message. Les mentions sont supprimées.
    
    En argument avec la commande est donnée la phrase à renvoyer."""
    if len(args)==0:
        quote="<:otLOVE:868537427298504765>"
    else:
        try:
            await ctx.message.delete()
        except:
            pass
        quote=createPhrase(args)
        await ctx.trigger_typing()
        await asyncio.sleep(0.42*len(args))
    await ctx.send(content=quote,allowed_mentions=discord.AllowedMentions(everyone=False,users=False,roles=False,replied_user=False))
