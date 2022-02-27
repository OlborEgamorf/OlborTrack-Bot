import asyncio
from random import choice, randint

import discord
from Core.Decorator import OTJeux
from Core.Fonctions.Embeds import createEmbed
from Core.Fonctions.Unpin import pin, unpin
from Jeux.Matrice.ClasseMatrice import JeuMatrice
from Jeux.Paris import Pari
from Stats.Tracker.Jeux import exeStatsJeux
from Titres.Carte import sendCarte
from Titres.Outils import gainCoins

dictEmotes={("B","C","C","P"):878357453828411392,("B","C","P","P"):878357453534801921,("B","C","P","G"):878357453576732692,("B","R","C","G"):878357453526401055,("B","R","C","P"):878357453400592455,("B","R","P","P"):878357453660643359,("B","R","P","G"):878357453614506025,("B","C","C","G"):878357453702561863,
("R","C","C","P"):878357454008774686,("R","C","P","P"):878357453450907710,("R","C","P","G"):878357453660643358,("R","R","C","G"):878357453656428605,("R","R","C","P"):878357453757108275,("R","R","P","P"):878357453614506026,("R","R","P","G"):878357453660643360,("R","C","C","G"):878357453673234522}
dict0={"B":"Bleu","R":"Rouge"}
dict1={"C":"Carre","R":"Rond"}
dict2={"C":"Creux","P":"Plein"}
dict3={"P":"Petit","G":"Grand"}
emotes=["<:ot1:705766186909958185>","<:ot2:705766186989912154>","<:ot3:705766186930929685>","<:ot4:705766186947706934>","<:ot5:705766186713088042>","<:ot6:705766187182850148>","<:ot7:705766187115741246>","<:ot8:705766187132256308>"]
dictCo={705766186909958185:0,705766186989912154:1,705766186930929685:2,705766186947706934:3,705766186713088042:4,705766187182850148:5,705766187115741246:6,705766187132256308:7}
dictX={1:0,2:1,3:2,4:3}
dictY={"a":0,"b":1,"c":2,"d":3}
dictYReverse={0:"A",1:"B",2:"C",3:"D"}

@OTJeux
async def startGameMatrice(ctx,bot,game,inGame,gamesMatrice):
    assert ctx.author.id not in inGame, "Terminez votre partie en cours avant de lancer ou rejoindre une partie."
    game=JeuMatrice(ctx.guild,ctx.author.id)
    game.ids.append(ctx.author.id)
    inGame.append(ctx.author.id)
    message=await ctx.send(embed=createEmbed("Matrice","Le jeu se joue à 2 joueurs.\nLe jeu fonctionne avec un plateau de 16 cases, 4x4.Il y a aussi 16 pions. Chaque joueur possède 8 pions de sa couleur.\nChaque pion possède 4 caractéristiques : la taille (grand/petit), la couleur (bleu/rouge), la forme (carré/rond) et le remplissage (plein/creux).\nLe but est d'aligner 4 pions ayant au moins une caractéristique en commun.\nPour jouer, servez vous des réactions <:ot1:705766186909958185> à <:ot8:705766187132256308> pour sélectionner votre pion, puis écrivez les coordonnées de la case que vous voulez, de la forme lettreCHIFFRE\nBonne chance !\n\nAppuyez sur la réaction <:otVALIDER:772766033996021761> pour rejoindre la partie de Course des tortues et <:otANNULER:811242376625782785> pour annuler votre participation.\n<@{0}> peut lancer la partie en appuyant sur <:otVALIDER:772766033996021761>, sinon elle se lancera automatiquement au bout de 1 minute.".format(ctx.author.id),0xad917b,ctx.invoked_with.lower(),ctx.guild))
    gamesMatrice[message.id]=game

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
        await message.edit(embed=createEmbed("Matrice","Une minute s'est écoulée et personne n'a répondu à l'invitation.",0xad917b,ctx.invoked_with.lower(),ctx.guild))
        for i in game.ids:
            inGame.remove(i)
            return
    
    couleurs=["rouge","bleu"]
    for i in game.ids:
        col=choice(couleurs)
        game.addPlayer(ctx.guild.get_member(i),col)
        couleurs.remove(col)

    descip="<:otVERT:868535645897912330> La partie commence "
    for i in game.joueurs:
        descip+="<@{0}> ".format(i.userid)
    await message.channel.send(descip)
    message=await message.channel.send(embed=discord.Embed(title="Préparation..."))
    gamesMatrice[message.id]=game
    await pin(message)
    for i in emotes:
        await message.add_reaction(i)
    await message.add_reaction("<:otCOINS:873226814527520809>")
    messAd=await bot.get_channel(870598360296488980).send("{0} - {1} : partie OT!matrice débutée\n2 joueurs".format(ctx.guild.name,ctx.guild.id))

    turn=randint(0,len(game.joueurs)-1)
    game.paris=Pari(game.ids,"Matrice")
    while game.playing:
        game.tours+=1
        await message.edit(embed=game.embedGame(turn))
        x,y=await game.play(turn,message,bot)

        win=game.tab.checkTab(x,y)
        if win[0]:            
            game.playing=False
            await message.edit(embed=game.embedGame(turn))
            embed=game.embedWin(turn,game.tab.checkNul(),win[1],win[3],win[2])
            await message.channel.send(embed=embed)
            await message.clear_reactions()
            await unpin(message)
            if turn==0: lose=1
            else: lose=0
            wins=exeStatsJeux(game.joueurs[turn].userid,game.joueurs[lose].userid,game.guild.id,"Matrice",game.tours,"win")
            await sendCarte(bot.get_user(game.joueurs[turn].id),"Matrice",wins,"classic",message.channel)
            gainCoins(game.joueurs[turn].userid,50+sum(game.paris.mises.values()))
            game.paris.distribParis(game.joueurs[turn].userid)
        elif game.tab.checkNul():
            await message.edit(embed=game.embedGame(turn))
            embed=game.embedWin(turn,game.tab.checkNul(),win[1],win[3],win[2])
            await message.clear_reactions()
            await unpin(message)
            game.playing=False
        
        game.fermeture()
        turn+=1
        if turn==len(game.joueurs):
            turn=0

    if "messAd" in locals():
        await messAd.delete()

    del gamesMatrice[message.id]
    return game
