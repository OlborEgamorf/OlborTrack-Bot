from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.Embeds import createEmbed, embedAssert
import asyncio
import discord
from Outils.Bienvenue.Manipulation import fusion, squaretoround
from Core.Fonctions.WebRequest import getAvatar

async def delImage(ctx,bot,args,option):
    dictTitres={"BV":"de bienvenue","AD":"d'adieu"}
    try:
        assert len(args)>0, "Vous devez me donner le numéro de l'image !"
        connexion,curseur=connectSQL(ctx.guild.id,"Guild","Guild",None,None)
        try:
            image=curseur.execute("SELECT * FROM images{0} WHERE Nombre={1}".format(option,args[0])).fetchone()
        except:
            raise AssertionError("Le numéro donné n'est pas valide.")
        assert image!=None, "Le numéro donné ne correspond à aucune image."
        connexion.close()
        await getAvatar(ctx.author)
        squaretoround(ctx.author.id)

        fusion(image["Path"],ctx.author,image["Message"],image["Couleur"],image["Taille"],ctx.guild)

        embed=createEmbed("Suppression image {0}".format(dictTitres[option]),"Voici l'image que vous voulez supprimer.\nSi vous être sûr de votre choix, appuyez sur <:otVALIDER:772766033996021761>.",0xf54269,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)
        message=await ctx.reply(embed=embed,file=discord.File("Temp/{0}{1}.png".format(option,ctx.author.id)))
        await message.add_reaction("<:otVALIDER:772766033996021761>")

        def check(reaction,user):
            if type(reaction.emoji)==str:
                return False
            return reaction.emoji.id==772766033996021761 and reaction.message.id==message.id and user.id==ctx.author.id
        
        reaction,user=await bot.wait_for('reaction_add', check=check, timeout=60)
        await message.clear_reactions()

        connexion,curseur=connectSQL(ctx.guild.id,"Guild","Guild",None,None)
        curseur.execute("DELETE FROM images{0} WHERE Nombre={1}".format(option,args[0]))

        for i in curseur.execute("SELECT * FROM images{0} WHERE Nombre>{1} ORDER BY Nombre ASC".format(option,args[0])).fetchall():
            curseur.execute("UPDATE images{0} SET Nombre={1} WHERE Nombre={2}".format(option,i["Nombre"]-1,i["Nombre"]))

        connexion.commit()

        embed=createEmbed("Suppression image {0}".format(dictTitres[option]),"L'image a bien été supprimée.",0xf54269,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)
        await ctx.reply(embed=embed)

    except AssertionError as er:
        await ctx.reply(embed=embedAssert(er))
    except asyncio.exceptions.TimeoutError:
        await message.reply(embed=embedAssert("Une minute s'est écoulée et vous n'avez pas confirmé la suppression. L'opération a été annulée"))
        await message.clear_reactions()