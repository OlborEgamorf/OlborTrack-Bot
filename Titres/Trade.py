import asyncio

from Core.Fonctions.Embeds import createEmbed, embedAssert
from Stats.SQL.ConnectSQL import connectSQL

from Titres.Outils import createAccount
from Titres.Vente import verifVente

dictStatut={0:"Fabuleux",1:"Rare",2:"Légendaire",3:"Unique"}
dictTrade={705766186909958185:"Coins",705766186989912154:"Titre"}
dictReverse={300:1,800:2,5000:3}
dictReverseSell={150:1,400:2,2500:3}

async def tradeTitre(ctx,idtitre,bot):
    try:
        def checkValide(reaction,user):
            if type(reaction.emoji)==str:
                return False
            return reaction.emoji.id==772766033996021761 and reaction.message.id==message.id and user.id!=ctx.author.id and not user.bot
        
        def checkWay(reaction,user):
            if type(reaction.emoji)==str:
                return False
            return (reaction.emoji.id==705766186909958185 or reaction.emoji.id==705766186989912154) and reaction.message.id==message.id and user.id==userTrade.id

        def checkTitre(mess):
            try:
                int(mess.content)
            except:
                return False
            return mess.author.id==userTrade.id and mess.channel.id==message.channel.id

        connexionUser,curseurUser=connectSQL("OT",ctx.author.id,"Titres",None,None)
        createAccount(connexionUser,curseurUser)
        titre=verifTrade(ctx,curseurUser,idtitre)
        curseurUser.close()
        
        embed=createEmbed("Échange de Titre","<@{0}> veut échanger le titre **{1}** !\nVous pouvez appuyer sur <:otVALIDER:772766033996021761> pour lancer la procédure et échanger avec lui !.".format(ctx.author.id,titre["Nom"]),0xf58d1d,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.author)
        message=await ctx.reply(embed=embed)
        await message.add_reaction("<:otVALIDER:772766033996021761>")

        reaction,userTrade=await bot.wait_for('reaction_add', check=checkValide, timeout=60)
        await message.clear_reactions()

        embed=createEmbed("Échange de Titre","<@{0}> accepte l'échange du titre {1} avec <@{2}> !\n<@{0}>, vous devez choisir si vous voulez échanger ce titre contre des OT Coins (<:ot1:705766186909958185>) ou un autre titre (<:ot2:705766186989912154>).".format(userTrade.id,titre["Nom"],ctx.author.id),0xf58d1d,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),userTrade)
        message=await ctx.reply(embed=embed)
        await message.add_reaction("<:ot1:705766186909958185>")
        await message.add_reaction("<:ot2:705766186989912154>")

        reaction,user=await bot.wait_for('reaction_add', check=checkWay, timeout=60)
        await message.clear_reactions()

        way=dictTrade[reaction.emoji.id]

        connexionTrade,curseurTrade=connectSQL("OT",userTrade.id,"Titres",None,None)
        createAccount(connexionTrade,curseurTrade)
        assert curseurTrade.execute("SELECT COUNT() AS Count FROM titresUser WHERE Rareté=3").fetchone()["Count"]==0, "Vous avez déjà un titre de type Unique." 
        if way=="Coins":
            coins=curseurTrade.execute("SELECT * FROM coins").fetchone()["Coins"]
            connexionTrade.close()

            embed=createEmbed("Échange de Titre","<@{0}>, parmis vos {1} OT Coins actuels, écrivez combien voulez vous donner pour acheter le titre **{2}**".format(userTrade.id,coins,titre["Nom"]),0xf58d1d,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),userTrade)
            message=await ctx.reply(embed=embed)

            mess=await bot.wait_for('message', check=checkTitre, timeout=60)
            somme=int(mess.content)
            assert coins-somme>=0, "Vous n'avez pas assez de OT Coins !"

            embed=createEmbed("Échange de Titre","<@{0}>, <@{1}> vous fait une proposition de **{2} OT Coins** pour acheter votre titre **{3}**\nAppuyez sur <:otVALIDER:772766033996021761> pour finaliser l'échange.\nAu bout de 60 secondes sans réponse, l'échange sera annulé.".format(ctx.author.id,userTrade.id,somme,titre["Nom"]),0xf58d1d,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.author)
            message=await ctx.reply(embed=embed)
            await message.add_reaction("<:otVALIDER:772766033996021761>")

            reaction,user=await bot.wait_for('reaction_add', check=checkValide, timeout=60)
            await message.clear_reactions()

            connexionUser,curseurUser=connectSQL("OT",ctx.author.id,"Titres",None,None)
            connexionTrade,curseurTrade=connectSQL("OT",userTrade.id,"Titres",None,None)
            titre=verifTrade(ctx,curseurUser,idtitre)
            coins=curseurTrade.execute("SELECT * FROM coins").fetchone()["Coins"]
            assert coins-somme>=0, "Vous n'avez pas assez de OT Coins !"
            assert curseurTrade.execute("SELECT COUNT() AS Count FROM titresUser WHERE Rareté=3").fetchone()["Count"]==0, "Vous avez déjà un titre de type Unique." 

            curseurTrade.execute("UPDATE coins SET Coins=Coins-{0}".format(somme))
            curseurTrade.execute("INSERT INTO titresUser VALUES({0},'{1}',{2})".format(idtitre,titre["Nom"],titre["Rareté"]))
            curseurUser.execute("DELETE FROM titresUser WHERE ID={0}".format(idtitre))

            connexionUser.commit()
            connexionTrade.commit()
        
        else:
            connexionTrade.close()
            embed=createEmbed("Échange de Titre","<@{0}>, parmis les titres que vous possèdez, écrivez l'ID de celui que vous voudriez échanger contre **{1}**.\nVous pouvez consulter votre liste de titres avec OT!titre perso.".format(userTrade.id,titre["Nom"]),0xf58d1d,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),userTrade)
            message=await ctx.reply(embed=embed)

            mess=await bot.wait_for('message', check=checkTitre, timeout=60)
            idtrade=int(mess.content)
            titreTrade=verifVente(userTrade.id,idtrade)

            embed=createEmbed("Échange de Titre","<@{0}>, <@{1}> vous fait une proposition d'échanger le titre **{2}** contre votre titre **{3}**\nAppuyez sur <:otVALIDER:772766033996021761> pour finaliser l'échange.\nAu bout de 60 secondes sans réponse, l'échange sera annulé.".format(ctx.author.id,userTrade.id,titreTrade[0],titre["Nom"]),0xf58d1d,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.author)
            message=await ctx.reply(embed=embed)
            await message.add_reaction("<:otVALIDER:772766033996021761>")

            reaction,user=await bot.wait_for('reaction_add', check=checkValide, timeout=60)
            await message.clear_reactions()

            connexionUser,curseurUser=connectSQL("OT",ctx.author.id,"Titres",None,None)
            connexionTrade,curseurTrade=connectSQL("OT",userTrade.id,"Titres",None,None)
            titre=verifTrade(ctx,curseurUser,idtitre)
            titreTrade=verifVente(userTrade.id,idtrade)
            assert curseurTrade.execute("SELECT COUNT() AS Count FROM titresUser WHERE Rareté=3").fetchone()["Count"]==0, "Vous avez déjà un titre de type Unique." 

            curseurTrade.execute("INSERT INTO titresUser VALUES({0},'{1}',{2})".format(idtitre,titre["Nom"],titre["Rareté"]))
            curseurUser.execute("DELETE FROM titresUser WHERE ID={0}".format(idtitre))
            curseurUser.execute("INSERT INTO titresUser VALUES({0},'{1}',{2})".format(idtrade,titreTrade[0],dictReverseSell[titreTrade[1]]))
            curseurTrade.execute("DELETE FROM titresUser WHERE ID={0}".format(idtrade))

            connexionUser.commit()
            connexionTrade.commit()
        
        embed=createEmbed("Échange de Titre","Échange terminé !",0xf58d1d,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.author)
        await ctx.reply(embed=embed)

    except asyncio.exceptions.TimeoutError:
        await embedAssert(ctx,"Une minute s'est écoulée et rien ne s'est produit. L'opération a été annulée",True)
        await message.clear_reactions()


def verifTrade(ctx,curseurUser1,idtitre):
    connexion,curseur=connectSQL("OT","Titres","Titres",None,None)
    titre=curseurUser1.execute("SELECT * FROM titresUser WHERE ID={0}".format(idtitre)).fetchone()
    assert titre!=None, "Vous ne possèdez pas ce titre !"
    assert titre["Rareté"]!=0, "Vous ne pouvez vendre ou échanger un titre Fabuleux."
    assert curseur.execute("SELECT * FROM active WHERE MembreID={0}".format(ctx.author.id)).fetchone()["TitreID"]!=int(idtitre), "Le titre que vous voulez échanger est celui qui est actuellement équipé pour vous."
    connexion.close()
    return titre
