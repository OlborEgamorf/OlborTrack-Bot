from Core.Fonctions.WebRequest import getAttachment, getAvatar
from Core.Fonctions.Embeds import createEmbed, embedAssert
from Outils.Bienvenue.Manipulation import fusion, squaretoround
from Core.Fonctions.Phrase import createPhrase
import discord
from Stats.SQL.ConnectSQL import connectSQL
import asyncio

async def addImage(ctx,bot):
    try:
        embed=createEmbed("Ajout image de bienvenue","Pour ajouter une image de bienvenue à la collection, envoyez l'image que vous voulez.\nElle doit dépasser 256 pixels en largeur et en hauteur.",0xf54269,ctx.invoked_with.lower(),ctx.guild)
        message=await ctx.reply(embed=embed)

        def check(mess):
            return mess.author.id==ctx.author.id and mess.channel.id==ctx.channel.id and mess.attachments!=[]
        
        mess=await bot.wait_for("message",check=check,timeout=60)

        path=await getAttachment(mess)
        await getAvatar(ctx.author)
        squaretoround(ctx.author.id)

        config=True
        while config:
            
            embed=createEmbed("Ajout image de bienvenue","Voulez vous ajouter un texte en dessous ?\nAppuyez sur <:otVALIDER:772766033996021761> pour en ajouter un, ou <:otANNULER:811242376625782785> pour continuer sans et voir l'aperçu final.",0xf54269,ctx.invoked_with.lower(),ctx.guild)
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
                embed=createEmbed("Ajout image de bienvenue","Pour ajouter un texte sur cette image, écrivez la phrase que vous voulez.\nPour afficher le nom du membre qui a rejoint, utilisez la balise `{name}`.\nPour écrire le nom de votre serveur, utilisez la balise `{guild}`.\nPour montrer le nombre de membre sur votre serveur, utilisez la balise `{number}`.",0xf54269,ctx.invoked_with.lower(),ctx.guild)
                message=await ctx.reply(embed=embed)

                def check(mess):
                    return mess.author.id==ctx.author.id and mess.channel.id==ctx.channel.id
                
                mess=await bot.wait_for("message",check=check,timeout=60)

                text=createPhrase(mess.content.split(" "))
            else:
                text=None

            fusion(path,ctx.author,text,"default",30,ctx.guild)
            embed=createEmbed("Ajout image de bienvenue","Voici le résultat final de votre image. Cela vous convient-il ?\nAppuyez sur <:otVALIDER:772766033996021761> pour valider ou <:otANNULER:811242376625782785> pour revenir en arrière.",0xf54269,ctx.invoked_with.lower(),ctx.guild)
            message=await ctx.reply(embed=embed,file=discord.File("Temp/BV{0}.png".format(ctx.author.id)))
            await message.add_reaction("<:otVALIDER:772766033996021761>")
            await message.add_reaction("<:otANNULER:811242376625782785>")

            def check(reaction,user):
                if type(reaction.emoji)==str:
                    return False
                return reaction.emoji.id in (772766033996021761,811242376625782785) and reaction.message.id==message.id and user.id==ctx.author.id
            
            reaction,user=await bot.wait_for('reaction_add', check=check, timeout=60)
            await message.clear_reactions()

            if reaction.emoji.id==772766033996021761:
                config=False

        connexion,curseur=connectSQL(ctx.guild.id,"Guild","Guild",None,None)
        num=curseur.execute("SELECT COUNT() as Nombre FROM imagesBV").fetchone()["Nombre"]+1
        curseur.execute("INSERT INTO imagesBV VALUES({0},'{1}','{2}','default',50,'all')".format(num,path,text))
        connexion.commit()

        embed=createEmbed("Ajout image de bienvenue","L'image a bien été enregistrée !\nNuméro de l'image : `{0}`".format(num),0xf54269,ctx.invoked_with.lower(),ctx.guild)
        await ctx.reply(embed=embed)
    
    except AssertionError as er:
        await ctx.reply(embed=embedAssert(er))
    except asyncio.exceptions.TimeoutError:
        await message.reply(embed=embedAssert("Une minute s'est écoulée et vous n'avez pas confirmé l'ajout. L'opération a été annulée"))
        await message.clear_reactions()