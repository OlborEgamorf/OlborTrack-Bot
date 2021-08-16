from Jeux.Trivial.BattleRoyale import BattleRoyale
from Jeux.Trivial.Classic import Question, Streak, embedTrivial
from Jeux.Trivial.Party import Party
from Jeux.Trivial.Versus import Versus
from Stats.SQL.Compteur import compteurTrivialS


async def trivialReact(message,client,emoji,user,guild,reaction,inGame,gamesTrivial):
    choix={705766186909958185:0,705766186989912154:1,705766186930929685:2,705766186947706934:3,473254057511878656:4}
    if message.id in gamesTrivial:
        tableQuestion=gamesTrivial[message.id]
        if type(tableQuestion) in (Question,Streak):
            if user.id!=tableQuestion.author.id:
                return
        elif type(tableQuestion) in (Versus,Party,BattleRoyale):
            if user.id in tableQuestion.reponses:
                if tableQuestion.reponses[user.id]==None:
                    tableQuestion.reponses[user.id]=choix[emoji.id]
            if not user.bot:
                await reaction.remove(user)
            return
        else:
            return
        if tableQuestion.vrai==choix[emoji.id]+1:
            tableQuestion.gestionMulti(True,inGame)
            if tableQuestion.option=="classic":
                await message.clear_reactions()
                message.embeds[0].colour=0x47b03c
                message.embeds[0].description=tableQuestion.affichageWin()
            elif tableQuestion.option=="streak":
                tableQuestion.serie+=1
                tableQuestion.changeTime()
                await reaction.remove(user)
                await embedTrivial(None,await client.get_context(message),client,user,"streak",inGame,gamesTrivial)
                return
        else:
            await message.clear_reactions()
            message.embeds[0].colour=0xcf1742
            message.embeds[0].description=tableQuestion.affichageLose(emoji.id)
            tableQuestion.gestionMulti(False,inGame)
            if tableQuestion.option=="streak":
                results=compteurTrivialS(tableQuestion.author.id,(0,tableQuestion.author.id,13,"TO","GL",tableQuestion.serie),tableQuestion.serie)
                if results[0]:
                    await message.channel.send("Bravo ! Vous avez battu votre record de série avec **{0}** bonnes réponses ! Votre ancien score était **{1}** bonnes réponses.".format(results[1],results[2]))
            del gamesTrivial[message.id]
        await message.edit(embed=message.embeds[0])
        return
    else:
        return
