import discord
embedE=discord.Embed(title="<:otROUGE:868535622237818910> Permission manquante", description="Je ne peux retirer votre réaction ! Donnez moi la permission 'gestion des messages' pour ne plus voir ce message.",color=0xff0000)
embedE.set_footer(text="Permission")

def getTurn(reaction:discord.Reaction) -> str:
    """Détermine en fonction de la réaction utilisée quel a été le mouvement de page (+, - ou None)"""
    if reaction.id==772766034376523776:
        return "+"
    elif reaction.id==772766034335236127:
        return "-"
    return None

async def removeReact(message:discord.Message,emote:int,user:discord.Member):
    """Retire la réaction ajoutée, et envoie un message d'alerte si le bot n'a pas les permissions pour."""
    global embedE
    try:
        if message.channel.type!=discord.ChannelType.private:
            for i in message.reactions:
                if i.emoji.id==emote:
                    await i.remove(user)
    except discord.errors.Forbidden:
        await message.channel.send(embed=embedE,delete_after=8)
    except:
        pass