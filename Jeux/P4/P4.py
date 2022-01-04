import asyncio
from random import randint

from Core.Fonctions.Embeds import createEmbed, embedAssert, exeErrorExcept
from Core.Fonctions.Unpin import pin, unpin
from Jeux.P4.ClasseP4 import JeuP4
from Jeux.Paris import Pari
from Stats.Tracker.Jeux import exeStatsJeux
from Titres.Carte import sendCarte
from Titres.Outils import gainCoins

emotes=["<:ot1:705766186909958185>","<:ot2:705766186989912154>","<:ot3:705766186930929685>","<:ot4:705766186947706934>","<:ot5:705766186713088042>","<:ot6:705766187182850148>","<:ot7:705766187115741246>"]
dictCo={705766186909958185:0,705766186989912154:1,705766186930929685:2,705766186947706934:3,705766186713088042:4,705766187182850148:5,705766187115741246:6}

async def startGameP4(ctx,bot,inGame,gamesP4):
    try:
        assert ctx.author.id not in inGame, "Terminez votre partie en cours avant de lancer ou rejoindre une partie."
        game=JeuP4(ctx.guild,ctx.author.id)
        game.ids.append(ctx.author.id)
        inGame.append(ctx.author.id)
        message=await ctx.send(embed=createEmbed("Puissance 4","Appuyez sur la réaction <:otVALIDER:772766033996021761> pour défier <@{0}> au Puissance 4.\nL'objectif est d'aligner 4 jetons de votre couleur dans n'importe quel sens (horizontallement, verticalement ou diagonalement) en premier !\nLes réactions allant de <:ot1:705766186909958185> à <:ot7:705766187115741246> représentent les colonnes où vous pouvez placer votre jeton. Cliquez sur l'une d'entre elles et le jeton apparaîtra !\nLa personne qui a demandé la partie peut cliquer sur <:otANNULER:811242376625782785> pour se retirer de la partie.".format(ctx.author.id),0xad917b,ctx.invoked_with.lower(),ctx.guild))
        gamesP4[message.id]=game

        await message.add_reaction("<:otVALIDER:772766033996021761>")
        await message.add_reaction("<:otANNULER:811242376625782785>")

        for i in range(60):
            if not game.playing:
                await asyncio.sleep(1)
            else:
                break
        
        game.playing=True
        await message.clear_reactions()
        if len(game.ids)<2:
            await message.edit(embed=createEmbed("Puissance 4","Une minute s'est écoulée et personne n'a répondu à l'invitation.",0xad917b,ctx.invoked_with.lower(),ctx.guild))
            for i in game.ids:
                inGame.remove(i)
            return
        for i in game.ids:
            game.addPlayer(ctx.guild.get_member(i))
        descip="<:otVERT:868535645897912330> La partie commence "
        for i in game.joueurs:
            descip+="<@{0}> ".format(i.id)
        await message.channel.send(descip)
        gamesP4[message.id]=game
        await pin(message)
        for i in emotes:
            await message.add_reaction(i)
        await message.add_reaction("<:otCOINS:873226814527520809>")
        messAd=await bot.get_channel(870598360296488980).send("{0} - {1} : partie OT!p4 débutée\n2 joueurs".format(ctx.guild.name,ctx.guild.id))

        turn=randint(0,1)
        game.paris=Pari(game.ids,"P4")
        while game.playing:
            await message.edit(embed=game.createEmbedP4(turn))
            add=await game.play(turn,message,bot)
            if add[0]==True:
                if game.tab.checkTab(add[1],add[2],turn+1)==True:
                    await message.clear_reactions()
                    await message.edit(embed=game.createEmbedP4(turn))
                    if turn==0: lose=1
                    else: lose=0
                    wins=exeStatsJeux(game.joueurs[turn].id,game.joueurs[lose].id,game.guild.id,"P4",game.tours,"win")
                    gainCoins(game.joueurs[turn].id,50+sum(game.paris.mises.values()))
                    game.paris.distribParis(game.joueurs[turn].id)
                    await message.channel.send(embed=game.embedWin(turn,False))
                    await sendCarte(bot.get_user(game.joueurs[turn].id),"P4",wins,"classic",message.channel)
                    game.playing=False
                    await unpin(message)
                else:
                    if game.tab.checkNul()==True:
                        await message.clear_reactions()
                        await message.edit(embed=game.createEmbedP4(turn))
                        await message.channel.send(embed=game.embedWin(turn,True))
                        game.playing=False
                        await unpin(message)
                    else:
                        game.tours+=1      
                        for i in range(7):
                            if game.tab.tableau[0][i]!=0:
                                await message.clear_reaction(emotes[i])
            
            game.fermeture()
            turn+=1
            if turn==len(game.joueurs):
                turn=0
        if "messAd" in locals():
            await messAd.delete()
    except AssertionError as er:
        await ctx.send(embed=embedAssert(er))
        return
    except:
        await ctx.send(embed=await exeErrorExcept(ctx,bot,""))
        await unpin(message)
    for i in game.ids:
        inGame.remove(i)
    del gamesP4[message.id]
