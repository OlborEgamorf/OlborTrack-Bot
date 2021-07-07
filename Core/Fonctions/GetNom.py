dictTrivia={3:"Images",2:"GIFs",1:"Fichiers",4:"Liens",5:"Réponses",6:"Réactions",7:"Edits",8:"Emotes",9:"Messages",10:"Mots",11:"Vocal"}
from math import inf

import discord
from Core.Fonctions.AligneText import aligne
from Core.Fonctions.Phrase import createPhrase
from Core.OTGuild import OTGuild
from discord.ext import commands
from Stats.SQL.EmoteDetector import emoteDetector


def nomsOptions(option:str,id:int,guildOT:OTGuild,bot:commands.Bot) -> str:
    """A partir d'une option et d'un ID, donne le formatage qu'il faut pour s'afficher normalement dans un embed.
    Entrées : 
        option : l'option de la commande
        id : l'ID de l'objet à formater
        guildOT : l'objet OTGuild du serveur concerné
        bot : l'objet bot du bot
    Sortie :
        nom : le formatage"""
    if option in ("Voice","Messages","Mots","Mentions","Mentionne"):
        if guildOT.users[id]["Hide"]==True:
            nom="*Membre masqué*"
        elif guildOT.users[id]["Leave"]==True:
            nom="*Ancien membre*"
        else:
            nom="<@{0}>".format(id)

    elif option in ("Reactions","Emotes"):
        try:
            nom=chr(id)
        except:
            emote=bot.get_emoji(id)
            if type(emote)!=discord.emoji.Emoji:
                nom="*??*"
            else:
                nom=str(emote)

    elif option in ("Salons","Voicechan"):
        if guildOT.chan[id]["Hide"]==True:
            nom="*Salon masqué*"
        else:
            nom="<#{0}>".format(id)
            
    elif option=="Freq":
        nom="{0}h-{1}h".format(id,id+1)

    elif option=="Divers":
        nom=dictTrivia[id]

    elif option=="Roles":
        nom="<@&{0}>".format(id)
    return nom

def getNomGraph(ctx:commands.Context,bot:commands.Bot,option:str,id:int) -> (str or discord.Member):
    """A partir d'une option et d'un ID, donne le formatage qu'il faut pour s'afficher normalement dans un graphique.
    Entrées : 
        option : l'option de la commande
        id : l'ID de l'objet à formater
        ctx : le contexte de la commande
        bot : l'objet bot du bot
    Sortie :
        nom : le formatage ou alors un membre en fonction de l'option donnée."""
    if option in ("Salons","Voicechan"):
        nom=bot.get_channel(id).name
        nom=nom if len(nom)<=15 else "{0}...".format(nom[0:15])
        return nom
    elif option in ("Emotes","Reactions"):
        return bot.get_emoji(id).name
    elif option=="Freq":
        return "{0}h-{1}h".format(id,id+1)
    elif option=="Divers":
        return dictTrivia[id]
    elif option=="Roles":
        nom=ctx.guild.get_role(id).name
        nom=nom if len(nom)<=15 else "{0}...".format(nom[0:15])
        return nom 
    else:
        return ctx.guild.get_member(id)

def getObj(option:str,ctx:commands.Context,nb:int) -> (str or None):
    """Permet d'obtenir un objet en particulier pour une commande.
    Entrées :
        option : l'option de la commande
        ctx : le contexte de la commande
        nb : pour la suite
    Sortie :
        None si rien n'est trouvé, sinon l'ID de l'objet"""
    if option not in ("Messages","Mots","Voice","Mentionne"):
        return getAuthor(option,ctx,nb)
    return None

def getAuthor(option:str,ctx:commands.Context,nb:int) -> (str or None):
    """Permet d'obtenir l'auteur visé de la commande
    Entrées :
        option : l'option de la commande
        ctx : le contexte de la commande
        nb : si on doit se servir des arguments de la commande, permet de savoir à quel indice commencer
    Sortie :
        None si rien n'est trouvé, sinon l'ID de l'auteur"""
    try:
        if option in ("Voice","Messages","Mots","Mentions","Mentionne"):
            author=ctx.author.id
        elif option=="Salons":
            author=ctx.message.channel_mentions[0].id
        elif option=="Freq":
            if ctx.args[nb][len(ctx.args[nb])-1].lower()=="h":
                author=ctx.args[nb][0:len(ctx.args[nb])-1]
            else:
                author=ctx.args[nb]
        elif option in ("Emotes","Reactions"):
            author=emoteDetector(ctx.args[nb])[0]
        elif option=="Divers":
            author=dictTrivia[ctx.args[nb]]
        elif option=="Roles":
            if ctx.message.role_mentions!=[]:
                author=ctx.message.role_mentions[0].id
            else:
                dictRolesNb={}
                role=createPhrase(ctx.args[nb:len(ctx.args)]).lower()
                assert role!=""
                for i in ctx.guild.roles:
                    dictRolesNb[i.id]=aligne(role,i.name.lower())
                maxi=dictRolesNb[ctx.guild.id]
                author=ctx.guild.id
                for i in dictRolesNb:
                    if dictRolesNb[i]>maxi:
                        maxi=dictRolesNb[i]
                        author=i
        elif option=="Voicechan":
            dictChanNb={}
            chan=createPhrase(ctx.args[nb:len(ctx.args)]).lower()
            assert chan!=""
            for i in ctx.guild.voice_channels:
                dictChanNb[i.id]=aligne(chan,i.name.lower())
            maxi=-inf
            author=None
            for i in dictChanNb:
                if dictChanNb[i]>maxi:
                    maxi=dictChanNb[i]
                    author=i
    except:
        author=None
    return author
