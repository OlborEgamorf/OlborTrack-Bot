import sqlite3
import sys

import discord
from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.GetNom import nomsOptions
from Core.OTGuild import OTGuild
from discord.ext import commands
from Core.Fonctions.TempsVoice import formatCount


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


def newDescip(descip:(str or discord.embeds._EmptyEmbed),option:str,obj:str,guildOT:OTGuild,bot:commands.Bot) -> str:
    """Si les statistiques affichées concernent un objet (salon, rôle, emote, ...), l'ajoute en haut de la description de l'embed. Si l'embed n'a pas de description, devient la description.
    Entrées : 
        descip : la description de l'embed
        option : le domaine de la commande
        obj : l'ID de l'objet
        guildOT : l'objet OTGuild du serveur d'où vient la commande (OTGuild)
        bot : l'objet bot du bot
    Sortie : 
        descip : la nouvelle description"""
    if type(descip)==discord.embeds._EmptyEmbed:
        descip=nomsOptions(option,int(obj),guildOT,bot)
    else:
        descip="{0}\n-----\n{1}".format(nomsOptions(option,int(obj),guildOT,bot),descip)
    return descip


def embedError(guild:discord.Guild,channel:discord.TextChannel,author:discord.Member,error:str,commande:str) -> (discord.Embed, discord.Embed):
    """Fonction qui génére deux embeds en cas d'erreur lors d'une commande : un pour l'utilisateur et un autre pour le support.
    Entrées : 
        guild : le serveur où l'erreur s'est produite
        channel : le salon où l'erreur s'est produite
        author : l'auteur de la commande qui a échoué
        error : les infos de l'erreur
        commande : le nom de la commande
    Sorties :
        embedTable : l'embed pour l'utilisateur
        embedHistorique : l'embed pour le support"""
    embedTable=discord.Embed(title="<:otRED:718392916061716481> Erreur", description="Une erreur est survenue lors de l'execution de la commande.\nUn rapport a été envoyé au support.\n"+error,color=0xff0000)
    embedTable.set_footer(text="Avertissement")
    embedHistorique=discord.Embed(description="**Erreur : OT!"+commande+"** "+str(channel)+" "+str(channel.id)+" | "+str(guild)+" "+str(guild.id)+" | "+str(author)+" "+str(author.id)+"\n"+error, color=0x3498db)
    embedHistorique.set_footer(text="OlborTrack Log")
    return embedTable, embedHistorique


async def exeErrorExcept(ctx:commands.Context,bot:commands.Bot,args:str) -> discord.Embed:
    """Fonction qui envoie deux embeds en cas d'erreur lors d'une commande : un pour l'utilisateur et un autre pour le support, avec des informations plus détaillées.
    Entrées : 
        ctx : toutes les infos de la commande
        bot : l'objet bot du bot
        args : les arguments qui avaient été donnés avec la commande
    Sortie :
        embedE : l'embed d'erreur pour l'utilisateur"""
    argsstr=""
    for i in range(1,len(ctx.args)):
        argsstr+=str(ctx.args[i])+" "
    error=str(sys.exc_info()[0])+"\n"+str(sys.exc_info()[1])+"\n"+str(sys.exc_info()[2].tb_frame)+"\n"+str(sys.exc_info()[2].tb_lineno)
    embedE=embedError(ctx.guild,ctx.message.channel,ctx.author,str(sys.exc_info()[0]),str(ctx.invoked_with)+" "+argsstr)[0]
    embedHistorique=embedError(ctx.guild,ctx.message.channel,ctx.author,error,str(ctx.invoked_with)+" "+argsstr)[1]
    await bot.get_channel(726000546401615912).send(embed=embedHistorique)
    return embedE


def createEmbed(title:str,descip:str,color:int,command:str,option:(discord.Member or discord.Guild)) -> discord.Embed:
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
    if type(option)==discord.Guild:
        auteur(option.id,option.name,option.icon,embed,"guild")
    else:
        auteur(option.id,option.name,option.avatar,embed,"user")
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
    if react:
        await ctx.message.edit(embed=embed)
        curseurCMD.execute("UPDATE commandes SET Page={0}, PageMax={1} WHERE MessageID={2}".format(page,pagemax,ctx.message.id))
        connexionCMD.commit()
    else:
        message=await ctx.reply(embed=embed)
        if pagemax!=1:
            await message.add_reaction("<:otGAUCHE:772766034335236127>")
            await message.add_reaction("<:otDROITE:772766034376523776>")
        if boutons:
            await message.add_reaction("<:otGRAPH:772766034558058506>")
            await message.add_reaction("<:otTRI:833666016491864114>")
            await message.add_reaction("<:otMOBILE:833736320919797780>")
        curseurCMD.execute("UPDATE commandes SET Page={0}, PageMax={1}, MessageID={2} WHERE MessageID={3}".format(page,pagemax,message.id,ctx.message.id))
        connexionCMD.commit()
        return message


def embedHisto(ctx:commands.Context,bot) -> discord.Embed:
    """Fonction qui génère l'embed à envoyer dans l'historique des commandes invoquées sur le serveur de tests."""
    return createEmbed("Commande exécutée","Commande : OT!{0}\nServeur : {1} - {2}\nSalon : {3} - {4}\nAuteur : {5} - {6}\n{7}".format(ctx.command.name,ctx.guild.name,ctx.guild.id,ctx.channel.name,ctx.channel.id,ctx.author.name,ctx.author.id,ctx.args[2:len(ctx.args)]),0x6ec8fa,"OT Log",bot.user)


def embedAssert(info:str) -> discord.Embed:
    """Génère l'embed à envoyer si une AssertionError est relevée.
    Entrée :
        info : les informations de l'erreur
    Sortie :
        embedTable : l'embed à envoyer"""
    if info=="mp":
        embedTable=discord.Embed(title="<:otORANGE:718396570755661884> Erreur", description="Cette commande n'est pas compatible dans les messages privés !",color=0xff9900)
    else:
        embedTable=discord.Embed(title="<:otRED:718392916061716481> Erreur", description=str(info),color=0xff0000)
    embedTable.set_footer(text="Avertissement")
    return embedTable

def countRankCompare(table,table2,i,option):
    if table2==None:
        rang1="__{0}e__".format(table[i]["Rank"])
        count1="__{0}__".format(formatCount(option,table[i]["Count"]))
        rang2="//"
        count2="//"
    else:
        if table[i]["Rank"]<table2["Rank"]:
            rang1="__{0}e__".format(table[i]["Rank"])
            rang2="{0}e".format(table2["Rank"])
        elif table[i]["Rank"]!=table2["Rank"]:
            rang1="{0}e".format(table[i]["Rank"])
            rang2="__{0}e__".format(table2["Rank"])
        else:
            rang1="{0}e".format(table[i]["Rank"])
            rang2="{0}e".format(table2["Rank"])
        
        if table[i]["Count"]>table2["Count"]:
            count1="__{0}__".format(formatCount(option,table[i]["Count"]))
            count2="{0}".format(formatCount(option,table2["Count"]))
        elif table[i]["Count"]!=table2["Count"]:
            count1="{0}".format(formatCount(option,table[i]["Count"]))
            count2="__{0}__".format(formatCount(option,table2["Count"]))
        else:
            count1="{0}".format(formatCount(option,table[i]["Count"]))
            count2="{0}".format(formatCount(option,table2["Count"]))
    return rang1,rang2,count1,count2