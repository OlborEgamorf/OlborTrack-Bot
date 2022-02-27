import asyncio
from random import randint

from Core.Decorator import OTJeux
from Core.Fonctions.Embeds import createEmbed
from Core.Fonctions.Unpin import pin, unpin
from Jeux.Morpion.ClasseMorpion import JeuMorpion
from Jeux.Paris import Pari
from Stats.Tracker.Jeux import exeStatsJeux
from Titres.Carte import sendCarte
from Titres.Outils import gainCoins


@OTJeux
async def startGameMorpion(ctx,bot,game,inGame,gamesMorpion):
    assert ctx.author.id not in inGame, "Terminez votre partie en cours avant de lancer ou rejoindre une partie."
    game=JeuMorpion(ctx.guild,ctx.author.id)
    game.ids.append(ctx.author.id)
    inGame.append(ctx.author.id)
    message=await ctx.send(embed=createEmbed("Morpion","Appuyez sur la réaction <:otVALIDER:772766033996021761> pour défier <@{0}> au Morpion.\nL'objectif est d'aligner 3 jetons de votre couleur dans n'importe quel sens (horizontallement, verticalement ou diagonalement) en premier !\nÉcrivez les coordonnées de la case où vous voulez poser votre jeton dans le salon lorsque c'est votre tour ! En commençant par la lettre puis le chiffre.\nLa personne qui a demandé la partie peut cliquer sur <:otANNULER:811242376625782785> pour se retirer de la partie.".format(ctx.author.id),0xad917b,ctx.invoked_with.lower(),ctx.guild))
    gamesMorpion[message.id]=game

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
        await message.edit(embed=createEmbed("Morpion","Une minute s'est écoulée et personne n'a répondu à l'invitation.",0xad917b,ctx.invoked_with.lower(),ctx.guild))
        for i in game.ids:
            inGame.remove(i)
        return
    for i in game.ids:
        game.addPlayer(ctx.guild.get_member(i))
    descip="<:otVERT:868535645897912330> La partie commence "
    for i in game.joueurs:
        descip+="<@{0}> ".format(i.id)
    await message.channel.send(descip)
    gamesMorpion[message.id]=game
    await pin(message)
    await message.add_reaction("<:otCOINS:873226814527520809>")
    messAd=await bot.get_channel(870598360296488980).send("{0} - {1} : partie OT!morpion débutée\n2 joueurs".format(ctx.guild.name,ctx.guild.id))

    turn=randint(0,1)
    game.paris=Pari(game.ids,"Morpion")
    while game.playing:
        await message.edit(embed=game.createEmbedMorpion(turn))
        add=await game.play(turn,message,bot)
        if add[0]==True:
            if game.tab.checkTab(add[1],add[2],turn+1)==True:
                await message.clear_reactions()
                await message.edit(embed=game.createEmbedMorpion(turn))
                if turn==0: lose=1
                else: lose=0
                wins=exeStatsJeux(game.joueurs[turn].id,game.joueurs[lose].id,game.guild.id,"Morpion",game.tours,"win")
                gainCoins(game.joueurs[turn].id,50+sum(game.paris.mises.values()))
                game.paris.distribParis(game.joueurs[turn].id)
                await message.channel.send(embed=game.embedWin(turn,False))
                await sendCarte(bot.get_user(game.joueurs[turn].id),"Morpion",wins,"classic",message.channel)
                game.playing=False
                await unpin(message)
            else:
                if game.tab.checkNul()==True:
                    await message.clear_reactions()
                    await message.edit(embed=game.createEmbedMorpion(turn))
                    await message.channel.send(embed=game.embedWin(turn,True))
                    game.playing=False
                    await unpin(message)
                else:
                    game.tours+=1
        
        game.fermeture()
        turn+=1
        if turn==len(game.joueurs):
            turn=0
    if "messAd" in locals():
        await messAd.delete()

    del gamesMorpion[message.id]
    return game
