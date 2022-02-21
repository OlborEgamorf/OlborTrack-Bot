import asyncio
from random import randint

import discord
from Core.Fonctions.Embeds import createEmbed
from Core.Fonctions.Unpin import pin, unpin
from Jeux.CrossServeur.ClasseTDCross import JeuTortuesDuoCross
from Jeux.Outils import joinGame
from Jeux.Paris import Pari
from Jeux.Tortues.ClassesAutres import Carte
from Core.Decorator import OTCross
from Stats.Tracker.Jeux import statsServ

emotes=["<:ot1:705766186909958185>","<:ot2:705766186989912154>","<:ot3:705766186930929685>","<:ot4:705766186947706934>","<:ot5:705766186713088042>","<:OTTbleu:860119157491892255>", "<:OTTjaune:860119157688631316>", "<:OTTrouge:860119157495693343>", "<:OTTvert:860119157331853333>", "<:OTTviolet:860119157672247326>"]
dictEmote={0:"<:otBlank:828934808200937492>","rouge":"<:OTTrouge:860119157495693343>","verte":"<:OTTvert:860119157331853333>","bleue":"<:OTTbleu:860119157491892255>","jaune":"<:OTTjaune:860119157688631316>","violette":"<:OTTviolet:860119157672247326>","last":"*dernière tortue*","multi":"*au choix*"}
dictColor={"bleue":0x00CCFF,"violette":0x993366,"rouge":0xFF0000,"verte":0x77B255,"jaune":0xFFFF00}
listeCouleurs=("rouge","jaune","bleue","verte","violette")

dictOnline=[]

@OTCross
async def startGameTortuesDuoCross(ctx,bot,game,inGame,gamesTortues):
    assert ctx.author.id not in inGame, "Terminez votre partie en cours avant de lancer ou rejoindre une partie."
    new=False
    if len(dictOnline)!=0 and dictOnline[0].playing==False:
        game=dictOnline[0]
        if ctx.guild.id in game.guilds:
            await joinGame(game.guildmess[ctx.guild.id],ctx.author,None,inGame,gamesTortues)
            return
    else:
        new=True
        game=JeuTortuesDuoCross(ctx.guild,ctx.author.id)
        dictOnline.append(game)
    game.guilds.append(ctx.guild.id)
    game.memguild[ctx.author.id]=ctx.guild.id
    game.messguild[ctx.message.id]=ctx.guild.id
    game.ids.append(ctx.author.id)
    inGame.append(ctx.author.id)
    if new:
        message=await ctx.send(embed=createEmbed("Course des tortues","**Vous avez créé une partie de OT!tortuesduo en Cross-Serveur. Vous êtes le propriétaire de la partie.**\n\nLe jeu se joue avec 4 joueurs, en 2 contre 2.\nAu début de la partie, chaque binome (aléatoire) se voit attribuer deux couleurs secrètes, envoyées en message privé, qui est celle de ses tortues.\nSauf que vous ne connaissez pas le deuxième membre de votre binome, qui doit faire gagner les mêmes tortues que vous !\nLe but est de faire atteindre l'arrivée avant tout le monde aux deux tortues, en jouant avec des cartes qui font avancer les tortues.\nLes joueurs jouent chacun leur tour. Les réactions <:ot1:705766186909958185> à <:ot5:705766186713088042> permettent de choisir sa carte.\nSi vous choisissez une carte 'au choix', cliquez ensuite sur la réaction de la tortue que vous voulez déplacer <:OTTbleu:860119157491892255> <:OTTjaune:860119157688631316> <:OTTrouge:860119157495693343> <:OTTvert:860119157331853333> <:OTTviolet:860119157672247326>.\nLes cartes 'dernière tortue' font avancer la dernière tortue.\nEn dehors de la case départ, les tortues s'empilent et avancent en même temps !\nSi plusieurs tortues arrivent en même temps, celle qui est le plus bas gagne !\nBonne chance !\n\nAppuyez sur la réaction <:otVALIDER:772766033996021761> pour rejoindre la partie et <:otANNULER:811242376625782785> pour annuler votre participation.\nLa partie se lancera automatiquement quand assez de joueurs auront rejoint, sinon au bout de 1 minute elle sera annulée.",0xad917b,ctx.invoked_with.lower(),ctx.guild))
    else:
        message=await ctx.send(embed=createEmbed("Course des tortues","**Vous avez rejoint une partie de OT!tortuesduo en Cross-Serveur. Vous n'êtes pas l'hôte de la partie.**\n\nLe jeu se joue avec 4 joueurs, en 2 contre 2.\nAu début de la partie, chaque binome (aléatoire) se voit attribuer deux couleurs secrètes, envoyées en message privé, qui est celle de ses tortues.\nSauf que vous ne connaissez pas le deuxième membre de votre binome, qui doit faire gagner les mêmes tortues que vous !\nLe but est de faire atteindre l'arrivée avant tout le monde aux deux tortues, en jouant avec des cartes qui font avancer les tortues.\nLes joueurs jouent chacun leur tour. Les réactions <:ot1:705766186909958185> à <:ot5:705766186713088042> permettent de choisir sa carte.\nSi vous choisissez une carte 'au choix', cliquez ensuite sur la réaction de la tortue que vous voulez déplacer <:OTTbleu:860119157491892255> <:OTTjaune:860119157688631316> <:OTTrouge:860119157495693343> <:OTTvert:860119157331853333> <:OTTviolet:860119157672247326>.\nLes cartes 'dernière tortue' font avancer la dernière tortue.\nEn dehors de la case départ, les tortues s'empilent et avancent en même temps !\nSi plusieurs tortues arrivent en même temps, celle qui est le plus bas gagne !\nBonne chance !\n\nAppuyez sur la réaction <:otVALIDER:772766033996021761> pour rejoindre la partie et <:otANNULER:811242376625782785> pour annuler votre participation.\nLa partie se lancera automatiquement quand assez de joueurs auront rejoint, sinon au bout de 1 minute elle sera annulée.",0xad917b,ctx.invoked_with.lower(),ctx.guild))
    gamesTortues[message.id]=game

    await message.add_reaction("<:otVALIDER:772766033996021761>")
    await message.add_reaction("<:otANNULER:811242376625782785>")

    game.messages.append(message)
    game.memmess[ctx.author.id]=message
    game.guildmess[ctx.guild.id]=message

    if len(game.ids)==4:
        game.playing=True
        await asyncio.sleep(2)

    if not new:
        return

    annonce=await bot.get_channel(878254347459366952).send("<:otVERT:868535645897912330> Partie de Tortues Duo Cross en recherche de joueurs !\n Faites OT!tortuesduocross pour rejoindre !")
    await annonce.publish()
    for i in range(60):
        if not game.playing:
            await asyncio.sleep(1)
        else:
            break
    await annonce.edit(content="~~{0}~~\nRecherche terminée.".format(annonce.content))
    
    game.playing=True
    dictOnline.remove(game)
    for i in game.memmess:
        await game.memmess[i].clear_reactions()

    while len(game.ids)>4:
        inGame.remove(game.ids[-1])
        await game.memmess[game.ids[-1]].channel.send("<:otROUGE:868535622237818910> Malheureusement, <@{0}> a rejoint alors que la partie était déjà complète. Veuillez relancer votre recherche.".format(game.ids[-1]))
        del game.ids[-1]

    if await game.checkPlayers(inGame,bot,4):
        await game.emotesUser(bot)
        for i in game.joueurs:
            team=randint(1,2)
            if len(game.equipe[team])!=2:
                game.equipe[team].append(i)
                i.setEquipe(team)
            else:
                if team==1:
                    game.equipe[2].append(i)
                    i.setEquipe(2)
                else:
                    game.equipe[1].append(i)
                    i.setEquipe(1)
        for i in game.joueurs:
            await i.user.send(embed=createEmbed("Course des tortues","Vos deux tortues à faire gagner sont : {0} {1} et {2} {3}".format(game.equipe[i.equipe][0].couleur,dictEmote[game.equipe[i.equipe][0].couleur],game.equipe[i.equipe][1].couleur,dictEmote[game.equipe[i.equipe][1].couleur]),dictColor[i.couleur],ctx.invoked_with.lower(),i.user))
        for i in game.messages:
            descip="<:otVERT:868535645897912330> La partie va commencer quand tous les messages seront chargés pour "
            for j in game.joueurs:
                if game.memmess[j.userid].id!=i.id:
                    descip+="{0} / ".format(j.titre)
                else:
                    descip+="<@{0}> / ".format(j.userid)
            await i.channel.send(descip[:-2])
        for i in game.messages:
            await i.edit(embed=discord.Embed(title="Votre couleur vous a été envoyée par MP..."))
            await pin(i)
            for j in emotes:
                await i.add_reaction(j)
            await i.add_reaction("<:otCOINS:873226814527520809>")
        messAd=await bot.get_channel(870598360296488980).send("{0} - {1} : partie OT!tortuesduo CROSS débutée\n{2} joueurs".format(ctx.guild.name,ctx.guild.id,len(game.joueurs)))
    else:
        return

    game.giveCards()
    turn=randint(0,len(game.joueurs)-1)
    game.paris=Pari(game.ids,"TortuesDuo")
    while game.playing:
        for i in game.messages:
            await i.edit(embed=game.embedGame(game.joueurs[turn],i.guild.id))
        couleur,valeur,carte=await game.play(turn,game.memmess[game.joueurs[turn].userid],bot)

        if game.mouvement(couleur,valeur):
            for i in range(len(game.plateau[9])):
                win=game.getWinner()
                if win!=None:
                    for j in game.messages:
                        await j.channel.send("La tortue {0} {1} est arrivée ! Elle gagne le droit de se reposer, et de ne plus jamais bouger... :zzz:".format(win.couleur,dictEmote[win.couleur]))
                    if win.equipe!=0:
                        game.score[win.equipe]+=1
                        if game.score[win.equipe]==2:
                            game.playing=False
                            for j in game.messages:
                                await j.edit(embed=game.embedGame(game.joueurs[turn],j.guild.id))
                                embed=game.embedWin(i.guild.id,bot)
                                await j.channel.send(embed=embed)
                                await j.clear_reactions()
                                await unpin(j)
                            for j in range(2):
                                statsServ(game,game.equipe[win.equipe][j].userid)
                                game.paris.distribParis(game.equipe[win.equipe][j].userid)
                            await game.stats(win.equipe)
                            break
        
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
