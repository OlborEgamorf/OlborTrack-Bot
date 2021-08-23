import asyncio
from random import choice, randint

import discord
from Core.Fonctions.Embeds import createEmbed, embedAssert, exeErrorExcept
from Jeux.Tortues.ClassesAutres import Carte
from Jeux.Tortues.ClasseTortues import JeuTortues
from Jeux.Paris import Pari

listeCouleurs=("rouge","jaune","bleue","verte","violette")
emotes=["<:ot1:705766186909958185>","<:ot2:705766186989912154>","<:ot3:705766186930929685>","<:ot4:705766186947706934>","<:ot5:705766186713088042>","<:OTTbleu:860119157491892255>", "<:OTTjaune:860119157688631316>", "<:OTTrouge:860119157495693343>", "<:OTTvert:860119157331853333>", "<:OTTviolet:860119157672247326>"]
dictEmote={0:"<:otBlank:828934808200937492>","rouge":"<:OTTrouge:860119157495693343>","verte":"<:OTTvert:860119157331853333>","bleue":"<:OTTbleu:860119157491892255>","jaune":"<:OTTjaune:860119157688631316>","violette":"<:OTTviolet:860119157672247326>","last":"*dernière tortue*","multi":"*au choix*"}
dictColor={"bleue":0x00CCFF,"violette":0x993366,"rouge":0xFF0000,"verte":0x77B255,"jaune":0xFFFF00}


async def startGameTortues(ctx,bot,inGame,gamesTortues):
    try:
        assert ctx.author.id not in inGame, "Terminez votre partie en cours avant de lancer ou rejoindre une partie."
        game=JeuTortues(ctx.guild,ctx.author.id)
        game.ids.append(ctx.author.id)
        inGame.append(ctx.author.id)
        message=await ctx.send(embed=createEmbed("Course des tortues","Le jeu se joue de 2 à 5 joueurs.\nAu début de la partie, chaque joueur se voit attribuer une couleur secrète, envoyée en message privé, qui est celle de sa tortue.\nLe but est d'atteindre l'arrivée avant tout le monde, en jouant avec des cartes qui font avancer les tortues.\nLes joueurs jouent chacun leur tour. Les réactions <:ot1:705766186909958185> à <:ot5:705766186713088042> permettent de choisir sa carte.\nSi vous choisissez une carte 'au choix', cliquez ensuite sur la réaction de la tortue que vous voulez déplacer <:OTTbleu:860119157491892255> <:OTTjaune:860119157688631316> <:OTTrouge:860119157495693343> <:OTTvert:860119157331853333> <:OTTviolet:860119157672247326>.\nLes cartes 'dernière tortue' font avancer la dernière tortue.\nEn dehors de la case départ, les tortues s'empilent et avancent en même temps !\nSi plusieurs tortues arrivent en même temps, celle qui est le plus bas gagne !\nBonne chance !\n\nAppuyez sur la réaction <:otVALIDER:772766033996021761> pour rejoindre la partie de Course des tortues et <:otANNULER:811242376625782785> pour annuler votre participation.\n<@{0}> peut lancer la partie en appuyant sur <:otVALIDER:772766033996021761>, sinon elle se lancera automatiquement au bout de 1 minute.".format(ctx.author.id),0xad917b,ctx.invoked_with.lower(),ctx.guild))
        gamesTortues[message.id]=game

        await message.add_reaction("<:otVALIDER:772766033996021761>")
        await message.add_reaction("<:otANNULER:811242376625782785>")

        for i in range(60):
            if not game.playing:
                await asyncio.sleep(1)
            else:
                break
        
        game.playing=True
        await message.clear_reactions()
        if await game.checkPlayers(message,inGame,ctx,2):
            await game.emotesUser(bot)
            descip="<:otVERT:868535645897912330> La partie commence "
            for i in game.joueurs:
                descip+="<@{0}> ".format(i.userid)
                await i.user.send(embed=createEmbed("Course des tortues : {0}".format(i.couleur),"Votre couleur est : {0} {1}".format(i.couleur,dictEmote[i.couleur]),dictColor[i.couleur],ctx.invoked_with.lower(),i.user))
            await message.channel.send(descip)
            message=await message.channel.send(embed=discord.Embed(title="Votre couleur vous a été envoyée par MP..."))
            gamesTortues[message.id]=game
            try:
                await message.pin()
            except:
                pass
            for i in emotes:
                await message.add_reaction(i)
            await message.add_reaction("<:otCOINS:873226814527520809>")
            messAd=await bot.get_channel(870598360296488980).send("{0} - {1} : partie OT!tortues débutée\n{2} joueurs".format(ctx.guild.name,ctx.guild.id,len(game.joueurs)))
        else:
            return

        game.giveCards()
        turn=randint(0,len(game.joueurs)-1)
        game.paris=Pari(game.ids,"Tortues")
        while game.playing:
            await message.edit(embed=game.embedGame(game.joueurs[turn].user))
            couleur,valeur,carte=await game.play(turn,message,bot)

            if game.mouvement(couleur,valeur):            
                game.playing=False
                await message.edit(embed=game.embedGame(game.joueurs[turn].user))
                embed=game.embedWin(game.getWinner())
                game.stats(game.getWinner())
                await message.channel.send(embed=embed)
                await message.clear_reactions()
                await message.unpin()

            game.fermeture()
            game.joueurs[turn].jeu.remove(carte)
            game.joueurs[turn].pioche(game.cartes)
            turn+=1
            if turn==len(game.joueurs):
                turn=0
            if len(game.cartes)==0:
                game.cartes=[Carte(i,1) for i in listeCouleurs]*5+[Carte(i,2) for i in listeCouleurs]+[Carte(i,-1) for i in listeCouleurs]*2+[Carte("multi",1) for i in range(5)]+[Carte("last",1) for i in range(3)]+[Carte("last",2) for i in range(2)]+[Carte("multi",-1) for i in range(2)]

        if "messAd" in locals():
            await messAd.delete()
    except AssertionError as er:
        await ctx.send(embed=embedAssert(er))
        return
    except:
        await ctx.send(embed=await exeErrorExcept(ctx,bot,""))
        try:
            await message.unpin()
        except:
            pass
    try:
        await game.delEmotes()
    except:
        pass
    for i in game.ids:
        inGame.remove(i)
    del gamesTortues[message.id]