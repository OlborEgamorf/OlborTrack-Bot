import asyncio
from random import choice

import discord
from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.Embeds import embedAssert, exeErrorExcept, createEmbed
from Stats.SQL.ConnectSQL import connectSQL
from Stats.SQL.Execution import exeJeuxSQL
from Titres.Outils import gainCoins
from Jeux.Trivial.Classic import Question
from math import inf
from Jeux.Paris import Pari
from Titres.Carte import sendCarte

listeNoms=["Culture","Divertissement","Sciences","Mythologie","Sport","Géographie","Histoire","Politique","Art","Célébrités","Animaux","Véhicules","Global"]
dictCateg={9:0,10:1,11:1,12:1,13:1,14:1,15:1,16:1,17:2,18:2,19:2,20:3,21:4,22:5,23:6,24:7,25:8,26:9,27:10,28:11,29:1,30:2,31:1,32:1}
dictDiff={"easy":"Facile (+10)","medium":"Moyenne (+15)","hard":"Difficile (+25)"}
emotesTrue=["<:ot1VRAI:773993429130149909>", "<:ot2VRAI:773993429050195979>", "<:ot3VRAI:773993429331738624>", "<:ot4VRAI:773993429423095859>"]
emotesFalse=["<:ot1FAUX:773993429315092490>", "<:ot2FAUX:773993429172486145>", "<:ot3FAUX:773993429402779698>", "<:ot4FAUX:773993429373026354>"]
emotes=["<:ot1:705766186909958185>","<:ot2:705766186989912154>","<:ot3:705766186930929685>","<:ot4:705766186947706934>"]

class Versus(Question):
    def __init__(self,guild,option):
        self.joueurs=[]
        self.ids=[]
        self.emotes={}
        self.reponses={}
        self.scores={}
        self.histo={}
        self.paris=None
        self.tour=0
        self.guild=guild
        self.playing=False
        self.max=5
        self.rota=[]
        self.invoke=None
        super().__init__(None,option)

    def maxTour(self):
        if self.tour==40:
            return True
        return False

    async def startGame(self,ctx,bot,inGame,gamesTrivial):
        self.ids.append(ctx.author.id)
        self.invoke=ctx.author.id
        inGame.append(ctx.author.id)
        dictHelp={"party":"Appuyez sur la réaction <:otVALIDER:772766033996021761> pour rejoindre la partie de Trivial Party et <:otANNULER:811242376625782785> pour annuler votre participation. La personne qui a demandé la partie peut cliquer sur <:otVALIDER:772766033996021761> pour lancer directement la partie. Sinon, elle va démarrer dans une minute.\n\n**Comment jouer ? : ** le Trivial Party se joue de 2 à 15 joueurs. Des questions vont se suivre, il faut obtenir 12 points pour gagner ! De manière aléatoire, des évènement peuvent se dérouler pour changer complétement la partie ! Le jeu se déroule dans ce salon et sur ce message. Les propositions sont numérotés de <:ot1:705766186909958185> à <:ot4:705766186947706934>, cliquez sur la réaction qui correspond pour choisir votre réponse. Au bout de 20s ou quand tout le monde a répondu, les résultats sont affichés. La prochaine question démarrera peu de temps après. Bonne chance !","versus":"Appuyez sur la réaction <:otVALIDER:772766033996021761> pour rejoindre la partie de Trivial Versus et <:otANNULER:811242376625782785> pour annuler votre participation. La personne qui a demandé la partie peut cliquer sur <:otVALIDER:772766033996021761> pour lancer directement la partie. Sinon, elle va démarrer dans une minute.\n\n**Comment jouer ? : ** le Trivial Versus se joue de 2 à 5 joueurs. Des questions vont se suivre, l'objectif est d'atteindre 5 bonnes réponses avant tout le monde ! Le jeu se déroule dans ce salon et sur ce message. Les propositions sont numérotés de <:ot1:705766186909958185> à <:ot4:705766186947706934>, cliquez sur la réaction qui correspond pour choisir votre réponse. Au bout de 20s ou quand tout le monde a répondu, les résultats sont affichés. La prochaine question démarrera 7s après. Bonne chance !","br":"Appuyez sur la réaction <:otVALIDER:772766033996021761> pour rejoindre la partie de Trivial Battle Royale et <:otANNULER:811242376625782785> pour annuler votre participation. La personne qui a demandé la partie peut cliquer sur <:otVALIDER:772766033996021761> pour lancer directement la partie. Sinon, elle va démarrer dans une minute.\n\n**Comment jouer ? : ** le Trivial BR se joue de 2 à 15 joueurs. Des questions vont se suivre, l'objectif est d'être le dernier en vie ! Au début vous avez 3 vies, et vous en perdez une par mauvaise réponse. Le jeu se déroule dans ce salon et sur ce message. Les propositions sont numérotés de <:ot1:705766186909958185> à <:ot4:705766186947706934>, cliquez sur la réaction qui correspond pour choisir votre réponse. Au bout de 20s ou quand tout le monde a répondu, les résultats sont affichés. Bonne chance !"}
        message=await ctx.send(embed=createEmbed("Trivial {0}".format(self.option.upper()),dictHelp[self.option],0xad917b,ctx.invoked_with.lower(),ctx.guild))
        gamesTrivial[message.id]=self
        await message.add_reaction("<:otVALIDER:772766033996021761>")
        await message.add_reaction("<:otANNULER:811242376625782785>")

        for i in range(60):
            if not self.playing:
                await asyncio.sleep(1)
            else:
                break

        self.playing=True
        await message.clear_reactions()
        if len(self.ids)<2:
            await message.edit(embed=createEmbed("Trivial Party","Une minute s'est écoulée et personne n'a répondu à l'invitation.",0xad917b,ctx.invoked_with.lower(),ctx.guild))
            for i in self.ids:
                inGame.remove(i)
            return False
        else:
            for i in self.ids:
                user=ctx.guild.get_member(i)
                self.addPlayer(user)
            await self.emotesUser(bot)
            descip="<:otVERT:868535645897912330> La partie commence "
            for i in self.ids:
                descip+="<@{0}> ".format(i)
            await message.channel.send(descip)
            try:
                await message.pin()
            except:
                pass
            for i in emotes:
                await message.add_reaction(i)
            await message.add_reaction("<:otCOINS:873226814527520809>")
            return message

    async def endGame(self,message,inGame,gamesTrivial):
        try:
            await self.delEmotes()
        except:
            pass
        for i in self.ids:
            inGame.remove(i)
        del gamesTrivial[message.id]

    async def emotesUser(self,bot):
        idServ=[759688015676309525,759690251521622016,776417458386763778,776417488698212383]
        for i in self.joueurs:
            for j in range(4):
                try:
                    emote=await bot.get_guild(idServ[j]).create_custom_emoji(name=str(i.id),image=await i.avatar_url_as(size=128).read(),roles=None,reason=None)
                    break
                except:
                    if j==3:
                        emote="<:otBlank:828934808200937492>"
            self.emotes[i.id]=emote
    
    async def delEmotes(self):
        for i in self.ids:
            if self.emotes[i]!="<:otBlank:828934808200937492>":
                await self.emotes[i].delete()

    def addPlayer(self,joueur):
        self.joueurs.append(joueur)
        self.reponses[joueur.id]=None
        self.scores[joueur.id]=0
        self.histo[joueur.id]=""
    
    def setDiff(self):
        if self.tour<=2:
            self.diff="easy"
        elif self.tour<=4:
            self.diff=choice(["easy","medium","medium"])
        else:
            self.diff=choice(["easy","medium","medium","hard","hard","hard"])
    
    def setCateg(self, args):
        if self.rota==[]:
            self.rota=["culture","divertissement","sciences","mythologie","sport","géographie","histoire","politique","art","célébrités","animaux","véhicules"]
        arg=choice(self.rota)
        self.rota.remove(arg)
        super().setCateg(arg)

    def createEmbed(self,results):
        embedT=discord.Embed(title=self.questionFR, description=self.affichageClassique(), color=0xad917b)
        embedT=auteur(self.guild.id,self.guild.name,self.guild.icon,embedT,"guild")
        embedT.add_field(name="Catégorie", value=listeNoms[dictCateg[self.arg]], inline=True)
        embedT.add_field(name="Difficulté", value=dictDiff[self.diff], inline=True)
        embedT.add_field(name="Auteur",value="[{0}](https://forms.gle/RNTGn9tds2LGVkdU8)".format(self.auteur),inline=True)
        embedT.add_field(name="Question n°", value=str(self.tour+1),inline=True)
        descip=""
        self.scores={k: v for k, v in sorted(self.scores.items(), key=lambda item: item[1], reverse=True)}
        count=0
        for i in self.scores:
            if count==8:
                embedT.add_field(name="Scores", value=descip,inline=True)
                descip=""
            try:
                assert results
                if self.reponses[i]==None or self.vrai==None:
                    descip+="{0} <@{1}> : **{2}**\n".format(str(self.emotes[i]),i,self.scores[i])
                elif self.reponses[i]==self.vrai-1:
                    descip+="{0} <@{1}> : **{2}** - {3}\n".format(str(self.emotes[i]),i,self.scores[i],emotesTrue[self.reponses[i]])
                else:
                    descip+="{0} <@{1}> : **{2}** - {3}\n".format(str(self.emotes[i]),i,self.scores[i],emotesFalse[self.reponses[i]])
            except:
                descip+="{0} <@{1}> : **{2}**\n".format(str(self.emotes[i]),i,self.scores[i])
            count+=1
        embedT.add_field(name="Scores", value=descip,inline=True)
        embedT.set_footer(text="OT!trivial{0}".format(self.option))
        return embedT

    def embedResults(self,winner):
        descip=""
        for i in self.scores:
            descip+="{0} <@{1}> : {2} -  {3}\n".format(str(self.emotes[i]),i,self.scores[i],self.histo[i])
        embedT=discord.Embed(title="Victoire de {0}".format(winner.name), description=descip, color=0xf2eb16)
        embedT.set_footer(text="OT!trivialversus")
        embedT=auteur(winner.id,winner.name,winner.avatar,embedT,"user")
        embedT.add_field(name="<:otCOINS:873226814527520809> gagnés par {0}".format(winner.name),value="{0} <:otCOINS:873226814527520809>".format(len(self.ids)*25+sum(self.paris.mises.values())))
        return embedT

    async def error(self,ctx,bot,message,inGame,gamesTrivial):
        await ctx.send(embed=await exeErrorExcept(ctx,bot,""))
        await self.endGame(message,inGame,gamesTrivial)
        await message.unpin()

    async def stats(self,win,option,chan):
        connexionGuild,curseurGuild=connectSQL(self.guild.id,"Guild","Guild",None,None)
        connexionOT,curseurOT=connectSQL("OT","Guild","Guild",None,None)
        for i in self.ids:
            if i==win.id:
                count,state=2,"W"
                gainCoins(i,25*len(self.ids)+sum(self.paris.mises.values()))
            else:
                count,state=-1,"L"
            exeJeuxSQL(i,None,state,self.guild.id,curseurGuild,count,option,None)
            wins=exeJeuxSQL(i,None,state,"OT",curseurOT,count,option,None)
            if state=="W":
                await sendCarte(win,option,wins,"classic",chan)
        connexionGuild.commit()
        connexionOT.commit()

    def fermeture(self):
        for i in self.scores:
            if self.scores[i]==3:
                self.paris.ouvert=False 


async def trivialVersus(ctx,bot,inGame,gamesTrivial):
    try:
        assert ctx.author.id not in inGame, "Terminez votre question en cours avant de lancer ou rejoindre une partie."
        game=Versus(ctx.guild,"versus")
        message=await game.startGame(ctx,bot,inGame,gamesTrivial)
        if message==False:
            return
        messAd=await bot.get_channel(870598360296488980).send("{0} - {1} : partie OT!trivialversus débutée\n{2} joueurs".format(ctx.guild.name,ctx.guild.id,len(game.joueurs)))
        game.paris=Pari(game.ids,"TrivialVersus")
        while game.playing:
            game.reponses={i:None for i in game.ids}
            game.setCateg(None)
            game.setDiff()
            game.newQuestion()
            embedT=game.createEmbed(False)
            await message.edit(embed=embedT)
            time,done=0,False
            while time!=20 and not done:
                await asyncio.sleep(1)
                done=True
                for j in game.reponses:
                    if game.reponses[j]==None:
                        done=False
                time+=1
            count=[]
            good=0
            for i in game.joueurs:
                if game.reponses[i.id]==game.vrai-1:
                    good+=1
                    game.scores[i.id]+=1
                    game.histo[i.id]+=emotesTrue[game.reponses[i.id]]
                    if game.scores[i.id]==game.max:
                        count.append(i)
                elif game.reponses[i.id]==None:
                    game.histo[i.id]+="<:otBlank:828934808200937492>"
                else:
                    game.histo[i.id]+=emotesFalse[game.reponses[i.id]]
            
            embedT=game.createEmbed(True)
            if good>0:
                embedT.colour=0x47b03c
                embedT.description="**{0} personnes ont eu juste !** {1}".format(good,game.affichageWin()[20:-1])
            else:
                embedT.colour=0xcf1742
                embedT.description="**Tout le monde s'est trompé...** {0}".format(game.affichageLose(None)[10:-1])
            await message.edit(embed=embedT)
            if game.maxTour():
                maxi,maxiJoueur=-inf,None
                for i in game.joueurs:
                    if game.scores[i.id]>maxi:
                        maxi,maxiJoueur=game.scores[i.id],i
                count=[maxiJoueur]
            if len(count)==1:
                await message.clear_reactions()
                await message.channel.send(embed=game.embedResults(count[0]))
                await message.unpin()
                game.playing=False
                await game.stats(count[0],"TrivialVersus",message.channel)
                game.paris.distribParis(count[0].id)
            elif len(count)>1:
                game.max+=1
            game.fermeture()
            game.tour+=1
            await asyncio.sleep(7)
        await game.endGame(message,inGame,gamesTrivial)
    except AssertionError as er:
        await ctx.send(embed=embedAssert(er))
    except:
        await game.error(ctx,bot,message,inGame,gamesTrivial)
    if "messAd" in locals():
        await messAd.delete()