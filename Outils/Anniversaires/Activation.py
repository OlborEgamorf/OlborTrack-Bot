import asyncio

from Core.Fonctions.Embeds import createEmbed, embedAssert
from Stats.SQL.ConnectSQL import connectSQL


async def toggleBienvenue(ctx,bot,chan,guild,option):
    try:
        connexion,curseur=connectSQL(ctx.guild.id,"Guild","Guild",None,None)
        etat=curseur.execute("SELECT * FROM etatAnniv WHERE Type='{0}'".format(option)).fetchone()
        if etat["Statut"]==False or chan:
            embed=createEmbed("Activation anniversaires","Pour activer les anniversaires automatiques, donnez moi le salon dans lequel les messages seront envoyés.",0xf54269,ctx.invoked_with.lower(),ctx.guild)
            message=await ctx.reply(embed=embed)

            def check(mess):
                return mess.author.id==ctx.author.id and mess.channel.id==ctx.channel.id and mess.channel_mentions!=[]
            
            mess=await bot.wait_for("message",check=check,timeout=60)
            chan=mess.channel_mentions[0].id

            assert mess.channel_mentions[0].permissions_for(ctx.guild.get_member(bot.user.id)).view_channel==True, "Le salon mentionné n'a pas les permissions nécessaires pour que je puisse le voir."
            assert mess.channel_mentions[0].permissions_for(ctx.guild.get_member(bot.user.id)).send_messages==True, "Le salon mentionné n'a pas les permissions nécessaires pour que je puisse envoyer des messages."

            embed=createEmbed("Activation anniversaires","Maintenant, donnez moi le message qui sera envoyé à chaque anniversaire.\nAjoutez la balise `{user}` pour mentionner le membre fêté.\nAjoutez la balise `{name}` pour ajouter le nom du membre fêté.\nAjoutez la balise `{date}` pour ajouter la date de l'anniversaire.\nAjoutez la balise `{age}` pour montrer l'âge du membre fêté.",0xf54269,ctx.invoked_with.lower(),ctx.guild)
            message=await ctx.reply(embed=embed)

            def check(mess):
                return mess.author.id==ctx.author.id and mess.channel.id==ctx.channel.id and mess.channel_mentions!=[]
            
            mess=await bot.wait_for("message",check=check,timeout=60)
            clean=createPhrase(mess.content.split(" "))
            exemple=formatageAnniv(clean,bot.user,strftime("%d"),strftime("%m"),strftime("%y"),31)

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

            embed=createEmbed("Activation anniversaires","Opération validée !\n----".format(option.lower()),0xf54269,ctx.invoked_with.lower(),ctx.guild)
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
        guild.getBV()
    except AssertionError as er:
        await ctx.reply(embed=embedAssert(er))
    except asyncio.exceptions.TimeoutError:
        await message.reply(embed=embedAssert("Une minute s'est écoulée et vous n'avez pas confirmé l'activation. L'opération a été annulée"))
        await message.clear_reactions()


def formatageAnniv(alerte,user,jour,mois,annee,age):
    new=""
    mention=alerte.split("{user}")
    longMention=len(mention)
    for i in range(longMention):
        new+=mention[i]
        if i!=longMention-1:
            new+="<@{0}>".format(user.id)
    
    newN=""
    name=new.split("{name}")
    longName=len(name)
    for i in range(longName):
        newN+=name[i]
        if i!=longName-1:
            newN+="{0}".format(user.name)

    newG=""
    guildName=newN.split("{date}")
    longGuild=len(guildName)
    for i in range(longGuild):
        newG+=guildName[i]
        if i!=longGuild-1:
            newG+="{0}/{1}/20{2}".format(jour,mois,annee)

    newN=""
    number=newG.split("{age}")
    longNumb=len(number)
    for i in range(longNumb):
        newN+=number[i]
        if i!=longNumb-1:
            newN+="{0}".format(age)
    
    return newN