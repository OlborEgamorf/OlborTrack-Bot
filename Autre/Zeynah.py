from random import choice

import rule34
from Core.Decorator import OTCommand
from Core.Fonctions.Embeds import createEmbed


@OTCommand
async def exeNeko(ctx,bot):
    """La seule et unique commande NSFW du Bot, inspirée par Zeynah suite à une private joke. C'est à cause de lui que vous avez installé la bibliothèque rule34. Son Twitter est @Zeyttsun si vous voulez vous plaindre.
    
    Envoie une image de Neko. Ne fonctionne que si le salon d'invocation est NSFW.
    
    Fuck Zey."""
    assert ctx.channel.is_nsfw(),"Cette commande doit être effectuée dans un salon NSFW"
    phrases=["T'as pas honte ?","Gros porc","Tu me dégoutes","Mais sérieux ?","Tu voudrais pas aller voir dehors ?","Tu te branles vraiment sur ça ?","Tes parents le savent ?","Je vais te retirer des stats si tu continues...","C'est dégueulasse","..."]
    rule = rule34.Rule34(bot.loop)
    liste=await rule.getImages("neko",singlePage=True,randomPID=True)
    embed=createEmbed(choice(phrases),"",ctx.author.color.value,ctx.invoked_with.lower(),ctx.author)
    embed.set_image(url=choice(liste).file_url)
    await ctx.send(embed=embed)
