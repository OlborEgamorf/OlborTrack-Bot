import discord
from Core.Decorator import OTCommand
from Core.Fonctions.Embeds import createEmbed
from Core.OT import OlborTrack
from Core.OTGuild import OTGuildCMD
from Stats.SQL.ConnectSQL import connectLocal, connectSQL


@OTCommand
async def exeHBUser(interaction:discord.Interaction,bot:OlborTrack,option:str,guild:OTGuildCMD):
    """Cette fonction permet à un utilisateur de se rendre masqué ou bloqué aux yeux du bot sur un serveur.
    
    L'utilisation de la commande suffit pour activer/désactiver l'une des options.
    
    L'option est donnée lors de l'exécution de la commande.
    
    Connexion à la base de données et reset dans l'objet OTGuild

    Options possibles : hide, blind, mute"""

    connexion,curseur=connectSQL(interaction.guild_id,"Guild","Guild",None,None)
    dictEmbed={"HideFalse":"masqué","BlindFalse":"invisible","HideTrue":"démasqué","BlindTrue":"visible"}
    etat=curseur.execute("SELECT * FROM users WHERE ID={0}".format(interaction.user.id)).fetchone()
    curseur.execute("UPDATE users SET {0}={1} WHERE ID={2}".format(option,bool(int(etat[option])-1),interaction.user.id))
    descip="Vous êtes désormais {0} à mes yeux sur ce serveur.".format(dictEmbed["{0}{1}".format(option,bool(etat[option]))])
    connexion.commit()
    guild.getHBM()
    await interaction.response.send_message(embed=createEmbed("Changement d'état",descip,0x220cc9,interaction.command.name,interaction.user))
