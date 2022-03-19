from Core.Decorator import OTCommand
from Core.Fonctions.Embeds import createEmbed


@OTCommand
async def exePP(ctx,bot):
    """Cette fonction renvoie l'image de profil d'une personne mentionnée'.
    
    Si personne n'est mentionné, renvoie l'image de profil de l'auteur de la commande."""
    if len(ctx.message.mentions)==0:
        embed=createEmbed("Photo de profil","",ctx.author.color.value,ctx.invoked_with.lower(),ctx.author)
        embed.set_image(url=ctx.author.avatar_url)
    else:
        embed=createEmbed("Photo de profil","",ctx.message.mentions[0].color.value,ctx.invoked_with.lower(),ctx.message.mentions[0])
        embed.set_image(url=ctx.message.mentions[0].avatar_url)
    await ctx.send(embed=embed)
