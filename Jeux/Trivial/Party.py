import asyncio
from random import choice

import discord
from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.Embeds import embedAssert
from Jeux.Trivial.Attente import attente
from Jeux.Trivial.Versus import Versus
from math import inf

emotes=["<:ot1:705766186909958185>","<:ot2:705766186989912154>","<:ot3:705766186930929685>","<:ot4:705766186947706934>"]
listeNoms=["Culture","Divertissement","Sciences","Mythologie","Sport","Géographie","Histoire","Politique","Art","Célébrités","Animaux","Véhicules","Global"]
dictCateg={9:0,10:1,11:1,12:1,13:1,14:1,15:1,16:1,17:2,18:2,19:2,20:3,21:4,22:5,23:6,24:7,25:8,26:9,27:10,28:11,29:1,30:2,31:1,32:1}

class Party(Versus):
    def __init__(self, guild,option):
        super().__init__(guild,option)
        self.max=12
        self.event=["malus","double","triple","10s","solo","ratio","theme1","themeA","speed","diff1","diffA","duo","vol",None]
        self.eventTimes={i:0 for i in self.event}
        self.eventMax={"malus":3,"double":2,"triple":1,"10s":2,"solo":2,"ratio":1,"theme1":2,"themeA":1,"speed":3,"diff1":2,"diffA":1,"duo":1,"vol":2,None:4}

    def setEvent(self):
        if len(self.event)==0:
            return "speed"
        event=choice(self.event)
        self.eventTimes[event]+=1
        if self.eventTimes[event]==self.eventMax[event]:
            self.event.remove(event)
        return event
    
    def affichageChoix(self,liste,titre):
        embed=discord.Embed(title=titre,color=0xad917b)
        embed=auteur(self.guild.id,self.guild.name,self.guild.icon,embed,"guild")
        descip=""
        for i in self.ids:
            descip+="{0} <@{1}> : **{2}**\n".format(str(self.emotes[i]),i,self.scores[i])
        embed.add_field(name="Scores", value=descip,inline=True)
        embed.add_field(name="Question n°", value=str(self.tour+1),inline=True)
        descip=""
        for i in range(len(liste)):
            descip+="{0} {1}\n".format(emotes[i],liste[i])
        embed.description=descip
        embed.set_footer(text="OT!trivial{0}".format(self.option))
        return embed
    
    def affichageEvent(self,event,users):
        dictDescip={"malus":"Les mauvaises réponses font **perdre des points** !","double":"Chaque bonne réponse vaut **4 points** !","triple":"Chaque bonne réponse vaut **6 points** !","10s":"Vous avez seulement **10 secondes** pour répondre. Ne pas répondre fait perdre **1 point** !","solo":"<@{0[0]}> est le seul à répondre ! Si il répond juste il gagne **4 points**, sinon tout le monde récupére **2 points** et lui en **perd 1** !","ratio":"Plus il y a de gens qui répondent juste, moins la question a de valeur !","theme1":"<@{0[0]}> a la chance de choisir le thème de la prochaine question !","themeA":"Tout le monde peut voter pour le choix du prochain thème !","speed":"Le premier qui répond juste gagne **3 points** ! Attention : répondre faux fera perdre **1 point** !","diff1":"<@{0[0]}> a la chance de choisir la difficulté de la prochaine question !","diffA":"Tout le monde peut voter pour le choix de la difficulté de la prochaine question !","duo":"<@{0[0]}> et <@{0[1]}> sont les seuls à répondre ! Ils doivent tout les deux répondre juste pour gagner chacun **3 points**. En cas d'échec, ils perdront **1 point** et tout le monde en gagnera **2** !","vol":"<@{0[0]}> est le seul à répondre ! Si il répond juste, il choisiera un joueur à qu'il volera **3 points** !","speedfinal":"{0} a (ont) atteint les 12 points et est (sont) finaliste(s) ! Seul lui (eux) peu(ven)t répondre, c'est une question de rapidité et en cas d'échec, il(s) retombe(nt) à 10 points !"}
        dictTitre={"malus":"question malus","double":"points doubles","triple":"points TRIPLES","10s":"temps réduit","solo":"question solo","ratio":"points rationalisés","theme1":"choix de thème","themeA":"vote de thème","speed":"rapidité","diff1":"choix de difficulté","diffA":"vote de difficulté","duo":"question duo","vol":"vol de points","speedfinal":"finale"}
        embedT=discord.Embed(title="Évènement : {0} !".format(dictTitre[event]), description=dictDescip[event].format(users), color=0xad917b)
        embedT=auteur(self.guild.id,self.guild.name,self.guild.icon,embedT,"guild")
        embedT.set_footer(text="OT!trivialparty")
        return embedT
    
    def embedResults(self,winner):
        descip=""
        for i in self.scores:
            descip+="{0} <@{1}> : {2}\n".format(str(self.emotes[i]),i,self.scores[i])
        embedT=discord.Embed(title="Victoire de {0}".format(winner.name), description=descip, color=0xf2eb16)
        embedT.set_footer(text="OT!trivialparty")
        embedT=auteur(winner.id,winner.name,winner.avatar,embedT,"user")
        embedT.add_field(name="<:otCOINS:873226814527520809> gagnés par {0}".format(winner.name),value="{0} <:otCOINS:873226814527520809>".format(len(self.ids)*25+sum(self.mises.values())))
        return embedT

    def createEmbed(self,results,event):
        dictTitre={"malus":"Question malus","double":"Points x2","triple":"Points x3","10s":"Temps réduit","solo":"Question solo","ratio":"Points rationalisés","theme1":"Choix de thème","themeA":"Vote de thème","speed":"Rapidité","diff1":"Choix de difficulté","diffA":"Vote de difficulté","duo":"Question duo","vol":"Vol de points","speedfinal":"FINALE",None:"Aucun"}
        embed=super().createEmbed(results)
        embed.add_field(name="Évènement",value=dictTitre[event])
        return embed


async def trivialParty(ctx,bot,inGame,gamesTrivial):
    try:
        assert ctx.author.id not in inGame, "Terminez votre question en cours avant de lancer ou rejoindre une partie."
        game=Party(ctx.guild,"party")
        message=await game.startGame(ctx,bot,inGame,gamesTrivial)
        if message==False:
            return
        messAd=await bot.get_channel(870598360296488980).send("{0} - {1} : partie OT!trivialparty débutée\n{2} joueurs".format(ctx.guild.name,ctx.guild.id,len(game.joueurs)))
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
                descip=""
                for i in liste:
                    descip+="<@{0}> ".format(i)
                await message.edit(embed=game.affichageEvent(event,descip))
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
                await message.edit(embed=game.affichageEvent(event,user))
                await asyncio.sleep(6)
                await message.edit(embed=game.affichageChoix(liste,"Choix du thème !"))
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
                await message.edit(embed=game.affichageEvent(event,user))
                await asyncio.sleep(6)
                embed=game.affichageChoix(liste,"Choix de la difficulté !")
                embed.add_field(name="Catégorie",value=listeNoms[dictCateg[game.arg]],inline=True)
                await message.edit(embed=embed)
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
                await message.edit(embed=game.affichageEvent(event,user))
                await asyncio.sleep(6)

            game.newQuestion()
            embedT=game.createEmbed(False,event)
            await message.edit(embed=embedT)
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
                            liste.append(choix.name)
                            listeID.append(choix.id)
                            listeJoueurs.remove(choix)
                        await message.edit(embed=game.affichageChoix(liste,"Vous avez eu juste ! Choississez un joueur pour lui voler 3 points."))
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

            embedT=game.createEmbed(True,event)
            embedT.description=game.affichageWin()
            embedT.colour=0x47b03c
            await message.edit(embed=embedT)
            if game.maxTour():
                maxi,maxiJoueur=-inf,None
                for i in game.joueurs:
                    if game.scores[i.id]>maxi:
                        maxi,maxiJoueur=game.scores[i.id],i
                end=[maxiJoueur]
            if len(end)!=0:
                await message.clear_reactions()
                await message.channel.send(embed=game.embedResults(end[0]))
                await message.unpin()
                game.playing=False
                game.stats(end[0],"TrivialParty")
            
            game.tour+=1
            await asyncio.sleep(7)
        await game.endGame(message,inGame,gamesTrivial)
    except AssertionError as er:
        await ctx.send(embed=embedAssert(er))
    except:
        await game.error(ctx,bot,message,inGame,gamesTrivial)
    if "messAd" in locals():
        await messAd.delete()