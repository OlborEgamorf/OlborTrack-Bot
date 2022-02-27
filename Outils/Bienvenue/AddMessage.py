import asyncio

from Core.Decorator import OTCommand
from Core.Fonctions.Embeds import createEmbed, embedAssert
from Core.Fonctions.Phrase import createPhrase
from Outils.Bienvenue.Manipulation import formatage
from Stats.SQL.ConnectSQL import connectSQL


@OTCommand
async def addMessage(ctx,bot,option):
    dictTitres={"BV":"de bienvenue","AD":"d'adieu"}
    try:
        def checkAuthor(mess):
            return mess.author.id==ctx.author.id and mess.channel.id==ctx.channel.id
        def checkValid(reaction,user):
            if type(reaction.emoji)==str:
                return False
            return reaction.emoji.id==772766033996021761 and reaction.message.id==message.id and user.id==ctx.author.id

        embed=createEmbed("Ajout message {0}".format(dictTitres[option]),"Pour ajouter un message "+dictTitres[option]+" à la collection, écrivez la phrase que vous voulez.\nPour mentionner le membre qui a rejoint de le message, utilisez la balise `{user}`.\nPour afficher juste son nom, utilisez la balise `{name}`\nPour écrire le nom de votre serveur, utilisez la balise `{guild}`.\n\nToutes les indications sur la configuration s'afficheront sur ce message, donc surveillez le au fil des étapes !",0xf54269,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)
        message=await ctx.reply(embed=embed)

        mess=await bot.wait_for("message",check=checkAuthor,timeout=60)

        clean=createPhrase(mess.content.split(" "))
        exemple=formatage(clean,bot.user,ctx.guild)

        embed=createEmbed("Ajout message {0}".format(dictTitres[option]),"{0}\nVoici un exemple avec moi-même d'à quoi ressemble votre nouveau message {1}. Vous convient-il ?\nAppuyez sur <:otVALIDER:772766033996021761> pour confirmer l'ajout.".format(exemple,option),0xf54269,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)
        await message.edit(embed=embed)
        await message.add_reaction("<:otVALIDER:772766033996021761>")

        reaction,user=await bot.wait_for('reaction_add', check=checkValid, timeout=60)
        await message.clear_reactions()

        connexion,curseur=connectSQL(ctx.guild.id,"Guild","Guild",None,None)
        num=curseur.execute("SELECT COUNT() as Nombre FROM messages{0}".format(option)).fetchone()["Nombre"]+1
        curseur.execute("INSERT INTO messages{0} VALUES({1},'{2}')".format(option,num,clean))
        connexion.commit()

        embed=createEmbed("Ajout message {0}".format(dictTitres[option]),"Le message a bien été ajouté !\nNuméro du message : `{0}`".format(num),0xf54269,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)
        await message.edit(embed=embed)
    
    except asyncio.exceptions.TimeoutError:
        await embedAssert(ctx,"Une minute s'est écoulée et vous n'avez pas confirmé l'ajout. L'opération a été annulée",True)
        await message.clear_reactions()
