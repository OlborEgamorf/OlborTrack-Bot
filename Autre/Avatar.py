import discord
from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.Embeds import exeErrorExcept


async def exePP(ctx,bot):
    """Cette fonction renvoie l'image de profil d'une personne mentionnée'.
    
    Si personne n'est mentionné, renvoie l'image de profil de l'auteur de la commande."""
    try:
        if len(ctx.message.mentions)==0:
            embedF=discord.Embed(title="Photo de profil :",color=ctx.author.color.value)
            embedF.set_image(url=ctx.author.avatar_url)
            embedF=auteur(ctx.author.id,ctx.author,ctx.author.avatar,embedF,"user") 
        else:
            embedF=discord.Embed(title="Photo de profil :",color=ctx.message.mentions[0].color.value)
            embedF.set_image(url=ctx.message.mentions[0].avatar_url)
            embedF=auteur(ctx.message.mentions[0].id,ctx.message.mentions[0],ctx.message.mentions[0].avatar,embedF,"user")
        embedF.set_footer(text="OT!avatar")
    except:
        embedF=await exeErrorExcept(ctx,bot,"")
    await ctx.send(embed=embedF)