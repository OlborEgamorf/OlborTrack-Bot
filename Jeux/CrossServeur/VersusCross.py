import asyncio

import discord
from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.Embeds import embedAssert
from Jeux.CrossServeur.ClasseTrivialVSCross import VersusCross
from Jeux.Outils import joinGame
from Stats.Tracker.Jeux import statsServ
from Core.Fonctions.Unpin import unpin
from math import inf
from Jeux.Paris import Pari

dictOnline=[]
emotesTrue=["<:ot1VRAI:773993429130149909>", "<:ot2VRAI:773993429050195979>", "<:ot3VRAI:773993429331738624>", "<:ot4VRAI:773993429423095859>"]
emotesFalse=["<:ot1FAUX:773993429315092490>", "<:ot2FAUX:773993429172486145>", "<:ot3FAUX:773993429402779698>", "<:ot4FAUX:773993429373026354>"]

async def trivialVersusCross(ctx,bot,inGame,gamesTrivial):
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
            game=VersusCross(ctx.guild,"versus")
            game.invoke=ctx.author.id
            dictOnline.append(game)
        
        message=await game.startGame(ctx,bot,inGame,gamesTrivial,new,dictOnline)
        if message==False:
            return
        messAd=await bot.get_channel(870598360296488980).send("{0} - {1} : partie OT!trivialversus CROSS débutée\n{2} joueurs".format(ctx.guild.name,ctx.guild.id,len(game.joueurs)))
        game.paris=Pari(game.ids,"TrivialVersus")
        while game.playing:
            game.reponses={i:None for i in game.ids}
            game.setCateg(None)
            game.setDiff()
            game.newQuestion()
            for i in game.messages:
                embedT=game.createEmbed(False,i.guild)
                await i.edit(embed=embedT)
            time,done=0,False
            while time!=20 and not done:
                await asyncio.sleep(1)
                done=True
                for j in game.reponses:
                    if game.reponses[j]==None:
                        done=False
                time+=1
            count=[]
            good=0
            for i in game.joueurs:
                if game.reponses[i.id]==game.vrai-1:
                    good+=1
                    game.scores[i.id]+=1
                    game.histo[i.id]+=emotesTrue[game.reponses[i.id]]
                    if game.scores[i.id]==game.max:
                        count.append(i)
                elif game.reponses[i.id]==None:
                    game.histo[i.id]+="<:otBlank:828934808200937492>"
                else:
                    game.histo[i.id]+=emotesFalse[game.reponses[i.id]]
            
            if good>0:
                color=0x47b03c
                descip="**{0} personnes ont eu juste !** {1}".format(good,game.affichageWin()[20:-1])
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
                        maxi,maxiJoueur=game.scores[i.id],i
                count=[maxiJoueur]
            if len(count)==1:
                for i in game.messages:
                    await i.clear_reactions()
                    await i.channel.send(embed=game.embedResults(count[0],i.guild.id))
                    await unpin(i)
                game.playing=False
                game.stats(count[0],"TrivialVersus")
                statsServ(game,count[0].id)
                game.paris.distribParis(count[0].id)
            elif len(count)>1:
                game.max+=1
                await asyncio.sleep(7)
            else:
                await asyncio.sleep(7)
            game.tour+=1
            game.fermeture()
        await game.endGame(message,inGame,gamesTrivial)
    except AssertionError as er:
        await ctx.send(embed=embedAssert(er))
    except:
        await game.error(ctx,bot,message,inGame,gamesTrivial)
    if "messAd" in locals():
        await messAd.delete()
