import asyncio
import html
import sqlite3
from random import choice, randint

import discord
from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.DichoTri import triID
from Core.Fonctions.Embeds import embedAssert, exeErrorExcept
from Stats.SQL.Compteur import compteurSQL
from Stats.SQL.ConnectSQL import connectSQL
from Titres.Outils import gainCoins, titresTrivial

emotes=["<:ot1:705766186909958185>","<:ot2:705766186989912154>","<:ot3:705766186930929685>","<:ot4:705766186947706934>"]
emotesTrue=["<:ot1VRAI:773993429130149909>", "<:ot2VRAI:773993429050195979>", "<:ot3VRAI:773993429331738624>", "<:ot4VRAI:773993429423095859>"]
emotesFalse=["<:ot1FAUX:773993429315092490>", "<:ot2FAUX:773993429172486145>", "<:ot3FAUX:773993429402779698>", "<:ot4FAUX:773993429373026354>"]
listeNoms=["Culture","Divertissement","Sciences","Mythologie","Sport","Géographie","Histoire","Politique","Art","Célébrités","Animaux","Véhicules","Global"]
dictCateg={9:0,10:1,11:1,12:1,13:1,14:1,15:1,16:1,17:2,18:2,19:2,20:3,21:4,22:5,23:6,24:7,25:8,26:9,27:10,28:11,29:1,30:2,31:1,32:1}
dictDiff={"easy":"Facile (+10)","medium":"Moyenne (+15)","hard":"Difficile (+25)"}

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
        multi=round(1+user[12]["Multi"]*0.05+user[self.categ]["Multi"]*0.02,2)
        if multi>3:
            self.multi=3
        else:
            self.multi=multi
    
    def setCateg(self,args):
        dictNomsVal={"culture":9,"divertissement":choice([10,11,12,13,14,15,16,29,31,32]),"sciences":choice([17,18,19,30]),"mythologie":20,"sport":21,"géographie":22,"histoire":23,"politique":24,"art":25,"célébrités":26,"animaux":27,"véhicules":28,"livres":10,"films":11,"musique":12,"anime":31,"manga":31}
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
    
    def gestionMulti(self,victoire,inGame):
        categ,multi,diff,author=self.categ,self.multi,self.diff,self.author.id
        points={"easy":10,"medium":15,"hard":25}
        niveaux=[30, 60, 100, 150, 200, 400, 600, 1000, 1500, 2000, 3000, 4000, 5000, 7500, 10000, 20000, 30000, 40000, 50000, 100000, 1000000]
        gainCoins(author,points[diff]*multi)
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
                if table[categ]["Niveau"]+count in (5,10):
                    try:
                        titresTrivial(table[categ]["Niveau"]+count,categ,author)
                    except:
                        pass

            count=0
            while curseur.execute("SELECT Exp FROM trivial{0} WHERE IDCateg=12".format(author)).fetchone()["Exp"]>=curseur.execute("SELECT Next FROM trivial{0} WHERE IDCateg=12".format(author)).fetchone()["Next"]:
                count+=1
                curseur.execute("UPDATE trivial{0} SET Next={1} WHERE IDCateg=12".format(author,niveaux[table[12]["Niveau"]+count-1]))
                curseur.execute("UPDATE trivial{0} SET Niveau={1} WHERE IDCateg=12".format(author,table[12]["Niveau"]+count))
                if table[12]["Niveau"]+count in (5,10):
                    try:
                        titresTrivial(table[12]["Niveau"]+count,12,author)
                    except:
                        pass
            connexion.commit()

            connexion,curseur=connectSQL("OT","ranks","Trivial",None,None)
            compteurSQL(curseur,"trivial{0}".format(categ),author,(0,author,categ,"TO","GL",points[diff]*multi),points[diff]*multi,None,None,None,None,2,None)
            compteurSQL(curseur,"trivial12",author,(0,author,12,"TO","GL",points[diff]*multi),points[diff]*multi,None,None,None,None,2,None)
        else:
            curseur.execute("UPDATE trivial{0} SET Multi=0 WHERE IDCateg={1}".format(author,categ))
            curseur.execute("UPDATE trivial{0} SET Multi=0 WHERE IDCateg=12".format(author))

        inGame.remove(author)
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

    async def timer(self,message,bot,ctx,inGame):
        await asyncio.sleep(20)
        try:
            newMessage=await message.channel.fetch_message(message.id)
        except:
            return
        if newMessage.embeds[0].color==discord.Colour(0xad917b):
            await newMessage.clear_reactions()
            newMessage.embeds[0].description=self.affichageLose(None)
            newMessage.embeds[0].colour=0xcf1742
            self.gestionMulti(False,inGame)
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
        super().setCateg((arg))

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

    async def timer(self,message,bot,ctx,inGame):
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
                self.gestionMulti(False,inGame)
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


async def embedTrivial(arg,ctx,bot,author,option,inGame,gamesTrivial):
    try:
        assert author.id not in inGame, "Vous êtes déjà en train de répondre à une question !"
        inGame.append(author.id)
        if option=="classic":
            question=Question(author,option)
        elif option=="streak":
            if ctx.message.id in gamesTrivial:
                question=gamesTrivial[ctx.message.id]
            else:
                question=Streak(author)
        if option!="streak":
            if len(arg)!=0:
                if arg[0].lower()=="art":
                    arg=None
        question.setCateg(arg)
        question.setUser()
        question.setDiff()
        question.newQuestion()
        embedT=question.createEmbed()
    except AssertionError as er:
        await ctx.send(embed=embedAssert(er))
    except sqlite3.OperationalError as er:
        await asyncio.sleep(0.2)
        inGame.remove(author.id)
        await embedTrivial(arg,ctx,bot,author,option,inGame,gamesTrivial)
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
        bot.loop.create_task(question.timer(message,bot,ctx,inGame))
