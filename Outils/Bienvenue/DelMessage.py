import asyncio

from Core.Fonctions.Embeds import createEmbed, embedAssert
from Core.Decorator import OTCommand
from Stats.SQL.ConnectSQL import connectSQL

@OTCommand
async def delMessage(ctx,bot,args,option):
    dictTitres={"BV":"de bienvenue","AD":"d'adieu"}
    try:
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
        connexion.close()

        embed=createEmbed("Suppression message {0}".format(dictTitres[option]),"Voici le message que vous voulez supprimer : {0}.\nSi vous être sûr de votre choix, appuyez sur <:otVALIDER:772766033996021761>.".format(texte["Message"]),0xf54269,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)
        message=await ctx.reply(embed=embed)
        await message.add_reaction("<:otVALIDER:772766033996021761>")
        
        reaction,user=await bot.wait_for('reaction_add', check=checkValid, timeout=60)
        await message.clear_reactions()

        connexion,curseur=connectSQL(ctx.guild.id,"Guild","Guild",None,None)
        curseur.execute("DELETE FROM messages{0} WHERE Nombre={1}".format(option,args[0]))

        for i in curseur.execute("SELECT * FROM messages{0} WHERE Nombre>{1} ORDER BY Nombre ASC".format(option,args[0])).fetchall():
            curseur.execute("UPDATE messages{0} SET Nombre={1} WHERE Nombre={2}".format(option,i["Nombre"]-1,i["Nombre"]))

        connexion.commit()

        embed=createEmbed("Suppression message {0}".format(dictTitres[option]),"Le message a bien été supprimé.",0xf54269,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)
        await ctx.reply(embed=embed)

    except asyncio.exceptions.TimeoutError:
        await embedAssert(ctx,"Une minute s'est écoulée et vous n'avez pas confirmé la suppression. L'opération a été annulée",True)
        await message.clear_reactions()
