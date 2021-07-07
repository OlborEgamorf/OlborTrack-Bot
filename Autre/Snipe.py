
from time import strftime
from Core.Fonctions.Embeds import createEmbed, exeErrorExcept, embedAssert

async def exeSnipe(ctx,bot,guild):
    """Cette fonction envoie le dernier message supprimé par un membre du serveur.
    
    Le message doit être stocké dans l'objet OTGuild du serveur. Ne prend pas en compte les images. Envoie un message d'erreur si aucun message n'est stocké."""
    try:
        assert guild.snipe.texte!=None, "Aucun message n'a été supprimé."
        user=ctx.guild.get_member(guild.snipe.id)
        if user==None:
            embed=createEmbed("Dernier message supprimé",guild.snipe.texte,ctx.guild.get_member(bot.user.id).color.value,"{0} - {1}".format(ctx.invoked_with.lower(),guild.snipe.date),bot.user)
        else:
            embed=createEmbed("Dernier message supprimé",guild.snipe.texte,user.color.value,"{0} - {1}".format(ctx.invoked_with.lower(),guild.snipe.date),user)
    except AssertionError as er:
        embed=embedAssert(str(er))
    except:
        embed=await exeErrorExcept(ctx,bot,"")
    await ctx.send(embed=embed)

def delSnipe(message,guild):
    """Cette fonction écrase le dernier message supprimé stocké par le dernier supprimé détecté dans l'objet OTGuild du serveur."""
    guild.snipe.setSnipe(message.content,strftime("%d")+"/"+strftime("%m")+"/"+strftime("%y")+" - "+strftime("%H")+":"+strftime("%M"),message.author.id)
    