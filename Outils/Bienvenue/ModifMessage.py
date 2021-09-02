from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.WebRequest import getAvatar
from Core.Fonctions.Embeds import createEmbed, embedAssert
from Core.Fonctions.Phrase import createPhrase
from Outils.Bienvenue.Manipulation import formatage
import asyncio

async def modifMessage(ctx,bot,args):
    try:
        assert len(args)>0, "Vous devez me donner le numéro du message !"
        connexion,curseur=connectSQL(ctx.guild.id,"Guild","Guild",None,None)
        try:
            texte=curseur.execute("SELECT * FROM messagesBV WHERE Nombre={0}".format(args[0])).fetchone()
        except:
            raise AssertionError("Le numéro donné n'est pas valide.")
        assert texte!=None, "Le numéro donné ne correspond à aucun message."
        connexion.close()
        
        embed=createEmbed("Modification message de bienvenue","Le message que vous voulez modifier est : "+texte["Message"]+".\nPour le faire, écrivez la nouvelle phrase corrigée.\nPour mentionner le membre qui a rejoint de le message, utilisez la balise `{user}`.\nPour afficher juste son nom, utilisez la balise `{name}`\nPour écrire le nom de votre serveur, utilisez la balise `{guild}`.",0xf54269,ctx.invoked_with.lower(),ctx.guild)
        message=await ctx.reply(embed=embed)

        def check(mess):
            return mess.author.id==ctx.author.id and mess.channel.id==ctx.channel.id
        
        mess=await bot.wait_for("message",check=check,timeout=60)

        clean=createPhrase(mess.content.split(" "))
        exemple=formatage(clean,bot.user,ctx.guild)

        embed=createEmbed("Modification message de bienvenue","{0}\nVoici un exemple avec moi-même d'à quoi ressemble votre nouveau message de bienvenue. Vous convient-il ?\nAppuyez sur <:otVALIDER:772766033996021761> pour confirmer la modification.".format(exemple),0xf54269,ctx.invoked_with.lower(),ctx.guild)
        message=await ctx.reply(embed=embed)
        await message.add_reaction("<:otVALIDER:772766033996021761>")

        def check(reaction,user):
            if type(reaction.emoji)==str:
                return False
            return reaction.emoji.id==772766033996021761 and reaction.message.id==message.id and user.id==ctx.author.id
        
        reaction,user=await bot.wait_for('reaction_add', check=check, timeout=60)
        await message.clear_reactions()

        connexion,curseur=connectSQL(ctx.guild.id,"Guild","Guild",None,None)
        curseur.execute("UPDATE messagesBV SET Message='{0}' WHERE Nombre={1}".format(clean,args[0]))
        connexion.commit()

        embed=createEmbed("Ajout message de bienvenue","Le message a bien été modifié !\nNuméro du message : `{0}`".format(args[0]),0xf54269,ctx.invoked_with.lower(),ctx.guild)
        await ctx.reply(embed=embed)

    except AssertionError as er:
        await ctx.reply(embed=embedAssert(er))
    except asyncio.exceptions.TimeoutError:
        await message.reply(embed=embedAssert("Une minute s'est écoulée et vous n'avez pas confirmé l'ajout. L'opération a été annulée"))
        await message.clear_reactions()