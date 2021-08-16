from Jeux.Tortues.ClasseTortues import JeuTortues
from Jeux.Tortues.ClasseTortuesDuo import JeuTortuesDuo
from Jeux.Trivial import Versus
from Jeux.Trivial.BattleRoyale import BattleRoyale
from Jeux.Trivial.Party import Party
from Jeux.NewP4 import JeuP4
from Core.Fonctions.Embeds import createEmbed, embedAssert
from Stats.SQL.ConnectSQL import connectSQL
from Titres.Outils import createAccount
import asyncio

dictMax={JeuTortues:5,JeuTortuesDuo:4,Versus:5,BattleRoyale:15,Party:15,JeuP4:2}

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
        game.mises[user.id]=0
        inGame.append(user.id)
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
        del game.mises[user.id]
        await message.channel.send("<:otROUGE:868535622237818910> <@{0}> ne souhaite plus jouer.".format(user.id))
        await reaction.remove(user)


async def checkReactDel(message,reaction,dictJeux):
    if message.id in dictJeux:
        await message.add_reaction(str(reaction))


async def miseCoins(message,user,reaction,inGame,dictJeux,bot):
    try:
        assert message.id in dictJeux
        if user.bot:
            return
        game=dictJeux[message.id]
        assert user.id in game.ids

        connexionUser,curseurUser=connectSQL("OT",user.id,"Titres",None,None)
        createAccount(connexionUser,curseurUser)
        coins=curseurUser.execute("SELECT * FROM coins").fetchone()["Coins"]
        connexionUser.close()

        assert coins>0, "Vous n'avez pas de OT Coins."
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
        nbCoins=int(mess.content)
        assert nbCoins>0, "Vous ne pouvez pas miser un nombre négatif d'OT Coins."
        connexionUser,curseurUser=connectSQL("OT",user.id,"Titres",None,None)
        coins=curseurUser.execute("SELECT * FROM coins").fetchone()["Coins"]
        assert nbCoins<coins, "Vous ne pouvez pas miser plus que ce que vous n'avez !"

        game.mises[user.id]+=nbCoins
        curseurUser.execute("UPDATE coins SET Coins=Coins-{0}".format(nbCoins))
        connexionUser.commit()

        embed=createEmbed("Mise d'OT Coins","Vous avez misé {0} <:otCOINS:873226814527520809> !".format(nbCoins),0xad917b,"LOL",user)
        embed.set_footer(text="Mise d'OT Coins")
        await messMise.edit(embed=embed)
    except AssertionError as er:
        if er!="":
            await message.reply(embed=embedAssert(er),delete_after=5)
    except asyncio.exceptions.TimeoutError:
        await messMise.edit(embed=embedAssert("La transaction a été annulée."),delete_after=5)
    await reaction.remove(user)