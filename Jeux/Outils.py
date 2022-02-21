import asyncio

from Core.Fonctions.Embeds import createEmbed, embedAssertClassic
from Stats.SQL.ConnectSQL import connectSQL
from Titres.Outils import createAccount

from Jeux.CodeNames.ClasseCodeNames import JeuCN
from Jeux.CrossServeur.ClasseP4Cross import JeuP4Cross
from Jeux.CrossServeur.ClasseTDCross import JeuTortuesDuoCross
from Jeux.CrossServeur.ClasseTortuesCross import JeuTortuesCross
from Jeux.CrossServeur.ClasseTrivialBRCross import BattleRoyaleCross
from Jeux.CrossServeur.ClasseTrivialPartyCross import PartyCross
from Jeux.CrossServeur.ClasseTrivialVSCross import VersusCross
from Jeux.Matrice.Matrice import JeuMatrice
from Jeux.Morpion.ClasseMorpion import JeuMorpion
from Jeux.P4.P4 import JeuP4
from Jeux.Tortues.ClasseTortues import JeuTortues
from Jeux.Tortues.ClasseTortuesDuo import JeuTortuesDuo
from Jeux.Trivial.BattleRoyale import BattleRoyale
from Jeux.Trivial.Party import Party
from Jeux.Trivial.Versus import Versus

dictMax={JeuTortues:5,JeuTortuesDuo:4,Versus:5,BattleRoyale:15,Party:15,JeuP4:2,JeuTortuesCross:5,JeuP4Cross:2,JeuTortuesDuoCross:4,VersusCross:5,BattleRoyaleCross:7,PartyCross:7,JeuMatrice:2,JeuCN:4,JeuMorpion:2}
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
        game.ids.append(user.id)
        inGame.append(user.id)
        if type(game) in (JeuTortuesCross,JeuP4Cross,JeuTortuesDuoCross,VersusCross,BattleRoyaleCross,PartyCross):
            game.memguild[user.id]=message.guild.id
            game.memmess[user.id]=message
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
        if type(game) in (JeuTortuesCross,JeuP4Cross,JeuTortuesDuoCross,VersusCross,BattleRoyaleCross,PartyCross):
            del game.memguild[user.id]
            del game.memmess[user.id]
        await message.channel.send("<:otROUGE:868535622237818910> <@{0}> ne souhaite plus jouer.".format(user.id))
        await reaction.remove(user)


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
                for i in range(len(game.ids)):
                    if game.paris.cotes[game.ids[i]]==None:
                        continue
                    if type(game) in (JeuTortuesCross,JeuP4Cross,JeuTortuesDuoCross,VersusCross,BattleRoyaleCross,PartyCross):
                        if game.memguild[game.ids[i]]!=reaction.message.guild.id:
                            continue
                    descip+="{0} : <@{1}> (côte : {2})\n".format(emotes[i],game.ids[i],game.paris.cotes[game.ids[i]])
                    dictPari[emotesIds[i]]=game.ids[i]
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
