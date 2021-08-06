from Core.Fonctions.Embeds import addtoFields, createEmbed, createFields, embedAssert, sendEmbed
from Titres.Verificateurs import verifAchat, verifVente
from Stats.SQL.ConnectSQL import connectSQL
import asyncio
from Core.Fonctions.setMaxPage import setMax, setPage
import discord
from Core.Fonctions.AuteurIcon import auteur

dictValue={0:"?",1:300,2:800,3:5000}
dictStatut={0:"Fabuleux",1:"Rare",2:"Légendaire",3:"Unique"}
dictReverse={300:1,800:2,5000:3}

async def achatTitre(ctx,idtitre,bot,gift):
    try:
        if gift:
            assert len(ctx.message.mentions)!=0, "Si vous voulez offrir un titre à quelqu'un, vous devez le mentionner."
        nom,valeur,coins=verifAchat(ctx,idtitre,gift)

        if gift:
            embed=createEmbed("Cadeau de Titre","Vous êtes sur le point d'offrir **{0}** pour *{1} <:otCOINS:873226814527520809>* à <@{2}>.\nVous possèdez {3} <:otCOINS:873226814527520809> au total et en aurez {4} après la transaction.\nAppuyez sur <:otVALIDER:772766033996021761> pour confirmer l'achat.".format(nom,valeur,ctx.message.mentions[0].id,coins,coins-valeur),0xf58d1d,ctx.invoked_with.lower(),ctx.author)
        else:
            embed=createEmbed("Achat de Titre","Vous êtes sur le point d'acheter **{0}** pour *{1} <:otCOINS:873226814527520809>*.\nVous possèdez {2} <:otCOINS:873226814527520809> au total et en aurez {3} après la transaction.\nAppuyez sur <:otVALIDER:772766033996021761> pour confirmer l'achat.".format(nom,valeur,coins,coins-valeur),0xf58d1d,ctx.invoked_with.lower(),ctx.author)

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
            embed=createEmbed("Cadeau de Titre","Titre offert avec succès !\n<@{0}> peut équiper **{1}** avec la commande **OT!titre set**.".format(ctx.message.mentions[0].id,nom),0xf58d1d,ctx.invoked_with.lower(),ctx.author)
        else:
            embed=createEmbed("Achat de Titre","Titre acheté avec succès !\nVous pouvez équiper **{0}** avec la commande **OT!titre set**.".format(nom),0xf58d1d,ctx.invoked_with.lower(),ctx.author)

        await message.reply(embed=embed)
    except AssertionError as er:
        await ctx.reply(embed=embedAssert(er))
    except asyncio.exceptions.TimeoutError:
        await message.reply(embed=embedAssert("Une minute s'est écoulée et vous n'avez pas confirmé l'achat. La transaction a été annulée."))
        await message.clear_reactions()


async def venteTitre(ctx,idtitre,bot):
    try:
        nom,valeur,coins=verifVente(ctx,idtitre)

        embed=createEmbed("Vente de Titre","Vous êtes sur le point de vendre **{0}** pour *{1} <:otCOINS:873226814527520809>*.\nVous possèdez {2} <:otCOINS:873226814527520809> au total, et en aurez {3} après la transaction.\nAppuyez sur <:otVALIDER:772766033996021761> pour confirmer la vente.".format(nom,valeur,coins,coins+valeur),0xf58d1d,ctx.invoked_with.lower(),ctx.author)
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


async def commandeTMP(ctx,turn,react,ligne,option):
    connexionCMD,curseurCMD=connectSQL(ctx.guild.id,"Commandes","Guild",None,None)
    connexion,curseur=connectSQL("OT","Titres","Titres",None,None)
    if not react:
        if option=="marketplace":
            table=curseur.execute("SELECT marketplace.ID,marketplace.Stock,titres.Rareté,titres.Nom FROM marketplace JOIN titres ON marketplace.ID=titres.ID ORDER BY Rareté DESC").fetchall()
        else:
            table=curseur.execute("SELECT * FROM titres ORDER BY Rareté DESC").fetchall()
        assert table!=[], "Il n'y a plus aucun titre en vente actuellement. Attendez le retour de stocks demain, ou que quelqu'un en vende un."
        pagemax=setMax(len(table))
        curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'titres','{2}','None','None','None','None',1,{3},'countDesc',False)".format(ctx.message.id,ctx.author.id,option,pagemax))
        ligne=curseurCMD.execute("SELECT * FROM commandes WHERE MessageID={0}".format(ctx.message.id)).fetchone()
    else:
        if option=="marketplace":
            table=curseur.execute("SELECT marketplace.ID,marketplace.Stock,titres.Rareté,titres.Nom FROM marketplace JOIN titres ON marketplace.ID=titres.ID ORDER BY Rareté DESC").fetchall()
        else:
            table=curseur.execute("SELECT * FROM titres ORDER BY Rareté DESC").fetchall()
        pagemax=setMax(len(table))

    page=setPage(ligne["Page"],pagemax,turn)

    embed=embedTMP(table,page,ligne["Mobile"])
    embed=auteur(ctx.guild.get_member(699728606493933650),None,None,embed,"olbor")
    embed.set_footer(text="Page {0}/{1}".format(page,pagemax))
    if option=="marketplace":
        embed.title="Titres en vente aujourd'hui"
    else:
        embed.title="Liste des titres existants"
    embed.color=0xf58d1d
    
    message=await sendEmbed(ctx,embed,react,False,curseurCMD,connexionCMD,page,pagemax)
    if not react:
        await message.add_reaction("<:otMOBILE:833736320919797780>")
    

def embedTMP(table,page,mobile):
    embed=discord.Embed()
    field1,field2,field3="","",""
    stop=15*page if 15*page<len(table) else len(table)
    for i in range(15*(page-1),stop):
        nom="__{0}__ - {1}".format(table[i]["ID"],table[i]["Nom"])
        stock=table[i]["Stock"]
        statut="{0} <:otCOINS:873226814527520809> - {1}".format(dictValue[table[i]["Rareté"]],dictStatut[table[i]["Rareté"]])
        if table[i]["Stock"]==0:
            nom="~~{0}~~".format(nom)
            stock="~~{0}~~".format(stock)
            statut="~~{0}~~".format(statut)
        field1,field2,field3=addtoFields(field1,field2,field3,mobile,nom,stock,statut)
    
    embed=createFields(mobile,embed,field1,field2,field3,"ID - Titre","Stock","Prix <:otCOINS:873226814527520809> - Type") 
    return embed