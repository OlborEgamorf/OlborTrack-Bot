############################################################################

 #######  #########     #########       #######
#       #     #                 #            #     Olbor Track Bot    
#       #     #                 #           #      Créé par OlborEgamorf  
#       #     #         #########          #       Fonctions Trivial
#       #     #         #                 #                  
 #######      #         ############# #  #                         

############################################################################

import asyncio
import html
import sqlite3
import sys
from random import choice, randint
from time import strftime

import discord
from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.DichoTri import triID
from Core.Fonctions.Embeds import embedAssert, exeErrorExcept, createEmbed
from Stats.SQL.Compteur import compteurSQL, compteurTrivialS
from Stats.SQL.ConnectSQL import connectSQL
from Stats.SQL.Execution import exeJeuxSQL

emotes=["<:ot1:705766186909958185>","<:ot2:705766186989912154>","<:ot3:705766186930929685>","<:ot4:705766186947706934>"]
emotesTrue=["<:ot1VRAI:773993429130149909>", "<:ot2VRAI:773993429050195979>", "<:ot3VRAI:773993429331738624>", "<:ot4VRAI:773993429423095859>"]
emotesFalse=["<:ot1FAUX:773993429315092490>", "<:ot2FAUX:773993429172486145>", "<:ot3FAUX:773993429402779698>", "<:ot4FAUX:773993429373026354>"]
listeNoms=["Culture","Divertissement","Sciences","Mythologie","Sport","Géographie","Histoire","Politique","Art","Célébrités","Animaux","Véhicules","Global"]
dictCateg={9:0,10:1,11:1,12:1,13:1,14:1,15:1,16:1,17:2,18:2,19:2,20:3,21:4,22:5,23:6,24:7,25:8,26:9,27:10,28:11,29:1,30:2,31:1,32:1}
dictDiff={"easy":"Facile (+10)","medium":"Moyenne (+15)","hard":"Difficile (+25)"}
gamesTrivial={}
inGameTrivial=[]
dictNomsVal={"culture":9,"divertissement":choice([10,11,12,13,14,15,16,29,31,32]),"sciences":choice([17,18,19,30]),"mythologie":20,"sport":21,"géographie":22,"histoire":23,"politique":24,"art":25,"célébrités":26,"animaux":27,"véhicules":28,"livres":10,"films":11,"musique":12,"anime":31,"manga":31}

class Question:
    def __init__(self,author,option):
        self.author=author
        self.option=option

        self.table=None
        self.categ=None
        self.diff=None
        self.arg=None
        self.questionFR=None
        self.questionEN=None
        self.vrai=None
        self.multi=None
        self.user=None
        self.auteur=None

    def newQuestion(self):
        connexion,curseur=connectSQL("OT","trivial","Trivial",None,None)
        table=curseur.execute("SELECT * FROM français WHERE Type='{0}' AND Difficulté='{1}' ORDER BY RANDOM()".format(self.arg,self.diff)).fetchone()
        tableENG=curseur.execute("SELECT * FROM anglais WHERE ID={0}".format(table["ID"])).fetchone()
        choix=[1,2,3,4]
        tableQuestion=[]
        for i in range(3):
            nb=choice(choix)
            choix.remove(nb)
            if tableENG!=None:
                tableQuestion.append({"ID":nb,"Reponse":html.unescape(tableENG["Mauvaise{0}".format(i+1)]),"Correct":False,"Trad":html.unescape(table["Mauvaise{0}".format(i+1)])})
            else:
                tableQuestion.append({"ID":nb,"Reponse":None,"Correct":False,"Trad":html.unescape(table["Mauvaise{0}".format(i+1)])})
        
        if tableENG!=None:
            tableQuestion.append({"ID":choix[0],"Reponse":html.unescape(tableENG["Bonne"]),"Correct":True,"Trad":html.unescape(table["Bonne"])})
        else:
            tableQuestion.append({"ID":choix[0],"Reponse":None,"Correct":True,"Trad":html.unescape(table["Bonne"])})
        if self.option=="br":
            tableQuestion.append({"ID":4,"Reponse":"Fake","Correct":False,"Trad":"Fake"})
        tableQuestion.sort(key=triID)
        self.table=tableQuestion
        self.questionFR=html.unescape(table["Question"])
        if tableENG!=None:
            self.questionEN=html.unescape(tableENG["Question"])
        self.vrai=choix[0]
        self.auteur=table["Auteur"]
        #print(self.vrai)

    def setUser(self):
        connexion,curseur=connectSQL("OT",self.author.id,"Trivial",None,None)
        curseur.execute("CREATE TABLE IF NOT EXISTS trivial{0} (ID BIGINT, IDCateg INT, Categ TEXT, Exp INT, Niveau INT, Next INT, Multi INT)".format(self.author.id))
        user=curseur.execute("SELECT * FROM trivial{0}".format(self.author.id)).fetchall()
        if user==[]:
            user=[{"ID":self.author.id,"IDCateg":i,"Categ":listeNoms[i],"Exp":0,"Niveau":1,"Next":30,"Multi":0} for i in range(len(listeNoms))]
            many=[tuple(i.values()) for i in user]
            curseur.executemany("INSERT INTO trivial{0} VALUES (?,?,?,?,?,?,?)".format(self.author.id),many)
            connexion.commit()
        self.user=user
        self.multi=round(1+user[12]["Multi"]*0.05+user[self.categ]["Multi"]*0.02,2)
    
    def setCateg(self,args):
        try:
            arg=dictNomsVal[args[0].lower()]
        except:
            arg=randint(9,32)
        self.arg=arg
        self.categ=dictCateg[arg]
    
    def setDiff(self):
        if self.user[self.categ]["Niveau"]==1:
            self.diff="easy"
        elif self.user[self.categ]["Niveau"]<=3:
            self.diff=choice(["easy","medium","medium"])
        else:
            self.diff=choice(["easy","medium","medium","hard","hard","hard"])

    def affichageClassique(self):
        descip=""
        for i in range(4):
            if self.table[i]["Reponse"]!=None:
                descip+="{0} {1} `({2})`\n".format(emotes[i],self.table[i]["Trad"],self.table[i]["Reponse"])
            else:
                descip+="{0} {1}\n".format(emotes[i],self.table[i]["Trad"])
        if self.questionEN!=None:
            descip+="\n||`({0})`||".format(self.questionEN)
        return descip

    def affichageWin(self):
        descip="**Bonne réponse ! **\n"
        trad=""
        for i in range(4):
            if self.table[i]["Reponse"]!=None:
                trad="`({0})`".format(self.table[i]["Reponse"])
            if i==self.vrai-1:
                descip+="{0} {1} {2}\n".format(emotesTrue[i],self.table[i]["Trad"],trad)
            else:
                descip+="{0} {1} {2}\n".format(emotes[i],self.table[i]["Trad"],trad)
        return descip

    def affichageLose(self,emoji):
        choix={705766186909958185:0,705766186989912154:1,705766186930929685:2,705766186947706934:3,473254057511878656:4,None:666}
        descip="**Raté !**\n"
        trad=""
        for i in range(4):
            if self.table[i]["Reponse"]!=None:
                trad="`({0})`".format(self.table[i]["Reponse"])
            if i==choix[emoji]:
                descip+="{0} {1} {2}\n".format(emotesFalse[i],self.table[i]["Trad"],trad)
            elif i==self.vrai-1:
                descip+="{0} {1} {2}\n".format(emotesTrue[i],self.table[i]["Trad"],trad)
            else:
                descip+="{0} {1} {2}\n".format(emotes[i],self.table[i]["Trad"],trad)
        return descip
    
    def gestionMulti(self,victoire):
        categ,multi,diff,author=self.categ,self.multi,self.diff,self.author.id
        points={"easy":10,"medium":15,"hard":25}
        niveaux=[30, 60, 100, 150, 200, 400, 600, 1000, 1500, 2000, 3000, 4000, 5000, 7500, 10000, 20000, 30000, 40000, 50000, 100000, 1000000]
        connexion,curseur=connectSQL("OT",author,"Trivial",None,None)
        table=curseur.execute("SELECT * FROM trivial{0}".format(author)).fetchall()
        if victoire:
            curseur.execute("UPDATE trivial{0} SET Multi={1} WHERE IDCateg={2}".format(author,table[categ]["Multi"]+1,categ))
            curseur.execute("UPDATE trivial{0} SET Multi={1} WHERE IDCateg=12".format(author,table[12]["Multi"]+1))

            curseur.execute("UPDATE trivial{0} SET Exp={1} WHERE IDCateg={2}".format(author,table[categ]["Exp"]+points[diff]*multi,categ))
            curseur.execute("UPDATE trivial{0} SET Exp={1} WHERE IDCateg=12".format(author,table[12]["Exp"]+points[diff]*multi))

            count=0
            while curseur.execute("SELECT Exp FROM trivial{0} WHERE IDCateg={1}".format(author,categ)).fetchone()["Exp"]>=curseur.execute("SELECT Next FROM trivial{0} WHERE IDCateg={1}".format(author,categ)).fetchone()["Next"]:
                count+=1
                curseur.execute("UPDATE trivial{0} SET Next={1} WHERE IDCateg={2}".format(author,niveaux[table[categ]["Niveau"]+count-1],categ))
                curseur.execute("UPDATE trivial{0} SET Niveau={1} WHERE IDCateg={2}".format(author,table[categ]["Niveau"]+count,categ))

            count=0
            while curseur.execute("SELECT Exp FROM trivial{0} WHERE IDCateg=12".format(author)).fetchone()["Exp"]>=curseur.execute("SELECT Next FROM trivial{0} WHERE IDCateg=12".format(author)).fetchone()["Next"]:
                count+=1
                curseur.execute("UPDATE trivial{0} SET Next={1} WHERE IDCateg=12".format(author,niveaux[table[categ]["Niveau"]+count-1]))
                curseur.execute("UPDATE trivial{0} SET Niveau={1} WHERE IDCateg=12".format(author,table[categ]["Niveau"]+count))
            connexion.commit()

            connexion,curseur=connectSQL("OT","ranks","Trivial",None,None)
            compteurSQL(curseur,"trivial{0}".format(categ),author,(0,author,categ,"TO","GL",points[diff]*multi),points[diff]*multi,None,None,None,None,None,2,None)
            compteurSQL(curseur,"trivial12",author,(0,author,12,"TO","GL",points[diff]*multi),points[diff]*multi,None,None,None,None,None,2,None)
        else:
            curseur.execute("UPDATE trivial{0} SET Multi=0 WHERE IDCateg={1}".format(author,categ))
            curseur.execute("UPDATE trivial{0} SET Multi=0 WHERE IDCateg=12".format(author))

        inGameTrivial.remove(author)
        connexion.commit()

    def createEmbed(self):
        embedT=discord.Embed(title=self.questionFR, description=self.affichageClassique(), color=0xad917b)
        embedT.set_footer(text="OT!trivial")
        embedT=auteur(self.author.id,self.author.name,self.author.avatar,embedT,"user")
        embedT.add_field(name="Catégorie", value=listeNoms[dictCateg[self.arg]], inline=True)
        embedT.add_field(name="Difficulté", value=dictDiff[self.diff], inline=True)
        embedT.add_field(name="Multiplicateur", value=str(self.multi),inline=True)
        embedT.add_field(name="Auteur",value="[{0}](https://forms.gle/RNTGn9tds2LGVkdU8)".format(self.auteur),inline=True)
        return embedT

    async def timer(self,message,bot,ctx):
        await asyncio.sleep(20)
        try:
            newMessage=await message.channel.fetch_message(message.id)
        except:
            return
        if newMessage.embeds[0].color==discord.Colour(0xad917b):
            await newMessage.clear_reactions()
            newMessage.embeds[0].description=self.affichageLose(None)
            newMessage.embeds[0].colour=0xcf1742
            self.gestionMulti(False)
            await newMessage.edit(embed=newMessage.embeds[0])
        return


class Streak(Question):
    def __init__(self, author):
        self.serie=0
        self.temps=20
        self.rota=["culture","divertissement","sciences","mythologie","sport","géographie","histoire","politique","art","célébrités","animaux","véhicules"]
        super().__init__(author,"streak")
        self.record=self.getRecord()

    def setDiff(self):
        if self.serie<=2:
            self.diff="easy"
        elif self.serie<=4:
            self.diff="medium"
        else:
            self.diff="hard"

    def setCateg(self, args):
        if self.rota==[]:
            self.rota=["culture","divertissement","sciences","mythologie","sport","géographie","histoire","politique","art","célébrités","animaux","véhicules"]
        arg=choice(self.rota)
        self.rota.remove(arg)
        super().setCateg(arg)

    def createEmbed(self):
        embedT=super().createEmbed()
        embedT.set_footer(text="OT!trivialstreak")
        embedT.add_field(name="Bonnes réponses", value=str(self.serie),inline=True)
        embedT.add_field(name="Temps pour répondre", value="{0} secondes".format(self.temps),inline=True)
        embedT.add_field(name="Record", value=self.record,inline=True)
        return embedT
    
    def changeTime(self):
        if self.serie%2==0 and self.temps>12:
            self.temps-=1

    async def timer(self,message,bot,ctx):
        serie=self.serie
        await asyncio.sleep(self.temps)
        try:
            newMessage=await message.channel.fetch_message(message.id)
        except:
            return
        if newMessage.embeds[0].color==discord.Colour(0xad917b):
            if self.serie==serie:
                await newMessage.clear_reactions()
                newMessage.embeds[0].description=self.affichageLose(None)
                newMessage.embeds[0].colour=0xcf1742
                self.gestionMulti(False)
                await newMessage.edit(embed=newMessage.embeds[0])
        return
       
    def getRecord(self):
        connexion,curseur=connectSQL("OT","ranks","Trivial",None,None)
        curseur.execute("CREATE TABLE IF NOT EXISTS trivialStreak (Rank INT, ID BIGINT PRIMARY KEY, IDComp BIGINT, Mois TEXT, Annee TEXT, Count INT)")
        etat=curseur.execute("SELECT * FROM trivialStreak WHERE ID={0}".format(self.author.id)).fetchone()
        if etat==None:
            return "Aucun"
        else:
            return "{0} - {1}e".format(etat["Count"],etat["Rank"])


class Versus(Question):
    def __init__(self,guild,option):
        self.joueurs=[]
        self.ids=[]
        self.emotes={}
        self.reponses={}
        self.scores={}
        self.histo={}
        self.tour=0
        self.guild=guild
        self.playing=False
        self.max=5
        self.rota=[]
        self.invoke=None
        super().__init__(None,option)

    async def startGame(self,ctx,bot):
        self.ids.append(ctx.author.id)
        self.invoke=ctx.author.id
        inGameTrivial.append(ctx.author.id)
        dictHelp={"party":"Appuyez sur la réaction <:otVALIDER:772766033996021761> pour rejoindre la partie de Trivial Party et <:otANNULER:811242376625782785> pour annuler votre participation. La personne qui a demandé la partie peut cliquer sur <:otVALIDER:772766033996021761> pour lancer directement la partie. Sinon, elle va démarrer dans une minute.\n\n**Comment jouer ? : ** le Trivial Party se joue de 2 à 15 joueurs. Des questions vont se suivre, il faut obtenir 15 points pour gagner ! De manière aléatoire, des évènement peuvent se dérouler pour changer complétement la partie ! Le jeu se déroule dans ce salon et sur ce message. Les propositions sont numérotés de <:ot1:705766186909958185> à <:ot4:705766186947706934>, cliquez sur la réaction qui correspond pour choisir votre réponse. Au bout de 20s ou quand tout le monde a répondu, les résultats sont affichés. La prochaine question démarrera peu de temps après. Bonne chance !","versus":"Appuyez sur la réaction <:otVALIDER:772766033996021761> pour rejoindre la partie de Trivial Versus et <:otANNULER:811242376625782785> pour annuler votre participation. La personne qui a demandé la partie peut cliquer sur <:otVALIDER:772766033996021761> pour lancer directement la partie. Sinon, elle va démarrer dans une minute.\n\n**Comment jouer ? : ** le Trivial Versus se joue de 2 à 5 joueurs. Des questions vont se suivre, l'objectif est d'atteindre 5 bonnes réponses avant tout le monde ! Le jeu se déroule dans ce salon et sur ce message. Les propositions sont numérotés de <:ot1:705766186909958185> à <:ot4:705766186947706934>, cliquez sur la réaction qui correspond pour choisir votre réponse. Au bout de 20s ou quand tout le monde a répondu, les résultats sont affichés. La prochaine question démarrera 7s après. Bonne chance !","br":"Appuyez sur la réaction <:otVALIDER:772766033996021761> pour rejoindre la partie de Trivial Battle Royale et <:otANNULER:811242376625782785> pour annuler votre participation. La personne qui a demandé la partie peut cliquer sur <:otVALIDER:772766033996021761> pour lancer directement la partie. Sinon, elle va démarrer dans une minute.\n\n**Comment jouer ? : ** le Trivial BR se joue de 2 à 15 joueurs. Des questions vont se suivre, l'objectif est d'être le dernier en vie ! Au début vous avez 3 vies, et vous en perdez une par mauvaise réponse. Le jeu se déroule dans ce salon et sur ce message. Les propositions sont numérotés de <:ot1:705766186909958185> à <:ot4:705766186947706934>, cliquez sur la réaction qui correspond pour choisir votre réponse. Au bout de 20s ou quand tout le monde a répondu, les résultats sont affichés. Bonne chance !"}
        message=await ctx.send(embed=createEmbed("Trivial {0}".format(self.option.upper()),dictHelp[self.option],0xad917b,ctx.invoked_with.lower(),ctx.guild))
        gamesTrivial[message.id]=self
        await message.add_reaction("<:otVALIDER:772766033996021761>")
        #await message.add_reaction("<:pepoG:825979653876482048>")
        #await message.add_reaction("<:KappaAngry:662410175097077780>")
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
                inGameTrivial.remove(i)
            return False
        else:
            for i in self.ids:
                user=ctx.guild.get_member(i)
                self.addPlayer(user)
            await self.emotesUser(bot)
            descip="La partie commence "
            for i in self.ids:
                descip+="<@{0}> ".format(i)
            await message.channel.send(descip)
            try:
                await message.pin()
            except:
                pass
            for i in emotes:
                await message.add_reaction(i)
            return message

    async def endGame(self,message):
        try:
            await self.delEmotes()
        except:
            pass
        for i in self.ids:
            inGameTrivial.remove(i)
        del gamesTrivial[message.id]

    async def emotesUser(self,bot):
        idServ=[759688015676309525,759690251521622016,776417458386763778,776417488698212383]
        for i in self.joueurs:
            for j in range(4):
                try:
                    emote=await bot.get_guild(idServ[j]).create_custom_emoji(name=i.name.split(" ")[0],image=await i.avatar_url_as(size=128).read(),roles=None,reason=None)
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
        return embedT

    async def error(self,ctx,bot,message):
        await ctx.send(embed=await exeErrorExcept(ctx,bot,""))
        await self.endGame(message)

    def stats(self,win,option):
        connexionGuild,curseurGuild=connectSQL(self.guild.id,"Guild","Guild",None,None)
        connexionOT,curseurOT=connectSQL("OT","Guild","Guild",None,None)
        for i in self.ids:
            if i==win.id:
                count,state=2,"W"
            else:
                count,state=-1,"L"
            exeJeuxSQL(i,None,state,self.guild.id,curseurGuild,count,option,None)
            exeJeuxSQL(i,None,state,"OT",curseurOT,count,option,None)
        connexionGuild.commit()
        connexionOT.commit()

class Party(Versus):
    def __init__(self, guild,option):
        super().__init__(guild,option)
        self.max=15
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
        dictDescip={"malus":"Les mauvaises réponses font **perdre des points** !","double":"Chaque bonne réponse vaut **4 points** !","triple":"Chaque bonne réponse vaut **6 points** !","10s":"Vous avez seulement **10 secondes** pour répondre. Ne pas répondre fait perdre **1 point** !","solo":"<@{0[0]}> est le seul à répondre ! Si il répond juste il gagne **4 points**, sinon tout le monde récupére **2 points** et lui en **perd 1** !","ratio":"Plus il y a de gens qui répondent juste, moins la question a de valeur !","theme1":"<@{0[0]}> a la chance de choisir le thème de la prochaine question !","themeA":"Tout le monde peut voter pour le choix du prochain thème !","speed":"Le premier qui répond juste gagne **3 points** ! Attention : répondre faux fera perdre **1 point** !","diff1":"<@{0[0]}> a la chance de choisir la difficulté de la prochaine question !","diffA":"Tout le monde peut voter pour le choix de la difficulté de la prochaine question !","duo":"<@{0[0]}> et <@{0[1]}> sont les seuls à répondre ! Ils doivent tout les deux répondre juste pour gagner chacun **3 points**. En cas d'échec, ils perdront **1 point** et tout le monde en gagnera **2** !","vol":"<@{0[0]}> est le seul à répondre ! Si il répond juste, il choisiera un joueur à qui il volera **3 points** !","speedfinal":"{0} ont atteint les 15 points et sont finalistes ! Seul eux peuvent répondre, c'est une question de rapidité et en cas d'échec, ils retombent à 13 points !"}
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
        return embedT

    def createEmbed(self,results,event):
        dictTitre={"malus":"Question malus","double":"Points x2","triple":"Points x3","10s":"Temps réduit","solo":"Question solo","ratio":"Points rationalisés","theme1":"Choix de thème","themeA":"Vote de thème","speed":"Rapidité","diff1":"Choix de difficulté","diffA":"Vote de difficulté","duo":"Question duo","vol":"Vol de points","speedfinal":"FINALE",None:"Aucun"}
        embed=super().createEmbed(results)
        embed.add_field(name="Évènement",value=dictTitre[event])
        return embed


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
        return embedT


async def attente(game:Versus,temps,event):
    time,done=0,False
    while time!=temps and not done:
        await asyncio.sleep(0.5)
        if event in ("speed","speedfinal"):
            count=len(game.reponses)
        else:
            done=True
        for j in game.reponses:
            if event=="speed" or event=="speedfinal":
                if game.reponses[j]!=None and game.reponses[j]==game.vrai-1:
                    done=True
                elif game.reponses[j]==None:
                    count-=1
            else:
                if game.reponses[j]==None:
                    done=False
        if event in ("speed","speedfinal"):
            if count==len(game.reponses):
                done=True
        time+=0.5

async def trivialParty(ctx,bot):
    try:
        assert ctx.author.id not in inGameTrivial, "Terminez votre question en cours avant de lancer ou rejoindre une partie."
        game=Party(ctx.guild,"party")
        message=await game.startGame(ctx,bot)
        if message==False:
            return
        if len(game.joueurs)<4:
            game.event.remove("duo")
        while game.playing:
            liste=[]
            for i in game.scores:
                if game.scores[i]>=15:
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
                    user.append(choix.id)
                    listeJoueurs.remove(user[i])
                game.reponses={i:None for i in user}
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
                        game.scores[i]=13
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
            if len(end)!=0:
                await message.clear_reactions()
                await message.channel.send(embed=game.embedResults(end[0]))
                await message.unpin()
                game.playing=False
                game.stats(end[0],"TrivialParty")
            
            game.tour+=1
            await asyncio.sleep(7)
        await game.endGame(message)
    except AssertionError as er:
        await ctx.send(embed=embedAssert(er))
    except:
        await game.error(ctx,bot,message)

async def trivialVersus(ctx,bot):
    try:
        assert ctx.author.id not in inGameTrivial, "Terminez votre question en cours avant de lancer ou rejoindre une partie."
        game=Versus(ctx.guild,"versus")
        message=await game.startGame(ctx,bot)
        if message==False:
            return
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
            if len(count)==1:
                await message.clear_reactions()
                await message.channel.send(embed=game.embedResults(count[0]))
                await message.unpin()
                game.playing=False
                game.stats(count[0],"TrivialVersus")
            elif len(count)>1:
                game.max+=1
            game.tour+=1
            await asyncio.sleep(7)
        await game.endGame(message)
    except AssertionError as er:
        await ctx.send(embed=embedAssert(er))
    except:
        await game.error(ctx,bot,message)

async def trivialBattleRoyale(ctx,bot):
    try:
        assert ctx.author.id not in inGameTrivial, "Terminez votre question en cours avant de lancer ou rejoindre une partie."
        game=BattleRoyale(ctx.guild,"br")
        message=await game.startGame(ctx,bot)
        if message==False:
            return
        game.restants=game.ids.copy()
        while game.playing:
            game.reponses={i:None for i in game.ids}
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
                        game.restants.remove(i)
            
            embedT=game.createEmbed(True)
            if good>0:
                embedT.colour=0x47b03c
                embedT.description="**{0} personnes ont eu juste !** {1}".format(good,game.affichageWin()[20:-1])
            else:
                embedT.colour=0xcf1742
                embedT.description="**Tout le monde s'est trompé...** {0}".format(game.affichageLose(None)[10:-1])
            await message.edit(embed=embedT)
            if len(game.restants)==1:
                game.histo[game.restants[0]]=1
                await message.clear_reactions()
                await message.channel.send(embed=game.embedResults(game.guild.get_member(game.restants[0])))
                await message.unpin()
                game.playing=False
                game.stats(game.guild.get_member(game.restants[0]),"TrivialBR")
            game.tour+=1
            await asyncio.sleep(5)
            await message.edit(embed=game.embedHub())
            await asyncio.sleep(5)
        await game.endGame(message)
    except AssertionError as er:
        await ctx.send(embed=embedAssert(er))
    except:
        await game.error(ctx,bot,message)


async def embedTrivial(arg,ctx,bot,author,option):
    try:
        assert author.id not in inGameTrivial, "Vous êtes déjà en train de répondre à une question !"
        inGameTrivial.append(author.id)
        if option=="classic":
            question=Question(author,option)
        elif option=="streak":
            if ctx.message.id in gamesTrivial:
                question=gamesTrivial[ctx.message.id]
            else:
                question=Streak(author)
        question.setCateg(arg)
        question.setUser()
        question.setDiff()
        question.newQuestion()
        embedT=question.createEmbed()
    except AssertionError as er:
        await ctx.send(embed=embedAssert(er))
    except sqlite3.OperationalError as er:
        await asyncio.sleep(0.2)
        inGameTrivial.remove(author.id)
        await embedTrivial(arg,ctx,bot,author,option)
    except:
        await ctx.send(embed=await exeErrorExcept(ctx,bot,""))
    else:
        if option=="streak" and question.serie!=0:
            await ctx.message.edit(embed=embedT)
            message=ctx.message
        else:
            message=await ctx.send(embed=embedT)
            gamesTrivial[message.id]=question
            for i in emotes:
                await message.add_reaction(i)
        bot.loop.create_task(question.timer(message,bot,ctx))

async def trivialReact(message,client,emoji,user,guild,reaction):
    choix={705766186909958185:0,705766186989912154:1,705766186930929685:2,705766186947706934:3,473254057511878656:4}
    if message.id in gamesTrivial:
        tableQuestion=gamesTrivial[message.id]
        if type(tableQuestion) in (Question,Streak):
            if user.id!=tableQuestion.author.id:
                return
        elif type(tableQuestion) in (Versus,Party,BattleRoyale):
            if user.id in tableQuestion.reponses:
                if tableQuestion.reponses[user.id]==None:
                    tableQuestion.reponses[user.id]=choix[emoji.id]
            if not user.bot:
                await reaction.remove(user)
            return
        if tableQuestion.vrai==choix[emoji.id]+1:
            tableQuestion.gestionMulti(True)
            if tableQuestion.option=="classic":
                await message.clear_reactions()
                message.embeds[0].colour=0x47b03c
                message.embeds[0].description=tableQuestion.affichageWin()
            elif tableQuestion.option=="streak":
                tableQuestion.serie+=1
                tableQuestion.changeTime()
                await reaction.remove(user)
                await embedTrivial(None,await client.get_context(message),client,user,"streak")
                return
        else:
            await message.clear_reactions()
            message.embeds[0].colour=0xcf1742
            message.embeds[0].description=tableQuestion.affichageLose(emoji.id)
            tableQuestion.gestionMulti(False)
            if tableQuestion.option=="streak":
                results=compteurTrivialS(tableQuestion.author.id,(0,tableQuestion.author.id,13,"TO","GL",tableQuestion.serie),tableQuestion.serie)
                if results[0]:
                    await message.channel.send("Bravo ! Vous avez battu votre record de série avec **{0}** bonnes réponses ! Votre ancien score était **{1}** bonnes réponses.".format(results[1],results[2]))
            del gamesTrivial[message.id]
        await message.edit(embed=message.embeds[0])
        return
    else:
        return

async def cancelGameTrivial(message,user,reaction):
    if message.id in gamesTrivial:
        game=gamesTrivial[message.id]
        if user.id not in game.ids:
            if not user.bot:
                await reaction.remove(user)
            return
        inGameTrivial.remove(user.id)
        game.ids.remove(user.id)
        await message.channel.send("<@{0}> ne souhaite plus jouer.".format(user.id))
        await reaction.remove(user)
    

async def joinVersus(message,user,reaction):
    try:
        if user.bot:
            return
        assert message.id in gamesTrivial
        game=gamesTrivial[message.id]
        if user.id==game.invoke and user.id in game.ids:
            game.playing=True
            return
        assert user.id not in game.ids
        assert user.id not in inGameTrivial
        game.ids.append(user.id)
        inGameTrivial.append(user.id)
        if type(game)==Versus:
            if len(game.ids)==5:
                game.playing=True
        else:
            if len(game.ids)==15:
                game.playing=True
        await message.channel.send("<@{0}> rejoint la partie !".format(user.id))
        await reaction.remove(user)
    except:
        pass
