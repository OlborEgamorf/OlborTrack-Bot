import discord
from Core.Decorator import OTCommand
from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.Embeds import createEmbed
from Core.OT import OlborTrack
from Core.OTGuild import OTGuildCMD
from discord.ext import commands
from Stats.SQL.ConnectSQL import connectSQL


@OTCommand
async def exeModules(ctx:commands.Context,bot:OlborTrack,args:list,guild:OTGuildCMD):
    """Fonction qui permet d'activer et de désactiver des modules de stats ou de commandes. Pour un serveur
    
    En argument avec la commande est donné le nom du module.
    
    Si aucun argument n'est donné, envoie un embed avec la liste des modules et s'ils sont activés
    
    Connexion à la base de données et reset dans l'objet OTGuild
    
    Commande Admin."""
    descip=""
    dictCommande={"modulestat":"modulesStats","modulecmd":"modulesCMD"}
    dictBool={False:"désactivé",True:"activé"}
    listeN=["Salons","Moyennes","Fréquences","Réactions","Mentions","Voice","Mots","Roles","Emojis","Messages","Autre"]
    listeC=["Stats","Sondages","Outils","Savezvous","Jeux"]
    connexion,curseur=connectSQL(ctx.guild.id,"Guild","Guild",None,None)
    if len(args)==0:
        await ctx.reply(embed=commandePerms(ctx,ctx.command.name,guild))
    else:
        nom=args[0][0].upper()+args[0][1:len(args[0])].lower()
        if ctx.command.name=="modulestat":
            assert nom in listeN, "Ce module n'existe pas."
        else:
            assert nom in listeC, "Ce module n'existe pas."
        if ctx.command.name=="modulestat":
            if nom in ("Moyennes","Roles") and guild.mstats[9]["Statut"]==False:
                raise AssertionError("Le module 'Messages' doit être activé pour que je puisse traquer les moyennes ou les rôles.")
            if nom=="Messages" and guild.mstats[9]["Statut"]==True:
                curseur.execute("UPDATE modulesStats SET Statut=False WHERE Module='Moyennes'")
                curseur.execute("UPDATE modulesStats SET Statut=False WHERE Module='Roles'")
                descip+="Moyennes : désactivé\nRoles : désactivé\n"
        if ctx.command.name=="modulecmd":
            if nom=="Stats":
                assert guild.stats, "Vous ne pouvez pas activer les commandes de statistiques si vous avez choisi de ne plus les traquer sur votre serveur."
        etat=curseur.execute("SELECT * FROM {0} WHERE Module='{1}'".format(dictCommande[ctx.command.name],nom)).fetchone()
        curseur.execute("UPDATE {0} SET Statut={1} WHERE Module='{2}'".format(dictCommande[ctx.command.name],bool(int(etat["Statut"])-1),nom))
        descip+="{0} : {1}".format(nom,dictBool[bool(int(etat["Statut"])-1)])
        connexion.commit()
        guild.getPerms()
        await ctx.reply(embed=createEmbed("Modification de modules",descip,0x220cc9,ctx.invoked_with.lower(),ctx.guild))


def commandePerms(ctx:commands.Context,option:str,guildOT:OTGuildCMD) -> discord.Embed:
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
    embed=discord.Embed(title="Modules",description=descip,color=0x220cc9)
    embed.set_footer(text="OT!{0}".format(option))
    embed=auteur(ctx.guild.id,ctx.guild.name,ctx.guild.icon,embed,"guild")
    return embed
