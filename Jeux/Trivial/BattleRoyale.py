import asyncio

import discord
from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.Embeds import embedAssert
from Jeux.Trivial.Attente import attente
from Jeux.Trivial.Versus import Versus
from math import inf
from Jeux.Paris import Pari

listeNoms=["Culture","Divertissement","Sciences","Mythologie","Sport","Géographie","Histoire","Politique","Art","Célébrités","Animaux","Véhicules","Global"]
dictCateg={9:0,10:1,11:1,12:1,13:1,14:1,15:1,16:1,17:2,18:2,19:2,20:3,21:4,22:5,23:6,24:7,25:8,26:9,27:10,28:11,29:1,30:2,31:1,32:1}
dictDiff={"easy":"Facile (+10)","medium":"Moyenne (+15)","hard":"Difficile (+25)"}
emotesTrue=["<:ot1VRAI:773993429130149909>", "<:ot2VRAI:773993429050195979>", "<:ot3VRAI:773993429331738624>", "<:ot4VRAI:773993429423095859>"]
emotesFalse=["<:ot1FAUX:773993429315092490>", "<:ot2FAUX:773993429172486145>", "<:ot3FAUX:773993429402779698>", "<:ot4FAUX:773993429373026354>"]

class BattleRoyale(Versus):
    def __init__(self, guild,option):
        super().__init__(guild,option)
        self.rangs={}
        self.restants=[]

    def addPlayer(self, joueur):
        super().addPlayer(joueur)
        self.scores[joueur.id]=3

    def createEmbed(self,results):
        embedT=discord.Embed(title=self.questionFR, description=self.affichageClassique(), color=0xad917b)
        embedT=auteur(self.guild.id,self.guild.name,self.guild.icon,embedT,"guild")
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
                assert results
                if self.scores[i]==0:
                    descip+="{0} <@{1}> : *Éliminé ! {2}e.*\n".format(str(self.emotes[i]),i,self.histo[i])
                elif self.reponses[i]==None or self.vrai==None:
                    descip+="{0} <@{1}> : **{2}**\n".format(str(self.emotes[i]),i,":blue_heart: "*self.scores[i])
                elif self.reponses[i]==self.vrai-1:
                    descip+="{0} <@{1}> : **{2}** - {3}\n".format(str(self.emotes[i]),i,":blue_heart: "*self.scores[i],emotesTrue[self.reponses[i]])
                else:
                    descip+="{0} <@{1}> : **{2}** - {3}\n".format(str(self.emotes[i]),i,":blue_heart: "*self.scores[i],emotesFalse[self.reponses[i]])
            except:
                descip+="{0} <@{1}> : **{2}**\n".format(str(self.emotes[i]),i,":blue_heart: "*self.scores[i])
            count+=1
        embedT.add_field(name="Scores", value=descip,inline=True)
        embedT.set_footer(text="OT!trivial{0}".format(self.option))
        return embedT
    
    def embedHub(self):
        embed=discord.Embed(title="Tableau des vies",description="Il reste {0} joueurs en vie !".format(len(self.restants)),color=0xad917b)
        embed=auteur(self.guild.id,self.guild.name,self.guild.icon,embed,"guild")
        for i in self.joueurs:
            if self.scores[i.id]==0:
                embed.add_field(name="{0} {1}".format(str(self.emotes[i.id]),i.name),value="*Éliminé ! {0}e.*\n".format(self.histo[i.id]),inline=True)
            else:
                embed.add_field(name="{0} {1}".format(str(self.emotes[i.id]),i.name),value=":blue_heart: "*self.scores[i.id],inline=True)
        embed.set_footer(text="OT!trivialbr".format(self.option))
        return embed
    
    def embedResults(self,winner:discord.Member):
        self.histo={k: v for k, v in sorted(self.histo.items(), key=lambda item: item[1])}
        descip=""
        for i in self.histo:
            if self.scores[i]==0:
                descip+="{0} <@{1}> : *Éliminé ! {2}e.*\n".format(str(self.emotes[i]),i,self.histo[i])
            else:
                descip+="{0} <@{1}> : **Victoire !** {2}\n".format(str(self.emotes[i]),i,":blue_heart: "*self.scores[i])
        embedT=discord.Embed(title="Victoire de {0}".format(winner.name), description=descip, color=0xf2eb16)
        embedT.set_footer(text="OT!trivialbr")
        embedT=auteur(winner.id,winner.name,winner.avatar,embedT,"user")
        embedT.add_field(name="<:otCOINS:873226814527520809> gagnés par {0}".format(winner.name),value="{0} <:otCOINS:873226814527520809>".format(len(self.ids)*25+sum(self.paris.mises.values())))
        return embedT

    def fermeture(self):
        for i in self.scores:
            if self.scores[i]==1:
                self.paris.ouvert=False 


async def trivialBattleRoyale(ctx,bot,inGame,gamesTrivial):
    try:
        assert ctx.author.id not in inGame, "Terminez votre question en cours avant de lancer ou rejoindre une partie."
        game=BattleRoyale(ctx.guild,"br")
        message=await game.startGame(ctx,bot,inGame,gamesTrivial)
        if message==False:
            return
        messAd=await bot.get_channel(870598360296488980).send("{0} - {1} : partie OT!trivialbr débutée\n{2} joueurs".format(ctx.guild.name,ctx.guild.id,len(game.joueurs)))
        game.restants=game.ids.copy()
        game.paris=Pari(game.ids,"TrivialBR")
        while game.playing:
            listeDel=[]
            game.reponses={i:None for i in game.restants}
            game.setCateg(None)
            game.setDiff()
            game.newQuestion()
            embedT=game.createEmbed(False)
            await message.edit(embed=embedT)
            await attente(game,20,None)

            count,left,good=0,len(game.restants),0
            for i in game.restants:
                if game.reponses[i]!=game.vrai-1:
                    game.scores[i]-=1
                    if game.scores[i]==0:
                        count+=1
                else:
                    good+=1
            if count==left:
                for i in game.restants:
                    game.scores[i]+=1
            else:
                for i in game.restants:
                    if game.scores[i]==0:
                        game.histo[i]=left-count+1
                        listeDel.append(i)
                for i in listeDel:
                    game.restants.remove(i)
            
            embedT=game.createEmbed(True)
            if good>0:
                embedT.colour=0x47b03c
                embedT.description="**{0} personne*(s)* a *(ont)* eu juste !** {1}".format(good,game.affichageWin()[20:-1])
            else:
                embedT.colour=0xcf1742
                embedT.description="**Tout le monde s'est trompé...** {0}".format(game.affichageLose(None)[10:-1])
            await message.edit(embed=embedT)
            if game.maxTour():
                maxi,maxiJoueur=-inf,None
                for i in game.joueurs:
                    if game.scores[i.id]>maxi:
                        maxi,maxiJoueur=game.scores[i.id],i.id
                game.restants=[maxiJoueur]
            if len(game.restants)==1:
                game.histo[game.restants[0]]=1
                await message.clear_reactions()
                await message.channel.send(embed=game.embedResults(game.guild.get_member(game.restants[0])))
                await message.unpin()
                game.playing=False
                game.stats(game.guild.get_member(game.restants[0]),"TrivialBR")
                game.paris.distribParis(game.restants[0])
            game.fermeture()
            game.tour+=1
            await asyncio.sleep(5)
            await message.edit(embed=game.embedHub())
            await asyncio.sleep(5)
        await game.endGame(message,inGame,gamesTrivial)
    except AssertionError as er:
        await ctx.send(embed=embedAssert(er))
    except:
        await game.error(ctx,bot,message,inGame,gamesTrivial)
    if "messAd" in locals():
        await messAd.delete()
