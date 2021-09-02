import asyncio

from Core.Fonctions.Embeds import createEmbed, embedAssert
from Stats.SQL.ConnectSQL import connectSQL


async def toggleBienvenue(ctx,bot,chan,guild):
    try:
        connexion,curseur=connectSQL(ctx.guild.id,"Guild","Guild",None,None)
        etat=curseur.execute("SELECT * FROM etatBVAD WHERE Type='BV'").fetchone()
        if etat["Statut"]==False or chan:
            embed=createEmbed("Activation messages de bienvenue","Pour activer les messages de bienvenue, donnez moi le salon dans lequel les messages seront envoyés.",0xf54269,ctx.invoked_with.lower(),ctx.guild)
            message=await ctx.reply(embed=embed)

            def check(mess):
                return mess.author.id==ctx.author.id and mess.channel.id==ctx.channel.id and mess.channel_mentions!=[]
            
            mess=await bot.wait_for("message",check=check,timeout=60)
            chan=mess.channel_mentions[0].id

            assert mess.channel_mentions[0].permissions_for(ctx.guild.get_member(bot.user.id)).view_channel==True, "Le salon mentionné n'a pas les permissions nécessaires pour que je puisse le voir."
            assert mess.channel_mentions[0].permissions_for(ctx.guild.get_member(bot.user.id)).send_messages==True, "Le salon mentionné n'a pas les permissions nécessaires pour que je puisse envoyer des messages."

            embed=createEmbed("Activation messages de bienvenue","Le salon dans lequel les messages seront envoyés sera <#{0}>. Est-ce bon ? Appuyez sur <:otVALIDER:772766033996021761> pour valider.".format(chan),0xf54269,ctx.invoked_with.lower(),ctx.guild)

            message=await ctx.reply(embed=embed)
            await message.add_reaction("<:otVALIDER:772766033996021761>")

            def check(reaction,user):
                if type(reaction.emoji)==str:
                    return False
                return reaction.emoji.id==772766033996021761 and reaction.message.id==message.id and user.id==ctx.author.id
            
            reaction,user=await bot.wait_for('reaction_add', check=check, timeout=60)
            await message.clear_reactions()

            curseur.execute("UPDATE etatBVAD SET Statut=True, Salon={0} WHERE Type='BV'".format(chan))
            connexion.commit()

            embed=createEmbed("Activation messages de bienvenue","Opération validée !\nVous pouvez commencer à ajouter des phrases avec --- et des images avec ---",0xf54269,ctx.invoked_with.lower(),ctx.guild)
            await ctx.reply(embed=embed)
        
        else:
            embed=createEmbed("Désactivation messages de bienvenue","Voulez-vous vraiment désactiver les messages de bienvenue pour votre serveur ?\nSi vous changez d'avis plus tard, les messages et les images enregistrées restent dans la base de données.\nAppuyez sur <:otVALIDER:772766033996021761> pour valider.",0xf54269,ctx.invoked_with.lower(),ctx.guild)

            message=await ctx.reply(embed=embed)
            await message.add_reaction("<:otVALIDER:772766033996021761>")

            def check(reaction,user):
                if type(reaction.emoji)==str:
                    return False
                return reaction.emoji.id==772766033996021761 and reaction.message.id==message.id and user.id==ctx.author.id

            reaction,user=await bot.wait_for('reaction_add', check=check, timeout=60)
            await message.clear_reactions()

            curseur.execute("UPDATE etatBVAD SET Statut=False, Salon=0 WHERE Type='BV'")
            connexion.commit()

            embed=createEmbed("Désactivation messages de bienvenue","Opération validée !",0xf54269,ctx.invoked_with.lower(),ctx.guild)
            await ctx.reply(embed=embed)
        guild.getBV()
    except AssertionError as er:
        await ctx.reply(embed=embedAssert(er))
    except asyncio.exceptions.TimeoutError:
        await message.reply(embed=embedAssert("Une minute s'est écoulée et vous n'avez pas confirmé l'ajout. L'opération a été annulée"))
        await message.clear_reactions()
