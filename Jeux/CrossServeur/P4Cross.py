

import asyncio
from random import randint

from Core.Fonctions.Embeds import createEmbed, embedAssert, exeErrorExcept
from Jeux.CrossServeur.ClasseP4Cross import JeuP4Cross
from Jeux.Outils import joinGame
from Stats.Tracker.Jeux import exeStatsJeux, statsServ
from Titres.Outils import gainCoins
from Core.Fonctions.Unpin import pin, unpin
from Stats.SQL.Execution import exeJeuxSQL
from Stats.SQL.ConnectSQL import connectSQL
from Jeux.Paris import Pari

emotes=["<:ot1:705766186909958185>","<:ot2:705766186989912154>","<:ot3:705766186930929685>","<:ot4:705766186947706934>","<:ot5:705766186713088042>","<:ot6:705766187182850148>","<:ot7:705766187115741246>"]
dictCo={705766186909958185:0,705766186989912154:1,705766186930929685:2,705766186947706934:3,705766186713088042:4,705766187182850148:5,705766187115741246:6}
dictOnline=[]


async def startGameP4Cross(ctx,bot,inGame,gamesP4):
    try:
        assert ctx.author.id not in inGame, "Terminez votre partie en cours avant de lancer ou rejoindre une partie."
        new=False
        if len(dictOnline)!=0 and dictOnline[0].playing==False:
            game=dictOnline[0]
            if ctx.guild.id in game.guilds:
                await joinGame(game.guildmess[ctx.guild.id],ctx.author,None,inGame,gamesP4)
                return
        else:
            new=True
            game=JeuP4Cross(ctx.guild,ctx.author.id)
            dictOnline.append(game)
        game.guilds.append(ctx.guild.id)
        game.memguild[ctx.author.id]=ctx.guild.id
        game.messguild[ctx.message.id]=ctx.guild.id
        game.ids.append(ctx.author.id)
        inGame.append(ctx.author.id)
        if new:
            message=await ctx.send(embed=createEmbed("Puissance 4","**Vous avez créé une partie de OT!p4 en Cross-Serveur. Vous êtes le propriétaire de la partie.**\n\nAppuyez sur la réaction <:otVALIDER:772766033996021761> pour défier <@{0}> au Puissance 4.\nL'objectif est d'aligner 4 jetons de votre couleur dans n'importe quel sens (horizontallement, verticalement ou diagonalement) en premier !\nLes réactions allant de <:ot1:705766186909958185> à <:ot7:705766187115741246> représentent les colonnes où vous pouvez placer votre jeton. Cliquez sur l'une d'entre elles et le jeton apparaîtra !\nLa personne qui a demandé la partie peut cliquer sur <:otANNULER:811242376625782785> pour se retirer de la partie.".format(ctx.author.id),0xad917b,ctx.invoked_with.lower(),ctx.guild))
        else:
            message=await ctx.send(embed=createEmbed("Puissance 4","**Vous avez rejoint une partie de OT!tortues en Cross-Serveur. Vous n'êtes pas l'hôte de la partie.**\n\nAppuyez sur la réaction <:otVALIDER:772766033996021761> pour défier <@{0}> au Puissance 4.\nL'objectif est d'aligner 4 jetons de votre couleur dans n'importe quel sens (horizontallement, verticalement ou diagonalement) en premier !\nLes réactions allant de <:ot1:705766186909958185> à <:ot7:705766187115741246> représentent les colonnes où vous pouvez placer votre jeton. Cliquez sur l'une d'entre elles et le jeton apparaîtra !\nLa personne qui a demandé la partie peut cliquer sur <:otANNULER:811242376625782785> pour se retirer de la partie.".format(ctx.author.id),0xad917b,ctx.invoked_with.lower(),ctx.guild))
            pass
        gamesP4[message.id]=game

        await message.add_reaction("<:otVALIDER:772766033996021761>")
        await message.add_reaction("<:otANNULER:811242376625782785>")

        game.messages.append(message)
        game.memmess[ctx.author.id]=message
        game.guildmess[ctx.guild.id]=message

        if len(game.ids)==2:
            game.playing=True
            await asyncio.sleep(2)

        if not new:
            return
        
        annonce=await bot.get_channel(878254347459366952).send("<:otVERT:868535645897912330> Partie de P4 Cross en recherche de joueurs !\n Faites OT!p4cross pour rejoindre !")
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
        if len(game.ids)<2:
            for i in game.memmess:
                await game.memmess[i].edit(embed=createEmbed("Puissance 4","Une minute s'est écoulée et personne n'a répondu à l'invitation.",0xad917b,ctx.invoked_with.lower(),ctx.guild))
            for i in game.ids:
                inGame.remove(i)
            return
        
        while len(game.ids)>2:
            inGame.remove(game.ids[-1])
            await game.memmess[game.ids[-1]].channel.send("<:otROUGE:868535622237818910> Malheureusement, <@{0}> a rejoint alors que la partie était déjà complète. Veuillez relancer votre recherche.".format(game.ids[-1]))
            del game.ids[-1]

        for i in game.memguild:
            if game.memguild[i] not in game.guilds:
                game.guilds.append(game.memguild[i])
        for i in game.memmess:
            if game.memmess[i] not in game.messages:
                game.messages.append(game.memmess[i])
        for i in game.ids:
            game.addPlayer(bot.get_user(i))

        for i in game.messages:
            descip="<:otVERT:868535645897912330> La partie commence pour "
            for j in game.joueurs:
                if game.memmess[j.id].id!=i.id:
                    descip+="{0} / ".format(j.titre)
                else:
                    descip+="<@{0}> / ".format(j.id)
            await i.channel.send(descip[:-2])

            await pin(i)

            for j in emotes:
                await i.add_reaction(j)
            await i.add_reaction("<:otCOINS:873226814527520809>")
            
        messAd=await bot.get_channel(870598360296488980).send("{0} - {1} : partie OT!p4 CROSS débutée\n2 joueurs".format(ctx.guild.name,ctx.guild.id))

        turn=randint(0,1)
        game.paris=Pari(game.ids,"P4")
        while game.playing:
            for i in game.messages:
                await i.edit(embed=game.createEmbedP4(game.joueurs[turn],i.guild.id))
            add=await game.play(turn,game.memmess[game.joueurs[turn].id],bot)
            if add[0]==True:
                if game.tab.checkTab(add[1],add[2],turn+1)==True:
                    if turn==0: lose=1
                    else: lose=0

                    connexionOT,curseurOT=connectSQL("OT","Guild","Guild",None,None)
                    exeJeuxSQL(game.joueurs[turn].id,game.joueurs[lose].id,"W","OT",curseurOT,2,"P4",game.tours)
                    exeJeuxSQL(game.joueurs[lose].id,game.joueurs[turn].id,"L","OT",curseurOT,-1,"P4",game.tours)
                    connexionOT.commit()

                    statsServ(game,game.joueurs[turn].id)
                    gainCoins(game.joueurs[turn].id,50+sum(game.paris.mises.values()))
                    game.paris.distribParis(game.joueurs[turn].id)
                    
                    for i in game.messages:
                        await i.clear_reactions()
                        await i.edit(embed=game.createEmbedP4(game.joueurs[turn],i.guild.id))
                        await i.channel.send(embed=game.embedWin(turn,False,i.guild.id))
                    
                    game.playing=False
                else:
                    if game.tab.checkNul()==True:
                        for i in game.messages:
                            await i.clear_reactions()
                            await i.edit(embed=game.createEmbedP4(game.joueurs[turn],i.guild.id))
                            await i.channel.send(embed=game.embedWin(turn,True,i.guild.id))
                        game.playing=False
                    else:
                        game.tours+=1      
                        for i in range(7):
                            if game.tab.tableau[0][i]!=0:
                                for j in game.messages:
                                    await j.clear_reaction(emotes[i])

            game.fermeture()
            turn+=1
            if turn==len(game.joueurs):
                turn=0

        if "messAd" in locals():
            await messAd.delete()
    except AssertionError as er:
        for i in game.messages:
            await i.channel.send(embed=embedAssert(er))
        return
    except:
        for i in game.messages:
            await i.channel.send(embed=await exeErrorExcept(ctx,bot,""))
            await unpin(i)
    try:
        await game.delEmotes()
    except:
        pass
    for i in game.ids:
        inGame.remove(i)
    for i in game.messages:
        del gamesP4[i.id]
