import asyncio
from math import inf

import discord
from Core.Fonctions.AuteurIcon import auteurJeux
from Core.Fonctions.Embeds import createEmbed

from Jeux.Outils.AttenteTrivial import attente
from Jeux.TrivialVersus import JeuTrivialVersus, JoueurVersus

listeNoms=["Culture","Divertissement","Sciences","Mythologie","Sport","Géographie","Histoire","Politique","Art","Célébrités","Animaux","Véhicules","Global"]
dictCateg={9:0,10:1,11:1,12:1,13:1,14:1,15:1,16:1,17:2,18:2,19:2,20:3,21:4,22:5,23:6,24:7,25:8,26:9,27:10,28:11,29:1,30:2,31:1,32:1}
dictDiff={"easy":"Facile (+10)","medium":"Moyenne (+15)","hard":"Difficile (+25)"}
emotesTrue=["<:ot1VRAI:773993429130149909>", "<:ot2VRAI:773993429050195979>", "<:ot3VRAI:773993429331738624>", "<:ot4VRAI:773993429423095859>"]
emotesFalse=["<:ot1FAUX:773993429315092490>", "<:ot2FAUX:773993429172486145>", "<:ot3FAUX:773993429402779698>", "<:ot4FAUX:773993429373026354>"]

class JoueurBR(JoueurVersus):
    def __init__(self,user,interaction):
        super().__init__(user,interaction)
        self.score=3
        self.vivant=True

class JeuTrivialBR(JeuTrivialVersus):
    def __init__(self,message,user,cross):
        super().__init__(message,user,"BR",cross)

    def addPlayer(self, user,message):
        self.joueurs.append(JoueurBR(user,message))
        self.ids.append(user.id)
        
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
                assert results
                if i.score==0:
                    descip+="{0} {1} : *Éliminé ! {2}e.*\n".format(emote,nom,i.histo)
                elif self.reponses[i.id]==None or self.vrai==None:
                    descip+="{0} {1} : **{2}**\n".format(emote,nom,":blue_heart: "*i.score)
                elif self.reponses[i.id]==self.vrai-1:
                    descip+="{0} {1} : **{2}** - {3}\n".format(emote,nom,":blue_heart: "*i.score,emotesTrue[self.reponses[i.id]])
                else:
                    descip+="{0} {1} : **{2}** - {3}\n".format(emote,nom,":blue_heart: "*i.score,emotesFalse[self.reponses[i.id]])
            except:
                descip+="{0} {1} : **{2}**\n".format(emote,nom,":blue_heart: "*i.score)
            count+=1
        embed.add_field(name="Scores", value=descip,inline=True)
        return embed
    
    def embedHub(self,guild,vivants):
        embed=createEmbed("Tableau des vies","Il reste {0} joueurs en vie !".format(vivants),0xad917b,"trivialbr",guild)
        for i in self.joueurs:
            if i.guild==guild.id:
                nom=i.nom
            else:
                nom=i.titre
            if i.emote!=None:
                emote=i.emote
            else:
                emote=""
            if i.score==0:
                embed.add_field(name="{0} {1}".format(emote,nom),value="*Éliminé ! {0}e.*\n".format(i.histo),inline=True)
            else:
                embed.add_field(name="{0} {1}".format(emote,nom),value=":blue_heart: "*i.score,inline=True)
        return embed
    
    def embedEnd(self,winner:discord.Member,guild):
        descip=""
        for i in self.joueurs:
            if i.guild==guild:
                nom="<@{0}>".format(i.id)
            else:
                nom=i.titre
            if i.emote!=None:
                emote=i.emote
            else:
                emote=""
            if i.score==0:
                descip+="{0} {1} : *Éliminé ! {2}e.*\n".format(emote,nom,i.histo)
            else:
                descip+="{0} {1} : **Victoire !** {2}\n".format(emote,nom,":blue_heart: "*i.score)

        if winner.guild==guild:
            embed=createEmbed("Victoire de {0}".format(winner.nom),descip,winner.color,"trivialbr",winner.user)
        else:
            embed=createEmbed("Victoire de {0}".format(winner.titre),descip,winner.color,"trivialbr",winner.user)
            auteurJeux(winner,embed)

        embed.add_field(name="<:otCOINS:873226814527520809> gagnés pour le vainqueur",value="{0} <:otCOINS:873226814527520809>".format(len(self.ids)*25+sum(self.paris.mises.values())))
        return embed

    def fermeture(self):
        for i in self.joueurs:
            if i.score==1:
                self.paris.ouvert=False 

    async def boucle(self,bot):
        vivants=self.joueurs
        while self.playing:

            self.reponses={i.id:None for i in vivants}
            self.setCateg()
            self.setDiff()
            self.newQuestion()

            for mess in self.messages:
                await mess.edit(embed=self.embedGame(False,mess.guild))

            await attente(self)

            count,left,good=0,len(vivants),0
            for i in vivants:
                if self.reponses[i.id]!=self.vrai-1:
                    i.score-=1
                    if i.score==0:
                        count+=1
                else:
                    good+=1
            if count==left or good==0:
                for i in vivants:
                    i.score+=1
            else:
                for i in vivants:
                    if i.score==0:
                        i.histo=left-count+1
                        i.vivant=False
            
            for mess in self.messages:
                embedT=self.embedGame(True,mess.guild)
                if good>0:
                    embedT.colour=0x47b03c
                    embedT.description="**{0} personne*(s)* a *(ont)* eu juste !** {1}".format(good,self.affichageWin()[20:-1])
                else:
                    embedT.colour=0xcf1742
                    embedT.description="**Tout le monde s'est trompé, la question est invalidée !** {0}".format(self.affichageLose(None)[10:-1])
                await mess.edit(embed=embedT)

            if self.maxTour():
                maxi,maxiJoueur=-inf,None
                for i in self.joueurs:
                    if i.score>maxi:
                        maxi,maxiJoueur=i.score
                vivants=[maxiJoueur]
            else:
                vivants=list(filter(lambda x:x.vivant, self.joueurs))

            if len(vivants)==1:
                vivants[0].histo=1
                winner=vivants[0]
                await self.stats(winner.id,winner.guild)
                for mess in self.messages:
                    await mess.edit(view=None)
                    await mess.reply(embed=self.embedEnd(winner,mess.guild.id))
                self.playing=False

            self.fermeture()
            self.tour+=1
            await asyncio.sleep(5)
            for mess in self.messages:
                await mess.edit(embed=self.embedHub(mess.guild,len(vivants)))
            await asyncio.sleep(5)
