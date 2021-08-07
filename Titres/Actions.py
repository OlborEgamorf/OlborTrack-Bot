import asyncio

import discord
from Stats.SQL.ConnectSQL import connectSQL

from Titres.Verificateurs import verifAchat, verifVente
from Core.Fonctions.Embeds import createEmbed, embedAssert
from Titres.Outils import createAccount
from Titres.Listes import commandeTMP

dictReverse={300:1,800:2,5000:3}
dictStatut={0:"Fabuleux",1:"Rare",2:"Légendaire",3:"Unique"}
dictTrade={705766186909958185:"Coins",705766186989912154:"Titre"}


async def achatTitre(ctx,idtitre,bot,gift):
    try:
        if gift:
            assert len(ctx.message.mentions)!=0, "Si vous voulez offrir un titre à quelqu'un, vous devez le mentionner."
        nom,valeur,coins=verifAchat(ctx,idtitre,gift)

        if gift:
            embed=createEmbed("Cadeau de Titre","Vous êtes sur le point d'offrir **{0}** pour *{1} <:otCOINS:873226814527520809>* à <@{2}>.\nVous possèdez {3} <:otCOINS:873226814527520809> au total et en aurez {4} <:otCOINS:873226814527520809> après la transaction.\nAppuyez sur <:otVALIDER:772766033996021761> pour confirmer l'achat.".format(nom,valeur,ctx.message.mentions[0].id,coins,coins-valeur),0xf58d1d,ctx.invoked_with.lower(),ctx.author)
        else:
            embed=createEmbed("Achat de Titre","Vous êtes sur le point d'acheter **{0}** pour *{1} <:otCOINS:873226814527520809>*.\nVous possèdez {2} <:otCOINS:873226814527520809> au total et en aurez {3} <:otCOINS:873226814527520809> après la transaction.\nAppuyez sur <:otVALIDER:772766033996021761> pour confirmer l'achat.".format(nom,valeur,coins,coins-valeur),0xf58d1d,ctx.invoked_with.lower(),ctx.author)

        message=await ctx.reply(embed=embed)
        await message.add_reaction("<:otVALIDER:772766033996021761>")

        def check(reaction,user):
            if type(reaction.emoji)==str:
                return False
            return reaction.emoji.id==772766033996021761 and reaction.message.id==message.id and user.id==ctx.author.id

        reaction,user=await bot.wait_for('reaction_add', check=check, timeout=60)
        await message.clear_reactions()
        nom,valeur,coins=verifAchat(ctx,idtitre,gift)

        connexion,curseur=connectSQL("OT","Titres","Titres",None,None)
        connexionUser,curseurUser=connectSQL("OT",ctx.author.id,"Titres",None,None)
        curseur.execute("UPDATE marketplace SET Stock=Stock-1 WHERE ID={0}".format(idtitre))
        curseurUser.execute("UPDATE coins SET Coins=Coins-{0}".format(valeur))

        if gift:
            connexionGift,curseurGift=connectSQL("OT",ctx.message.mentions[0].id,"Titres",None,None)
            curseurGift.execute("INSERT INTO titresUser VALUES({0},'{1}',{2})".format(idtitre,nom,dictReverse[valeur]))
            connexionGift.commit()
        else:
            curseurUser.execute("INSERT INTO titresUser VALUES({0},'{1}',{2})".format(idtitre,nom,dictReverse[valeur]))

        connexion.commit()
        connexionUser.commit()

        if gift:
            embed=createEmbed("Cadeau de Titre","Titre offert avec succès !\n<@{0}> peut équiper **{1}** avec la commande **OT!titre set {2}**.".format(ctx.message.mentions[0].id,nom,idtitre),0xf58d1d,ctx.invoked_with.lower(),ctx.author)
        else:
            embed=createEmbed("Achat de Titre","Titre acheté avec succès !\nVous pouvez équiper **{0}** avec la commande **OT!titre set {1}**.".format(nom,idtitre),0xf58d1d,ctx.invoked_with.lower(),ctx.author)

        await message.reply(embed=embed)
    except AssertionError as er:
        await ctx.reply(embed=embedAssert(er))
    except asyncio.exceptions.TimeoutError:
        await message.reply(embed=embedAssert("Une minute s'est écoulée et vous n'avez pas confirmé l'achat. La transaction a été annulée."))
        await message.clear_reactions()


async def venteTitre(ctx,idtitre,bot):
    try:
        nom,valeur,coins=verifVente(ctx,idtitre)

        embed=createEmbed("Vente de Titre","Vous êtes sur le point de vendre **{0}** pour *{1} <:otCOINS:873226814527520809>*.\nVous possèdez {2} <:otCOINS:873226814527520809> au total, et en aurez {3} <:otCOINS:873226814527520809> après la transaction.\nAppuyez sur <:otVALIDER:772766033996021761> pour confirmer la vente.".format(nom,valeur,coins,coins+valeur),0xf58d1d,ctx.invoked_with.lower(),ctx.author)
        message=await ctx.reply(embed=embed)
        await message.add_reaction("<:otVALIDER:772766033996021761>")

        def check(reaction,user):
            if type(reaction.emoji)==str:
                return False
            return reaction.emoji.id==772766033996021761 and reaction.message.id==message.id and user.id==ctx.author.id

        reaction,user=await bot.wait_for('reaction_add', check=check, timeout=60)
        await message.clear_reactions()
        nom,valeur,coins=verifVente(ctx,idtitre)

        connexion,curseur=connectSQL("OT","Titres","Titres",None,None)
        connexionUser,curseurUser=connectSQL("OT",ctx.author.id,"Titres",None,None)
        if curseur.execute("SELECT * FROM marketplace WHERE ID={0}".format(idtitre)).fetchone()==None:
            curseur.execute("INSERT INTO marketplace VALUES({0},0)".format(idtitre))
        curseur.execute("UPDATE marketplace SET Stock=Stock+1 WHERE ID={0}".format(idtitre))
        curseurUser.execute("UPDATE coins SET Coins=Coins+{0}".format(valeur))
        curseurUser.execute("DELETE FROM titresUser WHERE ID={0}".format(idtitre))

        connexion.commit()
        connexionUser.commit()

        embed=createEmbed("Vente de Titre","Titre vendu avec succès !\nVous possèdez désormais **{0} <:otCOINS:873226814527520809>**.".format(coins+valeur),0xf58d1d,ctx.invoked_with.lower(),ctx.author)
        await message.reply(embed=embed)
    except AssertionError as er:
        await ctx.reply(embed=embedAssert(er))
    except asyncio.exceptions.TimeoutError:
        await message.reply(embed=embedAssert("Une minute s'est écoulée et vous n'avez pas confirmé la vente. La transaction a été annulée."))
        await message.clear_reactions()


async def setTitre(ctx,idtitre,bot):
    try:
        connexion,curseur=connectSQL("OT","Titres","Titres",None,None)
        connexionUser,curseurUser=connectSQL("OT",ctx.author.id,"Titres",None,None)
        titre=curseurUser.execute("SELECT * FROM titresUser WHERE ID={0}".format(idtitre)).fetchone()
        assert titre!=None, "Vous ne possèdez pas ce titre."
        if curseur.execute("SELECT * FROM active WHERE MembreID={0}".format(ctx.author.id)).fetchone()==None:
            curseur.execute("INSERT INTO active VALUES({0},{1})".format(idtitre,ctx.author.id))
        else:
            curseur.execute("UPDATE active SET TitreID={0} WHERE MembreID={1}".format(idtitre,ctx.author.id))
        embed=createEmbed("Titre équipé","Titre équipé avec succès !\nVotre nouveau titre est maintenant : **{0}**.".format(titre["Nom"]),0xf58d1d,ctx.invoked_with.lower(),ctx.author)
        await ctx.reply(embed=embed)
        connexion.commit()
    except AssertionError as er:
        await ctx.reply(embed=embedAssert(er))


async def tradeTitre(ctx,idtitre,bot):
    try:
        assert len(ctx.message.mentions)!=0, "Vous devez mentionner quelqu'un pour lancer un échange !"
        connexionUser1,curseurUser1=connectSQL("OT",ctx.author.id,"Titres",None,None)
        connexionUser2,curseurUser2=connectSQL("OT",ctx.message.mentions[0].id,"Titres",None,None)
        createAccount(connexionUser1,curseurUser1)
        createAccount(connexionUser2,curseurUser2)
        assert curseurUser2.execute("SELECT * FROM titresUser").fetchall()!=[], "La personne avec qui vous voulez échanger ne possède aucun titre !"

        user1,user2=ctx.author,ctx.message.mentions[0]


        embed=createEmbed("Échange de Titre","<@{0}> veut échanger des titres avec <@{1}> !\n<@{1}> doit appuyer sur <:otVALIDER:772766033996021761> pour lancer la procédure.".format(user1.id,user2.id),0xf58d1d,ctx.invoked_with.lower(),bot.user)
        message=await ctx.reply(embed=embed)
        await message.add_reaction("<:otVALIDER:772766033996021761>")

        def checkValide(reaction,user):
            if type(reaction.emoji)==str:
                return False
            return reaction.emoji.id==772766033996021761 and reaction.message.id==message.id and user.id==user2.id

        reaction,user=await bot.wait_for('reaction_add', check=checkValide, timeout=60)
        await message.clear_reactions()


        ctx.author=ctx.message.mentions[0]
        await commandeTMP(ctx,None,False,None,"user")

        embed=createEmbed("Échange de Titre","Vous êtes sur le point d'échanger des titres avec <@{0}> !\nParmi la liste de titres de <@{0}>, choisissez celui que vous souhaitez avoir.\nUne fois fait, envoyez **l'ID du titre**.".format(user2.id),0xf58d1d,ctx.invoked_with.lower(),user1)
        message=await ctx.reply(embed=embed)

        def checkTitre(mess):
            try:
                int(mess.content)
                assert curseurUser2.execute("SELECT * FROM titresUser WHERE ID={0}".format(int(mess.content))).fetchone()!=None
            except:
                return False
            return user.id==user1.id and mess.channel.id==message.channel.id

        mess=await bot.wait_for('message', check=checkTitre, timeout=60)
        titre=curseurUser2.execute("SELECT * FROM titresUser WHERE ID={0}".format(int(mess.content))).fetchone()


        embed=createEmbed("Échange de Titre","<@{0}> souhaite obtenir votre titre {1} ({2}) !\nAppuyez sur <:otVALIDER:772766033996021761> pour valider l'échange et choisir contre quoi vous voulez l'échanger.".format(user1.id,titre["Nom"],dictStatut[titre["Rareté"]]),0xf58d1d,ctx.invoked_with.lower(),user2)
        message=await ctx.reply(embed=embed)
        await message.add_reaction("<:otVALIDER:772766033996021761>")

        def checkValide(reaction,user):
            if type(reaction.emoji)==str:
                return False
            return reaction.emoji.id==772766033996021761 and reaction.message.id==message.id and user.id==user2.id

        reaction,user=await bot.wait_for('reaction_add', check=checkValide, timeout=60)
        await message.clear_reactions()

        coins=curseurUser1.execute("SELECT * FROM coins").fetchone()["Coins"]
        titres=curseurUser1.execute("SELECT Count() AS Count FROM titresUser").fetchone()["Count"]

        assert coins!=0 or titres!=0, "<@{0}> n'a rien a échanger !".format(user1.id)
        if coins!=0 and titres!=0:
            embed=createEmbed("Échange de Titre","<@{0}> peut échanger le titre {1} ({2}) avec un autre titre ou des OT Coins <:otCOINS:873226814527520809>.\nChoisissez sous quelle forme vous voulez échanger : \n- <:ot1:705766186909958185> : OT Coins\n- <:ot2:705766186989912154> : Autre titre".format(user1.id,titre["Nom"],dictStatut[titre["Rareté"]]),0xf58d1d,ctx.invoked_with.lower(),ctx.author)
            message=await ctx.reply(embed=embed)
            await message.add_reaction("<:ot1:705766186909958185>")
            await message.add_reaction("<:ot2:705766186989912154>")

            def checkValide(reaction,user):
                if type(reaction.emoji)==str:
                    return False
                return (reaction.emoji.id==705766186909958185 or reaction.emoji.id==705766186989912154) and reaction.message.id==message.id and user.id==user2

            reaction,user=await bot.wait_for('reaction_add', check=checkValide, timeout=60)
            await message.clear_reactions()

            way=dictTrade[reaction.emoji.id]
        elif coins!=0:
            way="Coins"
        else:
            way="Titre"

        if way=="Coins":
            embed=createEmbed("Échange de Titre","Vous êtes sur le point d'échanger le titre {0} ({1}) contre des OT Coins <:otCOINS:873226814527520809> !\n.".format(user2.id),0xf58d1d,ctx.invoked_with.lower(),user1)
            message=await ctx.reply(embed=embed)

            def checkTitre(mess):
                try:
                    int(mess.content)
                    assert curseurUser2.execute("SELECT * FROM titresUser WHERE ID={0}".format(int(mess.content))).fetchone()!=None
                except:
                    return False
                return user.id==user1.id and mess.channel.id==message.channel.id

            mess=await bot.wait_for('message', check=checkTitre, timeout=60)



    except AssertionError as er:
        await ctx.reply(embed=embedAssert(er))
    except asyncio.exceptions.TimeoutError:
        await message.reply(embed=embedAssert("Une minute s'est écoulée et rien ne s'est produit. La transaction a été annulée."))
        await message.clear_reactions()