import asyncio
import html
from random import choice, randint

import discord
from Core.Decorator import OTCommand
from Core.Fonctions.Embeds import createEmbed
from discord.ext import commands
from Stats.SQL.Compteur import compteurSQL, compteurTrivialS
from Stats.SQL.ConnectSQL import connectSQL
from Titres.Outils import gainCoins, titresTrivial

emotes=["<:ot1:705766186909958185>","<:ot2:705766186989912154>","<:ot3:705766186930929685>","<:ot4:705766186947706934>"]
emotesTrue=["<:ot1VRAI:773993429130149909>", "<:ot2VRAI:773993429050195979>", "<:ot3VRAI:773993429331738624>", "<:ot4VRAI:773993429423095859>"]
emotesFalse=["<:ot1FAUX:773993429315092490>", "<:ot2FAUX:773993429172486145>", "<:ot3FAUX:773993429402779698>", "<:ot4FAUX:773993429373026354>"]
listeNoms=["Culture","Divertissement","Sciences","Mythologie","Sport","Géographie","Histoire","Politique","Art","Célébrités","Animaux","Véhicules","Global"]
dictCateg={9:0,10:1,11:1,12:1,13:1,14:1,15:1,16:1,17:2,18:2,19:2,20:3,21:4,22:5,23:6,24:7,25:8,26:9,27:10,28:11,29:1,30:2,31:1,32:1}
dictDiff={"easy":"Facile (+10)","medium":"Moyenne (+15)","hard":"Difficile (+25)"}

class Question:
    def __init__(self,author:discord.Member,option:str):
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
        self.temps=20

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
        tableQuestion.sort(key=lambda x:x["ID"])
        self.table=tableQuestion
        self.questionFR=html.unescape(table["Question"])
        if tableENG!=None:
            self.questionEN=html.unescape(tableENG["Question"])
        self.vrai=choix[0]
        print(self.vrai)
        self.auteur=table["Auteur"]

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
    
    def gestionMulti(self,victoire):
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

        connexion.commit()

    def createEmbed(self):
        embedT=createEmbed(self.questionFR,self.affichageClassique(),0xad917b,"trivial",self.author)
        embedT.add_field(name="Catégorie", value=listeNoms[dictCateg[self.arg]], inline=True)
        embedT.add_field(name="Difficulté", value=dictDiff[self.diff], inline=True)
        embedT.add_field(name="Multiplicateur", value=str(self.multi),inline=True)
        embedT.add_field(name="Auteur",value="[{0}](https://forms.gle/RNTGn9tds2LGVkdU8)".format(self.auteur),inline=True)
        return embedT

class Streak(Question):
    def __init__(self, author):
        self.serie=0
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
       
    def getRecord(self):
        connexion,curseur=connectSQL("OT","ranks","Trivial",None,None)
        curseur.execute("CREATE TABLE IF NOT EXISTS trivialStreak (Rank INT, ID BIGINT PRIMARY KEY, IDComp BIGINT, Mois TEXT, Annee TEXT, Count INT)")
        etat=curseur.execute("SELECT * FROM trivialStreak WHERE ID={0}".format(self.author.id)).fetchone()
        if etat==None:
            return "Aucun"
        else:
            return "{0} - {1}e".format(etat["Count"],etat["Rank"])


@OTCommand
async def embedTrivial(ctx:commands.Context,bot:commands.Bot,args:list,option:str,inGame:list):
    choix={705766186909958185:0,705766186989912154:1,705766186930929685:2,705766186947706934:3,473254057511878656:4}
    assert ctx.author.id not in inGame, "Vous êtes déjà en train de répondre à une question !"
    inGame.append(ctx.author.id)
    if option=="classic":
        question=Question(ctx.author,option)
        if len(args)!=0:
            if args[0].lower()=="art":
                args=None
    elif option=="streak":
        question=Streak(ctx.author)
        
    question.setCateg(args)
    question.setUser()
    question.setDiff()
    question.newQuestion()

    message=await ctx.send(embed=question.createEmbed())
    for i in emotes:
        await message.add_reaction(i)
    
    def checkAnswer(reaction,user):
        if type(reaction.emoji)==str:
            return False
        return user.id==ctx.author.id and reaction.message.id==message.id and reaction.emoji.id in (705766186909958185,705766186989912154,705766186930929685,705766186947706934)

    play=True
    while play:
        try:
            react,user=await bot.wait_for("reaction_add",check=checkAnswer,timeout=question.temps)
            rep=choix[react.emoji.id]+1
            emoji=react.emoji.id
        except asyncio.exceptions.TimeoutError:
            rep=None
            emoji=None

        if question.vrai==rep:
            question.gestionMulti(True)
            if question.option=="classic":
                play=False
                message.embeds[0].colour=0x47b03c
                message.embeds[0].description=question.affichageWin()
            elif question.option=="streak":
                await react.remove(user)
                question.serie+=1
                question.changeTime()
                question.setCateg(None)
                question.setUser()
                question.setDiff()
                question.newQuestion()
                await message.edit(embed=question.createEmbed())
        else:
            play=False
            message.embeds[0].colour=0xcf1742
            message.embeds[0].description=question.affichageLose(emoji)
            question.gestionMulti(False)
            if question.option=="streak":
                results=compteurTrivialS(question.author.id,(0,question.author.id,13,"TO","GL",question.serie),question.serie)
                if results[0]:
                    await ctx.reply("Bravo ! Vous avez battu votre record de série avec **{0}** bonnes réponses ! Votre ancien score était **{1}** bonnes réponses.".format(results[1],results[2]))
        await message.edit(embed=message.embeds[0])
    await message.clear_reactions()
    inGame.remove(ctx.author.id)
