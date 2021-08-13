from Stats.SQL.ConnectSQL import connectSQL
from Titres.Outils import createAccount
from Core.Fonctions.Embeds import createEmbed, embedAssert
from random import randint
import asyncio

listeReact=["<:ot1:705766186909958185>","<:ot2:705766186989912154>","<:ot3:705766186930929685>"]
dictValuePack={705766186909958185:500,705766186989912154:1500,705766186930929685:3000}
dictSell={1:150,2:400,3:2500}
dictStatut={0:"Fabuleux",1:"Rare",2:"Légendaire",3:"Unique"}

async def packTitre(ctx,bot):
    try:
        connexionUser,curseurUser=connectSQL("OT",ctx.author.id,"Titres",None,None)
        createAccount(connexionUser,curseurUser)
        coins=curseurUser.execute("SELECT * FROM coins").fetchone()["Coins"]
        curseurUser.close()
        assert coins>=500, "Vous n'avez pas assez d'OT Coins pour acheter un Pack."
        liste=[1]
        listeReactID=[705766186909958185]

        if coins>=1500:
            liste.append(2)
            listeReactID.append(705766186989912154)
        elif coins>=3000:
            liste.append(3)
            listeReactID.append(705766186930929685)

        descip="Voici la liste des Packs que vous pouvez acheter :\n"
        for i in liste:
            if i==1:
                descip+="\n<:ot1:705766186909958185> : **Petit Pack** - 1 à 2 titres, faible probabilité d'obtenir un titre Légendaire. **500** <:otCOINS:873226814527520809>"
            elif i==2:
                descip+="\n<:ot2:705766186989912154> : **Pack Classique** - 3 à 4 titres, probabilité raisonnable d'obtenir un titre Légendaire. **1500** <:otCOINS:873226814527520809>"
            elif i==3:
                descip+="\n<:ot3:705766186930929685> : **Super Pack** - 5 titres, minimum 2 Légendaires. **3000** <:otCOINS:873226814527520809>"
        
        descip+="\n\nCliquez sur la réaction correspondante au pack pour l'acheter. Vous avez actuellement {0} OT Coins.".format(coins)
        
        embed=createEmbed("Packs de Titres",descip,0xf58d1d,ctx.invoked_with.lower(),ctx.author)
        message=await ctx.reply(embed=embed)
        for i in range(len(liste)):
            await message.add_reaction(listeReact[i])
        
        def checkPack(reaction,user):
            if type(reaction.emoji)==str:
                return False
            return reaction.emoji.id in listeReactID and reaction.message.id==message.id and user.id==ctx.author.id
        
        reaction,user=await bot.wait_for('reaction_add', check=checkPack, timeout=60)
        await message.clear_reactions()

        connexionUser,curseurUser=connectSQL("OT",ctx.author.id,"Titres",None,None)
        coins=curseurUser.execute("SELECT * FROM coins").fetchone()["Coins"]
        assert coins>=dictValuePack[reaction.emoji.id], "Vous n'avez pas assez d'OT Coins pour acheter ce Pack."

        connexion,curseur=connectSQL("OT","Titres","Titres",None,None)
        if reaction.emoji.id==705766186909958185:
            nb=randint(1,2)
            leg=True if randint(1,20)==3 else False
        elif reaction.emoji.id==705766186989912154:
            nb=randint(3,4)
            leg=True if randint(1,10)==3 else False
        elif reaction.emoji.id==705766186930929685:
            nb=3
            leg=True if randint(1,30)==3 else False
        
        titres=[]
        for i in range(nb):
            if i==0 and leg:
                titres.append(curseur.execute("SELECT * FROM titres WHERE Rareté=2 AND Stock<>0 ORDER BY RANDOM()").fetchone())
            else:
                titres.append(curseur.execute("SELECT * FROM titres WHERE Rareté=1 AND Stock<>0 ORDER BY RANDOM()").fetchone())
        if reaction.emoji.id==705766186930929685:
            titres.append(curseur.execute("SELECT * FROM titres WHERE Rareté=2 AND Stock<>0 ORDER BY RANDOM()").fetchone())
            titres.append(curseur.execute("SELECT * FROM titres WHERE Rareté=2 AND Stock<>0 ORDER BY RANDOM()").fetchone())

        descip="**Contenu de votre Pack :**\n"
        doublons=0
        for i in titres:
            if i==None:
                doublons+=200
                descip+="\nManque de stock. 200 <:otCOINS:873226814527520809>"
            else:
                if curseurUser.execute("SELECT * FROM titresUser WHERE ID={0}".format(i["ID"])).fetchone()!=None:
                    doublons+=dictSell[i["Rareté"]]
                    descip+="\n~~`{0}` {1} ({2})~~ : Doublon. {2} <:otCOINS:873226814527520809>".format(i["ID"],i["Nom"],dictStatut[i["Rareté"]],dictSell[i["Rareté"]])
                else:
                    curseurUser.execute("INSERT INTO titresUser VALUES({0},'{1}',{2})".format(i["ID"],i["Nom"],i["Rareté"]))
                    curseur.execute("UPDATE titres SET Stock=Stock-1 WHERE ID={0}".format(i["ID"]))
                    curseur.execute("UPDATE titres SET Known=True WHERE ID={0}".format(i["ID"]))
                    descip+="\n`{0}` {1} ({2})".format(i["ID"],i["Nom"],dictStatut[i["Rareté"]])

        curseurUser.execute("UPDATE coins SET Coins=Coins-{0}".format(dictValuePack[reaction.emoji.id]-doublons))
        connexion.commit()
        connexionUser.commit()
        
        embed=createEmbed("Packs de Titres acheté !",descip,0xf58d1d,ctx.invoked_with.lower(),ctx.author)
        message=await ctx.reply(embed=embed)
    except AssertionError as er:
        await ctx.reply(embed=embedAssert(er))
    except asyncio.exceptions.TimeoutError:
        await message.clear_reactions()