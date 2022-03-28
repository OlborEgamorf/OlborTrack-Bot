import asyncio

from Core.Fonctions.Embeds import createEmbed, embedAssert
from Stats.SQL.ConnectSQL import connectSQL


async def toggleDynIcon(ctx,bot,guild):
    try:
        def checkValid(reaction,user):
            if type(reaction.emoji)==str:
                return False
            return reaction.emoji.id==772766033996021761 and reaction.message.id==message.id and user.id==ctx.author.id

        connexion,curseur=connectSQL(ctx.guild.id,"Guild","Guild",None,None)
        etat=curseur.execute("SELECT * FROM etatPP").fetchone()
        if etat["Statut"]==False:
            embed=createEmbed("Activation icone de serveur dynamique","Chaque jour, l'icone du serveur sera changée aléatoirement avec les images fournises par vous et votre serveur.\nLa commande pour en ajouter est **OT!dynicon add**.\nPour que l'image soit aussi envoyé chaque jour dans un salon précis, faites **OT!dynicon chan**.\nAppuyez sur <:otVALIDER:772766033996021761> pour les activer. Pour les désactiver, il suffira de refaire cette commande.",0xf54269,ctx.invoked_with.lower(),ctx.guild)
            message=await ctx.reply(embed=embed)

            await message.add_reaction("<:otVALIDER:772766033996021761>")

            reaction,user=await bot.wait_for('reaction_add', check=checkValid, timeout=60)

            curseur.execute("UPDATE etatPP SET Statut=True")
            connexion.commit()

            embed=createEmbed("Activation icone de serveur dynamique","Opération validée !\n",0xf54269,ctx.invoked_with.lower(),ctx.guild)
            await ctx.reply(embed=embed)
        
        else:
            embed=createEmbed("Désactivation icone de serveur dynamique","Voulez-vous vraiment désactiver les icones de serveur dynamique pour votre serveur ?\nSi vous changez d'avis plus tard, les images données restent dans la base de donnée.\nAppuyez sur <:otVALIDER:772766033996021761> pour valider.",0xf54269,ctx.invoked_with.lower(),ctx.guild)

            message=await ctx.reply(embed=embed)
            await message.add_reaction("<:otVALIDER:772766033996021761>")

            reaction,user=await bot.wait_for('reaction_add', check=checkValid, timeout=60)
            
            curseur.execute("UPDATE etatPP SET Statut=False, Salon=0")
            connexion.commit()

            embed=createEmbed("Désactivation icone de serveur dynamique","Opération validée !",0xf54269,ctx.invoked_with.lower(),ctx.guild)
            await message.edit(embed=embed)
            
        await message.clear_reactions()
        guild.getDynIcon()
    except asyncio.exceptions.TimeoutError:
        await embedAssert(ctx,"Une minute s'est écoulée et vous n'avez pas confirmé l'activation. L'opération a été annulée",True)
        await message.clear_reactions()
