import discord
from Core.Fonctions.AuteurIcon import auteur
from Jeux.CrossServeur.ClasseTrivialVSCross import VersusCross
from Stats.SQL.EmoteDetector import emoteDetector
from random import choice

emotes=["<:ot1:705766186909958185>","<:ot2:705766186989912154>","<:ot3:705766186930929685>","<:ot4:705766186947706934>"]

class PartyCross(VersusCross):
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
    
    def affichageChoix(self,liste,titre,guild):
        embed=discord.Embed(title=titre,color=0xad917b)
        embed=auteur(guild.id,guild.name,guild.icon,embed,"guild")
        descip=""
        for i in self.ids:
            if self.memguild[i]==guild.id:
                descip+="{0} <@{1}> : **{2}**\n".format(str(self.emotes[i]),i,self.scores[i])
            else:
                descip+="{0} {1} : **{2}**\n".format(self.emotesCustom[i],self.titres[i],self.scores[i])
        embed.add_field(name="Scores", value=descip,inline=True)
        embed.add_field(name="Question n°", value=str(self.tour+1),inline=True)
        descip=""
        for i in range(len(liste)):
            descip+="{0} {1}\n".format(emotes[i],liste[i])
        embed.description=descip
        embed.set_footer(text="OT!trivial{0}".format(self.option))
        return embed
    
    def affichageEvent(self,event,users,guild):
        dictDescip={"malus":"Les mauvaises réponses font **perdre des points** !","double":"Chaque bonne réponse vaut **4 points** !","triple":"Chaque bonne réponse vaut **6 points** !","10s":"Vous avez seulement **10 secondes** pour répondre. Ne pas répondre fait perdre **1 point** !","solo":"{0[0]} est le seul à répondre ! Si il répond juste il gagne **4 points**, sinon tout le monde récupére **2 points** et lui en **perd 1** !","ratio":"Plus il y a de gens qui répondent juste, moins la question a de valeur !","theme1":"{0[0]} a la chance de choisir le thème de la prochaine question !","themeA":"Tout le monde peut voter pour le choix du prochain thème !","speed":"Le premier qui répond juste gagne **3 points** ! Attention : répondre faux fera perdre **1 point** !","diff1":"{0[0]} a la chance de choisir la difficulté de la prochaine question !","diffA":"Tout le monde peut voter pour le choix de la difficulté de la prochaine question !","duo":"{0[0]} et {0[1]} sont les seuls à répondre ! Ils doivent tout les deux répondre juste pour gagner chacun **3 points**. En cas d'échec, ils perdront **1 point** et tout le monde en gagnera **2** !","vol":"{0[0]} est le seul à répondre ! Si il répond juste, il choisiera un joueur à qu'il volera **3 points** !","speedfinal":"{0} a (ont) atteint les 12 points et est (sont) finaliste(s) ! Seul lui (eux) peu(ven)t répondre, c'est une question de rapidité et en cas d'échec, il(s) retombe(nt) à 10 points !"}
        dictTitre={"malus":"question malus","double":"points doubles","triple":"points TRIPLES","10s":"temps réduit","solo":"question solo","ratio":"points rationalisés","theme1":"choix de thème","themeA":"vote de thème","speed":"rapidité","diff1":"choix de difficulté","diffA":"vote de difficulté","duo":"question duo","vol":"vol de points","speedfinal":"finale"}
        embedT=discord.Embed(title="Évènement : {0} !".format(dictTitre[event]), description=dictDescip[event].format(users), color=0xad917b)
        embedT=auteur(guild.id,guild.name,guild.icon,embedT,"guild")
        embedT.set_footer(text="OT!trivialparty")
        return embedT
    
    def embedResults(self,winner,guild):
        descip=""
        for i in self.scores:
            if self.memguild[i]==guild: 
                descip+="{0} <@{1}> : {2}\n".format(str(self.emotes[i]),i,self.scores[i])
            else:
                descip+="{0} {1} : {2}\n".format(self.emotesCustom[i],self.titres[i],self.scores[i])
        if self.memguild[winner.id]==guild:
            embedT=discord.Embed(title="Victoire de {0}".format(winner.name), description=descip, color=0xf2eb16)
            embedT=auteur(winner.id,winner.name,winner.avatar,embedT,"user")
        else:
            embedT=discord.Embed(title="Victoire de {0}".format(self.titres[winner.id]), description=descip, color=0xf2eb16)
            embedT.set_author(name=self.titres[winner.id],icon_url="https://cdn.discordapp.com/emojis/{0}.png".format(emoteDetector(self.emotesCustom[winner.id])[0]))
            
        embedT.set_footer(text="OT!trivialparty")
        embedT.add_field(name="<:otCOINS:873226814527520809> gagnés par {0}".format(winner.name),value="{0} <:otCOINS:873226814527520809>".format(len(self.ids)*25+sum(self.mises.values())))
        return embedT

    def createEmbed(self,results,event,guild):
        dictTitre={"malus":"Question malus","double":"Points x2","triple":"Points x3","10s":"Temps réduit","solo":"Question solo","ratio":"Points rationalisés","theme1":"Choix de thème","themeA":"Vote de thème","speed":"Rapidité","diff1":"Choix de difficulté","diffA":"Vote de difficulté","duo":"Question duo","vol":"Vol de points","speedfinal":"FINALE",None:"Aucun"}
        embed=super().createEmbed(results,guild)
        embed.add_field(name="Évènement",value=dictTitre[event])
        return embed