import discord
from Core.Fonctions.AuteurIcon import auteur

async def exeSCount(ctx,bot):
    """Cette fonction affiche le nombre de serveurs où le bot est présent."""
    
    embedTable=discord.Embed(title="Nombre de serveurs :",description="Je suis présent dans **"+str(len(bot.guilds))+"** serveurs actuellement !\nAidez-moi à grandir en m'invitant sur d'autres serveurs !",color=0xfcfc03)
    embedTable=auteur(bot.user,ctx.author,ctx.author.avatar,embedTable,"olbor")
    embedTable.set_footer(text="OT!servcount")
    await ctx.channel.send(embed=embedTable)