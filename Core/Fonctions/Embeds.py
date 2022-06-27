import sqlite3
import sys
import traceback

import discord
from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.GetNom import nomsOptions
from Core.OTGuild import OTGuild
from discord.ext import commands



def defEvol(ligne:dict,evol:bool) -> str: 
    """Cette fonction renvoie une emote d'évolution en fonction du nombre de positions indiquées pour la personne.
    Entrées :
        ligne : les infos de la personne
        evol : indique si une emote doit être renvoyée
    Sortie : 
        l'emote ou alors une chaine de charactères vide"""
    if evol:
        rank=ligne["Evol"]
        if rank>0 and rank<=3:
            return "<:otEvolU1:791683643600666624>"
        elif rank>3 and rank<=6:
            return "<:otEvolU2:791684557878591508>"
        elif rank>6:
            return "<:otEvolU3:791684557677002754>"
        elif rank<0 and rank>=-3:
            return "<:otEvolD1:791683740261810226>"
        elif rank<-3 and rank>=-6:
            return "<:otEvolD2:791684085008826389>"
        elif rank<-6:
            return "<:otEvolD3:791684336784769045>"
        return ""
    return ""


def addtoFields(field1:str,field2:str,field3:str,mobile:bool,rank:str,nom:str,count:str) -> (str, str, str):
    """Ajoute aux textes de champs d'un embed les infos concernant le rang, le nom et le compteur d'une personne. Si l'embed doit avoir un affichage mobile, la mise en forme est différente.
    Entrées :
        field1, field2, field3 : les textes des trois champs de l'embed
        mobile : si l'affichage mobile est activé
        rank, nom, count : le rang, le nom et le compteur à ajouter
    Sorties :
        field1, field2, field3 : les textes des trois champs de l'embed modifiés"""
    if mobile:
        field1+="{0} : {1} - {2}\n".format(rank,nom,count)
    else:
        field1+="{0}\n".format(rank)
        field2+="{0}\n".format(nom)
        field3+="{0}\n".format(count)
    return field1, field2, field3

def createFields(mobile,embed,f1,f2,f3,nf1,nf2,nf3):
    if mobile:
        embed.description="**{0} : {1} - {2}**\n{3}".format(nf1,nf2,nf3,f1)
    else:
        embed.add_field(name=nf1,value=f1,inline=True)
        embed.add_field(name=nf2,value=f2,inline=True)
        embed.add_field(name=nf3,value=f3,inline=True)
    return embed


def newDescip(descip:(str or None),option:str,obj:str,guildOT:OTGuild,bot:commands.Bot) -> str:
    """Si les statistiques affichées concernent un objet (salon, rôle, emote, ...), l'ajoute en haut de la description de l'embed. Si l'embed n'a pas de description, devient la description.
    Entrées : 
        descip : la description de l'embed
        option : le domaine de la commande
        obj : l'ID de l'objet
        guildOT : l'objet OTGuild du serveur d'où vient la commande (OTGuild)
        bot : l'objet bot du bot
    Sortie : 
        descip : la nouvelle description"""
    if descip==None:
        descip=nomsOptions(option,int(obj),guildOT,bot)
    else:
        descip="{0}\n-----\n{1}".format(nomsOptions(option,int(obj),guildOT,bot),descip)
    return descip

async def exeErrorExcept(interaction:discord.Interaction,bot:commands.Bot,reply) -> discord.Embed:
    """Fonction qui envoie deux embeds en cas d'erreur lors d'une commande : un pour l'utilisateur et un autre pour le support, avec des informations plus détaillées.
    Entrées : 
        ctx : toutes les infos de la commande
        bot : l'objet bot du bot
        args : les arguments qui avaient été donnés avec la commande
    Sortie :
        embedE : l'embed d'erreur pour l'utilisateur"""

    embedUser=createEmbed("<:otROUGE:868535622237818910> Erreur","Une erreur est survenue lors de l'execution de la commande.\nUn rapport a été envoyé au support.\n{0}".format(sys.exc_info()[0]),0xff0000,interaction.command.name,interaction.user)
    embedLog=createEmbed("Erreur","Commande : {0}\nSalon : {1} | {1.id}\nServeur : {2} | {2.id}\nAuteur : {3} | {3.id}\nInfos : {4}\nArguments : {5}".format(interaction.command.name,interaction.message.channel,interaction.guild,interaction.user,traceback.format_exc(),interaction.namespace),0x3498db,"Log",interaction.guild)
    
    await bot.get_channel(726000546401615912).send(embed=embedLog)
    if reply:
        await interaction.response.send_message(embed=embedUser)
    elif reply==None:
        return embedUser


def createEmbed(title:str,descip:str,color:int,command:str,author:(discord.Member or discord.Guild)) -> discord.Embed:
    """Cette fonction créée un embed rapidement.
    Entrées : 
        title : le titre de l'embed
        descip : la description de l'embed
        color : la couleur de l'embed
        command : le nom de la commande
        option : l'option pour savoir quoi mettre en author
    Sortie :
        embed : l'embed créé"""

    embed=discord.Embed(title=title,description=descip,color=color)
    embed.set_footer(text="OT!"+command)
    if type(author)==discord.Guild:
        auteur(author.id,author.name,author.icon,embed,"guild")
    elif type(author)==discord.Member:
        auteur(author.id,author.nick or author.name,author.display_avatar,embed,"user")
    elif author is None:
        pass
    else:
        auteur(author.id,author.name,author.display_avatar,embed,"user")
    return embed


async def sendEmbed(ctx:commands.Context,embed:discord.Embed,react:bool,boutons:bool,curseurCMD:sqlite3.Cursor,connexionCMD:sqlite3.Connection,page:int,pagemax:int) -> (discord.Message or None):
    """Fonction qui envoie et modifie les embeds des commandes nécessitants des boutons. Elle permet aussi de mettre à jour la base de données des commandes du serveur d'où provient la commande, notamment quelle est la page actuelle et quel est le nombre de pages maximal.
    Entrées : 
        ctx : contexte de la commande
        embed : embed à envoyer
        react : s'il faut éditer ou envoyer le message
        boutons : s'il faut réagir avec les boutons spéciaux
        curseurCMD, connexionCMD : connexion à la base de données des commandes du serveur
        page : page actuelle
        pagemax : page maximale
    Sortie :
        Si react==True : rien, sinon le message envoyé."""

    try:
        if react:
            await ctx.message.edit(embed=embed)
            curseurCMD.execute("UPDATE commandes SET Page={0}, PageMax={1} WHERE MessageID={2}".format(page,pagemax,ctx.message.id))
            connexionCMD.commit()
        else:
            message=await ctx.reply(embed=embed)
            if pagemax!=1:
                await message.add_reaction("<:otGAUCHE:772766034335236127>")
                await message.add_reaction("<:otDROITE:772766034376523776>")
                await message.add_reaction("<:otCHOIXPAGE:887022335578767420>")
            if boutons:
                await message.add_reaction("<:otGRAPH:772766034558058506>")
                await message.add_reaction("<:otTRI:833666016491864114>")
                await message.add_reaction("<:otMOBILE:833736320919797780>")
            curseurCMD.execute("UPDATE commandes SET Page={0}, PageMax={1}, MessageID={2} WHERE MessageID={3}".format(page,pagemax,message.id,ctx.message.id))
            connexionCMD.commit()
            return message
    except discord.errors.Forbidden:
        await embedAssert(ctx,"Je n'ai pas pu envoyer les réactions de cette commande, qui servent à naviguer dedans. Donnez moi les permissions 'utiliser emojis externes' et 'ajouter des réactions' si vous ne voulez plus voir ce message, et profiter à fond de mes possibilités.",True)


def embedHisto(ctx:commands.Context,bot:commands.Bot) -> discord.Embed:
    """Fonction qui génère l'embed à envoyer dans l'historique des commandes invoquées sur le serveur de tests."""
    if ctx.guild==None:
        return createEmbed("Commande exécutée","Commande : OT!{0}\nServeur : Message Privé\nAuteur : {1} - {2}\n{3}".format(ctx.command.qualified_name,ctx.author.name,ctx.author.id,ctx.args[2:len(ctx.args)]),0x6ec8fa,"OT Log",bot.user)
    else:
        return createEmbed("Commande exécutée","Commande : OT!{0}\nServeur : {1} - {2}\nSalon : {3} - {4}\nAuteur : {5} - {6}\n{7}".format(ctx.command.qualified_name,ctx.guild.name,ctx.guild.id,ctx.channel.name,ctx.channel.id,ctx.author.name,ctx.author.id,ctx.args[2:len(ctx.args)]),0x6ec8fa,"OT Log",bot.user)


async def embedAssert(interaction:discord.Interaction,info:str,reply:bool) -> discord.Embed:
    """Génère l'embed à envoyer si une AssertionError est relevée.
    Entrée :
        info : les informations de l'erreur
    Sortie :
        embedTable : l'embed à envoyer"""
    if info=="mp":
        embed=createEmbed("<:otORANGE:868538903584456745> Erreur","Cette commande n'est pas compatible dans les messages privés !",0xff9900,interaction.command.name,interaction.user)
    else:
        embed=createEmbed("<:otROUGE:868535622237818910> Erreur",str(info),0xff0000,interaction.command.name,interaction.user)
    await interaction.response.send_message(embed=embed)

def embedAssertClassic(info:str) -> discord.Embed:
    """Génère l'embed à envoyer si une AssertionError est relevée.
    Entrée :
        info : les informations de l'erreur
    Sortie :
        embedTable : l'embed à envoyer"""
    if info=="mp":
        embedTable=discord.Embed(title="<:otORANGE:868538903584456745> Erreur", description="Cette commande n'est pas compatible dans les messages privés !",color=0xff9900)
    else:
        embedTable=discord.Embed(title="<:otROUGE:868535622237818910> Erreur", description=str(info),color=0xff0000)
    embedTable.set_footer(text="Avertissement")
    return embedTable
