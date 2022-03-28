import asyncio
import os
import sqlite3
from random import choice

import discord
from colorthief import ColorThief
from Core.Decorator import OTCommand
from Core.Fonctions.Embeds import createEmbed
from Core.Fonctions.Phrase import createPhrase
from Core.Fonctions.WebRequest import getIcon
from discord.ext import commands
from Outils.DynamicPP.Toggle import toggleDynIcon
from PIL import Image
from Sondages.exePolls import exePolltime
from Stats.SQL.ConnectSQL import connectSQL


@OTCommand
async def exeDynIcon(ctx,bot,args,guildOT):
    connexion,curseur=connectSQL(ctx.guild.id,"Guild","Guild",None,None)
    if ctx.invoked_with not in ("add", "del", "chan","edit","membres"):
        await toggleDynIcon(ctx,bot,guildOT)
        return
    else:
        assert curseur.execute("SELECT * FROM etatPP").fetchone()["Statut"]==True, "Les icones de serveur dynamiques ne sont pas activées sur votre serveur, vous ne pouvez donc faire aucun ajout ou modification."
        if ctx.invoked_with.lower()=="add":
            embed=await addDynIcon(ctx,bot,args,curseur)
        elif ctx.invoked_with=="del":
            embed=delDynIcon(ctx,args,curseur)
        elif ctx.invoked_with=="chan":
            embed=await chanDynIcon(ctx,curseur)
        elif ctx.invoked_with=="edit":
            embed=editDynIcon(ctx,args,curseur)
        elif ctx.invoked_with=="membres":
            embed=membersDynIcon(ctx,args,curseur)
    connexion.commit()
    await ctx.reply(embed=embed)

async def chanDynIcon(ctx,curseur):
    if ctx.message.channel_mentions==[]:
        curseur.execute("UPDATE etatPP SET Salon=0")
        return createEmbed("Désactivation salon d'envoi","Les icones de serveur ne seront plus envoyées dans le salon précédent.",0xf54269,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)
    else:
        assert type(ctx.message.channel_mentions[0])==discord.TextChannel, "Vous ne pouvez pas me donner de salon vocal !"
        curseur.execute("UPDATE etatPP SET Salon={0}".format(ctx.message.channel_mentions[0].id))
        return createEmbed("Activation/Changement salon d'envoi","Les icones de serveur seront désormais envoyées dans ce salon : <#{0}>.".format(ctx.message.channel_mentions[0].id),0xf54269,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)


# Nombre, Path, Description, Membres, Auteur, Rotation
async def addDynIcon(ctx,bot,args,curseur):
    assert ctx.message.attachments!=[], "Vous devez me donner une image !"

    path=await getIcon(ctx.message)
    resize(path)
    nom=path.split("/")[2]
    if len(args)!=0:
        descip=createPhrase(args)
    else:
        descip="None"

    assert len(descip)<500, "La description de l'image ne doit pas dépasser les 500 caractères !"

    nb=curseur.execute("SELECT COUNT() as Nombre FROM icons").fetchone()["Nombre"]+1
    if ctx.author.guild_permissions.manage_messages:
        curseur.execute("INSERT INTO icons VALUES ({0},'{1}','{2}','None',{3},False)".format(nb,path,descip,ctx.author.id))
        return createEmbed("Icone ajoutée","L'icone a été ajoutée à la rotation.\nDescription : {0}\nNuméro de l'icone : {1}".format(descip,nb),0x00ffd0,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)

    else:
        message=await ctx.reply(embed=createEmbed("Ajout d'icone","<@{0}> souhaite ajouter une icone à la collection d'icones dynamiques du serveur.\nUn modérateur doit valider l'ajout avec <:otVALIDER:772766033996021761>. Il est aussi possible d'invoquer un sondage de 3min avec <:OTHpoll:859840447210848306>.".format(ctx.author.id),0x00ffd0,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild))
        await message.add_reaction("<:otVALIDER:772766033996021761>")
        await message.add_reaction("<:otANNULER:811242376625782785>")
        await message.add_reaction("<:OTHpoll:859840447210848306>")

        def checkValid(reaction,user):
            if type(reaction.emoji)==str:
                return False
            return reaction.emoji.id in (772766033996021761,811242376625782785,859840447210848306) and reaction.message.id==message.id and user.guild_permissions.manage_messages and not user.bot

        try:
            reaction,user=await bot.wait_for('reaction_add', check=checkValid, timeout=300)
            await message.clear_reactions()

            if reaction.emoji.id==772766033996021761:
                curseur.execute("INSERT INTO icons VALUES ({0},'{1}','{2}','None',{3},False)".format(nb,path,descip,ctx.author.id))
                return createEmbed("Icone ajoutée","L'icone a été ajoutée à la rotation, par approbation d'un modérateur.\nDescription : {0}\nNuméro de l'icone : {1}".format(descip,nb),0x00ffd0,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)

            elif reaction.emoji.id==859840447210848306:
                poll=await exePolltime(await bot.get_context(message),bot,["Est-ce qu'il faut ajouter l'icone de {0} ?".format(ctx.author.nick or ctx.author.name), "Oui", "Non", "10s"],"polltime")
                if poll==705766186909958185:
                    curseur.execute("INSERT INTO icons VALUES ({0},'{1}','{2}','None',{3},False)".format(nb,path,descip,ctx.author.id))
                    return createEmbed("Icone ajoutée","L'icone a été ajoutée à la rotation, par vote démocratique.\nDescription : {0}\nNuméro de l'icone : {1}".format(descip,nb),0x00ffd0,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)
                else:
                    os.remove(path)
                    return createEmbed("Ajout refusé","Le peuple a décidé que votre icone ne sera pas ajoutée à la rotation.",0x00ffd0,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)

            else:
                os.remove(path)
                return createEmbed("Ajout refusé","Un modérateur a refusé que votre icone soit ajoutée à la rotation.",0x00ffd0,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)

        except asyncio.exceptions.TimeoutError:
            await message.clear_reactions()
            os.remove(path)
            return createEmbed("Ajout refusé","Le temps de réaction est écoulé, votre icone est refusée.",0x00ffd0,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)


def delDynIcon(ctx:commands.Context,args:list,curseur:sqlite3.Cursor) -> discord.Embed:
    """Fonction qui supprime une phrase de la boite SavezVous d'un serveur. Doit être accompagné d'un numéro de phrase valide pour le serveur dans args, sinon renvoie une erreur. Une phrase ne peut être supprimée que par son auteur ou un modérateur."""
    assert len(args)!=0, "Vous devez me donner le numéro de l'icone que vous voulez supprimer !"
    try:
        icon=curseur.execute("SELECT * FROM icons WHERE Nombre={0}".format(args[0])).fetchone()
    except:
        raise AssertionError("Le numéro donné n'est pas valide.")
    assert icon!=None, "Le numéro donné ne correspond à aucune phrase."
    assert ctx.author.id==icon["Auteur"] or ctx.author.guild_permissions.manage_messages==True, "Cette phrase ne vous appartient pas."
    curseur.execute("DELETE FROM icons WHERE Nombre={0}".format(args[0]))
    for i in curseur.execute("SELECT * FROM icons WHERE Nombre>{0} ORDER BY Nombre ASC".format(args[0])).fetchall():
        curseur.execute("UPDATE icons SET Nombre={0} WHERE Nombre={1}".format(i["Nombre"]-1, i["Nombre"]))
    return createEmbed("Icone supprimée","`{0}` : {1}".format(args[0],icon["Description"]),0x00ffd0,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)


def editDynIcon(ctx:commands.Context,args:list,curseur:sqlite3.Cursor) -> discord.Embed:
    """Fonction qui édite une phrase de la boite SavezVous d'un serveur. La phrase doit appartenir à l'auteur de la commande, doit être accompagné d'un numéro de phrase valide pour le serveur dans args, et d'une nouvelle phrase, sinon renvoie une erreur."""
    assert len(args)>1, "Vous devez me donner le numéro de l'icone que vous voulez modifier et la nouvelle description !"
    try:
        icon=curseur.execute("SELECT * FROM icons WHERE Nombre={0}".format(args[0])).fetchone()
        assert icon!=None, "Le numéro donné ne correspond à aucune phrase."
    except:
        raise AssertionError("Le numéro donné n'est pas valide.")
    if icon["Membres"]=="None":
        members=[]
    else:
        members=icon["Membres"].split(";")
    assert ctx.author.id==icon["Auteur"] or str(ctx.author.id) in members, "Cette phrase ne vous appartient pas ou vous n'êtes pas dessus."
    descip=createPhrase(args[1:])
    assert len(descip)<500, "Votre description est trop longue."
    curseur.execute("UPDATE icons SET Description='{0}' WHERE Nombre={1}".format(descip,args[0]))
    return createEmbed("Description d'icone modifiée","`{0}` : {1}".format(args[0],descip),0x00ffd0,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)


def membersDynIcon(ctx:commands.Context,args:list,curseur:sqlite3.Cursor) -> discord.Embed:
    """Fonction qui édite une phrase de la boite SavezVous d'un serveur. La phrase doit appartenir à l'auteur de la commande, doit être accompagné d'un numéro de phrase valide pour le serveur dans args, et d'une nouvelle phrase, sinon renvoie une erreur."""
    assert len(args)>1, "Vous devez me donner le numéro de l'icone que vous voulez modifier et les membres à ajouter/retirer !"
    assert len(ctx.message.mentions)!=0, "Vous devez mentionner les membres que vous voulez ajouter ou retirer !"
    try:
        icon=curseur.execute("SELECT * FROM icons WHERE Nombre={0}".format(args[0])).fetchone()
        assert icon!=None, "Le numéro donné ne correspond à aucune phrase."
    except:
        raise AssertionError("Le numéro donné n'est pas valide.")
    assert ctx.author.id==icon["Auteur"], "Cette icone ne vous appartient pas."

    if icon["Membres"]=="None":
        members=[]
    else:
        members=icon["Membres"].split(";")

    ids=list(map(lambda x:str(x.id), ctx.message.mentions))
    add=list(filter(lambda x:x not in members,ids))
    delete=list(filter(lambda x:x in members,ids))
    for i in delete:
        members.remove(i)
    for i in add:
        members.append(i)
    
    if len(members)==0:
        end="None"
    else:
        end=";".join(members)

    descip=""
    for i in members:
        descip+="<@{0}> ".format(i)

    curseur.execute("UPDATE icons SET Membres='{0}' WHERE Nombre={1}".format(end,args[0]))
    return createEmbed("Membres présents sur l'icone modifiés","`{0}` : {1}".format(args[0],descip[:-1]),0x00ffd0,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)


async def rotation(guild,channel):
    connexion,curseur=connectSQL(guild.id,"Guild","Guild",None,None)
    icons=curseur.execute("SELECT * FROM icons WHERE Rotation=0").fetchall()
    if len(icons)==0:
        curseur.execute("UPDATE icons SET Rotation=0")
        icons=curseur.execute("SELECT * FROM icons WHERE Rotation=0").fetchall()
        if len(icons)==0:
            return

    img=choice(icons)
    with open(img["Path"],"rb") as image:
        i=image.read()
    color=ColorThief(img["Path"]).get_color(quality=1)
    hexcolor=int('%02x%02x%02x' % color, base=16)

    if True:
        await guild.edit(icon=i)
        embed=discord.Embed(title="Icone du serveur du jour !",color=hexcolor)
        if img["Description"]!="None":
            embed.description=img["Description"]
        else:
            embed.description="*Cette icone n'a pas encore de description !*"
        embed.set_image(url="https://cdn.discordapp.com/icons/{0}/{1}.png?size=600".format(guild.id,guild.icon))
        embed.set_author(icon_url="https://cdn.discordapp.com/icons/{0}/{1}.png".format(guild.id,guild.icon),name=guild.name)
        embed.set_footer(text="OT!dynicon")
        embed.add_field(name="Ajouté par",value="<@{0}>".format(img["Auteur"]),inline=True)
        if img["Membres"]!="None":
            members=img["Membres"].split(";")
            descip=""
            for i in members:
                descip+="<@{0}> ".format(i)
            embed.add_field(name="Membres présents",value=descip,inline=True)
        embed.add_field(name="N°",value="`{0}`".format(img["Nombre"]))
        if channel!=0:
            await guild.get_channel(channel).send(embed=embed)
    """except:
        pass"""

    curseur.execute("UPDATE icons SET Rotation=1 WHERE Nombre={0}".format(img["Nombre"]))
    connexion.commit()


def resize(path):
    img=Image.open(path)
    size=img.size
    if img.size[0]>800:
        img=img.resize((800,int(size[1]*800/size[0])))
    if img.size[1]>800:
        img=img.resize((int(size[0]*800/size[1]),800))
    assert img.size[0]>=400 and img.size[1]>=400, "Il est conseillé d'avoir une image d'au moins 400x400. Essayez de donner des images carrées aussi !"

    img.save(path)
    