import asyncio

import discord
from Core.Fonctions.Embeds import createEmbed, embedAssert
from Core.Fonctions.Phrase import createPhrase
from Core.Fonctions.WebRequest import getAvatar
from Outils.Bienvenue.Manipulation import fusion, fusionAdieu, squaretoround
from Stats.SQL.ConnectSQL import connectSQL


async def modifImage(ctx,bot,args,option):
    dictTitres={"BV":"de bienvenue","AD":"d'adieu"}
    try:
        assert len(args)>0, "Vous devez me donner le numéro de l'image !"
        connexion,curseur=connectSQL(ctx.guild.id,"Guild","Guild",None,None)
        try:
            image=curseur.execute("SELECT * FROM images{0} WHERE Nombre={1}".format(option,args[0])).fetchone()
        except:
            raise AssertionError("Le numéro donné n'est pas valide.")
        assert image!=None, "Le numéro donné ne correspond à aucune image."
        await getAvatar(ctx.author)
        squaretoround(ctx.author.id)
        config=True
        
        while config:
            image=curseur.execute("SELECT * FROM images{0} WHERE Nombre={1}".format(option,args[0])).fetchone()
            texte,couleur,taille,mode=image["Message"],image["Couleur"],image["Taille"],image["Mode"]

            if option=="BV":
                embed=createEmbed("Modification image {0}".format(dictTitres[option]),"Quelles modifications voulez vous effectuer sur votre image ?\n- <:ot1:705766186909958185> : Modifier le texte\n- <:ot2:705766186989912154> : Modifier la taille *(actuel : {0})*\n- <:ot3:705766186930929685> : Modifier la couleur *(actuel : {1})*\n- <:ot4:705766186947706934> Modifier le mode (heure d'activation de l'image) *(actuel : {2})*\n- <:otANNULER:811242376625782785> Ne plus rien faire".format(taille,couleur,mode),0xf54269,ctx.invoked_with.lower(),ctx.guild)
                liste=["<:ot1:705766186909958185>","<:ot2:705766186989912154>","<:ot3:705766186930929685>","<:ot4:705766186947706934>","<:otANNULER:811242376625782785>"]
            else:
                filtre=image["Filtre"]
                dictFiltre={0:"Désactivé",1:"Activé"}
                embed=createEmbed("Modification image {0}".format(dictTitres[option]),"Quelles modifications voulez vous effectuer sur votre image ?\n- <:ot1:705766186909958185> : Modifier le texte\n- <:ot2:705766186989912154> : Modifier la taille *(actuel : {0})*\n- <:ot3:705766186930929685> : Modifier la couleur *(actuel : {1})*\n- <:ot4:705766186947706934> Modifier le mode (heure d'activation de l'image) *(actuel : {2})*\n- <:ot5:705766186713088042> Activer/Désactiver le filtre gris *(actuel : {3})*\n- <:otANNULER:811242376625782785> Ne plus rien faire".format(taille,couleur,mode,dictFiltre[filtre]),0xf54269,ctx.invoked_with.lower(),ctx.guild)
                liste=["<:ot1:705766186909958185>","<:ot2:705766186989912154>","<:ot3:705766186930929685>","<:ot4:705766186947706934>","<:ot5:705766186713088042>","<:otANNULER:811242376625782785>"]

            message=await ctx.reply(embed=embed)
            for i in liste:
                await message.add_reaction(i)

            def check(reaction,user):
                if type(reaction.emoji)==str:
                    return False
                return reaction.emoji.id in (705766186909958185,705766186989912154,705766186930929685,705766186947706934,811242376625782785,705766186713088042) and reaction.message.id==message.id and user.id==ctx.author.id
            
            reaction,user=await bot.wait_for('reaction_add', check=check, timeout=60)
            await message.clear_reactions()

            if reaction.emoji.id==705766186909958185:
                embed=createEmbed("Modification image {0}".format(dictTitres[option]),"Pour ajouter un texte sur cette image, écrivez la phrase que vous voulez.\nPour afficher le nom du membre qui a rejoint, utilisez la balise `{name}`.\nPour écrire le nom de votre serveur, utilisez la balise `{guild}`.\nPour montrer le nombre de membre sur votre serveur, utilisez la balise `{number}`.",0xf54269,ctx.invoked_with.lower(),ctx.guild)
                message=await ctx.reply(embed=embed)

                def check(mess):
                    return mess.author.id==ctx.author.id and mess.channel.id==ctx.channel.id
                
                mess=await bot.wait_for("message",check=check,timeout=60)

                texte=createPhrase(mess.content.split(" "))
            elif reaction.emoji.id==705766186989912154:
                embed=createEmbed("Modification image {0}".format(dictTitres[option]),"Pour ajuster la taille du texte, donnez moi un nombre.\nLa taille actuelle est : **{0}**".format(taille),0xf54269,ctx.invoked_with.lower(),ctx.guild)
                message=await ctx.reply(embed=embed)

                def check(mess):
                    try:
                        int(mess.content)
                    except:
                        pass
                    return mess.author.id==ctx.author.id and mess.channel.id==ctx.channel.id
                
                mess=await bot.wait_for("message",check=check,timeout=60)
                taille=int(mess.content)
            elif reaction.emoji.id==705766186930929685:
                embed=createEmbed("Modification image {0}".format(dictTitres[option]),"Pour modifier la couleur du texte, choisissez entre : default (blanc ou noir en fonction du fond), blanc, noir, rouge, vert, bleu, jaune, cyan.\nLa couleur actuelle est : **{0}**".format(couleur),0xf54269,ctx.invoked_with.lower(),ctx.guild)
                message=await ctx.reply(embed=embed)
                dictColor=["blanc","noir","rouge","vert","bleu","jaune","cyan","default"]
                def check(mess):
                    try:
                        assert mess.content in dictColor
                    except:
                        pass
                    return mess.author.id==ctx.author.id and mess.channel.id==ctx.channel.id
                
                mess=await bot.wait_for("message",check=check,timeout=60)
                couleur=mess.content
            elif reaction.emoji.id==705766186947706934:
                embed=createEmbed("Modification image {0}".format(dictTitres[option]),"Le mode détermine à quelle heure de la journée l'image peut être envoyée. Pour modifier le mode de l'image, choisissez entre : all (s'active tout le temps), jour (ne s'active qu'entre 9h et 22h), nuit (ne s'active qu'entre 22h et 9h).\nLa couleur actuelle est : **{0}**\n*Attention : aucune modification ne sera visible, le mode ne concerne que le déclenchement de la fonctionnalité*".format(mode),0xf54269,ctx.invoked_with.lower(),ctx.guild)
                message=await ctx.reply(embed=embed)
                dictMode=["all","jour","nuit"]
                def check(mess):
                    try:
                        assert mess.content in dictMode
                    except:
                        pass
                    return mess.author.id==ctx.author.id and mess.channel.id==ctx.channel.id
                
                mess=await bot.wait_for("message",check=check,timeout=60)
                mode=mess.content
            elif reaction.emoji.id==705766186713088042:
                embed=createEmbed("Modification image {0}".format(dictTitres[option]),"Le filtre gris est automatiquement activé pour les images d'adieu. Actuellement il est : **{0}**\nAppuyez sur <:otVALIDER:772766033996021761> pour l'activer ou <:otANNULER:811242376625782785> pour le retirer.".format(dictFiltre[filtre]),0xf54269,ctx.invoked_with.lower(),ctx.guild)
                message=await ctx.reply(embed=embed)
                await message.add_reaction("<:otVALIDER:772766033996021761>")
                await message.add_reaction("<:otANNULER:811242376625782785>")

                def check(reaction,user):
                    if type(reaction.emoji)==str:
                        return False
                    return reaction.emoji.id in (772766033996021761,811242376625782785) and reaction.message.id==message.id and user.id==ctx.author.id
                
                reaction,user=await bot.wait_for('reaction_add', check=check, timeout=60)
                await message.clear_reactions()
                if reaction.emoji.id==772766033996021761:
                    filtre=True
                else:
                    filtre=False
            else:
                return
            
            if option=="BV":
                fusion(image["Path"],ctx.author,texte,couleur,taille,ctx.guild)
            else:
                fusionAdieu(image["Path"],ctx.author,texte,couleur,taille,ctx.guild,filtre)
            embed=createEmbed("Modification image {0}".format(dictTitres[option]),"Voici le résultat final de votre image. Cela vous convient-il ?\nAppuyez sur <:otVALIDER:772766033996021761> pour valider ou <:otANNULER:811242376625782785> pour revenir en arrière.",0xf54269,ctx.invoked_with.lower(),ctx.guild)
            message=await ctx.reply(embed=embed,file=discord.File("Temp/{0}{1}.png".format(option,ctx.author.id)))
            await message.add_reaction("<:otVALIDER:772766033996021761>")
            await message.add_reaction("<:otANNULER:811242376625782785>")

            def check(reaction,user):
                if type(reaction.emoji)==str:
                    return False
                return reaction.emoji.id in (772766033996021761,811242376625782785) and reaction.message.id==message.id and user.id==ctx.author.id
            
            reaction,user=await bot.wait_for('reaction_add', check=check, timeout=60)
            await message.clear_reactions()
            if reaction.emoji.id==772766033996021761:
                if option=="BV":
                    curseur.execute("UPDATE imagesBV SET Message='{0}', Couleur='{1}', Taille={2}, Mode='{3}' WHERE Nombre={4}".format(texte,couleur,taille,mode,args[0]))
                else:
                    curseur.execute("UPDATE imagesAD SET Message='{0}', Couleur='{1}', Taille={2}, Mode='{3}', Filtre={4} WHERE Nombre={5}".format(texte,couleur,taille,mode,filtre,args[0]))
                connexion.commit()
    except AssertionError as er:
        await ctx.reply(embed=embedAssert(er))
    except asyncio.exceptions.TimeoutError:
        await message.reply(embed=embedAssert("Une minute s'est écoulée et vous n'avez pas confirmé la modification. L'opération a été annulée"))
        await message.clear_reactions()
