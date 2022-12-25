from Core.Decorator import OTCommand
from Core.Fonctions.Embeds import createEmbed
from Stats.SQL.ConnectSQL import connectSQL


@OTCommand
async def voiceEphemRename(interaction,bot,nom):

    connexion,curseur=connectSQL(interaction.guild_id)

    assert interaction.user.author.voice!=None, "Vous n'êtes dans aucun salon vocal"
    salon=curseur.execute("SELECT * FROM salons WHERE IDOwner={0} AND IDChannel={1}".format(interaction.user.id,interaction.user.voice.channel.id)).fetchone()
    assert salon!=None, "Le salon dans lequel vous êtes ne vous appartient pas, ou alors n'est pas éphémère, vous ne pouvez donc pas le modifier."
    
    await interaction.user.voice.channel.edit(name=nom)
    await interaction.response.send_message(embed=createEmbed("Nom du salon éphémère modifié.","Nouveau nom : {0}".format(nom),0xf54269,interaction.command.qualified_name,interaction.guild))


@OTCommand
async def voiceEphemLock(interaction,bot):
    connexion,curseur=connectSQL(interaction.guild_id)

    assert interaction.user.voice!=None, "Vous n'êtes dans aucun salon vocal"
    salon=curseur.execute("SELECT * FROM salons WHERE IDOwner={0} AND IDChannel={1}".format(interaction.user.id,interaction.user.voice.channel.id)).fetchone()
    assert salon!=None, "Le salon dans lequel vous êtes ne vous appartient pas, ou alors n'est pas éphémère, vous ne pouvez donc pas le modifier."

    if salon["Lock"]==True:
        hub=bot.get_channel(salon["IDHub"])
        await interaction.user.voice.channel.edit(overwrites=hub.overwrites)
        curseur.execute("UPDATE salons SET Lock=False WHERE IDChannel={0}".format(interaction.user.voice.channel.id))
        embed=createEmbed("Salon éphémère déverrouillé","Le salon est revenu à ses autorisations de base, établies à partir de son hub.",0xf54269,interaction.command.qualified_name,interaction.guild)
    else:
        for i in interaction.guild.roles:
            try:
                await interaction.user.voice.channel.set_permissions(i, connect=False)
            except:
                pass
        curseur.execute("UPDATE salons SET Lock=True WHERE IDChannel={0}".format(interaction.user.voice.channel.id))
        embed=createEmbed("Salon éphémère verrouillé","Seul les administrateurs de votre serveur peuvent accéder à votre salon.",0xf54269,interaction.command.qualified_name,interaction.guild)
    
    connexion.commit()
    await interaction.response.send_message(embed=embed)


@OTCommand
async def voiceEphemLimit(interaction,bot,nombre):
    connexion,curseur=connectSQL(interaction.guild.id)

    assert interaction.user.voice!=None, "Vous n'êtes dans aucun salon vocal"
    salon=curseur.execute("SELECT * FROM salons WHERE IDOwner={0} AND IDChannel={1}".format(interaction.user.id,interaction.user.voice.channel.id)).fetchone()
    assert salon!=None, "Le salon dans lequel vous êtes ne vous appartient pas, ou alors n'est pas éphémère, vous ne pouvez donc pas le modifier."

    if nombre<=0 or nombre>99:
        await interaction.user.voice.channel.edit(user_limit=None)
    else:
        await interaction.user.voice.channel.edit(user_limit=nombre)

    await interaction.response.send_message(embed=createEmbed("Limite modifiée","La nouvelle limite de membres pour votre salon éphémère est : {0}".format(nombre),0xf54269,interaction.command.qualified_name,interaction.guild))

@OTCommand
async def infosVoiceEphem(interaction,bot):
    connexion,curseur=connectSQL(interaction.guild.id)

    assert interaction.user.voice!=None, "Vous n'êtes dans aucun salon vocal"
    chan=interaction.user.voice.channel
    salon=curseur.execute("SELECT * FROM salons WHERE IDChannel={0}".format(chan.id)).fetchone()
    assert salon!=None, "Hmmm... Une erreur a eu lieu..."

    embed=createEmbed("Votre salon éphémère","",0xf54269,interaction.command.qualified_name,interaction.guild)
    embed.add_field(name="Nom du salon",value="<#{0}>".format(interaction.user.voice.channel.id),inline=True)
    embed.add_field(name="Parent",value="<#{0}>".format(salon["IDHub"]),inline=True)
    embed.add_field(name="Propriétaire",value="<@{0}>".format(salon["IDOwner"]),inline=True)
    embed.add_field(name="Limite de membres",value=str(chan.user_limit),inline=True)
    embed.add_field(name="Verrouillé",value=str(bool(salon["Lock"])),inline=True)

    await interaction.response.send_message(embed=embed)