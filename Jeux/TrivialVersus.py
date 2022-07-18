import asyncio
from math import inf
from random import choice

from Core.Fonctions.AuteurIcon import auteurJeux
from Core.Fonctions.Embeds import createEmbed

from Jeux.Outils.AttenteTrivial import attente
from Jeux.Outils.Bases import JeuBase, JoueurBase
from Jeux.Trivial import Question

listeNoms=["Culture","Divertissement","Sciences","Mythologie","Sport","Géographie","Histoire","Politique","Art","Célébrités","Animaux","Véhicules","Global"]
dictCateg={9:0,10:1,11:1,12:1,13:1,14:1,15:1,16:1,17:2,18:2,19:2,20:3,21:4,22:5,23:6,24:7,25:8,26:9,27:10,28:11,29:1,30:2,31:1,32:1}
dictDiff={"easy":"Facile (+10)","medium":"Moyenne (+15)","hard":"Difficile (+25)"}
emotesTrue=["<:ot1VRAI:773993429130149909>", "<:ot2VRAI:773993429050195979>", "<:ot3VRAI:773993429331738624>", "<:ot4VRAI:773993429423095859>"]
emotesFalse=["<:ot1FAUX:773993429315092490>", "<:ot2FAUX:773993429172486145>", "<:ot3FAUX:773993429402779698>", "<:ot4FAUX:773993429373026354>"]
emotes=["<:ot1:705766186909958185>","<:ot2:705766186989912154>","<:ot3:705766186930929685>","<:ot4:705766186947706934>"]

class JoueurVersus(JoueurBase):
    def __init__(self,user,interaction):
        super().__init__(user,interaction)
        self.histo=""
        self.score=0

class JeuTrivialVersus(Question,JeuBase):
    def __init__(self,message,invoke,trivial,cross):
        self.reponses={}
        self.tour=0
        self.max=1
        self.rota=[]
        self.trivial=trivial
        Question.__init__(self,None,"classic")
        JeuBase.__init__(self,message,invoke,"Trivial{0}".format(trivial),cross)

    def maxTour(self):
        if self.tour==40:
            return True
        return False

    def addPlayer(self,user,interaction):
        self.joueurs.append(JoueurVersus(user,interaction))
        self.reponses[user.id]=None
        self.ids.append(user.id)
    
    def setDiff(self):
        if self.tour<=2:
            self.diff="easy"
        elif self.tour<=4:
            self.diff=choice(["easy","medium","medium"])
        else:
            self.diff=choice(["easy","medium","medium","hard","hard","hard"])
    
    def setCateg(self):
        if self.rota==[]:
            self.rota=["culture","divertissement","sciences","mythologie","sport","géographie","histoire","politique","art","célébrités","animaux","véhicules"]
        arg=choice(self.rota)
        self.rota.remove(arg)
        super().setCateg(arg)

    def embedGame(self,results,guild):
        embed=createEmbed(self.questionFR,self.affichageClassique(),0xad917b,"trivial{0}".format(self.trivial),guild)
        embed.add_field(name="Catégorie", value=listeNoms[dictCateg[self.arg]], inline=True)
        embed.add_field(name="Difficulté", value=dictDiff[self.diff], inline=True)
        embed.add_field(name="Auteur",value="[{0}](https://forms.gle/RNTGn9tds2LGVkdU8)".format(self.auteur),inline=True)
        embed.add_field(name="Question n°", value=str(self.tour+1),inline=True)
        descip=""
        self.joueurs.sort(key=lambda x:x.score, reverse=True)
        count=0
        for i in self.joueurs:
            if count==8:
                embed.add_field(name="Scores", value=descip,inline=True)
                descip=""
            try:
                if i.guild==guild.id:
                    nom="<@{0}>".format(i.id)
                else:
                    nom=i.titre
                if i.emote!=None:
                    emote=i.emote
                else:
                    emote=""
                if self.reponses[i.id]==None or self.vrai==None or not results:
                    descip+="{0} {1} : **{2}**\n".format(emote,nom,i.score)
                elif self.reponses[i.id]==self.vrai-1:
                    descip+="{0} {1} : **{2}** - {3}\n".format(emote,nom,i.score,emotesTrue[self.reponses[i.id]])
                else:
                    descip+="{0} {1} : **{2}** - {3}\n".format(emote,nom,i.score,emotesFalse[self.reponses[i.id]])
            except:
                descip+="{0} {1} : **{2}**\n".format(emote,nom,i.score)
            count+=1
        embed.add_field(name="Scores", value=descip,inline=True)
        return embed

    def embedEnd(self,winner,guild):
        descip=""
        for joueur in self.joueurs:
            if joueur.guild==guild: 
                descip+="{0} <@{1}> : {2} -  {3}\n".format(joueur.emote,joueur.id,joueur.score,joueur.histo)
            else:
                descip+="{0} {1} : {2} -  {3}\n".format(joueur.emote,joueur.titre,joueur.score,joueur.histo)
        if winner.guild==guild:
            embed=createEmbed("Victoire de {0}".format(winner.nom),descip,winner.color,"trivialversus",winner.user)
        else:
            embed=createEmbed("Victoire de {0}".format(winner.titre),descip,winner.color,"trivialversus",winner.user)
            auteurJeux(winner,embed)

        embed.add_field(name="<:otCOINS:873226814527520809> gagnés pour le vainqueur",value="{0} <:otCOINS:873226814527520809>".format(len(self.ids)*25+sum(self.paris.mises.values())))
        return embed

    def fermeture(self):
        for i in self.joueurs:
            if i.score==3:
                self.paris.ouvert=False 

    async def boucle(self,bot):
        while self.playing:
            self.reponses={i:None for i in self.ids}
            self.setCateg()
            self.setDiff()
            self.newQuestion()
            for mess in self.messages:
                await mess.edit(embed=self.embedGame(False,mess.guild))

            await attente(self)

            count=[]
            good=0
            for joueur in self.joueurs:
                if self.reponses[joueur.id]==self.vrai-1:
                    good+=1
                    joueur.score+=1
                    joueur.histo+=emotesTrue[self.reponses[joueur.id]]
                    if joueur.score==self.max:
                        count.append(joueur)
                elif self.reponses[joueur.id]==None:
                    joueur.histo+="<:otBlank:828934808200937492>"
                else:
                    joueur.histo+=emotesFalse[self.reponses[joueur.id]]
            
            for mess in self.messages:
                embed=self.embedGame(True,mess.guild)
                if good>0:
                    embed.colour=0x47b03c
                    embed.description="**{0} personnes ont eu juste !** {1}".format(good,self.affichageWin()[20:-1])
                else:
                    embed.colour=0xcf1742
                    embed.description="**Tout le monde s'est trompé...** {0}".format(self.affichageLose(None)[10:-1])
                await mess.edit(embed=embed)

            if self.maxTour():
                maxi,maxiJoueur=-inf,None
                for i in self.joueurs:
                    if self.scores[i.id]>maxi:
                        maxi,maxiJoueur=self.scores[i.id],i
                count=[maxiJoueur]

            if len(count)==1:
                winner=count[0]
                await self.stats(winner.id,winner.guild)
                for mess in self.messages:
                    await mess.edit(view=None)
                    await mess.reply(embed=self.embedEnd(winner,mess.guild))
                self.playing=False
            elif len(count)>1:
                self.max+=1

            self.fermeture()
            self.tour+=1
            await asyncio.sleep(7)
