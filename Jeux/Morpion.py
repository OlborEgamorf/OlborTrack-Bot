import asyncio
from random import choice

from Core.Fonctions.AuteurIcon import auteurJeux
from Core.Fonctions.Embeds import createEmbed
from Core.Fonctions.Unpin import unpin

from Jeux.Outils.Bases import JeuBase

dictEmote={0:":one:",1:":two:",2:":three:"}
dictLettre={"A":0,"B":1,"C":2}
dictVal={0:"A",1:"B",2:"C"}

class TabMorpion:
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


class JeuMorpion(JeuBase):
    def __init__(self,message,user,cross):
        super().__init__(message,user,"Morpion",cross)
        self.tab=TabMorpion()
        self.tours=0

    def embedGame(self,guild):
        user=self.joueurs[self.turn]
        if user.guild==guild:
            embed=createEmbed("Au tour de {0}".format(user.nom),self.affichageTab(),user.color,"morpion",user.user)
        else:
            embed=createEmbed("Au tour de {0}".format(user.titre),self.affichageTab(),user.color,"morpion",user.user)
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

    def embedEnd(self,nul,guild):
        if nul:
            return createEmbed("Match nul !","Le tableau est bloqué, et personne n'a gagné !",0xad917b,"morpion",guild)
        else:
            user=self.joueurs[self.turn]
            embed=createEmbed("Victoire de {0}".format(user.nom),"Bravo à lui/elle !",user.color,"morpion",user.user)
            
            if user.guild==guild.id:
                embed=createEmbed("Victoire de {0}".format(user.nom),"Bravo à lui/elle !",user.color,"morpion",user.user)
            else:
                embed=createEmbed("Victoire de {0}".format(user.titre),"Bravo à lui/elle !",user.color,"morpion",user.user)
                auteurJeux(user,embed)

            embed.add_field(name="<:otCOINS:873226814527520809> gagnés",value="{0} <:otCOINS:873226814527520809>".format(50+sum(self.paris.mises.values())))
            return embed


    async def play(self,message,bot):

        def check(mess):
            try:
                if len(mess.content)!=2 or mess.content[0].upper() not in ("A","B","C") or mess.content[1] not in ("1","2","3") or (int(mess.content[1].upper())-1,dictLettre[mess.content[0].upper()]) not in self.tab.available:
                    return False
                return mess.channel.id==message.channel.id and self.joueurs[self.turn].id==mess.author.id
            except:
                return False

        try:
            mess=await bot.wait_for('message', check=check, timeout=30)
        except asyncio.exceptions.TimeoutError:
            choix=choice(self.tab.available)
            add=self.tab.addJeton(choix[0],choix[1],self.turn+1)
        else:
            add=self.tab.addJeton(int(mess.content[1].upper())-1,dictLettre[mess.content[0].upper()],self.turn+1)
        return add

    def fermeture(self):
        if self.tours==3:
            self.paris.ouvert=False

    async def boucle(self,bot):
        for mess in self.messages:
            await mess.edit(embed=self.embedGame(mess.guild.id))
        while self.playing:
            add=await self.play(self.joueurs[self.turn].message,bot)
            if add[0]:
                nul=self.tab.checkNul()
                if self.tab.checkTab(add[1],add[2],self.turn+1) or nul:
                    if not nul:
                        await self.stats(self.joueurs[self.turn].id,self.joueurs[self.turn].guild)
                    for mess in self.messages:
                        await mess.clear_reactions()
                        await mess.reply(embed=self.embedEnd(nul,mess.guild))
                        await unpin(mess)
                    self.playing=False
                else:
                    self.tours+=1 
                    if self.turn==0: self.turn=1
                    else: self.turn=0
            
            self.fermeture()
            for mess in self.messages:
                await mess.edit(embed=self.embedGame(mess.guild.id))
