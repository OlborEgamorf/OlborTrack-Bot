from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.Embeds import createEmbed, embedAssert
import asyncio

async def delMessage(ctx,bot,args):
    try:
        assert len(args)>0, "Vous devez me donner le numéro du message !"
        connexion,curseur=connectSQL(ctx.guild.id,"Guild","Guild",None,None)
        try:
            texte=curseur.execute("SELECT * FROM messagesBV WHERE Nombre={0}".format(args[0])).fetchone()
        except:
            raise AssertionError("Le numéro donné n'est pas valide.")
        assert texte!=None, "Le numéro donné ne correspond à aucun message."
        connexion.close()

        embed=createEmbed("Suppression message de bienvenue","Voici le message que vous voulez supprimer : {0}.\nSi vous être sûr de votre choix, appuyez sur <:otVALIDER:772766033996021761>.".format(texte["Message"]),0xf54269,ctx.invoked_with.lower(),ctx.guild)
        message=await ctx.reply(embed=embed)
        await message.add_reaction("<:otVALIDER:772766033996021761>")

        def check(reaction,user):
            if type(reaction.emoji)==str:
                return False
            return reaction.emoji.id==772766033996021761 and reaction.message.id==message.id and user.id==ctx.author.id
        
        reaction,user=await bot.wait_for('reaction_add', check=check, timeout=60)
        await message.clear_reactions()

        connexion,curseur=connectSQL(ctx.guild.id,"Guild","Guild",None,None)
        curseur.execute("DELETE FROM messagesBV WHERE Nombre={0}".format(args[0]))

        for i in curseur.execute("SELECT * FROM messagesBV WHERE Nombre>{0} ORDER BY Nombre ASC".format(args[0])).fetchall():
            curseur.execute("UPDATE messagesBV SET Nombre={0} WHERE Nombre={1}".format(i["Nombre"]-1,i["Nombre"]))

        connexion.commit()

        embed=createEmbed("Suppression message de bienvenue","Le message a bien été supprimé.",0xf54269,ctx.invoked_with.lower(),ctx.guild)
        await ctx.reply(embed=embed)

    except AssertionError as er:
        await ctx.reply(embed=embedAssert(er))
    except asyncio.exceptions.TimeoutError:
        await message.reply(embed=embedAssert("Une minute s'est écoulée et vous n'avez pas confirmé l'ajout. L'opération a été annulée"))
        await message.clear_reactions()