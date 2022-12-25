import discord
from Core.Decorator import OTCommand
from Core.Fonctions.Embeds import createEmbed
from Core.OT import OlborTrack
from Core.OTGuild import OTGuildCMD
from discord.ext import commands
from Stats.SQL.ConnectSQL import connectSQL


@OTCommand
async def exeModules(interaction:discord.Interaction,bot:OlborTrack,module:str,guild:OTGuildCMD):
    """Fonction qui permet d'activer et de désactiver des modules de stats ou de commandes. Pour un serveur
    
    En argument avec la commande est donné le nom du module.
    
    Si aucun argument n'est donné, envoie un embed avec la liste des modules et s'ils sont activés
    
    Connexion à la base de données et reset dans l'objet OTGuild
    
    Commande Admin."""
    descip=""
    dictCommande={"modulesstats":"etatStats","modulescmd":"etatModules"}
    dictBool={False:"désactivé",True:"activé"}
    listeN=["Messages","Voice","Emotes","Reactions","Divers"]
    listeC=["BV","AD","DynIcon","Stats","Polls","Twitch","Twitter","YouTube","Tableaux","VoiceEphem","CMDAuto","SavezVous","Jeux","Anniv","Timeline","RoleSelector","CMDCustom"]

    connexion,curseur=connectSQL(interaction.guild_id)
    if module==None:
        await interaction.response.send_message(embed=commandePerms(interaction,interaction.command.name,guild))
    else:
        module=module.value
        
        if interaction.command.name=="modulestat":
            if module in ("Moyennes","Roles") and guild.mstats[9]["Statut"]==False:
                raise AssertionError("Le module 'Messages' doit être activé pour que je puisse traquer les moyennes ou les rôles.")
            if module=="Messages" and guild.mstats[9]["Statut"]==True:
                curseur.execute("UPDATE modulesStats SET Statut=False WHERE Module='Moyennes'")
                curseur.execute("UPDATE modulesStats SET Statut=False WHERE Module='Roles'")
                descip+="Moyennes : désactivé\nRoles : désactivé\n"
        if interaction.command.name=="modulecmd":
            if module=="Stats":
                assert guild.stats, "Vous ne pouvez pas activer les commandes de statistiques si vous avez choisi de ne plus les traquer sur votre serveur."
        etat=curseur.execute("SELECT * FROM {0} WHERE Module='{1}'".format(dictCommande[interaction.command.name],module)).fetchone()
        curseur.execute("UPDATE {0} SET Statut={1} WHERE Module='{2}'".format(dictCommande[interaction.command.name],bool(int(etat["Statut"])-1),module))
        descip+="{0} : {1}".format(module,dictBool[bool(int(etat["Statut"])-1)])
        connexion.commit()
        guild.getPerms()
        await interaction.response.send_message(embed=createEmbed("Modification de modules",descip,0x220cc9,interaction.command.name,interaction.guild))


def commandePerms(interaction:discord.Interaction,option:str,guildOT:OTGuildCMD) -> discord.Embed:
    """Embed qui affiche pour un serveur les modules de stats ou de commandes et leur état
    
    Type de la sortie : discord.Embed"""
    dictStatut={False:"__désactivé__",True:"**activé**"}
    descip=""
    if option=="modulestat":
        for i in guildOT.mstats:
            descip+="{0} : {1}\n".format(i["Module"],dictStatut[i["Statut"]])
    else:
        for i in guildOT.mcmd:
            descip+="{0} : {1}\n".format(i["Module"],dictStatut[i["Statut"]])
    return createEmbed("Modules",descip,0x220cc9,option,interaction.guild)
