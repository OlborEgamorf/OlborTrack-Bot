import rule34
from random import choice
import discord
from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.Embeds import exeErrorExcept, embedAssert


async def exeNeko(ctx,bot):
    """La seule et unique commande NSFW du Bot, inspirée par Zeynah suite à une private joke. C'est à cause de lui que vous avez installé la bibliothèque rule34. Son Twitter est @Zeyttsun si vous voulez vous plaindre.
    
    Envoie une image de Neko. Ne fonctionne que si le salon d'invocation est NSFW.
    
    Fuck Zey."""
    try:
        assert ctx.channel.is_nsfw(),"Cette commande doit être effectuée dans un salon NSFW"
        phrases=["T'as pas honte ?","Gros porc","Tu me dégoutes","Mais sérieux ?","Tu voudrais pas aller voir dehors ?","Tu te branles vraiment sur ça ?","Tes parents le savent ?","Je vais te retirer des stats si tu continues...","C'est dégueulasse","..."]
        rule = rule34.Rule34(bot.loop)
        liste=await rule.getImages("neko",singlePage=True,randomPID=True)
        embed=discord.Embed(title=choice(phrases),color=ctx.author.color.value)
        embed.set_image(url=choice(liste).file_url)
        embed.set_footer(text="OT!zeynah")
        embed=auteur(ctx.author.id,ctx.author,ctx.author.avatar,embed,"user")
    except AssertionError as er:
        embed=embedAssert(str(er))
    except:
        embed=await exeErrorExcept(ctx,bot,[])
    await ctx.send(embed=embed)