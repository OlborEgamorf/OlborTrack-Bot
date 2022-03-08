import asyncio

from Core.Fonctions.Embeds import createEmbed, embedAssert
from Core.Fonctions.Phrase import createPhrase
from Core.Decorator import OTCommand
from Outils.Bienvenue.Manipulation import formatage
from Stats.SQL.ConnectSQL import connectSQL

@OTCommand
async def modifMessage(ctx,bot,args,option):
    dictTitres={"BV":"de bienvenue","AD":"d'adieu"}
    try:
        def checkAuthor(mess):
            return mess.author.id==ctx.author.id and mess.channel.id==ctx.channel.id
        def checkValid(reaction,user):
            if type(reaction.emoji)==str:
                return False
            return reaction.emoji.id==772766033996021761 and reaction.message.id==message.id and user.id==ctx.author.id

        assert len(args)>0, "Vous devez me donner le numéro du message !"
        connexion,curseur=connectSQL(ctx.guild.id,"Guild","Guild",None,None)
        try:
            texte=curseur.execute("SELECT * FROM messages{0} WHERE Nombre={1}".format(option,args[0])).fetchone()
        except:
            raise AssertionError("Le numéro donné n'est pas valide.")
        assert texte!=None, "Le numéro donné ne correspond à aucun message."

        if curseur.execute("SELECT * FROM etatBVAD WHERE Type='{0}'".format(option)).fetchone()["Statut"]==True:
            await ctx.reply("<:otORANGE:868538903584456745> le message que vous cherchez existe bien, mais les messages {0} sont actuellement désactivés sur votre serveur. Le modifier est donc peu pertinant, mais libre à vous !".format(dictTitres[option]))

        connexion.close()
        
        embed=createEmbed("Modification message {0}".format(dictTitres[option]),"Le message que vous voulez modifier est : "+texte["Message"]+".\nPour le faire, écrivez la nouvelle phrase corrigée.\nPour mentionner le membre qui a rejoint de le message, utilisez la balise `{user}`.\nPour afficher juste son nom, utilisez la balise `{name}`\nPour écrire le nom de votre serveur, utilisez la balise `{guild}`.",0xf54269,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)
        message=await ctx.reply(embed=embed)

        mess=await bot.wait_for("message",check=checkAuthor,timeout=60)

        clean=createPhrase(mess.content.split(" "))
        exemple=formatage(clean,bot.user,ctx.guild)

        embed=createEmbed("Modification message {0}".format(dictTitres[option]),"{0}\nVoici un exemple avec moi-même d'à quoi ressemble votre nouveau message {1}. Vous convient-il ?\nAppuyez sur <:otVALIDER:772766033996021761> pour confirmer la modification.".format(exemple,dictTitres[option]),0xf54269,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)
        await message.edit(embed=embed)
        await message.add_reaction("<:otVALIDER:772766033996021761>")

        reaction,user=await bot.wait_for('reaction_add', check=checkValid, timeout=60)
        await message.clear_reactions()

        connexion,curseur=connectSQL(ctx.guild.id,"Guild","Guild",None,None)
        curseur.execute("UPDATE messages{0} SET Message='{1}' WHERE Nombre={2}".format(option,clean,args[0]))
        connexion.commit()

        embed=createEmbed("Modification message {0}".format(dictTitres[option]),"Le message a bien été modifié !\nNuméro du message : `{0}`".format(args[0]),0xf54269,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)
        await message.edit(embed=embed)

    except asyncio.exceptions.TimeoutError:
        await embedAssert(ctx,"Une minute s'est écoulée et vous n'avez pas confirmé la modification. L'opération a été annulée",True)
        await message.clear_reactions()
