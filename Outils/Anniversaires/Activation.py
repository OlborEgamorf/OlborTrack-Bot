import asyncio

from Core.Decorator import OTCommand
from Core.Fonctions.Embeds import createEmbed, embedAssert
from Core.Fonctions.Phrase import createPhrase
from Outils.Anniversaires.Formatage import formatageAnniv
from Stats.SQL.ConnectSQL import connectSQL


@OTCommand
async def toggleAnniversaire(ctx,bot,chan,guild):
    try:
        def checkMentions(mess):
            return mess.author.id==ctx.author.id and mess.channel.id==ctx.channel.id and mess.channel_mentions!=[]
        def checkAuthor(mess):
            return mess.author.id==ctx.author.id and mess.channel.id==ctx.channel.id
        def checkValid(reaction,user):
            if type(reaction.emoji)==str:
                return False
            return reaction.emoji.id==772766033996021761 and reaction.message.id==message.id and user.id==ctx.author.id

        connexion,curseur=connectSQL(ctx.guild.id,"Guild","Guild",None,None)
        etat=curseur.execute("SELECT * FROM etatAnniv").fetchone()
        if etat["Statut"]==False or chan:
            embed=createEmbed("Activation anniversaires","Pour activer les anniversaires automatiques, donnez moi le salon dans lequel les messages seront envoyés.",0x11f738,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)
            message=await ctx.reply(embed=embed)

            mess=await bot.wait_for("message",check=checkMentions,timeout=60)
            chan=mess.channel_mentions[0].id

            assert mess.channel_mentions[0].permissions_for(ctx.guild.get_member(bot.user.id)).view_channel==True, "Le salon mentionné n'a pas les permissions nécessaires pour que je puisse le voir."
            assert mess.channel_mentions[0].permissions_for(ctx.guild.get_member(bot.user.id)).send_messages==True, "Le salon mentionné n'a pas les permissions nécessaires pour que je puisse envoyer des messages."

            embed=createEmbed("Activation anniversaires","Maintenant, donnez moi le message qui sera envoyé à chaque anniversaire.\nAjoutez la balise `{user}` pour mentionner le membre fêté.\nAjoutez la balise `{name}` pour ajouter le nom du membre fêté.\nAjoutez la balise `{date}` pour ajouter la date du jour.",0x11f738,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)
            await message.edit(embed=embed)

            mess=await bot.wait_for("message",check=checkAuthor,timeout=60)
            clean=createPhrase(mess.content.split(" "))
            exemple=formatageAnniv(clean,bot.user)

            embed=createEmbed("Activation anniversaires","Le salon dans lequel les messages seront envoyés sera <#{0}>.\nLe message sera : {1}\n Est-ce bon ? Appuyez sur <:otVALIDER:772766033996021761> pour valider.".format(chan,exemple),0x11f738,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)

            await message.edit(embed=embed)
            await message.add_reaction("<:otVALIDER:772766033996021761>")

            reaction,user=await bot.wait_for('reaction_add', check=checkValid, timeout=60)

            curseur.execute("UPDATE etatAnniv SET Statut=True, Salon={0}, Message='{1}'".format(chan,clean))
            connexion.commit()

            embed=createEmbed("Activation anniversaires","Opération validée !\n",0x11f738,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)
            await message.edit(embed=embed)
        
        else:
            embed=createEmbed("Désactivation anniversaires","Voulez-vous vraiment désactiver les messages d'anniversaires pour votre serveur ?\nSi vous changez d'avis plus tard, les dates enregistrées restent dans la base de données.\nAppuyez sur <:otVALIDER:772766033996021761> pour valider.",0x11f738,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)

            message=await ctx.reply(embed=embed)
            await message.add_reaction("<:otVALIDER:772766033996021761>")

            reaction,user=await bot.wait_for('reaction_add', check=checkValid, timeout=60)
            
            curseur.execute("UPDATE etatAnniv SET Statut=False, Salon=0, Message='None'")
            connexion.commit()

            embed=createEmbed("Désactivation anniversaires","Opération validée !",0x11f738,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)
            await message.edit(embed=embed)
            
        await message.clear_reactions()
        guild.getAnniv()
    except asyncio.exceptions.TimeoutError:
        await embedAssert(ctx,"Une minute s'est écoulée et vous n'avez pas confirmé l'activation. L'opération a été annulée",True)
        await message.clear_reactions()
