import asyncio
from random import randint

import discord
from Core.Fonctions.AuteurIcon import auteur

emotes=["<:ot1:705766186909958185>","<:ot2:705766186989912154>","<:ot3:705766186930929685>","<:ot4:705766186947706934>","<:ot5:705766186713088042>","<:ot6:705766187182850148>","<:ot7:705766187115741246>"]
dictCo={705766186909958185:0,705766186989912154:1,705766186930929685:2,705766186947706934:3,705766186713088042:4,705766187182850148:5,705766187115741246:6}

class JoueurP4:
    def __init__(self,user):
        self.id=user.id
        self.nom=user.name
        self.color=user.color.value
        self.avatar=user.avatar

class TabP4:
    def __init__(self):
        self.tableau=[[0 for j in range(7)] for i in range(6)]

    def checkTab(self,x,y,player):
        xD,yD=self.getDiag(x,y,"d")
        if xD==0 and yD!=6:
            ranD=yD+1
        else:
            ranD=yD-xD
        xG,yG=self.getDiag(x,y,"g")
        if xG==0 and yG!=0:
            ranG=7-yG
        else:
            ranG=6-xG

        etat=False
        listeRan=[7,6,ranD,ranG]
        for z in range(4):
            if etat==False:
                count,liste=0,[]
                for i in range(listeRan[z]):
                    dic={0:[x,i],1:[i,y],2:[xD+i,yD-i],3:[xG+i,yG+i]}
                    xT,yT=dic[z]
                    if count==0 and 7-i<4:
                        break
                    if self.tableau[xT][yT]==player:
                        count+=1
                        liste.append((xT,yT))
                    else:
                        count=0
                        liste=[]
                    if count==4:
                        etat=True
                        break
        
        if etat==False:
            return False
        else:
            for i in liste:
                self.tableau[i[0]][i[1]]=10+player
            return True
    
    def checkNul(self):
        for i in self.tableau:
            for j in i:
                if j==0:
                    return False
        return True

    def getDiag(self,x,y,option):
        d1={"d":6,"g":0}
        d2={"d":1,"g":-1}
        while x!=0 and y!=d1[option]:
            x-=1
            y+=d2[option]
        return x,y

    def addJeton(self,colonne,player):
        add=False
        i=len(self.tableau)-1
        while add==False and i!=-1:
            if self.tableau[i][colonne]==0:
                self.tableau[i][colonne]=player
                add=True
            i=i-1
        return add,i+1,colonne

class JeuP4:
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
        self.joueurs.append(JoueurP4(user))

    def createEmbedP4(self,turn):
        embed=discord.Embed(title="Au tour de {0}".format(self.joueurs[turn].nom),description=self.affichageTab(),color=self.joueurs[turn].color)
        auteur(self.joueurs[turn].id,self.joueurs[turn].nom,self.joueurs[turn].avatar,embed,"user")
        embed.set_footer(text="OT!p4")
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
        descip=""
        for i in self.tab.tableau:
            for j in i:
                if j==1:
                    descip+="<:otP1:726164724882079854>"
                elif j==2:
                    descip+="<:otP2:726165146229145610>"
                elif j==11:
                    descip+="<:otP1WIN:726165146120093766>"
                elif j==12:
                    descip+="<:otP2WIN:728191188477411377>"
                else:
                    descip+="<:otVide:727103624106344548>"
            descip+="\n"
        return descip

    def embedWin(self,win,nul):
        if nul==True:
            embed=discord.Embed(title="Match nul !", description="Le tableau est bloqué, et personne n'a gagné !", color=0xad917b)
        else:
            embed=discord.Embed(title="Victoire de {0}".format(self.joueurs[win].nom), description="Bravo à lui/elle !", color=self.joueurs[win].color)
            embed=auteur(self.joueurs[win].id,self.joueurs[win].nom,self.joueurs[win].avatar,embed,"user")
            embed.add_field(name="<:otCOINS:873226814527520809> gagnés",value="{0} <:otCOINS:873226814527520809>".format(50+sum(self.paris.mises.values())))

        embed.set_footer(text="OT!p4")
        return embed


    async def play(self,turn,message,bot):

        def check(reaction,user):
            if type(reaction.emoji)==str:
                return False
            return reaction.emoji.id in (705766186909958185,705766186989912154,705766186930929685,705766186947706934,705766186713088042,705766187182850148,705766187115741246) and reaction.message.id==message.id and self.joueurs[turn].id==user.id

        try:
            reaction,user=await bot.wait_for('reaction_add', check=check, timeout=60)
            await reaction.remove(user)
        except asyncio.exceptions.TimeoutError:
            add=self.tab.addJeton(randint(0,6),turn+1)
        else:
            add=self.tab.addJeton(dictCo[reaction.emoji.id],turn+1)
        return add

    def fermeture(self):
        if self.tours==6:
            self.paris.ouvert=False
