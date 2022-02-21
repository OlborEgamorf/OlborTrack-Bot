from Core.Fonctions.Embeds import createEmbed
from Core.Decorator import OTCommand

@OTCommand
async def exeFeedback(ctx,bot,args):
    """Cette fonction permet d'envoyer un message à OlborEgamorf et de donner des feedbacks sur le Bot.
    
    En argument avec la commande est donné une phrase commentaire.
    
    La phrase est ensuite envoyée dans un salon privé sur le serveur de test du bot."""
    assert len(args)>0, "Votre message est vide !"
    embed=createEmbed("<:otVERT:868535645897912330> Message envoyé"," ".join(args),0x339966,ctx.invoked_with.lower(),ctx.author)
    await bot.get_channel(737041049939345408).send(embed=embed)
    await ctx.reply(embed=embed)
    