import asyncio

from Core.Fonctions.Embeds import embedAssert
from Jeux.CrossServeur.ClasseTrivialPartyCross import PartyCross
from Jeux.Outils import joinGame
from Jeux.Trivial.Attente import attente
from numpy.random.mtrand import choice
from Stats.Tracker.Jeux import statsServ
from Core.Fonctions.Unpin import unpin
from math import inf

dictOnline=[]
listeNoms=["Culture","Divertissement","Sciences","Mythologie","Sport","Géographie","Histoire","Politique","Art","Célébrités","Animaux","Véhicules","Global"]
dictCateg={9:0,10:1,11:1,12:1,13:1,14:1,15:1,16:1,17:2,18:2,19:2,20:3,21:4,22:5,23:6,24:7,25:8,26:9,27:10,28:11,29:1,30:2,31:1,32:1}

async def trivialPartyCross(ctx,bot,inGame,gamesTrivial):
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
            game=PartyCross(ctx.guild,"party")
            game.invoke=ctx.author.id
            dictOnline.append(game)

        message=await game.startGame(ctx,bot,inGame,gamesTrivial,new,dictOnline)
        if message==False:
            return
        messAd=await bot.get_channel(870598360296488980).send("{0} - {1} : partie OT!trivialparty CROSS débutée\n{2} joueurs".format(ctx.guild.name,ctx.guild.id,len(game.joueurs)))
        if len(game.joueurs)<4:
            game.event.remove("duo")
        while game.playing:
            dictNomsVal={"culture":9,"divertissement":choice([10,11,12,13,14,15,16,29,31,32]),"sciences":choice([17,18,19,30]),"mythologie":20,"sport":21,"géographie":22,"histoire":23,"politique":24,"art":25,"célébrités":26,"animaux":27,"véhicules":28,"livres":10,"films":11,"musique":12,"anime":31,"manga":31}
            liste=[]
            for i in game.scores:
                if game.scores[i]>=game.max:
                    liste.append(i)
            if len(liste)!=0:
                event="speedfinal"
                game.reponses={i:None for i in liste}
                for i in game.messages:
                    descip=""
                    for j in range(len(liste)):
                        if game.memguild[liste[j]]==i.guild.id:
                            descip+="<@{0}> ".format(liste[j])
                        else:
                            descip+="{0} ".format(game.titres[liste[j]])
                    await i.edit(embed=game.affichageEvent(event,descip,i.guild))
                await asyncio.sleep(5)
            elif game.tour<3:
                event=None
            else:
                event=game.setEvent()

            if event in ("theme1","themeA"):
                liste=[]
                listeChoix={i:0 for i in range(4)}
                listeThemes=["culture","divertissement","sciences","mythologie","sport","géographie","histoire","politique","art","célébrités","animaux","véhicules"]
                for i in range(4):
                    liste.append(choice(listeThemes))
                    listeThemes.remove(liste[i])
                if event=="theme1":
                    user=[choice(game.ids)]
                    game.reponses={user[0]:None}
                else:
                    game.reponses={i:None for i in game.ids}
                    user=[]
                for i in game.messages:
                    newUser=[]
                    for j in range(len(user)):
                        if game.memguild[user[j]]==i.guild.id:
                            newUser.append("<@{0}>".format(user[j]))
                        else:
                            newUser.append(game.titres[user[j]])
                    await i.edit(embed=game.affichageEvent(event,newUser,i.guild))
                await asyncio.sleep(6)
                for i in game.messages:
                    await i.edit(embed=game.affichageChoix(liste,"Choix du thème !",i.guild))
                await attente(game,12,None)
                for i in game.reponses:
                    if game.reponses[i]!=None:
                        listeChoix[game.reponses[i]]+=1
                arg=dictNomsVal[liste[max(listeChoix,key=lambda x:listeChoix[x])]]
                game.arg=arg
                game.categ=dictCateg[arg]
            else:
                game.setCateg(None)

            if event in ("diff1","diffA"):
                liste=["Facile","Moyen","Difficile","Aléatoire"]
                dictDiffV={"Facile":"easy","Moyen":"medium","Difficile":"hard","Aléatoire":choice(["easy","medium","hard"])}
                listeChoix={i:0 for i in range(4)}
                if event=="diff1":
                    user=[choice(game.ids)]
                    game.reponses={user[0]:None}
                else:
                    game.reponses={i:None for i in game.ids}
                    user=[]
                for i in game.messages:
                    newUser=[]
                    for j in range(len(user)):
                        if game.memguild[user[j]]==i.guild.id:
                            newUser.append("<@{0}>".format(user[j]))
                        else:
                            newUser.append(game.titres[user[j]])
                    await i.edit(embed=game.affichageEvent(event,newUser,i.guild))
                await asyncio.sleep(6)
                for i in game.messages:
                    embed=game.affichageChoix(liste,"Choix de la difficulté !",i.guild)
                    embed.add_field(name="Catégorie",value=listeNoms[dictCateg[game.arg]],inline=True)
                    await i.edit(embed=embed)
                await attente(game,12,None)
                for i in game.reponses:
                    if game.reponses[i]!=None:
                        listeChoix[game.reponses[i]]+=1
                game.diff=dictDiffV[liste[max(listeChoix,key=lambda x:listeChoix[x])]]
            else:
                game.setDiff()

            user=[]
            if event in ("solo","vol"):
                user=[choice(game.ids)]
                game.reponses={user[0]:None}
            elif event=="duo":
                user=[]
                listeJoueurs=game.joueurs.copy()
                for i in range(2):
                    choix=choice(listeJoueurs)
                    user.append(choix)
                    listeJoueurs.remove(user[i])
                game.reponses={i.id:None for i in user}
            elif event=="speedfinal":
                pass
            else: 
                game.reponses={i:None for i in game.ids}

            if event not in (None,"theme1","themeA","diff1","diffA","speedfinal"):
                for i in game.messages:
                    newUser=[]
                    for j in range(len(user)):
                        if game.memguild[user[j]]==i.guild.id:
                            newUser.append("<@{0}>".format(user[j]))
                        else:
                            newUser.append(game.titres[user[j]])
                    await i.edit(embed=game.affichageEvent(event,newUser,i.guild))
                await asyncio.sleep(6)

            game.newQuestion()
            for i in game.messages:
                embedT=game.createEmbed(False,event,i.guild)
                await i.edit(embed=embedT)
            if event=="10s":
                await attente(game,20,event)
            else:
                await attente(game,20,event)

            end=[]
            if event=="malus":
                for i in game.joueurs:
                    if game.reponses[i.id]==game.vrai-1:
                        game.scores[i.id]+=2
                    else:
                        game.scores[i.id]-=1
            elif event=="double":
                for i in game.joueurs:
                    if game.reponses[i.id]==game.vrai-1:
                        game.scores[i.id]+=4
            elif event=="triple":
                for i in game.joueurs:
                    if game.reponses[i.id]==game.vrai-1:
                        game.scores[i.id]+=6
            elif event=="10s":
                for i in game.joueurs:
                    if game.reponses[i.id]==game.vrai-1:
                        game.scores[i.id]+=2
                    elif game.reponses[i.id]==None:
                        game.scores[i.id]-=1
            elif event=="solo":
                for i in game.reponses:
                    if game.reponses[i]==game.vrai-1:
                        game.scores[i]+=4
                    else:
                        game.scores[i]-=3
                        for j in game.joueurs:
                            game.scores[j.id]+=2
            elif event=="ratio":
                count=0
                for i in game.joueurs:
                    if game.reponses[i.id]==game.vrai-1:
                        count+=1
                for i in game.joueurs:
                    if game.reponses[i.id]==game.vrai-1:
                        if count==1:
                            game.scores[i.id]+=5
                        elif count/len(game.joueurs)<0.25:
                            game.scores[i.id]+=3
                        elif count/len(game.joueurs)<0.5:
                            game.scores[i.id]+=2
                        else:
                            game.scores[i.id]+=1
            elif event=="speed":
                for i in game.joueurs:
                    if game.reponses[i.id]==game.vrai-1:
                        game.scores[i.id]+=3
                    elif game.reponses[i.id]==None:
                        pass
                    else:
                        game.scores[i.id]-=1
            elif event=="speedfinal":
                for i in game.reponses:
                    if game.reponses[i]==game.vrai-1:
                        game.scores[i]=100
                        for j in game.joueurs:
                            if j.id==i:
                                end.append(j)
                                break
                    else:
                        game.scores[i]=10
            elif event=="duo":
                count=0
                for i in game.reponses:
                    if game.reponses[i]==game.vrai-1:
                        count+=1
                for i in game.reponses:
                    if count==2:
                        game.scores[i]+=3
                    else:
                        game.scores[i]-=3
                        for j in game.joueurs:
                            game.scores[j.id]+=2
            elif event=="vol":
                for i in game.reponses:
                    if game.reponses[i]==game.vrai-1:
                        temp=game.reponses.copy()
                        liste=[]
                        listeID=[]
                        listeChoix={i:0 for i in range(4)}
                        listeJoueurs=game.joueurs.copy()
                        for j in range(4 if len(game.joueurs)>4 else len(game.joueurs)):
                            choix=choice(listeJoueurs)
                            liste.append(choix)
                            listeID.append(choix.id)
                            listeJoueurs.remove(choix)
                        for j in game.messages:
                            newListe=[]
                            for h in liste:
                                if game.memguild[i.id]==game.memguild[h.id]:
                                    newListe.append(h.name)
                                else:
                                    newListe.append(game.titres[h.id])
                            await i.edit(embed=game.affichageChoix(newListe,"Vous avez eu juste ! Choississez un joueur pour lui voler 3 points.",i.guild))
                        game.reponses={i:None}
                        await attente(game,12,None)
                        for j in game.reponses:
                            if game.reponses[j]!=None:
                                listeChoix[game.reponses[j]]+=1
                        game.scores[listeID[max(listeChoix,key=lambda x:listeChoix[x])]]-=3
                        game.scores[i]+=3
                        game.reponses=temp
            else:
                for i in game.joueurs:
                    if game.reponses[i.id]==game.vrai-1:
                        game.scores[i.id]+=2
            
            for i in game.messages:
                embedT=game.createEmbed(True,event,i.guild)
                embedT.description=game.affichageWin()
                embedT.colour=0x47b03c
                await i.edit(embed=embedT)
            if game.maxTour():
                maxi,maxiJoueur=-inf,None
                for i in game.joueurs:
                    if game.scores[i.id]>maxi:
                        maxi,maxiJoueur=game.scores[i.id],i
                end=[maxiJoueur]
            if len(end)!=0:
                for i in game.messages:
                    await i.clear_reactions()
                    await i.channel.send(embed=game.embedResults(end[0],i.guild))
                    await unpin(i)
                game.playing=False
                game.stats(end[0],"TrivialParty")
                statsServ(game,end[0].id)
            
            game.tour+=1
            await asyncio.sleep(7)
        await game.endGame(message,inGame,gamesTrivial)
    except AssertionError as er:
        await ctx.send(embed=embedAssert(er))
    except:
        await game.error(ctx,bot,message,inGame,gamesTrivial)
    if "messAd" in locals():
        await messAd.delete()
