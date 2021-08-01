import discord

def getTurn(reaction:discord.Reaction) -> str:
    """Détermine en fonction de la réaction utilisée quel a été le mouvement de page (+, - ou None)"""
    if reaction.id==772766034376523776:
        return "+"
    elif reaction.id==772766034335236127:
        return "-"
    return None

async def removeReact(message:discord.Message,emote:int,user:discord.Member):
    """Retire la réaction ajoutée, et envoie un message d'alerte si le bot n'a pas les permissions pour."""
    if message.channel.type!=discord.ChannelType.private:
        for i in message.reactions:
            if i.emoji.id==emote:
                await i.remove(user)