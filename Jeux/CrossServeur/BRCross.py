from Jeux.Trivial.Attente import attente
import asyncio
from Core.Fonctions.Embeds import embedAssert
from Jeux.Outils import joinGame
from Jeux.CrossServeur.ClasseTrivialBRCross import BattleRoyaleCross
from Stats.Tracker.Jeux import statsServ
from Core.Fonctions.Unpin import unpin
from math import inf

dictOnline=[]

async def trivialBattleRoyaleCross(ctx,bot,inGame,gamesTrivial):
    try:
        assert ctx.author.id not in inGame, "Terminez votre question en cours avant de lancer ou rejoindre une partie."
        new=False
        if len(dictOnline)!=0 and dictOnline[0].playing==False:
            game=dictOnline[0]
            if ctx.guild.id in game.guilds:
                await joinGame(game.guildmess[ctx.guild.id],ctx.author,None,inGame,gamesTrivial)
                return
        else:
            new=True
            game=BattleRoyaleCross(ctx.guild,"br")
            game.invoke=ctx.author.id
            dictOnline.append(game)

        message=await game.startGame(ctx,bot,inGame,gamesTrivial,new,dictOnline)
        if message==False:
            return
        messAd=await bot.get_channel(870598360296488980).send("{0} - {1} : partie OT!trivialbr CROSS débutée\n{2} joueurs".format(ctx.guild.name,ctx.guild.id,len(game.joueurs)))
        game.restants=game.ids.copy()
        
        while game.playing:
            listeDel=[]
            game.reponses={i:None for i in game.restants}
            game.setCateg(None)
            game.setDiff()
            game.newQuestion()
            for i in game.messages:
                embedT=game.createEmbed(False,i.guild)
                await i.edit(embed=embedT)
            await attente(game,20,None)

            count,left,good=0,len(game.restants),0
            for i in game.restants:
                if game.reponses[i]!=game.vrai-1:
                    game.scores[i]-=1
                    if game.scores[i]==0:
                        count+=1
                else:
                    good+=1
            if count==left:
                for i in game.restants:
                    game.scores[i]+=1
            else:
                for i in game.restants:
                    if game.scores[i]==0:
                        game.histo[i]=left-count+1
                        listeDel.append(i)
                for i in listeDel:
                    game.restants.remove(i)
            
            if good>0:
                color=0x47b03c
                descip="**{0} personne*(s)* a *(ont)* eu juste !** {1}".format(good,game.affichageWin()[20:-1])
            else:
                color=0xcf1742
                descip="**Tout le monde s'est trompé...** {0}".format(game.affichageLose(None)[10:-1])
            for i in game.messages:
                embedT=game.createEmbed(True,i.guild)
                embedT.description=descip
                embedT.color=color
                await i.edit(embed=embedT)
            
            if game.maxTour():
                maxi,maxiJoueur=-inf,None
                for i in game.joueurs:
                    if game.scores[i.id]>maxi:
                        maxi,maxiJoueur=game.scores[i.id],i.id
                game.restants=[maxiJoueur]    
            if len(game.restants)==1:
                game.histo[game.restants[0]]=1
                for i in game.messages:
                    await i.clear_reactions()
                    await i.channel.send(embed=game.embedResults(bot.get_user(game.restants[0]),i.guild.id))
                    await unpin(i)
                game.playing=False
                game.stats(bot.get_user(game.restants[0]),"TrivialBR")
                statsServ(game,game.restants[0])
            game.tour+=1
            await asyncio.sleep(5)
            for i in game.messages:
                await i.edit(embed=game.embedHub(i.guild))
            await asyncio.sleep(5)
        await game.endGame(message,inGame,gamesTrivial)
    except AssertionError as er:
        await ctx.send(embed=embedAssert(er))
    except:
        await game.error(ctx,bot,message,inGame,gamesTrivial)
    if "messAd" in locals():
        await messAd.delete()
