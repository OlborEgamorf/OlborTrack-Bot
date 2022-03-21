import asyncio
from random import choice, randint

from Core.Fonctions.AuteurIcon import auteurJeux
from Core.Fonctions.Embeds import createEmbed
from Core.Fonctions.Unpin import unpin

from Jeux.Outils.Bases import JeuBase, JoueurBase

dictEmotes={("B","C","C","P"):878357453828411392,("B","C","P","P"):878357453534801921,("B","C","P","G"):878357453576732692,("B","R","C","G"):878357453526401055,("B","R","C","P"):878357453400592455,("B","R","P","P"):878357453660643359,("B","R","P","G"):878357453614506025,("B","C","C","G"):878357453702561863,
("R","C","C","P"):878357454008774686,("R","C","P","P"):878357453450907710,("R","C","P","G"):878357453660643358,("R","R","C","G"):878357453656428605,("R","R","C","P"):878357453757108275,("R","R","P","P"):878357453614506026,("R","R","P","G"):878357453660643360,("R","C","C","G"):878357453673234522}
dict0={"B":"Bleu","R":"Rouge"}
dict1={"C":"Carré","R":"Rond"}
dict2={"C":"Creux","P":"Plein"}
dict3={"P":"Petit","G":"Grand"}
emotes=["<:ot1:705766186909958185>","<:ot2:705766186989912154>","<:ot3:705766186930929685>","<:ot4:705766186947706934>","<:ot5:705766186713088042>","<:ot6:705766187182850148>","<:ot7:705766187115741246>","<:ot8:705766187132256308>"]
dictCo={705766186909958185:0,705766186989912154:1,705766186930929685:2,705766186947706934:3,705766186713088042:4,705766187182850148:5,705766187115741246:6,705766187132256308:7}
dictX={1:0,2:1,3:2,4:3}
dictY={"a":0,"b":1,"c":2,"d":3}
dictYReverse={0:"A",1:"B",2:"C",3:"D"}

class JoueurMatrice(JoueurBase):
    def __init__(self,user,message,couleur):
        super().__init__(user,message)
        self.couleur=couleur
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


class JeuMatrice(JeuBase):
    def __init__(self,message,user,cross):
        super().__init__(message,user,"Matrice",cross)
        self.tab=TabMatrice()
        self.tours=0
        self.couleurs=["bleu","rouge"]
        
    def addPlayer(self,user,message):
        couleur=choice(self.couleurs)
        self.couleurs.remove(couleur)
        self.joueurs.append(JoueurMatrice(user,message,couleur))
        self.ids.append(user.id)

    def embedGame(self,guild:int):
        user=self.joueurs[self.turn]
        if user.guild==guild:
            embed=createEmbed("Au tour de {0}".format(user.nom),self.affichageTab(),user.color,"matrice",user.user)
        else:
            embed=createEmbed("Au tour de {0}".format(user.titre),self.affichageTab(),user.color,"matrice",user.user)
            auteurJeux(user,embed)

        for i in self.joueurs:
            descip=""
            if self.paris.ouvert and i.guild==guild and self.paris.cotes[i.id]!=None:
                descip+="*Côte : {0}*\n".format(self.paris.cotes[i.id])
            else:
                if self.paris.mises[i.id]!=0:
                    descip+="*Mise : {0} <:otCOINS:873226814527520809>*\n".format(self.paris.mises[i.id])

            for j in i.pions:
                if i.pions[j]==None:
                    descip+="{0} : //\n".format(emotes[j])
                else:
                    nom=dict0[i.pions[j][0]]+dict1[i.pions[j][1]]+dict2[i.pions[j][2]]+dict3[i.pions[j][3]]
                    descip+="{0} : <:{1}:{2}>\n".format(emotes[j],nom,dictEmotes[i.pions[j]])
            
            if i.emote==None:
                emote=""
            else:
                emote=i.emote
            if i.guild==guild:
                embed.add_field(name="{0} Jeu de {1}".format(emote,i.nom),value=descip)
            else:
                embed.add_field(name="{0} Jeu de {1}".format(emote,i.titre),value=descip)

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

    def embedEnd(self,nul,categ,cara,i,guild):
        if nul:
            return createEmbed("Match nul !","Le tableau est bloqué, et personne n'a gagné !",0xad917b,"matrice",guild)
        else:
            user=self.joueurs[self.turn]
            embed=createEmbed("Victoire de {0}".format(user.nom),"Bravo à lui/elle !",user.color,"matrice",user.user)
            
            if user.guild==guild.id:
                embed=createEmbed("Victoire de {0}".format(user.nom),"Bravo à lui/elle !",user.color,"matrice",user.user)
            else:
                embed=createEmbed("Victoire de {0}".format(user.titre),"Bravo à lui/elle !",user.color,"matrice",user.user)
                auteurJeux(user,embed)

            embed.add_field(name="<:otCOINS:873226814527520809> gagnés",value="{0} <:otCOINS:873226814527520809>".format(50+sum(self.paris.mises.values())))
            liste=[dict0,dict1,dict2,dict3]
            embed.add_field(name="Combinaison",value="{0}, {1}".format(categ,liste[i][cara]))
            return embed

    async def play(self,message,bot):

        def check(reaction,user):
            if type(reaction.emoji)==str:
                return False
            if reaction.emoji.id in (705766186909958185,705766186989912154,705766186930929685,705766186947706934,705766186713088042,705766187182850148,705766187115741246,705766187132256308) and reaction.message.id==message.id and self.joueurs[self.turn].id==user.id:
                return self.joueurs[self.turn].checkPion(dictCo[reaction.emoji.id])

        try:
            reaction,user=await bot.wait_for('reaction_add', check=check, timeout=40)
            await reaction.remove(user)
            nb=dictCo[reaction.emoji.id]

            def check(mess):
                return self.joueurs[self.turn].id==mess.author.id and message.channel.id==mess.channel.id and self.tab.checkPos(mess.content)

            pion=self.joueurs[self.turn].pions[dictCo[reaction.emoji.id]]
            nom=dict0[pion[0]]+dict1[pion[1]]+dict2[pion[2]]+dict3[pion[3]]
            ask=await message.channel.send("<@{0}> : choisissez sur quelle case poser <:{1}:{2}>".format(self.joueurs[self.turn].id,nom,dictEmotes[pion]))

            messageCoord=await bot.wait_for("message",check=check,timeout=40)
            await ask.delete()
            mot=messageCoord.content
            x,y=dictX[int(mot[1])],dictY[mot[0].lower()]
            await messageCoord.delete()

        except asyncio.exceptions.TimeoutError:
            mot="00"
            while not self.tab.checkPos(mot):
                mot=choice(["a","b","c","d"])+choice(["1","2","3","4"])
            x,y=dictX[int(mot[1])],dictY[mot[0].lower()]
            pion=None
            while pion==None:
                nb=randint(0,7)
                self.joueurs[self.turn].checkPion(nb)
            self.tab.addPion(self.joueurs[self.turn],x,y,nb)
        else:
            self.tab.addPion(self.joueurs[self.turn],x,y,nb)
        return x,y

    def fermeture(self):
        if self.tours==4:
            self.paris.ouvert=False

    async def boucle(self,bot):
        for mess in self.messages:
            await mess.edit(embed=self.embedGame(mess.guild.id))
        while self.playing:
            self.tours+=1
            x,y=await self.play(self.joueurs[self.turn].message,bot)
            win=self.tab.checkTab(x,y)
            if win[0]:  
                nul=self.tab.checkNul()
                if self.tab.checkTab(x,y) or nul:
                    if not nul:
                        await self.stats(self.joueurs[self.turn].id,self.joueurs[self.turn].guild)
                    for mess in self.messages:
                        await mess.clear_reactions()
                        await mess.reply(embed=self.embedEnd(nul,win[1],win[3],win[2],mess.guild))
                        await unpin(mess)
                    self.playing=False
            else:
                if self.turn==0: self.turn=1
                else: self.turn=0
            
            self.fermeture()
            for mess in self.messages:
                await mess.edit(embed=self.embedGame(mess.guild.id))
