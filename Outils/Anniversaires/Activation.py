import asyncio
from time import strftime

from Core.Fonctions.Embeds import createEmbed, embedAssert
from Core.Fonctions.GetPeriod import getAnnee, getMois
from Core.Fonctions.Phrase import createPhrase
from Outils.Anniversaires.Formatage import formatageAnniv
from Stats.SQL.ConnectSQL import connectSQL


async def toggleAnniversaire(ctx,bot,chan,guild):
    try:
        connexion,curseur=connectSQL(ctx.guild.id,"Guild","Guild",None,None)
        etat=curseur.execute("SELECT * FROM etatAnniv").fetchone()
        if etat["Statut"]==False or chan:
            embed=createEmbed("Activation anniversaires","Pour activer les anniversaires automatiques, donnez moi le salon dans lequel les messages seront envoyés.",0xf54269,ctx.invoked_with.lower(),ctx.guild)
            message=await ctx.reply(embed=embed)

            def check(mess):
                return mess.author.id==ctx.author.id and mess.channel.id==ctx.channel.id and mess.channel_mentions!=[]
            
            mess=await bot.wait_for("message",check=check,timeout=60)
            chan=mess.channel_mentions[0].id

            assert mess.channel_mentions[0].permissions_for(ctx.guild.get_member(bot.user.id)).view_channel==True, "Le salon mentionné n'a pas les permissions nécessaires pour que je puisse le voir."
            assert mess.channel_mentions[0].permissions_for(ctx.guild.get_member(bot.user.id)).send_messages==True, "Le salon mentionné n'a pas les permissions nécessaires pour que je puisse envoyer des messages."

            embed=createEmbed("Activation anniversaires","Maintenant, donnez moi le message qui sera envoyé à chaque anniversaire.\nAjoutez la balise `{user}` pour mentionner le membre fêté.\nAjoutez la balise `{name}` pour ajouter le nom du membre fêté.\nAjoutez la balise `{date}` pour ajouter la date du jour.",0xf54269,ctx.invoked_with.lower(),ctx.guild)
            message=await ctx.reply(embed=embed)

            def check(mess):
                return mess.author.id==ctx.author.id and mess.channel.id==ctx.channel.id
            
            mess=await bot.wait_for("message",check=check,timeout=60)
            clean=createPhrase(mess.content.split(" "))
            exemple=formatageAnniv(clean,bot.user)

            embed=createEmbed("Activation anniversaires","Le salon dans lequel les messages seront envoyés sera <#{0}>.\nLe message sera : {1}\n Est-ce bon ? Appuyez sur <:otVALIDER:772766033996021761> pour valider.".format(chan,exemple),0xf54269,ctx.invoked_with.lower(),ctx.guild)

            message=await ctx.reply(embed=embed)
            await message.add_reaction("<:otVALIDER:772766033996021761>")

            def check(reaction,user):
                if type(reaction.emoji)==str:
                    return False
                return reaction.emoji.id==772766033996021761 and reaction.message.id==message.id and user.id==ctx.author.id
            
            reaction,user=await bot.wait_for('reaction_add', check=check, timeout=60)
            await message.clear_reactions()

            curseur.execute("UPDATE etatAnniv SET Statut=True, Salon={0}, Message='{1}'".format(chan,clean))
            connexion.commit()

            embed=createEmbed("Activation anniversaires","Opération validée !\n----",0xf54269,ctx.invoked_with.lower(),ctx.guild)
            await ctx.reply(embed=embed)
        
        else:
            embed=createEmbed("Désactivation anniversaires","Voulez-vous vraiment désactiver les messages d'anniversaires pour votre serveur ?\nSi vous changez d'avis plus tard, les dates enregistrées restent dans la base de données.\nAppuyez sur <:otVALIDER:772766033996021761> pour valider.",0xf54269,ctx.invoked_with.lower(),ctx.guild)

            message=await ctx.reply(embed=embed)
            await message.add_reaction("<:otVALIDER:772766033996021761>")

            def check(reaction,user):
                if type(reaction.emoji)==str:
                    return False
                return reaction.emoji.id==772766033996021761 and reaction.message.id==message.id and user.id==ctx.author.id

            reaction,user=await bot.wait_for('reaction_add', check=check, timeout=60)
            await message.clear_reactions()

            curseur.execute("UPDATE etatAnniv SET Statut=False, Salon=0, Message='None'")
            connexion.commit()

            embed=createEmbed("Désactivation anniversaires","Opération validée !",0xf54269,ctx.invoked_with.lower(),ctx.guild)
            await ctx.reply(embed=embed)
        guild.getAnniv()
    except AssertionError as er:
        await ctx.reply(embed=embedAssert(er))
    except asyncio.exceptions.TimeoutError:
        await message.reply(embed=embedAssert("Une minute s'est écoulée et vous n'avez pas confirmé l'activation. L'opération a été annulée"))
        await message.clear_reactions()
