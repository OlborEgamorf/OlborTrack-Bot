from Stats.SQL.ConnectSQL import connectSQL
from Titres.Outils import createAccount
from Core.Fonctions.Embeds import createEmbed, embedAssert
from Titres.Listes import commandeTMP
import asyncio

dictStatut={0:"Fabuleux",1:"Rare",2:"Légendaire",3:"Unique"}
dictTrade={705766186909958185:"Coins",705766186989912154:"Titre"}

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