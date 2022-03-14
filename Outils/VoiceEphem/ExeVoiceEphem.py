from Core.Decorator import OTCommand
from Core.Fonctions.Embeds import createEmbed
from Outils.VoiceEphem.ModifVoiceEphem import (voiceEphemLimit, voiceEphemLock,
                                               voiceEphemRename)
from Stats.SQL.ConnectSQL import connectSQL

@OTCommand
async def exeVoiceEphem(ctx,bot,args):
    connexion,curseur=connectSQL(ctx.guild.id,"VoiceEphem","Guild",None,None)

    assert ctx.author.voice!=None, "Vous n'êtes dans aucun salon vocal"
    salon=curseur.execute("SELECT * FROM salons WHERE IDOwner={0} AND IDChannel={1}".format(ctx.author.id,ctx.author.voice.channel.id)).fetchone()
    assert salon!=None, "Le salon dans lequel vous êtes ne vous appartient pas, ou alors n'est pas éphémère, vous ne pouvez donc pas le modifier."

    if ctx.invoked_with=="limite":
        embed=await voiceEphemLimit(ctx,args,curseur)
    elif ctx.invoked_with=="rename":
        embed=await voiceEphemRename(ctx,args)
    elif ctx.invoked_with=="lock":
        embed=await voiceEphemLock(ctx,curseur,bot)
    else:
        embed=infosVoiceEphem(ctx,curseur)

    connexion.commit()
    await ctx.send(embed=embed)


def infosVoiceEphem(ctx,curseur):
    chan=ctx.author.voice.channel
    salon=curseur.execute("SELECT * FROM salons WHERE IDChannel={0}".format(chan.id)).fetchone()
    assert salon!=None, "Hmmm... Une erreur a eu lieu..."
    embed=createEmbed("Votre salon éphémère","",0xf54269,ctx.invoked_with.lower(),ctx.guild)
    embed.add_field(name="Nom du salon",value="<#{0}>".format(ctx.author.voice.channel.id),inline=True)
    embed.add_field(name="Parent",value="<#{0}>".format(salon["IDHub"]),inline=True)
    embed.add_field(name="Propriétaire",value="<@{0}>".format(salon["IDOwner"]),inline=True)
    embed.add_field(name="Limite de membres",value=str(chan.user_limit),inline=True)
    embed.add_field(name="Verrouillé",value=str(bool(salon["Lock"])),inline=True)
    return embed