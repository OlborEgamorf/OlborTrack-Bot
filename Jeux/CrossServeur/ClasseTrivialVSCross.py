import discord
from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.Embeds import createEmbed, exeErrorExcept
from Core.Fonctions.GetNom import getTitre
from Jeux.Trivial.Versus import Versus
from Stats.SQL.ConnectSQL import connectSQL
from Stats.SQL.EmoteDetector import emoteDetector
from Titres.Emote import getEmoteJeux

emotes=["<:ot1:705766186909958185>","<:ot2:705766186989912154>","<:ot3:705766186930929685>","<:ot4:705766186947706934>"]
emotesTrue=["<:ot1VRAI:773993429130149909>", "<:ot2VRAI:773993429050195979>", "<:ot3VRAI:773993429331738624>", "<:ot4VRAI:773993429423095859>"]
emotesFalse=["<:ot1FAUX:773993429315092490>", "<:ot2FAUX:773993429172486145>", "<:ot3FAUX:773993429402779698>", "<:ot4FAUX:773993429373026354>"]
emotes=["<:ot1:705766186909958185>","<:ot2:705766186989912154>","<:ot3:705766186930929685>","<:ot4:705766186947706934>"]
listeNoms=["Culture","Divertissement","Sciences","Mythologie","Sport","Géographie","Histoire","Politique","Art","Célébrités","Animaux","Véhicules","Global"]
dictCateg={9:0,10:1,11:1,12:1,13:1,14:1,15:1,16:1,17:2,18:2,19:2,20:3,21:4,22:5,23:6,24:7,25:8,26:9,27:10,28:11,29:1,30:2,31:1,32:1}
dictDiff={"easy":"Facile (+10)","medium":"Moyenne (+15)","hard":"Difficile (+25)"}

import asyncio
from Titres.Outils import gainCoins
from Stats.SQL.Execution import exeJeuxSQL
from Core.Fonctions.Unpin import pin, unpin


class VersusCross(Versus):
    def __init__(self,guild,option):
        self.guilds=[]
        self.messages=[]
        self.memguild={}
        self.messguild={}
        self.guildmess={}
        self.memmess={}
        self.emotesCustom={}
        self.titres={}
        super().__init__(guild,option)

    async def startGame(self,ctx,bot,inGame,gamesTrivial,new,dictOnline):
        
        self.guilds.append(ctx.guild.id)
        self.memguild[ctx.author.id]=ctx.guild.id
        self.messguild[ctx.message.id]=ctx.guild.id
        self.ids.append(ctx.author.id)
        self.mises[ctx.author.id]=0
        inGame.append(ctx.author.id)
        if new:
            dictHelp={"party":"**Vous avez créé une partie de OT!trivialparty en Cross-Serveur. Vous êtes le propriétaire de la partie.**\n\nAppuyez sur la réaction <:otVALIDER:772766033996021761> pour rejoindre la partie de Trivial Party et <:otANNULER:811242376625782785> pour annuler votre participation. La personne qui a demandé la partie peut cliquer sur <:otVALIDER:772766033996021761> pour lancer directement la partie. Sinon, elle va démarrer dans une minute.\n\n**Comment jouer ? : ** le Trivial Party se joue de 2 à 15 joueurs. Des questions vont se suivre, il faut obtenir 12 points pour gagner ! De manière aléatoire, des évènement peuvent se dérouler pour changer complétement la partie ! Le jeu se déroule dans ce salon et sur ce message. Les propositions sont numérotés de <:ot1:705766186909958185> à <:ot4:705766186947706934>, cliquez sur la réaction qui correspond pour choisir votre réponse. Au bout de 20s ou quand tout le monde a répondu, les résultats sont affichés. La prochaine question démarrera peu de temps après. Bonne chance !",
            "versus":"**Vous avez créé une partie de OT!trivialversus en Cross-Serveur. Vous êtes le propriétaire de la partie.**\n\nAppuyez sur la réaction <:otVALIDER:772766033996021761> pour rejoindre la partie de Trivial Versus et <:otANNULER:811242376625782785> pour annuler votre participation. La personne qui a demandé la partie peut cliquer sur <:otVALIDER:772766033996021761> pour lancer directement la partie. Sinon, elle va démarrer dans une minute.\n\n**Comment jouer ? : ** le Trivial Versus se joue de 2 à 5 joueurs. Des questions vont se suivre, l'objectif est d'atteindre 5 bonnes réponses avant tout le monde ! Le jeu se déroule dans ce salon et sur ce message. Les propositions sont numérotés de <:ot1:705766186909958185> à <:ot4:705766186947706934>, cliquez sur la réaction qui correspond pour choisir votre réponse. Au bout de 20s ou quand tout le monde a répondu, les résultats sont affichés. La prochaine question démarrera 7s après. Bonne chance !",
            "br":"**Vous avez créé une partie de OT!trivialbr en Cross-Serveur. Vous êtes le propriétaire de la partie.**\n\nAppuyez sur la réaction <:otVALIDER:772766033996021761> pour rejoindre la partie de Trivial Battle Royale et <:otANNULER:811242376625782785> pour annuler votre participation. La personne qui a demandé la partie peut cliquer sur <:otVALIDER:772766033996021761> pour lancer directement la partie. Sinon, elle va démarrer dans une minute.\n\n**Comment jouer ? : ** le Trivial BR se joue de 2 à 15 joueurs. Des questions vont se suivre, l'objectif est d'être le dernier en vie ! Au début vous avez 3 vies, et vous en perdez une par mauvaise réponse. Le jeu se déroule dans ce salon et sur ce message. Les propositions sont numérotés de <:ot1:705766186909958185> à <:ot4:705766186947706934>, cliquez sur la réaction qui correspond pour choisir votre réponse. Au bout de 20s ou quand tout le monde a répondu, les résultats sont affichés. Bonne chance !"}
        else:
            dictHelp={"party":"**Vous avez rejoint une partie de OT!trivialparty en Cross-Serveur. Vous n'êtes pas l'hôte de la partie.**\n\nAppuyez sur la réaction <:otVALIDER:772766033996021761> pour rejoindre la partie de Trivial Party et <:otANNULER:811242376625782785> pour annuler votre participation. La partie va bientôt débuter.\n\n**Comment jouer ? : ** le Trivial Party se joue de 2 à 15 joueurs. Des questions vont se suivre, il faut obtenir 12 points pour gagner ! De manière aléatoire, des évènement peuvent se dérouler pour changer complétement la partie ! Le jeu se déroule dans ce salon et sur ce message. Les propositions sont numérotés de <:ot1:705766186909958185> à <:ot4:705766186947706934>, cliquez sur la réaction qui correspond pour choisir votre réponse. Au bout de 20s ou quand tout le monde a répondu, les résultats sont affichés. La prochaine question démarrera peu de temps après. Bonne chance !",
            "versus":"**Vous avez rejoint une partie de OT!trivialversus en Cross-Serveur. Vous n'êtes pas l'hôte de la partie.**\n\nAppuyez sur la réaction <:otVALIDER:772766033996021761> pour rejoindre la partie de Trivial Party et <:otANNULER:811242376625782785> pour annuler votre participation. La partie va bientôt débuter.\n\n**Comment jouer ? : ** le Trivial Versus se joue de 2 à 5 joueurs. Des questions vont se suivre, l'objectif est d'atteindre 5 bonnes réponses avant tout le monde ! Le jeu se déroule dans ce salon et sur ce message. Les propositions sont numérotés de <:ot1:705766186909958185> à <:ot4:705766186947706934>, cliquez sur la réaction qui correspond pour choisir votre réponse. Au bout de 20s ou quand tout le monde a répondu, les résultats sont affichés. La prochaine question démarrera 7s après. Bonne chance !",
            "br":"**Vous avez rejoint une partie de OT!trivialbr en Cross-Serveur. Vous n'êtes pas l'hôte de la partie.**\n\nAppuyez sur la réaction <:otVALIDER:772766033996021761> pour rejoindre la partie de Trivial Party et <:otANNULER:811242376625782785> pour annuler votre participation. La partie va bientôt débuter.\n\n**Comment jouer ? : ** le Trivial BR se joue de 2 à 15 joueurs. Des questions vont se suivre, l'objectif est d'être le dernier en vie ! Au début vous avez 3 vies, et vous en perdez une par mauvaise réponse. Le jeu se déroule dans ce salon et sur ce message. Les propositions sont numérotés de <:ot1:705766186909958185> à <:ot4:705766186947706934>, cliquez sur la réaction qui correspond pour choisir votre réponse. Au bout de 20s ou quand tout le monde a répondu, les résultats sont affichés. Bonne chance !"}
        maxPlay={"party":7,"br":7,"versus":5}
        message=await ctx.send(embed=createEmbed("Trivial {0}".format(self.option.upper()),dictHelp[self.option],0xad917b,ctx.invoked_with.lower(),ctx.guild))
        gamesTrivial[message.id]=self

        await message.add_reaction("<:otVALIDER:772766033996021761>")
        await message.add_reaction("<:otANNULER:811242376625782785>")

        self.messages.append(message)
        self.memmess[ctx.author.id]=message
        self.guildmess[ctx.guild.id]=message

        if len(self.ids)==maxPlay[self.option]:
            self.playing=True
            await asyncio.sleep(2)

        if not new:
            return False

        annonce=await bot.get_channel(878254347459366952).send("<:otVERT:868535645897912330> Partie de Trivial {0} en recherche de joueurs !".format(self.option.upper()))
        await annonce.publish()
        for i in range(60):
            if not self.playing:
                await asyncio.sleep(1)
            else:
                break
        await annonce.delete()

        self.playing=True
        dictOnline.remove(self)
        for i in self.memmess:
            await self.memmess[i].clear_reactions()
        if len(self.ids)<2:
            for i in self.memmess:
                await i.edit(embed=createEmbed("Trivial {0}".format(self.option.upper()),"Une minute s'est écoulée et personne n'a répondu à l'invitation.",0xad917b,ctx.invoked_with.lower(),ctx.guild))
            for i in self.ids:
                inGame.remove(i)
            return False

        while len(self.ids)>maxPlay[self.option]:
            inGame.remove(self.ids[-1])
            await self.memmess[self.ids[-1]].channel.send("<:otROUGE:868535622237818910> Malheureusement, <@{0}> a rejoint alors que la partie était déjà complète. Veuillez relancer votre recherche.".format(self.ids[-1]))
            del self.ids[-1]

        for i in self.memguild:
            if self.memguild[i] not in self.guilds:
                self.guilds.append(self.memguild[i])
        for i in self.memmess:
            if self.memmess[i] not in self.messages:
                self.messages.append(self.memmess[i])
        for i in self.ids:
            self.addPlayer(bot.get_user(i))

        await self.emotesUser(bot)
        for i in self.messages:
            descip="<:otVERT:868535645897912330> La partie commence pour "
            for j in self.joueurs:
                if self.memmess[j.id].id!=i.id:
                    descip+="{0} / ".format(self.titres[j.id])
                else:
                    descip+="<@{0}> / ".format(j.id)
            await i.channel.send(descip[:-2])

            await pin(i)

            for j in emotes:
                await i.add_reaction(j)
            await i.add_reaction("<:otCOINS:873226814527520809>")
        return message

    def addPlayer(self,joueur):
        super().addPlayer(joueur)
        connexion,curseur=connectSQL("OT","Titres","Titres",None,None)
        self.titres[joueur.id]=getTitre(curseur,joueur.id)
        emote=getEmoteJeux(joueur.id)
        if emote==None:
            self.emotesCustom[joueur.id]=""
        else:
            self.emotesCustom[joueur.id]=emote

    def createEmbed(self,results,guild):
        embedT=discord.Embed(title=self.questionFR, description=self.affichageClassique(), color=0xad917b)
        embedT=auteur(guild.id,guild.name,guild.icon,embedT,"guild")
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
                if self.memguild[i]==guild.id:
                    nom="<@{0}>".format(i)
                    emote=str(self.emotes[i])
                else:
                    nom=self.titres[i]
                    emote=self.emotesCustom[i]
                assert results
                if self.reponses[i]==None or self.vrai==None:
                    descip+="{0} {1} : **{2}**\n".format(emote,nom,self.scores[i])
                elif self.reponses[i]==self.vrai-1:
                    descip+="{0} {1} : **{2}** - {3}\n".format(emote,nom,self.scores[i],emotesTrue[self.reponses[i]])
                else:
                    descip+="{0} {1} : **{2}** - {3}\n".format(emote,nom,self.scores[i],emotesFalse[self.reponses[i]])
            except:
                descip+="{0} {1} : **{2}**\n".format(emote,nom,self.scores[i])
            count+=1
        embedT.add_field(name="Scores", value=descip,inline=True)
        embedT.set_footer(text="OT!trivial{0}cross".format(self.option))
        return embedT

    def embedResults(self,winner,guild):
        descip=""
        for i in self.scores:
            if self.memguild[i]==guild: 
                descip+="{0} <@{1}> : {2} -  {3}\n".format(str(self.emotes[i]),i,self.scores[i],self.histo[i])
            else:
                descip+="{0} {1} : {2} -  {3}\n".format(self.emotesCustom[i],self.titres[i],self.scores[i],self.histo[i])
        if self.memguild[winner.id]==guild:
            embedT=discord.Embed(title="Victoire de {0}".format(winner.name), description=descip, color=0xf2eb16)
            embedT=auteur(winner.id,winner.name,winner.avatar,embedT,"user")
            embedT.add_field(name="<:otCOINS:873226814527520809> gagnés par {0}".format(winner.name),value="{0} <:otCOINS:873226814527520809>".format(len(self.ids)*25+sum(self.mises.values())))
        else:
            embedT=discord.Embed(title="Victoire de {0}".format(self.titres[winner.id]), description=descip, color=0xf2eb16)
            embedT.set_author(name=self.titres[winner.id],icon_url="https://cdn.discordapp.com/emojis/{0}.png".format(emoteDetector(self.emotesCustom[winner.id])[0]))
            embedT.add_field(name="<:otCOINS:873226814527520809> gagnés par {0}".format(self.titres[winner.id]),value="{0} <:otCOINS:873226814527520809>".format(len(self.ids)*25+sum(self.mises.values())))
        embedT.set_footer(text="OT!trivialversuscross")
        return embedT

    async def endGame(self,message,inGame,gamesTrivial):
        try:
            await self.delEmotes()
        except:
            pass
        for i in self.ids:
            inGame.remove(i)
        for i in self.messages:
            del gamesTrivial[i.id]

    async def error(self,ctx,bot,message,inGame,gamesTrivial):
        for i in self.messages:
            await i.channel.send(embed=await exeErrorExcept(ctx,bot,""))
            await unpin(i)
        await self.endGame(message,inGame,gamesTrivial)

    def stats(self,win,option):
        connexionOT,curseurOT=connectSQL("OT","Guild","Guild",None,None)
        for i in self.ids:
            if i==win.id:
                count,state=2,"W"
                gainCoins(i,25*len(self.ids)+sum(self.mises.values()))
            else:
                count,state=-1,"L"
            exeJeuxSQL(i,None,state,"OT",curseurOT,count,option,None)
        connexionOT.commit()
