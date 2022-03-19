from Core.Fonctions.Embeds import createEmbed
from Core.Fonctions.Phrase import createPhrase

async def voiceEphemRename(ctx,args):
    assert len(args)>0, "Vous devez me donner un nom de salon !"
    phrase=createPhrase(args)
    await ctx.author.voice.channel.edit(name=phrase)
    return createEmbed("Nom du salon éphémère modifié.","Nouveau nom : {0}".format(phrase),0xf54269,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)


async def voiceEphemLock(ctx,curseur,bot):
    salon=curseur.execute("SELECT * FROM salons WHERE IDOwner={0} AND IDChannel={1}".format(ctx.author.id,ctx.author.voice.channel.id)).fetchone()

    if salon["Lock"]==True:
        hub=bot.get_channel(salon["IDHub"])
        await ctx.author.voice.channel.edit(overwrites=hub.overwrites)
        curseur.execute("UPDATE salons SET Lock=False WHERE IDChannel={0}".format(ctx.author.voice.channel.id))
        return createEmbed("Salon éphémère déverrouillé","Le salon est revenu à ses autorisations de base, établies à partir de son hub.",0xf54269,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)
    else:
        for i in ctx.guild.roles:
            try:
                await ctx.author.voice.channel.set_permissions(i, connect=False)
            except:
                pass
        curseur.execute("UPDATE salons SET Lock=True WHERE IDChannel={0}".format(ctx.author.voice.channel.id))
        return createEmbed("Salon éphémère verrouillé","Seul les administrateurs de votre serveur peuvent accéder à votre salon.",0xf54269,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)


async def voiceEphemLimit(ctx,args,curseur):
    assert len(args)>0, "Vous devez me donner la limite à imposer !"
    try:
        if args[0].lower()!="inf":
            int(args[0])
    except:
        raise AssertionError("Vous devez me donner un nombre valide ou alors 'inf' pour retirer la limite actuelle !")

    if args[0].lower()=="inf":
        await ctx.author.voice.channel.edit(user_limit=None)
    else:
        await ctx.author.voice.channel.edit(user_limit=int(args[0]))

    return createEmbed("Limite modifiée","La nouvelle limite de membres pour votre salon éphémère est : {0}".format(args[0]),0xf54269,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)