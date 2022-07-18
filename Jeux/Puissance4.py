import asyncio
from random import randint

from Core.Fonctions.AuteurIcon import auteurJeux
from Core.Fonctions.Embeds import createEmbed

from Jeux.Outils.Bases import JeuBase

emotes=["<:ot1:705766186909958185>","<:ot2:705766186989912154>","<:ot3:705766186930929685>","<:ot4:705766186947706934>","<:ot5:705766186713088042>","<:ot6:705766187182850148>","<:ot7:705766187115741246>"]
dictCo={"ot:p4_1":0,"ot:p4_2":1,"ot:p4_3":2,"ot:p4_4":3,"ot:p4_5":4,"ot:p4_6":5,"ot:p4_7":6}


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
            if not etat:
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
        
        if not etat:
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
        while not add and i!=-1:
            if self.tableau[i][colonne]==0:
                self.tableau[i][colonne]=player
                add=True
            i=i-1
        return add,i+1,colonne


class JeuP4(JeuBase):
    def __init__(self,message,invoke,cross):
        super().__init__(message,invoke,"P4",cross)
        self.tab=TabP4()
        self.tours=0

    def embedGame(self,guild):
        user=self.joueurs[self.turn]
        if user.guild==guild:
            embed=createEmbed("Au tour de {0}".format(user.nom),self.affichageTab(),user.color,"p4",user.user)
        else:
            embed=createEmbed("Au tour de {0}".format(user.titre),self.affichageTab(),user.color,"p4",user.user)
            auteurJeux(user,embed)

        listeEmote=["<:otP1:726164724882079854>","<:otP2:726165146229145610>"]

        for i in range(2):
            descip="**Jeton :** {0}\n".format(listeEmote[i])
            if self.paris.mises[self.joueurs[i].id]!=0: 
                descip+="**Mise :** {0} <:otCOINS:873226814527520809>\n".format(self.paris.mises[self.joueurs[i].id])
            if self.paris.cotes[self.joueurs[i].id]!=None and self.joueurs[i].guild==guild and self.paris.ouvert:
                descip+="**Côte :** {0}\n".format(self.paris.cotes[self.joueurs[i].id])

            if self.joueurs[i].emote==None:
                emote=""
            else:
                emote=self.joueurs[i].emote

            if self.joueurs[i].guild==guild:
                embed.add_field(name="{0} {1}".format(emote,self.joueurs[i].nom),value=descip,inline=True)
            else:
                embed.add_field(name="{0} {1}".format(emote,self.joueurs[i].titre),value=descip,inline=True)

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

    def embedEnd(self,nul,guild):
        if nul:
            return createEmbed("Match nul !","Le tableau est bloqué, et personne n'a gagné !",0xad917b,"p4",guild)
        else:
            user=self.joueurs[self.turn]
            embed=createEmbed("Victoire de {0}".format(user.nom),"Bravo à lui/elle !",user.color,"p4",user.user)
            
            if user.guild==guild.id:
                embed=createEmbed("Victoire de {0}".format(user.nom),"Bravo à lui/elle !",user.color,"p4",user.user)
            else:
                embed=createEmbed("Victoire de {0}".format(user.titre),"Bravo à lui/elle !",user.color,"p4",user.user)
                auteurJeux(user,embed)

            embed.add_field(name="<:otCOINS:873226814527520809> gagnés",value="{0} <:otCOINS:873226814527520809>".format(50+sum(self.paris.mises.values())))
            return embed

    def fermeture(self):
        if self.tours==6:
            self.paris.ouvert=False

    async def play(self,bot,interactionUser):

        def check(interaction):
            return interaction.data["custom_id"] in ("ot:p4_1","ot:p4_2","ot:p4_3","ot:p4_4","ot:p4_5","ot:p4_6","ot:p4_7") and interaction.message.id==interactionUser.message.id and self.joueurs[self.turn].id==interaction.user.id

        try:
            interaction=await bot.wait_for('interaction', check=check, timeout=60)
        except asyncio.exceptions.TimeoutError:
            add=self.tab.addJeton(randint(0,6),self.turn+1)
        else:
            add=self.tab.addJeton(dictCo[interaction.data["custom_id"]],self.turn+1)
        return add

    async def boucle(self,bot):
        for mess in self.messages:
            await mess.edit(embed=self.embedGame(mess.guild.id))
        while self.playing:
            add=await self.play(bot,self.joueurs[self.turn].interaction)
            if add[0]:
                nul=self.tab.checkNul()
                win=self.tab.checkTab(add[1],add[2],self.turn+1)
                if win:
                    nul=False
                if win or nul:
                    if not nul:
                        await self.stats(self.joueurs[self.turn].id,self.joueurs[self.turn].guild)
                    for mess in self.messages:
                        await mess.edit(view=None)
                        await mess.reply(embed=self.embedEnd(nul,mess.guild))
                    self.playing=False
                else:
                    self.tours+=1      
                    for i in range(7):
                        if self.tab.tableau[0][i]!=0:
                            for mess in self.messages:
                                await mess.clear_reaction(emotes[i])
                    if self.turn==0: self.turn=1
                    else: self.turn=0
            
            self.fermeture()
            for mess in self.messages:
                await mess.edit(embed=self.embedGame(mess.guild.id))
