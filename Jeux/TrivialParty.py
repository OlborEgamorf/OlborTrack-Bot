import asyncio
from math import inf
from random import choice, randint

from Core.Fonctions.Embeds import createEmbed

from Jeux.Outils.AttenteTrivial import attente
from Jeux.TrivialVersus import JeuTrivialVersus

emotes=["<:ot1:705766186909958185>","<:ot2:705766186989912154>","<:ot3:705766186930929685>","<:ot4:705766186947706934>"]
listeNoms=["Culture","Divertissement","Sciences","Mythologie","Sport","Géographie","Histoire","Politique","Art","Célébrités","Animaux","Véhicules","Global"]
dictCateg={9:0,10:1,11:1,12:1,13:1,14:1,15:1,16:1,17:2,18:2,19:2,20:3,21:4,22:5,23:6,24:7,25:8,26:9,27:10,28:11,29:1,30:2,31:1,32:1}

class JeuTrivialParty(JeuTrivialVersus):
    def __init__(self, message,user,cross):
        super().__init__(message,user,"Party",cross)
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
    
    def affichageChoix(self,liste,titre,guild):
        descip=""
        for i in self.joueurs:
            if i.emote!=None:
                emote=i.emote
            else:
                emote=""
            if i.guild==guild.id:
                descip+="{0} <@{1}> : **{2}**\n".format(emote,i,i.score)
            else:
                descip+="{0} {1} : **{2}**\n".format(emote,i.titre,i.score)
        scores=""
        for i in range(len(liste)):
            scores+="{0} {1}\n".format(emotes[i],liste[i])
        embed=createEmbed(titre,descip,0xad917b,"trivialparty",guild)
        embed.add_field(name="Scores", value=scores,inline=True)
        embed.add_field(name="Question n°", value=str(self.tour+1),inline=True)
        return embed
    
    def affichageEvent(self,event,users,guild):
        dictDescip={"malus":"Les mauvaises réponses font **perdre des points** !","double":"Chaque bonne réponse vaut **4 points** !","triple":"Chaque bonne réponse vaut **6 points** !","10s":"Vous avez seulement **10 secondes** pour répondre. Ne pas répondre fait perdre **1 point** !","solo":"<@{0[0]}> est le seul à répondre ! Si il répond juste il gagne **4 points**, sinon tout le monde récupére **2 points** et lui en **perd 1** !","ratio":"Plus il y a de gens qui répondent juste, moins la question a de valeur !","theme1":"<@{0[0]}> a la chance de choisir le thème de la prochaine question !","themeA":"Tout le monde peut voter pour le choix du prochain thème !","speed":"Le premier qui répond juste gagne **3 points** ! Attention : répondre faux fera perdre **1 point** !","diff1":"<@{0[0]}> a la chance de choisir la difficulté de la prochaine question !","diffA":"Tout le monde peut voter pour le choix de la difficulté de la prochaine question !","duo":"<@{0[0]}> et <@{0[1]}> sont les seuls à répondre ! Ils doivent tout les deux répondre juste pour gagner chacun **3 points**. En cas d'échec, ils perdront **1 point** et tout le monde en gagnera **2** !","vol":"<@{0[0]}> est le seul à répondre ! Si il répond juste, il choisiera un joueur à qu'il volera **3 points** !","speedfinal":"{0} a (ont) atteint les 12 points et est (sont) finaliste(s) ! Seul lui (eux) peu(ven)t répondre, c'est une question de rapidité et en cas d'échec, il(s) retombe(nt) à 10 points !"}
        dictTitre={"malus":"question malus","double":"points doubles","triple":"points TRIPLES","10s":"temps réduit","solo":"question solo","ratio":"points rationalisés","theme1":"choix de thème","themeA":"vote de thème","speed":"rapidité","diff1":"choix de difficulté","diffA":"vote de difficulté","duo":"question duo","vol":"vol de points","speedfinal":"finale"}
        return createEmbed("Évènement : {0} !".format(dictTitre[event]),dictDescip[event].format(users),0xad917b,"trivialparty",guild)

    def embedGame(self,results,event,guild):
        dictTitre={"malus":"Question malus","double":"Points x2","triple":"Points x3","10s":"Temps réduit","solo":"Question solo","ratio":"Points rationalisés","theme1":"Choix de thème","themeA":"Vote de thème","speed":"Rapidité","diff1":"Choix de difficulté","diffA":"Vote de difficulté","duo":"Question duo","vol":"Vol de points","speedfinal":"FINALE",None:"Aucun"}
        embed=super().embedGame(results,guild)
        embed.add_field(name="Évènement",value=dictTitre[event])
        return embed

    def fermeture(self):
        for i in self.joueurs:
            if i.score>5:
                self.paris.ouvert=False 

    async def boucle(self,bot):
        while self.playing:
            dictNomsVal={"culture":9,"divertissement":choice([10,11,12,13,14,15,16,29,31,32]),"sciences":choice([17,18,19,30]),"mythologie":20,"sport":21,"géographie":22,"histoire":23,"politique":24,"art":25,"célébrités":26,"animaux":27,"véhicules":28,"livres":10,"films":11,"musique":12,"anime":31,"manga":31}
            liste=[]
            for i in self.joueurs:
                if i.score>=self.max:
                    liste.append(i.id)
            if len(liste)!=0:
                event="speedfinal"
                self.reponses={i:None for i in liste}
                descip=""
                for i in liste:
                    descip+="<@{0}> ".format(i)
                for mess in self.messages:
                    await mess.edit(embed=self.affichageEvent(event,descip,mess.guild))
                await asyncio.sleep(5)
            elif self.tour<3:
                event=None
            else:
                event=self.setEvent()

            if event in ("theme1","themeA"):
                liste=[]
                listeChoix={i:0 for i in range(4)}
                listeThemes=["culture","divertissement","sciences","mythologie","sport","géographie","histoire","politique","art","célébrités","animaux","véhicules"]
                for i in range(4):
                    liste.append(choice(listeThemes))
                    listeThemes.remove(liste[i])
                if event=="theme1":
                    user=[choice(self.ids)]
                    self.reponses={user[0]:None}
                else:
                    self.reponses={i:None for i in self.ids}
                    user=[]
                for mess in self.messages:
                    await mess.edit(embed=self.affichageEvent(event,user,mess.guild))
                await asyncio.sleep(6)
                for mess in self.messages:
                    await mess.edit(embed=self.affichageChoix(liste,"Choix du thème !",mess.guild))
                await attente(self,12,None)
                for i in self.reponses:
                    if self.reponses[i]!=None:
                        listeChoix[self.reponses[i]]+=1
                arg=dictNomsVal[liste[max(listeChoix,key=lambda x:listeChoix[x])]]
                self.arg=arg
                self.categ=dictCateg[arg]
            else:
                self.setCateg()

            if event in ("diff1","diffA"):
                liste=["Facile","Moyen","Difficile","Aléatoire"]
                dictDiffV={"Facile":"easy","Moyen":"medium","Difficile":"hard","Aléatoire":choice(["easy","medium","hard"])}
                listeChoix={i:0 for i in range(4)}
                if event=="diff1":
                    user=[choice(self.ids)]
                    self.reponses={user[0]:None}
                else:
                    self.reponses={i:None for i in self.ids}
                    user=[]
                for mess in self.messages:
                    await mess.edit(embed=self.affichageEvent(event,user,mess.guild))
                await asyncio.sleep(6)
                for mess in self.messages:
                    embed=self.affichageChoix(liste,"Choix de la difficulté !",mess.guild)
                    embed.add_field(name="Catégorie",value=listeNoms[dictCateg[self.arg]],inline=True)
                    await mess.edit(embed=embed)
                await attente(self,12,None)
                for i in self.reponses:
                    if self.reponses[i]!=None:
                        listeChoix[self.reponses[i]]+=1
                self.diff=dictDiffV[liste[max(listeChoix,key=lambda x:listeChoix[x])]]
            else:
                self.setDiff()

            user=[]
            if event in ("solo","vol"):
                user=[choice(self.ids)]
                self.reponses={user[0]:None}
            elif event=="duo":
                user=[]
                listeJoueurs=self.joueurs.copy()
                for i in range(2):
                    choix=choice(listeJoueurs)
                    user.append(choix)
                    listeJoueurs.remove(user[i])
                self.reponses={i.id:None for i in user}
            elif event=="speedfinal":
                pass
            else: 
                self.reponses={i:None for i in self.ids}

            if event not in (None,"theme1","themeA","diff1","diffA","speedfinal"):
                for mess in self.messages:
                    await mess.edit(embed=self.affichageEvent(event,user,mess.guild))
                await asyncio.sleep(6)

            self.newQuestion()
            embedT=self.createEmbed(False,event)
            for mess in self.messages:
                await mess.edit(embed=embedT)
            if event=="10s":
                await attente(self,20,event)
            else:
                await attente(self,20,event)

            end=[]
            if event=="malus":
                for i in self.joueurs:
                    if self.reponses[i.id]==self.vrai-1:
                        i.score+=2
                    else:
                        i.score-=1
            elif event=="double":
                for i in self.joueurs:
                    if self.reponses[i.id]==self.vrai-1:
                        i.score+=4
            elif event=="triple":
                for i in self.joueurs:
                    if self.reponses[i.id]==self.vrai-1:
                        i.score+=6
            elif event=="10s":
                for i in self.joueurs:
                    if self.reponses[i.id]==self.vrai-1:
                        i.score+=2
                    elif self.reponses[i.id]==None:
                        i.score-=1
            elif event=="solo":
                for i in self.joueurs:
                    if i.id in self.reponses:
                        if self.reponses[i.id]==self.vrai-1:
                            i.score+=4
                        else:
                            i.score-=3
                            for j in self.joueurs:
                                j.score+=2
            elif event=="ratio":
                count=0
                for i in self.joueurs:
                    if self.reponses[i.id]==self.vrai-1:
                        count+=1
                for i in self.joueurs:
                    if self.reponses[i.id]==self.vrai-1:
                        if count==1:
                            i.score+=5
                        elif count/len(self.joueurs)<0.25:
                            i.score+=3
                        elif count/len(self.joueurs)<0.5:
                            i.score+=2
                        else:
                            i.score+=1
            elif event=="speed":
                for i in self.joueurs:
                    if self.reponses[i.id]==self.vrai-1:
                        i.score+=3
                    elif self.reponses[i.id]==None:
                        pass
                    else:
                        i.score-=1
            elif event=="speedfinal":
                for i in self.joueurs:
                    if i.id in self.reponses:
                        if self.reponses[i.id]==self.vrai-1:
                            i.score=100
                            end.append(i)
                        else:
                            i.score=10
            elif event=="duo":
                count=0
                for i in self.joueurs:
                    if i.id in self.reponses:
                        if self.reponses[i.id]==self.vrai-1:
                            count+=1
                for i in self.joueurs:
                    if count==2:
                        if i.id in self.reponses: 
                            i.score+=3
                    else:
                        if i.id in self.reponses:
                            i.score-=3
                        else:
                            i.score+=2
            elif event=="vol":
                for i in self.joueurs:
                    if i.id in self.reponses:
                        if self.reponses[i.id]==self.vrai-1:
                            liste=[]
                            listeJoueur=[]
                            listePossible=self.joueurs.copy()
                            listePossible.remove(i)
                            dictChoix={}
                            for j in range(4 if len(listePossible)>4 else len(listePossible)):
                                choix=choice(listePossible)
                                liste.append(choix.name)
                                listeJoueur.append(choix)
                                listePossible.remove(choix)
                                dictChoix[j]=0
                            for mess in self.messages:
                                await mess.edit(embed=self.affichageChoix(liste,"Vous avez eu juste ! Choisissez un joueur pour lui voler 3 points.",mess.guild))
                            self.reponses={i.id:None}
                            await attente(self,12,None)
                            for j in self.reponses:
                                if self.reponses[j] in dictChoix:
                                    vol=self.reponses[j]
                                else:
                                    vol=randint(0,len(listeJoueur)-1)
                            listeJoueur[vol].score-=3
                            i.score+=3
            else:
                for i in self.joueurs:
                    if self.reponses[i.id]==self.vrai-1:
                        i.score+=2

            for mess in self.messages:
                embedT=self.createEmbed(True,event)
                embedT.description=self.affichageWin()
                embedT.colour=0x47b03c
                await mess.edit(embed=embedT)
            if self.maxTour():
                maxi,maxiJoueur=-inf,None
                for i in self.joueurs:
                    if i.score>maxi:
                        maxi,maxiJoueur=i.score,i
                end=[maxiJoueur]
            if len(end)!=0:
                winner=end[0]
                await self.stats(winner.id,winner.guild)
                for mess in self.messages:
                    await mess.edit(view=None)
                    await mess.reply(embed=self.embedEnd(winner,mess.guild))
                self.playing=False
            self.fermeture()
            self.tour+=1
            await asyncio.sleep(7)
