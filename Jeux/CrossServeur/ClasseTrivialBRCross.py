import discord
from Core.Fonctions.AuteurIcon import auteur
from Jeux.CrossServeur.ClasseTrivialVSCross import VersusCross
from Stats.SQL.EmoteDetector import emoteDetector

listeNoms=["Culture","Divertissement","Sciences","Mythologie","Sport","Géographie","Histoire","Politique","Art","Célébrités","Animaux","Véhicules","Global"]
dictCateg={9:0,10:1,11:1,12:1,13:1,14:1,15:1,16:1,17:2,18:2,19:2,20:3,21:4,22:5,23:6,24:7,25:8,26:9,27:10,28:11,29:1,30:2,31:1,32:1}
dictDiff={"easy":"Facile (+10)","medium":"Moyenne (+15)","hard":"Difficile (+25)"}
emotesTrue=["<:ot1VRAI:773993429130149909>", "<:ot2VRAI:773993429050195979>", "<:ot3VRAI:773993429331738624>", "<:ot4VRAI:773993429423095859>"]
emotesFalse=["<:ot1FAUX:773993429315092490>", "<:ot2FAUX:773993429172486145>", "<:ot3FAUX:773993429402779698>", "<:ot4FAUX:773993429373026354>"]

class BattleRoyaleCross(VersusCross):
    def __init__(self, guild,option):
        super().__init__(guild,option)
        self.rangs={}
        self.restants=[]

    def addPlayer(self, joueur):
        super().addPlayer(joueur)
        self.scores[joueur.id]=3

    def createEmbed(self,results,guild):
        embedT=discord.Embed(title=self.questionFR, description=self.affichageClassique(), color=0xad917b)
        embedT=auteur(guild.id,guild.name,guild.icon,embedT,"guild")
        embedT.add_field(name="Catégorie", value=listeNoms[dictCateg[self.arg]], inline=True)
        embedT.add_field(name="Difficulté", value=dictDiff[self.diff], inline=True)
        embedT.add_field(name="Auteur",value="[{0}](https://forms.gle/RNTGn9tds2LGVkdU8)".format(self.auteur),inline=True)
        embedT.add_field(name="Question n°", value=str(self.tour+1),inline=True)
        descip=""
        count=0
        self.scores={k: v for k, v in sorted(self.scores.items(), key=lambda item: item[1], reverse=True)}
        for i in self.scores:
            if count==8:
                embedT.add_field(name="Scores", value=descip,inline=True)
                descip=""
            try:
                if self.memguild[i]==guild.id:
                    nom="<@{0}>".format(i)
                    emote=str(self.emotes[i])
                else:
                    nom=self.titres[i]
                    emote=self.emotesCustom[i]
                assert results
                if self.scores[i]==0:
                    descip+="{0} {1} : *Éliminé ! {2}e.*\n".format(emote,nom,self.histo[i])
                elif self.reponses[i]==None or self.vrai==None:
                    descip+="{0} {1} : **{2}**\n".format(emote,nom,":blue_heart: "*self.scores[i])
                elif self.reponses[i]==self.vrai-1:
                    descip+="{0} {1} : **{2}** - {3}\n".format(emote,nom,":blue_heart: "*self.scores[i],emotesTrue[self.reponses[i]])
                else:
                    descip+="{0} {1} : **{2}** - {3}\n".format(emote,nom,":blue_heart: "*self.scores[i],emotesFalse[self.reponses[i]])
            except:
                descip+="{0} {1} : **{2}**\n".format(emote,nom,":blue_heart: "*self.scores[i])
            count+=1
        embedT.add_field(name="Scores", value=descip,inline=True)
        embedT.set_footer(text="OT!trivial{0}cross".format(self.option))
        return embedT
    
    def embedHub(self,guild):
        embed=discord.Embed(title="Tableau des vies",description="Il reste {0} joueurs en vie !".format(len(self.restants)),color=0xad917b)
        embed=auteur(guild.id,guild.name,guild.icon,embed,"guild")
        for i in self.joueurs:
            if self.memguild[i.id]==guild.id:
                nom=i.name
                emote=str(self.emotes[i.id])
            else:
                nom=self.titres[i.id]
                emote=self.emotesCustom[i.id]
            if self.scores[i.id]==0:
                embed.add_field(name="{0} {1}".format(emote,nom),value="*Éliminé ! {0}e.*\n".format(self.histo[i.id]),inline=True)
            else:
                embed.add_field(name="{0} {1}".format(emote,nom),value=":blue_heart: "*self.scores[i.id],inline=True)
        embed.set_footer(text="OT!trivialbrcross")
        return embed
    
    def embedResults(self,winner:discord.Member,guild):
        self.histo={k: v for k, v in sorted(self.histo.items(), key=lambda item: item[1])}
        descip=""
        for i in self.histo:
            if self.memguild[i]==guild:
                nom="<@{0}>".format(i)
                emote=str(self.emotes[i])
            else:
                nom=self.titres[i]
                emote=self.emotesCustom[i]
            if self.scores[i]==0:
                descip+="{0} {1} : *Éliminé ! {2}e.*\n".format(emote,nom,self.histo[i])
            else:
                descip+="{0} {1} : **Victoire !** {2}\n".format(emote,nom,":blue_heart: "*self.scores[i])
        embedT=discord.Embed(title="Victoire de {0}".format(winner.name), description=descip, color=0xf2eb16)
        embedT.set_footer(text="OT!trivialbr")
        if self.memguild[winner.id]==guild:
            embedT=auteur(winner.id,winner.name,winner.avatar,embedT,"user")
        else:
            embedT.set_author(name=self.titres[winner.id],icon_url="https://cdn.discordapp.com/emojis/{0}.png".format(emoteDetector(self.emotesCustom[winner.id])[0]))
        embedT.add_field(name="<:otCOINS:873226814527520809> gagnés par {0}".format(winner.name),value="{0} <:otCOINS:873226814527520809>".format(len(self.ids)*25+sum(self.mises.values())))
        return embedT