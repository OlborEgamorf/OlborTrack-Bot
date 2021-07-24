import discord
from Core.Fonctions.Embeds import exeErrorExcept,embedAssert


async def exeFeedback(ctx,bot,args):
    """Cette fonction permet d'envoyer un message à OlborEgamorf et de donner des feedbacks sur le Bot.
    
    En argument avec la commande est donné une phrase commentaire.
    
    La phrase est ensuite envoyée dans un salon privé sur le serveur de test du bot."""
    try:
        assert len(args)>0, "Votre message est vide !"
        phrase=""
        for i in args:
            phrase+=" "+i
        embedTable=discord.Embed(title="<:otVERT:868535645897912330> Message envoyé :", description=phrase, color=0x339966)
        embedTable.set_footer(text="OT!feedback - {0} - {1}".format(ctx.author.name,ctx.author.id))
        await bot.get_channel(737041049939345408).send(embed=embedTable)
    except AssertionError as er:
        embedTable=embedAssert(str(er))
    except:
        embedTable=await exeErrorExcept(ctx,bot,args)
    await ctx.send(embed=embedTable)
    return