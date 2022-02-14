import asyncio
from random import choice

import discord
from Core.Fonctions.AuteurIcon import auteur

dictEmote={0:":one:",1:":two:",2:":three:"}
dictLettre={"A":0,"B":1,"C":2}
dictVal={0:"A",1:"B",2:"C"}

class JoueurMorpion:
    def __init__(self,user):
        self.id=user.id
        self.nom=user.name
        self.color=user.color.value
        self.avatar=user.avatar

class TabP4:
    def __init__(self):
        self.tableau=[[0 for j in range(3)] for i in range(3)]
        self.available=[(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]

    def checkTab(self,x,y,player):

        for k in range(4):
            count=0
            for i in range(3):
                prob=((x,i),(i,y),(i,i),(i,2-i))
                if self.tableau[prob[k][0]][prob[k][1]]==player:
                    count+=1
            if count==3:
                for i in range(3):
                    prob=((x,i),(i,y),(i,i),(i,2-i))
                    self.tableau[prob[k][0]][prob[k][1]]=10+player
                break
        else:
            return False
        return True
    
    def checkNul(self):
        for i in self.tableau:
            for j in i:
                if j==0:
                    break
            if j==0:
                break
        else:
            return True
        return False

    def addJeton(self,x,y,player):
        if self.tableau[x][y]==0:
            self.available.remove((x,y))
            self.tableau[x][y]=player
            return True, x, y
        return False, 0, 0


class JeuMorpion:
    def __init__(self,guild,user):
        self.joueurs=[]
        self.ids=[]
        self.emotes={}
        self.guild=guild
        self.tab=TabP4()
        self.tours=0
        self.playing=False
        self.invoke=user
        self.paris=None
    
    def addPlayer(self,user):
        self.joueurs.append(JoueurMorpion(user))

    def createEmbedMorpion(self,turn):
        embed=discord.Embed(title="Au tour de {0}".format(self.joueurs[turn].nom),description=self.affichageTab(),color=self.joueurs[turn].color)
        auteur(self.joueurs[turn].id,self.joueurs[turn].nom,self.joueurs[turn].avatar,embed,"user")
        embed.set_footer(text="OT!morpion")
        embed.add_field(name="Joueurs",value="<@{0}> : <:otP1:726164724882079854>\n<@{1}> : <:otP2:726165146229145610>".format(self.joueurs[0].id,self.joueurs[1].id))
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
        descip="<:otBlank:828934808200937492>:regional_indicator_a::regional_indicator_b::regional_indicator_c:\n"
        for i in range(3):
            descip+=dictEmote[i]
            for j in self.tab.tableau[i]:
                if j==1:
                    descip+="<:otP1:726164724882079854>"
                elif j==2:
                    descip+="<:otP2:726165146229145610>"
                elif j==11:
                    descip+="<:otP1WIN:726165146120093766>"
                elif j==12:
                    descip+="<:otP2WIN:728191188477411377>"
                else:
                    descip+="<:otBlank:828934808200937492>"
            descip+="\n"
        return descip

    def embedWin(self,win,nul):
        if nul==True:
            embed=discord.Embed(title="Match nul !", description="Le tableau est bloqué, et personne n'a gagné !", color=0xad917b)
        else:
            embed=discord.Embed(title="Victoire de {0}".format(self.joueurs[win].nom), description="Bravo à lui/elle !", color=self.joueurs[win].color)
            embed=auteur(self.joueurs[win].id,self.joueurs[win].nom,self.joueurs[win].avatar,embed,"user")
            embed.add_field(name="<:otCOINS:873226814527520809> gagnés",value="{0} <:otCOINS:873226814527520809>".format(50+sum(self.paris.mises.values())))

        embed.set_footer(text="OT!morpion")
        return embed


    async def play(self,turn,message,bot):

        def check(mess):
            try:
                if len(mess.content)!=2 or mess.content[0].upper() not in ("A","B","C") or mess.content[1] not in ("1","2","3") or (int(mess.content[1].upper())-1,dictLettre[mess.content[0].upper()]) not in self.tab.available:
                    return False
                return mess.channel.id==message.channel.id and self.joueurs[turn].id==mess.author.id
            except:
                return False

        try:
            mess=await bot.wait_for('message', check=check, timeout=30)
        except asyncio.exceptions.TimeoutError:
            choix=choice(self.tab.available)
            add=self.tab.addJeton(choix[0],choix[1],turn+1)
        else:
            add=self.tab.addJeton(int(mess.content[1].upper())-1,dictLettre[mess.content[0].upper()],turn+1)
        return add

    def fermeture(self):
        if self.tours==3:
            self.paris.ouvert=False
