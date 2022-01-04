import asyncio
from random import choice, randint

import discord
from Core.Fonctions.AuteurIcon import auteur

dictEmotes={("B","C","C","P"):878357453828411392,("B","C","P","P"):878357453534801921,("B","C","P","G"):878357453576732692,("B","R","C","G"):878357453526401055,("B","R","C","P"):878357453400592455,("B","R","P","P"):878357453660643359,("B","R","P","G"):878357453614506025,("B","C","C","G"):878357453702561863,
("R","C","C","P"):878357454008774686,("R","C","P","P"):878357453450907710,("R","C","P","G"):878357453660643358,("R","R","C","G"):878357453656428605,("R","R","C","P"):878357453757108275,("R","R","P","P"):878357453614506026,("R","R","P","G"):878357453660643360,("R","C","C","G"):878357453673234522}
dict0={"B":"Bleu","R":"Rouge"}
dict1={"C":"Carre","R":"Rond"}
dict2={"C":"Creux","P":"Plein"}
dict3={"P":"Petit","G":"Grand"}
emotes=["<:ot1:705766186909958185>","<:ot2:705766186989912154>","<:ot3:705766186930929685>","<:ot4:705766186947706934>","<:ot5:705766186713088042>","<:ot6:705766187182850148>","<:ot7:705766187115741246>","<:ot8:705766187132256308>"]
dictCo={705766186909958185:0,705766186989912154:1,705766186930929685:2,705766186947706934:3,705766186713088042:4,705766187182850148:5,705766187115741246:6,705766187132256308:7}
dictX={1:0,2:1,3:2,4:3}
dictY={"a":0,"b":1,"c":2,"d":3}
dictYReverse={0:"A",1:"B",2:"C",3:"D"}

class JoueurMatrice:
    def __init__(self,user,couleur):
        self.userid=user.id
        self.name=user.name
        self.color=user.color.value
        self.avatar=user.avatar
        if couleur=="rouge":
            self.pions={0:("R","C","P","P"),1:("R","C","C","P"),2:("R","C","P","G"),3:("R","C","C","G"),4:("R","R","P","P"),5:("R","R","C","P"),6:("R","R","P","G"),7:("R","R","C","G")}
        else:
            self.pions={0:("B","C","P","P"),1:("B","C","C","P"),2:("B","C","P","G"),3:("B","C","C","G"),4:("B","R","P","P"),5:("B","R","C","P"),6:("B","R","P","G"),7:("B","R","C","G")}

    def checkPion(self,nb):
        if self.pions[nb]==None:
            return False
        return True

class TabMatrice:
    def __init__(self):
        self.tableau=[[0 for j in range(4)] for i in range(4)]

    def checkTab(self,x,y):
        if x==y:
            if 0 not in (self.tableau[0][0],self.tableau[1][1],self.tableau[2][2],self.tableau[3][3]):
                for i in range(4):
                    count=1
                    cara=self.tableau[0][0][i]
                    for j in range(1,4):
                        if self.tableau[j][j][i]==cara:
                            count+=1
                        else:
                            break
                    if count==4:
                        return True, "Diagonale Droite", i, cara
        if x+y==3:
            if 0 not in (self.tableau[0][3],self.tableau[1][2],self.tableau[2][1],self.tableau[3][0]):
                for i in range(4):
                    count=1
                    cara=self.tableau[0][3][i]
                    for j in range(1,4):
                        if self.tableau[0+j][3-j][i]==cara:
                            count+=1
                        else:
                            break
                    if count==4:
                        return True, "Diagonale Gauche", i, cara
        if 0 not in (self.tableau[x][0],self.tableau[x][1],self.tableau[x][2],self.tableau[x][3]):
            for i in range(4):
                count=1
                cara=self.tableau[x][0][i]
                for j in range(1,4):
                    if self.tableau[x][j][i]==cara:
                        count+=1
                    else:
                        break
                if count==4:
                    return True, "Ligne {0}".format(x+1), i, cara
        if 0 not in (self.tableau[0][y],self.tableau[1][y],self.tableau[2][y],self.tableau[3][y]):
            for i in range(4):
                count=1
                cara=self.tableau[0][y][i]
                for j in range(1,4):
                    if self.tableau[j][y][i]==cara:
                        count+=1
                    else:
                        break
                if count==4:
                    return True, "Colonne {0}".format(dictYReverse[y]), i, cara
        return False, None, None, None, None
    
    def checkNul(self):
        for i in self.tableau:
            for j in i:
                if j==0:
                    return False
        return True

    def checkPos(self,mot):
        try:
            assert len(mot)==2
            assert mot[0].lower() in dictY
            assert int(mot[1]) in dictX
            assert self.tableau[dictX[int(mot[1])]][dictY[mot[0].lower()]]==0
        except:
            return False
        return True

    def addPion(self,joueur,x,y,nb):
        self.tableau[x][y]=joueur.pions[nb]
        joueur.pions[nb]=None


class JeuMatrice:
    def __init__(self,guild,user):
        self.joueurs=[]
        self.ids=[]
        self.emotes={}
        self.guild=guild
        self.tab=TabMatrice()
        self.tours=0
        self.playing=False
        self.invoke=user
        self.paris=None
    
    def addPlayer(self,user,couleur):
        self.joueurs.append(JoueurMatrice(user,couleur))

    def embedGame(self,turn):
        embed=discord.Embed(title="Au tour de {0}".format(self.joueurs[turn].name),description=self.affichageTab(),color=self.joueurs[turn].color)
        auteur(self.joueurs[turn].userid,self.joueurs[turn].name,self.joueurs[turn].avatar,embed,"user")
        embed.set_footer(text="OT!matrice")
        for i in self.joueurs:
            descip=""
            for j in i.pions:
                if i.pions[j]==None:
                    descip+="{0} : //\n".format(emotes[j])
                else:
                    nom=dict0[i.pions[j][0]]+dict1[i.pions[j][1]]+dict2[i.pions[j][2]]+dict3[i.pions[j][3]]
                    descip+="{0} : <:{1}:{2}>\n".format(emotes[j],nom,dictEmotes[i.pions[j]])
            embed.add_field(name=i.name,value=descip,inline=True)
        if sum(self.paris.mises.values())!=0:
            descip=""
            for i in self.paris.mises:
                if self.paris.mises[i]!=0:
                    descip+="<@{0}> : {1} <:otCOINS:873226814527520809>\n".format(i,self.paris.mises[i])
            embed.add_field(name="Mises d'OT Coins",value=descip)
        if self.paris.ouvert:
            descip=""
            for i in self.paris.cotes:
                if self.paris.cotes[i]!=None:
                    descip+="<@{0}> : {1}\n".format(i,self.paris.cotes[i])
            if descip!="":
                embed.add_field(name="Côtes",value=descip)
        return embed

    def affichageTab(self):
        descip="<:otBlank:828934808200937492>:regional_indicator_a::regional_indicator_b::regional_indicator_c::regional_indicator_d:\n"
        for i in range(len(self.tab.tableau)):
            if i+1<10:
                descip+="` {0}`".format(i+1)
            else:
                descip+="`{0}`".format(i+1)
            for j in self.tab.tableau[i]:
                if j==0:
                    descip+="<:otVide:727103624106344548>"
                else:
                    nom=dict0[j[0]]+dict1[j[1]]+dict2[j[2]]+dict3[j[3]]
                    descip+="<:{0}:{1}>".format(nom,dictEmotes[j])
            descip+="\n"
        return descip

    def embedWin(self,win,nul,categ,cara,i):
        if nul==True:
            embed=discord.Embed(title="Match nul !", description="Le tableau est bloqué, et personne n'a gagné !", color=0xad917b)
        else:
            liste=[dict0,dict1,dict2,dict3]
            embed=discord.Embed(title="Victoire de {0}".format(self.joueurs[win].name), description="Bravo à lui/elle !", color=self.joueurs[win].color)
            embed=auteur(self.joueurs[win].userid,self.joueurs[win].name,self.joueurs[win].avatar,embed,"user")
            embed.add_field(name="<:otCOINS:873226814527520809> gagnés",value="{0} <:otCOINS:873226814527520809>".format(50+sum(self.paris.mises.values())))
            embed.add_field(name="Combinaison",value="{0}, {1}".format(categ,liste[i][cara]))

        embed.set_footer(text="OT!p4")
        return embed


    async def play(self,turn,message,bot):

        def check(reaction,user):
            if type(reaction.emoji)==str:
                return False
            if reaction.emoji.id in (705766186909958185,705766186989912154,705766186930929685,705766186947706934,705766186713088042,705766187182850148,705766187115741246,705766187132256308) and reaction.message.id==message.id and self.joueurs[turn].userid==user.id:
                return self.joueurs[turn].checkPion(dictCo[reaction.emoji.id])

        try:
            reaction,user=await bot.wait_for('reaction_add', check=check, timeout=40)
            await reaction.remove(user)
            nb=dictCo[reaction.emoji.id]

            def check(mess):
                return self.joueurs[turn].userid==mess.author.id and message.channel.id==mess.channel.id and self.tab.checkPos(mess.content)

            pion=self.joueurs[turn].pions[dictCo[reaction.emoji.id]]
            nom=dict0[pion[0]]+dict1[pion[1]]+dict2[pion[2]]+dict3[pion[3]]
            ask=await message.channel.send("<@{0}> : choisissez sur quelle case poser <:{1}:{2}>".format(self.joueurs[turn].userid,nom,dictEmotes[pion]))

            messageCoord=await bot.wait_for("message",check=check,timeout=40)
            await ask.delete()
            mot=messageCoord.content
            x,y=dictX[int(mot[1])],dictY[mot[0].lower()]
            await messageCoord.delete()

        except asyncio.exceptions.TimeoutError:
            mot="00"
            while self.tab.checkPos(mot)==False:
                mot=choice(["a","b","c","d"])+choice(["1","2","3","4"])
            x,y=dictX[int(mot[1])],dictY[mot[0].lower()]
            pion=None
            while pion==None:
                nb=randint(0,7)
                self.joueurs[turn].checkPion(nb)
            self.tab.addPion(self.joueurs[turn],x,y,nb)
        else:
            self.tab.addPion(self.joueurs[turn],x,y,nb)
        return x,y

    def fermeture(self):
        if self.tours==4:
            self.paris.ouvert=False
