from random import choice, randint

from Core.Fonctions.Embeds import createEmbed
from Stats.SQL.ConnectSQL import connectSQL
from Stats.SQL.Execution import exeJeuxSQL
from Titres.Carte import sendCarte
from Titres.Outils import gainCoins

from Jeux.Tortues import Carte, FakeTortue, JeuTortues, JoueurTortue, Pile

dictEmote={0:"<:otBlank:828934808200937492>","rouge":"<:OTTrouge:860119157495693343>","verte":"<:OTTvert:860119157331853333>","bleue":"<:OTTbleu:860119157491892255>","jaune":"<:OTTjaune:860119157688631316>","violette":"<:OTTviolet:860119157672247326>","last":"*dernière tortue*","multi":"*au choix*"}
dictColor={"bleue":0x00CCFF,"violette":0x993366,"rouge":0xFF0000,"verte":0x77B255,"jaune":0xFFFF00}
listeCouleurs=("rouge","jaune","bleue","verte","violette")

class JoueurTortueDuo(JoueurTortue):
    def __init__(self,user,interaction,couleur):
        super().__init__(user,interaction,couleur)
        self.equipe=0

    def setEquipe(self,equipe):
        self.equipe=equipe

class FakeTortueDuo(FakeTortue):
    def __init__(self,couleur):
        super().__init__(couleur)
        self.equipe=0

class JeuTortuesDuo(JeuTortues):
    def __init__(self,message,user,cross):
        super().__init__(message,user,"TortuesDuo",cross)
        self.equipe={1:[],2:[]}
        self.score={1:0,2:0}
        self.fini=[]
    
    def addPlayer(self,user,interaction):
        tortue=choice(self.tortues)
        self.tortues.remove(tortue)
        self.joueurs.append(JoueurTortueDuo(user,interaction,tortue))
        self.ids.append(user.id)
        
    def embedEnd(self,bot,guild):
        descip=""
        for i in self.joueurs:
            if i.guild==guild:
                descip+="{0} : <@{1}>\n".format(dictEmote[i.couleur],i.id)
            else:
                descip+="{0} : {1}\n".format(dictEmote[i.couleur],i.titre)

        for i in self.score:
            if self.score[i]==2:
                if self.equipe[i][0].guild==guild:
                    nameP1=self.equipe[i][0].nom
                else:
                    nameP1=self.equipe[i][0].titre

                if self.equipe[i][1].guild==guild:
                    nameP2=self.equipe[i][1].nom
                else:
                    nameP2=self.equipe[i][1].titre

        embed=createEmbed("Victoire de {0} et {1} !".format(nameP1,nameP2),"Ils étaient les tortues {0} et {1} ! {2} {3}\n\n{4}".format(self.equipe[i][0].couleur,self.equipe[i][1].couleur,dictEmote[self.equipe[i][0].couleur],dictEmote[self.equipe[i][1].couleur],descip),dictColor[self.equipe[i][0].couleur],"tortuesduo",bot.user)
        embed.add_field(name="<:otCOINS:873226814527520809> gagnés par chacun des gagnants",value="{0} <:otCOINS:873226814527520809>".format(75+sum(self.paris.mises.values())/2))
        return embed

    def getWinner(self):
        already=True
        cont=len(self.plateau[9])
        temp=Pile()
        for j in range(cont):
            temp.empiler(self.plateau[9].depiler())
        cel=temp.contenu
        while cel is not None:
            win=cel.valeur
            if cel.valeur not in self.fini:
                already=False
                self.fini.append(cel.valeur)
                break 
            cel=cel.suivante
        for j in range(cont):
            self.plateau[9].empiler(temp.depiler())
        if already:
            return None
        winID=list(filter(lambda x:x.couleur==win, self.joueurs))
        if len(winID)==0:
            return FakeTortueDuo(win)
        return winID[0]

    async def stats(self,team,guild):
        connexionGuild,curseurGuild=connectSQL(guild,"Guild","Guild",None,None)
        connexionOT,curseurOT=connectSQL("OT","Guild","Guild",None,None)
        for i in self.joueurs:
            if i.equipe==team:
                gainCoins(i.id,len(self.ids)*25+sum(self.paris.mises.values()))
                self.paris.distribParis(i.id)
                state="W"
            else:
                state="L"
            if len(self.guilds)==1:
                exeJeuxSQL(i.id,None,state,guild,curseurGuild,self.jeu,None)
            wins=exeJeuxSQL(i.id,None,state,"OT",curseurOT,self.jeu,None)
            if state=="W":
                await sendCarte(i.user,self.jeu,wins,i.interaction.message.channel)
        connexionGuild.commit()
        connexionOT.commit()

    async def sendTortues(self):
        for i in self.joueurs:
            team=randint(1,2)
            if len(self.equipe[team])!=2:
                self.equipe[team].append(i)
                i.setEquipe(team)
            else:
                if team==1:
                    self.equipe[2].append(i)
                    i.setEquipe(2)
                else:
                    self.equipe[1].append(i)
                    i.setEquipe(1)
        for i in self.joueurs:
            await i.interaction.followup.send(embed=createEmbed("Course des tortues","Vos deux tortues à faire gagner sont : {0} {1} et {2} {3}".format(self.equipe[i.equipe][0].couleur,dictEmote[self.equipe[i.equipe][0].couleur],self.equipe[i.equipe][1].couleur,dictEmote[self.equipe[i.equipe][1].couleur]),dictColor[i.couleur],"tortuesduo",i.user),ephemeral=True)
        self.giveCards()

    async def boucle(self,bot):
        while self.playing:
            for mess in self.messages:
                await mess.edit(embed=self.embedGame(self.joueurs[self.turn],mess.guild.id))
            couleur,valeur,carte=await self.play(bot,self.joueurs[self.turn].interaction)

            if self.mouvement(couleur,valeur):
                for i in range(len(self.plateau[9])):
                    win=self.getWinner()
                    if win!=None:
                        for mess in self.messages:
                            await mess.channel.send("La tortue {0} {1} est arrivée ! Elle gagne le droit de se reposer, et de ne plus jamais bouger... :zzz:".format(win.couleur,dictEmote[win.couleur]))
                        if win.equipe!=0:
                            self.score[win.equipe]+=1
                            if self.score[win.equipe]==2:
                                self.playing=False
                                await self.stats(win.equipe,win.guild)
                                for mess in self.messages:
                                    await mess.edit(embed=self.embedGame(self.joueurs[self.turn],mess.guild.id),view=None)
                                    await mess.reply(embed=self.embedEnd(bot,mess.guild.id))
                                break
            
            self.fermeture()
            self.joueurs[self.turn].jeu.remove(carte)
            self.joueurs[self.turn].pioche(self.cartes)
            self.turn+=1
            if self.turn==len(self.joueurs):
                self.turn=0
            if len(self.cartes)==0:
                self.cartes=[Carte(i,1) for i in listeCouleurs]*5+[Carte(i,2) for i in listeCouleurs]+[Carte(i,-1) for i in listeCouleurs]*2+[Carte("multi",1) for i in range(5)]+[Carte("last",1) for i in range(3)]+[Carte("last",2) for i in range(2)]+[Carte("multi",-1) for i in range(2)]
