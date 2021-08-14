from Jeux.Tortues.ClasseTortues import JeuTortues
from Jeux.Tortues.ClasseTortuesDuo import JeuTortuesDuo
from Jeux.Trivial import Versus

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
        if type(game)==JeuTortues:
            if len(game.ids)==5:
                game.playing=True
        elif type(game)==JeuTortuesDuo:
            if len(game.ids)==4:
                game.playing=True
        elif type(game)==Versus:
            if len(game.ids)==5:
                game.playing=True
        else:
            if len(game.ids)==15:
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
        await message.channel.send("<:otROUGE:868535622237818910> <@{0}> ne souhaite plus jouer.".format(user.id))
        await reaction.remove(user)


async def checkReactDel(message,reaction,dictJeux):
    if message.id in dictJeux:
        await message.add_reaction(str(reaction))