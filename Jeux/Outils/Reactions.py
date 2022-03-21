import asyncio

from Core.Fonctions.Embeds import createEmbed, embedAssertClassic
from Jeux.CodeNames import JeuCodeNames
from Jeux.Matrice import JeuMatrice
from Jeux.Morpion import JeuMorpion
from Jeux.Puissance4 import JeuP4
from Jeux.Tortues import JeuTortues
from Jeux.TortuesDuo import JeuTortuesDuo
from Jeux.TrivialBR import JeuTrivialBR
from Jeux.TrivialParty import JeuTrivialParty
from Jeux.TrivialVersus import JeuTrivialVersus
from Stats.SQL.ConnectSQL import connectSQL
from Titres.Outils import createAccount

dictMax={JeuTortues:5,JeuTortuesDuo:4,JeuTrivialVersus:5,JeuTrivialBR:15,JeuTrivialParty:15,JeuP4:2,JeuMatrice:2,JeuCodeNames:4,JeuMorpion:2}
emotes=["<:ot1:705766186909958185>","<:ot2:705766186989912154>","<:ot3:705766186930929685>","<:ot4:705766186947706934>","<:ot5:705766186713088042>","<:ot6:705766187182850148>","<:ot7:705766187115741246>","<:ot8:705766187132256308>","<:ot9:705766187145101363>","<:ot10:705766186909958206>"]
emotesIds=[705766186909958185,705766186989912154,705766186930929685,705766186947706934,705766186713088042,705766187182850148,705766187115741246,705766187132256308,705766187145101363,705766186909958206]

async def joinGame(message,user,reaction,inGame,dictJeux):
    try:
        assert message.id in dictJeux
        if user.bot:
            return
        game=dictJeux[message.id]
        if user.id==game.invoke and user.id in game.ids:
            game.playing=True
            return
        assert user.id not in game.ids
        assert user.id not in inGame
        inGame.append(user.id)
        game.addPlayer(user,message)
        if len(game.ids)==dictMax[type(game)]:
            game.playing=True
        await message.channel.send("<:otVERT:868535645897912330> <@{0}> rejoint la partie !".format(user.id))
        await reaction.remove(user)
    except:
        pass


async def cancelGame(message,user,reaction,inGame,dictJeux):
    if message.id in dictJeux:
        game=dictJeux[message.id]
        if user.id not in game.ids:
            if not user.bot:
                await reaction.remove(user)
            return
        inGame.remove(user.id)
        game.ids.remove(user.id)
        for i in game.joueurs:
            if i.id==user.id:
                if type(game)==JeuTortues:
                    game.tortues.append(i.couleur)
                elif type(game)==JeuMatrice:
                    game.couleurs.append(i.couleur)
                game.joueurs.remove(i)
            
        await message.channel.send("<:otROUGE:868535622237818910> <@{0}> ne souhaite plus jouer.".format(user.id))
        await reaction.remove(user)


async def trivialReact(message,emoji,user,reaction,gamesTrivial):
    try:
        choix={705766186909958185:0,705766186989912154:1,705766186930929685:2,705766186947706934:3,473254057511878656:4}
        if message.id in gamesTrivial:
            tableQuestion=gamesTrivial[message.id]
            assert type(tableQuestion) in (JeuTrivialBR, JeuTrivialParty, JeuTrivialVersus)
            if user.id in tableQuestion.reponses:
                if tableQuestion.reponses[user.id]==None:
                    tableQuestion.reponses[user.id]=choix[emoji.id]
            if not user.bot:
                await reaction.remove(user)
    except AssertionError:
        pass


async def checkReactDel(message,reaction,dictJeux):
    if message.id in dictJeux:
        await message.add_reaction(str(reaction))


async def miseCoins(message,user,reaction,dictJeux,bot):
    try:
        if user.bot:
            return
        assert message.id in dictJeux
        game=dictJeux[message.id]

        connexionUser,curseurUser=connectSQL("OT",user.id,"Titres",None,None)
        createAccount(connexionUser,curseurUser)
        coins=int(curseurUser.execute("SELECT * FROM coins").fetchone()["Coins"])
        connexionUser.close()

        assert coins>0, "Vous n'avez pas de OT Coins."
        if user.id in game.ids:
            cle="Mise"
            embed=createEmbed("Mise d'OT Coins","Pour miser des OT Coins, écrivez combien vous souhaitez mettre sur cette partie.\nVous avez actuellement {0} <:otCOINS:873226814527520809>.\nA la fin de la partie, ces OT Coins reviendront au gagnant.".format(coins),0xad917b,"LOL",user)
            embed.set_footer(text="Mise d'OT Coins")
            messMise=await message.reply(embed=embed)

            def checkMise(mess):
                try:
                    int(mess.content)
                except:
                    return False
                return mess.author.id==user.id and mess.channel.id==message.channel.id

            mess=await bot.wait_for('message', check=checkMise, timeout=20)
        else:
            cle="Pari"
            assert game.paris.ouvert, "Les paris pour cette partie sont fermés !"
            if user.id not in game.paris.paris:
                descip=""
                dictPari={}
                for i in range(len(game.joueurs)):
                    if game.paris.cotes[game.joueurs[i].id]==None or game.joueurs[i].guild!=reaction.message.guild.id:
                        continue
                    descip+="{0} : <@{1}> (côte : {2})\n".format(emotes[i],game.joueurs[i].id,game.paris.cotes[game.joueurs[i].id])
                    dictPari[emotesIds[i]]=game.joueurs[i].id
                embed=createEmbed("Pari d'OT Coins","Vous devez préciser sur qui vous voulez parier des OT Coins. Réagissez avec le chiffre correspondant au joueur que vous voulez.\n{0}".format(descip),0xad917b,"LOL",user)
                embed.set_footer(text="Pari d'OT Coins")
                messMise=await message.reply(embed=embed)
                for i in dictPari.keys():
                    await messMise.add_reaction(emotes[emotesIds.index(i)])

                def checkJoueur(react,userReact):
                    if type(reaction.emoji)==str or type(react.emoji)==str:
                        return False
                    return react.emoji.id in list(dictPari.keys()) and userReact.id==user.id and react.message.id==messMise.id
                
                react,userReact=await bot.wait_for("reaction_add",check=checkJoueur,timeout=20)
                await messMise.clear_reactions()
                game.paris.paris[user.id]=dictPari[react.emoji.id]
                game.paris.parissomme[user.id]=0
            
            embed=createEmbed("Pari d'OT Coins","Pour parier des OT Coins sur <@{0}>, écrivez combien vous souhaitez miser.\nVous avez actuellement {1} <:otCOINS:873226814527520809>.\nA la fin de la partie, si <@{0}> gagne, vous remporterez votre mise multiplié par sa côte : {2}.".format(game.paris.paris[user.id],coins,game.paris.cotes[game.paris.paris[user.id]]),0xad917b,"LOL",user)
            embed.set_footer(text="Pari d'OT Coins")
            messMise=await message.reply(embed=embed)

            def checkMise(mess):
                try:
                    int(mess.content)
                except:
                    return False
                return mess.author.id==user.id and mess.channel.id==message.channel.id

            mess=await bot.wait_for('message', check=checkMise, timeout=20)


        nbCoins=int(mess.content)
        assert nbCoins>0, "Vous ne pouvez pas miser un nombre négatif d'OT Coins."
        connexionUser,curseurUser=connectSQL("OT",user.id,"Titres",None,None)
        coins=curseurUser.execute("SELECT * FROM coins").fetchone()["Coins"]
        assert nbCoins<coins, "Vous ne pouvez pas miser plus que ce que vous n'avez !"

        if user.id in game.ids:
            game.paris.mises[user.id]+=nbCoins
        else:
            game.paris.parissomme[user.id]+=nbCoins
        curseurUser.execute("UPDATE coins SET Coins=Coins-{0}".format(nbCoins))
        connexionUser.commit()

        embed=createEmbed("{0} d'OT Coins".format(cle),"Vous avez misé {0} <:otCOINS:873226814527520809> !".format(nbCoins),0xad917b,"LOL",user)
        embed.set_footer(text="{0} d'OT Coins".format(cle))
        await messMise.edit(embed=embed)
    except AssertionError as er:
        if er!="":
            await message.reply(embed=embedAssertClassic(er),delete_after=5)
    except asyncio.exceptions.TimeoutError:
        await messMise.edit(embed=embedAssertClassic("La transaction a été annulée."),delete_after=5)
    await reaction.remove(user)
