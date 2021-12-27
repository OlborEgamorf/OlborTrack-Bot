import discord
from Core.Fonctions.Embeds import createEmbed


async def exePermsChan(ctx,bot):
    """Cette fonction renvoie tous les salons textuels auquel le bot a accès, qu'ils soient blind ou non"""
    quote=""
    for i in ctx.guild.text_channels:
        if i.permissions_for(ctx.guild.get_member(699728606493933650)).read_messages==True and i.permissions_for(ctx.guild.get_member(699728606493933650)).view_channel==True:
            quote+="<#"+str(i.id)+"> "
    embedTable=createEmbed("Salons auquel j'ai accès :",quote,0x220cc9,ctx.command.invoked_with.lower(),ctx.guild)
    await ctx.channel.send(embed=embedTable)
    return
