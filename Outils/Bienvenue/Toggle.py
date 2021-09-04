import asyncio

from Core.Fonctions.Embeds import createEmbed, embedAssert
from Stats.SQL.ConnectSQL import connectSQL


async def toggleBienvenue(ctx,bot,chan,guild,option):
    dictTitres={"BV":"de bienvenue","AD":"d'adieu"}
    try:
        connexion,curseur=connectSQL(ctx.guild.id,"Guild","Guild",None,None)
        etat=curseur.execute("SELECT * FROM etatBVAD WHERE Type='{0}'".format(option)).fetchone()
        if etat["Statut"]==False or chan:
            embed=createEmbed("Activation messages {0}".format(dictTitres[option]),"Pour activer les messages {0}, donnez moi le salon dans lequel les messages seront envoyés.".format(dictTitres[option]),0xf54269,ctx.invoked_with.lower(),ctx.guild)
            message=await ctx.reply(embed=embed)

            def check(mess):
                return mess.author.id==ctx.author.id and mess.channel.id==ctx.channel.id and mess.channel_mentions!=[]
            
            mess=await bot.wait_for("message",check=check,timeout=60)
            chan=mess.channel_mentions[0].id

            assert mess.channel_mentions[0].permissions_for(ctx.guild.get_member(bot.user.id)).view_channel==True, "Le salon mentionné n'a pas les permissions nécessaires pour que je puisse le voir."
            assert mess.channel_mentions[0].permissions_for(ctx.guild.get_member(bot.user.id)).send_messages==True, "Le salon mentionné n'a pas les permissions nécessaires pour que je puisse envoyer des messages."

            embed=createEmbed("Activation messages {0}".format(dictTitres[option]),"Le salon dans lequel les messages seront envoyés sera <#{0}>. Est-ce bon ? Appuyez sur <:otVALIDER:772766033996021761> pour valider.".format(chan),0xf54269,ctx.invoked_with.lower(),ctx.guild)

            message=await ctx.reply(embed=embed)
            await message.add_reaction("<:otVALIDER:772766033996021761>")

            def check(reaction,user):
                if type(reaction.emoji)==str:
                    return False
                return reaction.emoji.id==772766033996021761 and reaction.message.id==message.id and user.id==ctx.author.id
            
            reaction,user=await bot.wait_for('reaction_add', check=check, timeout=60)
            await message.clear_reactions()

            curseur.execute("UPDATE etatBVAD SET Statut=True, Salon={0} WHERE Type='{1}'".format(chan,option))
            connexion.commit()

            embed=createEmbed("Activation messages {0}".format(dictTitres[option]),"Opération validée !\nVous pouvez commencer à ajouter des phrases avec `OT!{0}message add` et des images avec `OT!{0}image add`".format(option.lower()),0xf54269,ctx.invoked_with.lower(),ctx.guild)
            await ctx.reply(embed=embed)
        
        else:
            embed=createEmbed("Désactivation messages {0}".format(dictTitres[option]),"Voulez-vous vraiment désactiver les messages {0} pour votre serveur ?\nSi vous changez d'avis plus tard, les messages et les images enregistrées restent dans la base de données.\nAppuyez sur <:otVALIDER:772766033996021761> pour valider.".format(dictTitres[option]),0xf54269,ctx.invoked_with.lower(),ctx.guild)

            message=await ctx.reply(embed=embed)
            await message.add_reaction("<:otVALIDER:772766033996021761>")

            def check(reaction,user):
                if type(reaction.emoji)==str:
                    return False
                return reaction.emoji.id==772766033996021761 and reaction.message.id==message.id and user.id==ctx.author.id

            reaction,user=await bot.wait_for('reaction_add', check=check, timeout=60)
            await message.clear_reactions()

            curseur.execute("UPDATE etatBVAD SET Statut=False, Salon=0 WHERE Type='{0}'".format(option))
            connexion.commit()

            embed=createEmbed("Désactivation messages {0}".format(dictTitres[option]),"Opération validée !",0xf54269,ctx.invoked_with.lower(),ctx.guild)
            await ctx.reply(embed=embed)
        guild.getBV()
    except AssertionError as er:
        await ctx.reply(embed=embedAssert(er))
    except asyncio.exceptions.TimeoutError:
        await message.reply(embed=embedAssert("Une minute s'est écoulée et vous n'avez pas confirmé l'activation. L'opération a été annulée"))
        await message.clear_reactions()
