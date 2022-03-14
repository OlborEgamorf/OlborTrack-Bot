import asyncio
from random import choice
import sqlite3
from time import strftime

from Core.Decorator import OTCommand
from Core.Fonctions.Embeds import createEmbed
from Core.Fonctions.Phrase import createPhrase
from Stats.SQL.ConnectSQL import connectSQL

from Savezvous.ListModo import commandeSV
import discord
from discord.ext import commands


@OTCommand
async def exeSavezVous(ctx:commands.Context,bot:commands.Bot,args:list):
    """Couroutine qui englobe l'exécution de toutes les commandes du module SavezVous. Fonctionne avec le système d'exceptions OTCommand."""
    args=args.split(" ")
    connexion,curseur=connectSQL(ctx.guild.id,"Guild","Guild",None,None)
    if len(args)==0 or args[0]=="" or ctx.invoked_with not in ("add", "del", "list", "modo", "edit", "source", "comment"):
        embed=showSV(ctx.guild,bot)
    else:
        if ctx.invoked_with=="add":
            embed=addSV(ctx,args,curseur)
        elif ctx.invoked_with=="del":
            embed=deleteSV(ctx,args,curseur)
        elif ctx.invoked_with=="edit":
            embed=editSV(ctx,args,curseur)
        elif ctx.invoked_with=="source":
            embed=sourceSV(ctx,args,curseur) 
        elif ctx.invoked_with=="comment":
            embed=await commentSV(ctx,args,bot,curseur) 
        else:
            await commandeSV(ctx,ctx.invoked_with,None,False,None,bot)
            return
    connexion.commit()
    await ctx.reply(embed=embed)


def showSV(guild:discord.Guild,bot:commands.Bot,number=None) -> discord.Embed:
    """Fonction qui génère un Embed contenant une phrase venant de la boîte SavezVous d'un serveur donné. Fonctionne pour la commande normale et la commande automatique.
    Renvoie une erreur si la boîte est vide."""
    connexion,curseur=connectSQL(guild.id,"Guild","Guild",None,None)
    
    if number==None:
        ligne=curseur.execute("SELECT * FROM savezvous ORDER BY RANDOM() ASC").fetchone()
    else:
        ligne=curseur.execute("SELECT * FROM savezvous WHERE Count={0}".format(number)).fetchone()
    assert ligne!=None, "Vous devez commencer par ajouter une phrase avec `OT!savezvous add` !"

    user=guild.get_member(ligne["ID"])
    if user==None:
        embed=createEmbed("","",guild.get_member(bot.user.id).color.value,"savezvous",bot.user)
    else:
        embed=createEmbed("","",user.color.value,"savezvous",user)

    embed.add_field(name="Savez-vous ?",value=ligne["Texte"],inline=False)
    
    if ligne["Image"]!="None":
        embed.set_image(url=ligne["Image"])
    
    embed.add_field(name="N°",value="`{0}`".format(ligne["Count"]),inline=True)

    updates=curseur.execute("SELECT * FROM svcomment WHERE Count={0} AND ID={1}".format(ligne["Count"],ligne["ID"])).fetchall()
    if updates!=[]:
        descip=""
        for i in updates:
            descip+="- {0} : {1}\n".format(i["Date"],i["Texte"])
        embed.add_field(name="Mises à jour de l'auteur",value=descip,inline=True)

    if ligne["Source"]!="None":
        embed.add_field(name="Source",value=ligne["Source"],inline=True)

    comment=curseur.execute("SELECT * FROM svcomment WHERE Count={0} AND ID<>{1} ORDER BY RANDOM() ASC".format(ligne["Count"],ligne["ID"])).fetchone()
    if comment!=None:
        user=guild.get_member(comment["ID"])
        if user==None:
            embed.add_field(name="Commentaire d'un ancien membre",value=comment["Texte"],inline=False)
        else:
            embed.add_field(name="Commentaire de {0}".format(user.nick or user.name),value=comment["Texte"],inline=False)
    return embed


def addSV(ctx:commands.Context,args:list,curseur:sqlite3.Cursor) -> discord.Embed:
    """Fonction qui ajoute une phrase à la boîte SavezVous d'un serveur. Renvoie une erreur si la phrase contenue dans args est vide ou si la phrase dépasse les 2000 caractères."""
    assert len(args)!=0, "Vous devez me donner une phrase !"
    if ctx.message.attachments!=[]:
        image=ctx.message.attachments[0].url
    else:
        image=None
    descip=createPhrase(args[0:len(args)])
    assert len(descip)<2000, "Votre phrase est trop longue."
    count=curseur.execute("SELECT COUNT() as Nb FROM savezvous").fetchone()["Nb"]
    curseur.execute("INSERT INTO savezvous VALUES('{0}',{1},'{2}',{3},'None')".format(descip,ctx.author.id,image,count+1))
    embed=createEmbed("Phrase ajoutée","`{0}` : {1}".format(count+1,descip),0x00ffd0,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)
    if image!=None:
        embed.set_image(url=image)
    return embed


def deleteSV(ctx:commands.Context,args:list,curseur:sqlite3.Cursor) -> discord.Embed:
    """Fonction qui supprime une phrase de la boite SavezVous d'un serveur. Doit être accompagné d'un numéro de phrase valide pour le serveur dans args, sinon renvoie une erreur. Une phrase ne peut être supprimée que par son auteur ou un modérateur."""
    assert len(args)!=0, "Vous devez me donner le numéro de la phrase que vous voulez supprimer !"
    try:
        descip=curseur.execute("SELECT * FROM savezvous WHERE Count={0}".format(args[0])).fetchone()
    except:
        raise AssertionError("Le numéro donné n'est pas valide.")
    assert descip!=None, "Le numéro donné ne correspond à aucune phrase."
    assert ctx.author.id==descip["ID"] or ctx.author.guild_permissions.manage_messages==True, "Cette phrase ne vous appartient pas."
    curseur.execute("DELETE FROM savezvous WHERE Count={0}".format(args[0]))
    for i in curseur.execute("SELECT * FROM savezvous WHERE Count>{0} ORDER BY Count ASC".format(args[0])).fetchall():
        curseur.execute("UPDATE savezvous SET Count={0} WHERE Count={1}".format(i["Count"]-1, i["Count"]))
    return createEmbed("Phrase supprimée","`{0}` : {1}".format(args[0],descip["Texte"]),0x00ffd0,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)


def editSV(ctx:commands.Context,args:list,curseur:sqlite3.Cursor) -> discord.Embed:
    """Fonction qui édite une phrase de la boite SavezVous d'un serveur. La phrase doit appartenir à l'auteur de la commande, doit être accompagné d'un numéro de phrase valide pour le serveur dans args, et d'une nouvelle phrase, sinon renvoie une erreur."""
    assert len(args)>1, "Vous devez me donner le numéro de la phrase que vous voulez modifier et la nouvelle phrase !"
    try:
        phrase=curseur.execute("SELECT * FROM savezvous WHERE Count={0}".format(args[0])).fetchone()
        assert phrase!=None, "Le numéro donné ne correspond à aucune phrase."
    except:
        raise AssertionError("Le numéro donné n'est pas valide.")
    assert ctx.author.id==phrase["ID"], "Cette phrase ne vous appartient pas."
    descip=createPhrase(args[1:len(args)])
    assert len(descip)<2000, "Votre phrase est trop longue."
    curseur.execute("UPDATE savezvous SET Texte='{0}' WHERE Count={1}".format(descip,args[0]))
    return createEmbed("Phrase modifiée","`{0}` : {1}".format(args[0],descip),0x00ffd0,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)


def sourceSV(ctx:commands.Context,args:list,curseur:sqlite3.Cursor) -> discord.Embed:
    """Fonction qui ajoute une source à une phrase de la boite SavezVous d'un serveur. La phrase doit appartenir à l'auteur de la commande, doit être accompagné d'un numéro de phrase valide pour le serveur dans args, et d'une nouvelle phrase, sinon renvoie une erreur."""
    assert len(args)>1, "Vous devez me donner le numéro de la phrase que vous voulez modifier et la nouvelle phrase !"
    try:
        phrase=curseur.execute("SELECT * FROM savezvous WHERE Count={0}".format(args[0])).fetchone()
        assert phrase!=None, "Le numéro donné ne correspond à aucune phrase."
    except:
        raise AssertionError("Le numéro donné n'est pas valide.")
    assert ctx.author.id==phrase["ID"], "Cette phrase ne vous appartient pas."
    descip=createPhrase(args[1:len(args)])
    assert len(descip)<200, "Votre source est trop longue."
    curseur.execute("UPDATE savezvous SET Source='{0}' WHERE Count={1}".format(descip,args[0]))
    return createEmbed("Phrase sourcée","`{0}` : {1}\n\nSource : {2}".format(args[0],phrase["Texte"],descip),0x00ffd0,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)


async def commentSV(ctx:commands.Context,args:list,bot:commands.Bot,curseur:sqlite3.Cursor) -> discord.Embed:
    """Fonction qui ajoute une source à une phrase de la boite SavezVous d'un serveur. La phrase doit appartenir à l'auteur de la commande, doit être accompagné d'un numéro de phrase valide pour le serveur dans args, et d'une nouvelle phrase, sinon renvoie une erreur."""
    assert len(args)>1, "Vous devez me donner le numéro de la phrase que vous voulez modifier et la nouvelle phrase !"
    try:
        phrase=curseur.execute("SELECT * FROM savezvous WHERE Count={0}".format(args[0])).fetchone()
        assert phrase!=None, "Le numéro donné ne correspond à aucune phrase."
    except:
        raise AssertionError("Le numéro donné n'est pas valide.")
    descip=createPhrase(args[1:len(args)])
    assert len(descip)<300, "Votre commentaire est trop long."
    if ctx.author.id==phrase["ID"]:
        curseur.execute("INSERT INTO svcomment VALUES ({0},{1},'{2}','{3}')".format(phrase["Count"],ctx.author.id,descip,strftime("%d/%m/%Y")))
        return createEmbed("Mise à jour ajoutée","`{0}` : {1}\n\nCommentaire : {2}".format(args[0],phrase["Texte"],descip),0x00ffd0,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)
    else:
        message=await ctx.reply(content="<@{0}>, quelqu'un veut ajouter un commentaire sur votre phrase :\n{1}".format(phrase["ID"],descip),embed=showSV(ctx.guild,bot,args[0]))
        await message.add_reaction("<:otVALIDER:772766033996021761>")
        await message.add_reaction("<:otANNULER:811242376625782785>")

        def checkValid(reaction,user):
            if type(reaction.emoji)==str:
                return False
            return reaction.emoji.id in (772766033996021761,811242376625782785) and reaction.message.id==message.id and user.id==phrase["ID"]

        try:
            reaction,user=await bot.wait_for('reaction_add', check=checkValid, timeout=600)
            await message.clear_reactions()
            if reaction.emoji.id==772766033996021761:
                curseur.execute("INSERT INTO svcomment VALUES ({0},{1},'{2}','{3}')".format(phrase["Count"],ctx.author.id,descip,strftime("%d/%m/%Y")))
                return createEmbed("Commentaire ajouté","`{0}` : {1}\n\nCommentaire : {2}".format(args[0],phrase["Texte"],descip),0x00ffd0,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)
            else:
                return createEmbed("Commentaire refusé","L'auteur de la phrase n'a pas voulu que votre commentaire soit ajouté.",0x00ffd0,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)
        except asyncio.exceptions.TimeoutError:
            await message.clear_reactions()
            return createEmbed("Commentaire refusé","L'auteur de la phrase n'a pas voulu que votre commentaire soit ajouté.",0x00ffd0,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)
