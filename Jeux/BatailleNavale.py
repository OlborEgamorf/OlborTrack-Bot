import asyncio
import sys
from operator import itemgetter
from random import randint

import discord
from Core.Fonctions.Embeds import (createEmbed, embedAssert,
                                   exeErrorExcept)
from Stats.Tracker.Jeux import exeStatsJeux

listeJoueurs={}
listeJeux={}
dictReact={2:"\U0001F534",3:"\U000026AA",4:"\U0001F7E0"}
dictEmotes={191:":mermaid:",192:":ocean:",193:":man_rowing_boat:",194:":man_swimming:",195:":person_surfing:",196:":woman_rowing_boat:",197:":speedboat:",198:":motorboat:",199:":cruise_ship:",200:":ferry:"}


class JeuBN:
    def __init__(self,guild,message):
        self.id=message.id
        self.message=message
        self.guild=guild
        self.J1=None
        self.J2=None
        self.temps=0
        self.cheat=False
        self.position=False
        self.playing=False
        self.ping=False
        self.count=0

    def addPlayer(self,user,player):
        if player==1:
            self.J1=JoueurBN(user,1)
        else:
            self.J2=JoueurBN(user,2)

    def setTurn(self):
        if randint(1,2)==1:
            self.J1.setPlay()
        else:
            self.J2.setPlay()

    def getPlaying(self):
        if self.J1.play:
            return self.J1
        return self.J2
    
    def getWaiting(self):
        if self.J1.play:
            return self.J2
        return self.J1
    
    def getOther(self,joueur):
        if joueur.numero==1:
            return self.J2
        else:
            return self.J1

    async def timerLoad(self):
        await asyncio.sleep(300)
        if self.playing==False and self.position==False:
            embedBN=discord.Embed(title="Pas d'adversaire trouvé !", description="5 minutes se sont écoulées et personne n'a répondu à l'invitation.", color=0xad917b)
            embedBN.set_footer(text="OT!bataillenavale")
            del listeJoueurs[self.J1.id]
            await self.message.clear_reactions()
            await self.message.edit(embed=createEmbed("Bataille navale","5 minutes se sont écoulées et personne n'a répondu à l'invitation.",0xad917b,"bataillenavale",self.J1.user))
            del listeJeux[self.id]
        
    async def timerGame(self):
        self.position=True
        while self.temps<180 and self.position:
            await asyncio.sleep(1)
            self.temps+=1
            if self.temps==160:
                if not self.J1.position:
                    await self.J1.user.send("<:otORANGE:868538903584456745> plus que 20 secondes pour finir vos placements !")
                if not self.J2.position:
                    await self.J2.user.send("<:otORANGE:868538903584456745> plus que 20 secondes pour finir vos placements !")

        if self.position:
            listeJ=[self.J1,self.J2]
            for joueur in listeJ:
                if not joueur.position:
                    listeP=[joueur.plateau.porteavion,joueur.plateau.croiseur,joueur.plateau.contretorp,joueur.plateau.sousmarin,joueur.plateau.torpilleur]
                    listeB=[PorteAvion(),Croiseur(),ContreTorpilleur(),SousMarin(),Torpilleur()]
                    for i in range(5):
                        if listeP[i]==None:
                            joueur.plateau.randomizer(listeB[i])
                    await joueur.editMessage(self,False)
                    await joueur.user.send("J'ai placé aléatoirement les bateaux qui vous restaient.")
            await endPosition(self)

        while self.temps<60 and self.playing:
            await asyncio.sleep(1)
            self.temps+=1
            if self.temps==50:
                if self.J1.play:
                    await self.J1.user.send("<:otORANGE:868538903584456745> plus que 10 secondes <@"+str(self.J1.id)+"> !")
                else:
                    await self.J2.user.send("<:otORANGE:868538903584456745> plus que 10 secondes <@"+str(self.J2.id)+"> !")

        if self.playing:
            self.J1.setPlay()
            self.J2.setPlay()
            await endGame(self)
        del listeJeux[self.id]

    def createEmbedBN(self,spoil,author,dev):
        descip=author.affichageTab(spoil)
        title="{0} vs {1}".format(self.J1.nom,self.J2.nom)
        embed=createEmbed(title,descip,author.color,"bataillenavale",author.user)
        nom=("`pa` Porte-avion (5 cases)","`cr` Croiseur (4)","`ct` Contre-torpilleur (3)","`sm` Sous-marin (3)","`to` Torpilleur (2)")
        if spoil and dev:
            value=""
            bateaux=(author.plateau.porteavion,author.plateau.croiseur,author.plateau.contretorp,author.plateau.sousmarin,author.plateau.torpilleur)
            for i in range(5):
                if bateaux[i] is None:
                    value+="{0} : Pas placé\n".format(nom[i])
                else:
                    coords=""
                    for j in bateaux[i]:
                        coords+="{0} ".format(convTabToCoord(j,author.plateau.tab))
                    value+="{0} : {1}\n".format(nom[i],coords)
            embed.add_field(name="Placements",value=value,inline=False)
        return embed
        

class JoueurBN:
    def __init__(self,user,num):
        self.id=user.id
        self.user=user
        self.messageP=None
        self.messageA=None
        self.nom=user.name
        self.color=user.color.value
        self.play=False
        self.position=False
        self.plateau=PlateauBN(user)
        self.numero=num
        self.dev=True
        self.count=0

    def setPlay(self):
        if self.play:
            self.play=False
        else:
            self.play=True

    async def unpinAll(self):
        for pin in await self.user.pins():
            await pin.unpin()

    async def setMessage(self,jeu,react):
        if self.messageP!=None:
            await self.messageP.delete()
        if self.messageA!=None:
            await self.messageA.delete()
        self.messageP=await self.user.send(embed=jeu.createEmbedBN(True,self,self.dev))
        self.messageA=await self.user.send(embed=jeu.createEmbedBN(False,jeu.getOther(self),False))
        await self.messageP.pin()
        await self.messageA.pin()
        if react:
            await self.messageP.add_reaction("<:otVALIDER:772766033996021761>")
        await self.messageP.add_reaction("<:otANNULER:811242376625782785>")

    async def editMessage(self,jeu,both):
        await self.messageP.edit(embed=jeu.createEmbedBN(True,self,self.dev))
        if both:
            await self.messageA.edit(embed=jeu.createEmbedBN(False,jeu.getOther(self),False))

    async def finishPosition(self):
        if None not in (self.plateau.porteavion,self.plateau.croiseur,self.plateau.contretorp,self.plateau.sousmarin,self.plateau.torpilleur):
            self.position=True
            return True
        else:
            await self.user.send("Vous n'avez pas placé tous vos bateaux !")
            return False

    def affichageTab(self,spoil):
        descip="<:otBlank:828934808200937492>:regional_indicator_a::regional_indicator_b::regional_indicator_c::regional_indicator_d::regional_indicator_e::regional_indicator_f::regional_indicator_g::regional_indicator_h::regional_indicator_i::regional_indicator_j:\n"
        count=0
        for i in range(len(self.plateau.tab)):
            if i+1<10:
                descip+="` {0}`".format(i+1)
            else:
                descip+="`{0}`".format(i+1)
            for j in self.plateau.tab[i]:
                if j==1 and spoil:
                    descip+=":blue_circle:"
                elif j==2:
                    descip+=":red_circle:"
                elif j==3:
                    descip+=":white_circle:"
                elif j==4:
                    descip+=":orange_circle:"
                else:
                    rand=randint(0,200)
                    if rand<=190 or count>=4:
                        descip+=":black_circle:"
                    else:
                        count+=1
                        descip+=dictEmotes[rand]
            descip+="\n"
        return descip


class PlateauBN:
    def __init__(self,joueur):
        self.tab=[[0]*10 for i in range(10)]
        self.porteavion=None
        self.croiseur=None
        self.contretorp=None
        self.sousmarin=None
        self.torpilleur=None
        self.joueur=joueur

    def tir(self,coords):
        if self.tab[coords[0]][coords[1]]==0:
            self.tab[coords[0]][coords[1]]=3
        elif self.tab[coords[0]][coords[1]]==1:
            self.tab[coords[0]][coords[1]]=2
            for i in (self.porteavion,self.croiseur,self.contretorp,self.sousmarin,self.torpilleur):
                if coords in i:
                    count=0
                    for j in i:
                        if self.tab[j[0]][j[1]]==2:
                            count+=1
                    if count==len(i):
                        for j in i:
                            self.tab[j[0]][j[1]]=4
                    break

        else:
            return False,0
        return True, self.tab[coords[0]][coords[1]]

    def victoire(self):
        for i in self.tab:
            if 1 in i:
                return False
        return True

    async def placement(self,coord,bateau):
        try:
            tabTemp=[]
            for i in self.tab:
                tabTemp.append(i.copy())

            if len(coord)!=bateau.cases and len(coord)==2:
                expend=[]
                if coord[0][0]==coord[1][0]:
                    for i in range(int(coord[0][1:len(coord[0])]),int(coord[1][1:len(coord[1])])+1):
                        expend.append("{0}{1}".format(coord[0][0],i))
                elif coord[0][1:len(coord[0])]==coord[1][1:len(coord[1])]:
                    for i in range(ord(coord[0][0]),ord(coord[1][0])+1):
                        expend.append("{0}{1}".format(chr(i),coord[0][1:len(coord[0])]))
                coord=expend

            assert len(coord)==bateau.cases, "Le nombre de cases données ne correspond pas à la taille du bateau. Il en faut {0} pour ce bateau.".format(bateau.cases)
            newCoord=[]
            bateau.supprime(self)
            for i in coord:
                new=convCoordToTab(i)
                assert self.checkOthers(new[0],new[1]), "La case {0} est déjà assignée !".format(i)
                newCoord.append(new)
            newCoord=sorted(newCoord,key=itemgetter(0),reverse=False)
            newCoord=sorted(newCoord,key=itemgetter(1),reverse=False)
            assert self.checkCoords(newCoord), "Le placement n'est pas correct."
            for i in newCoord:
                self.tab[i[0]][i[1]]=1
            bateau.placement(newCoord,self)

        except AssertionError as er:
            await self.joueur.send(er,delete_after=8)
            self.tab=tabTemp
            return False
        return True

    def checkCoords(self,coord):
        countI,countJ=1,1
        tempI,tempJ=coord[0][0],coord[0][1]
        stillI,stillJ=coord[0][1],coord[0][0]
        for i in range(1,len(coord)):
            if tempI==coord[i][0]-1 and stillI==coord[i][1]:
                countI+=1
                tempI=coord[i][0]
            if tempJ==coord[i][1]-1 and stillJ==coord[i][0]:
                countJ+=1
                tempJ=coord[i][1] 
        return countI==len(coord) or countJ==len(coord)

    def checkOthers(self,x,y):
        return self.tab[x][y]==0

    def randomizer(self,bateau):
        cases=bateau.cases
        posi=False
        while not posi:
            liste=[]
            if randint(1,2)==1:                     # hauteur
                x,y=randint(0,9-cases),randint(0,9)
                for i in range(cases):
                    if self.tab[x+i][y]==0:
                        liste.append((x+i,y))
            else:                                   # longueur
                x,y=randint(0,9),randint(0,9-cases)
                for i in range(cases):
                    if self.tab[x][y+i]==0:
                        liste.append((x,y+i))
            if len(liste)==cases:
                posi=True
        for i in liste:
            self.tab[i[0]][i[1]]=1
        bateau.placement(liste,self)
        return liste


class PorteAvion:
    def __init__(self):
        self.cases=5

    def placement(self,coord,plateau):
        plateau.porteavion=coord

    def supprime(self,plateau):
        if plateau.porteavion!=None:
            for i in plateau.porteavion:
                plateau.tab[i[0]][i[1]]=0

class Croiseur:
    def __init__(self):
        self.cases=4

    def placement(self,coord,plateau):
        plateau.croiseur=coord

    def supprime(self,plateau):
        if plateau.croiseur!=None:
            for i in plateau.croiseur:
                plateau.tab[i[0]][i[1]]=0

class ContreTorpilleur:
    def __init__(self):
        self.cases=3

    def placement(self,coord,plateau):
        plateau.contretorp=coord
    
    def supprime(self,plateau):
        if plateau.contretorp!=None:
            for i in plateau.contretorp:
                plateau.tab[i[0]][i[1]]=0

class SousMarin:
    def __init__(self):
        self.cases=3

    def placement(self,coord,plateau):
        plateau.sousmarin=coord
    
    def supprime(self,plateau):
        if plateau.sousmarin!=None:
            for i in plateau.sousmarin:
                plateau.tab[i[0]][i[1]]=0

class Torpilleur:
    def __init__(self):
        self.cases=2

    def placement(self,coord,plateau):
        plateau.torpilleur=coord
    
    def supprime(self,plateau):
        if plateau.torpilleur!=None:
            for i in plateau.torpilleur:
                plateau.tab[i[0]][i[1]]=0


async def createGame(ctx,args,client):
    try:
        assert ctx.author.id not in listeJoueurs, "Vous êtes déjà dans une partie !"
        if len(ctx.message.mentions)>0:
            assert not ctx.message.mentions[0].bot, "Vous ne pouvez pas jouer contre un robot !"
            assert ctx.message.mentions[0]!=ctx.author, "Vous voulez vraiment vous défier vous même ?"
            assert ctx.message.mentions[0].id not in listeJoueurs, "La personne défiée est déjà dans une partie !"
            descip="<@{1}> est défié par <@{0}> pour une partie de bataille navale !\n<@{1}> doit appuyer sur la réaction <:otVALIDER:772766033996021761> pour accepter ou <:otANNULER:811242376625782785> pour refuser ou annuler le défi.".format(ctx.author.id,ctx.message.mentions[0].id)
        else:
            descip="Appuyez sur la réaction <:otVALIDER:772766033996021761> pour défier <@{0}> à la bataille navale. La personne qui a demandé la partie peut cliquer sur <:otANNULER:811242376625782785> pour annuler la recherche.".format(ctx.author.id)
        message=await ctx.send(embed=createEmbed("Bataille navale",descip,0xad917b,ctx.invoked_with.lower(),ctx.author))
        listeJeux[message.id]=JeuBN(ctx.guild.id,message)
        listeJeux[message.id].addPlayer(ctx.author,1)
        if len(ctx.message.mentions)>0:
            listeJeux[message.id].ping=ctx.message.mentions[0].id
        listeJoueurs[ctx.author.id]=message.id
        client.loop.create_task(listeJeux[message.id].timerLoad())
        await message.add_reaction("<:otVALIDER:772766033996021761>")
        await message.add_reaction("<:otANNULER:811242376625782785>")
    except AssertionError as er:
        await ctx.send(embed=embedAssert(str(er)))
    except:
        await ctx.send(embed=await exeErrorExcept(ctx,client,args))

async def joinGame(message,user,reaction,client):
    try:
        if message.id not in listeJeux:
            return
        if user.id in listeJoueurs or user.bot or (listeJeux[message.id].ping!=False and listeJeux[message.id].ping!=user.id):
            if not user.bot:
                try:
                    await reaction.remove(user)
                except:
                    pass
            return
        game=listeJeux[message.id]
        listeJoueurs[user.id]=message.id
        game.addPlayer(user,2)
        game.setTurn()
        game.position=True
        listeJ=[game.J1,game.J2]
        for joueur in listeJ:
            await joueur.unpinAll()
            await joueur.setMessage(game,True)
            await joueur.user.send("<:otVERT:868535645897912330> Bienvenue dans cette partie ! Vous avez 3 minutes pour placer vos bateaux. Pour ce faire, donnez moi un diminutif de bateau (pa, cr, ct, sm, to) et les cases où vous voulez le placer. Vous avez un exemplaire de chaque bateau, et chaque bateau a son nombre de cases à respecter, visible dans la section 'placements'. Les cases doivent se suivre dans le tableau, à l'horizontale ou à la verticale.\nExemples : cr B2 B3 B4 B5 / to G2 F2 / sm A6 B6 C6 / pa J2 J6\nPour confirmer votre positionnement, vous devez avoir placé les 5 bateaux, puis cliquer sur la réaction <:otVALIDER:772766033996021761>.")
        client.loop.create_task(game.timerGame())
        await message.channel.send("<:otVERT:868535645897912330> Le challenge de <@{0}> a été relevé !".format(game.J1.id))
        await message.clear_reactions()
        await message.edit(embed=createEmbed("Partie en cours.","Les résultats arrivent bientôt.",0xad917b,"bataillenavale",message.guild))
        listeJeux[message.id].messAd=await client.get_channel(870598360296488980).send("{0} - {1} : partie OT!bataillenavale débutée".format(message.guild.name,message.guild.id))
    except discord.errors.Forbidden:
        del listeJoueurs[game.J1.id]
        del listeJoueurs[game.J2.id]
        game.playing=None
        await message.channel.send(embed=embedAssert("Je ne suis pas authorisé à envoyer des messages privés à un des deux joueurs de la partie. Vériez vos paramètres."))

async def playGame(user,message):
    if user.id not in listeJoueurs:
        return
    game=listeJeux[listeJoueurs[user.id]]
    content=message.content.lower().split(" ")
    joueur=getUser(game,user.id)

    if game.position:
        joueur.count+=1
        if joueur.count>10:
            await joueur.setMessage(game,True)
            joueur.count=0

        if joueur.position:
            return
        else:
            try:
                if await joueur.plateau.placement(content[1:len(content)],dictArgs[content[0]]):
                    await joueur.editMessage(game,False)
                    await message.add_reaction("<:otOUI:726840394150707282>")
                else:
                    await message.add_reaction("<:otNON:740174227998769172>")
            except:
                await message.add_reaction("<:otNON:740174227998769172>")

    elif game.playing:
        messageO=await game.getOther(joueur).user.send("{0} : {1}".format(joueur.nom,message.content))
        game.count+=1
        if not game.cheat:
            if (game.J1.id==user.id and game.J1.play) or (game.J2.id==user.id and game.J2.play):
                game.cheat=True
                try:
                    tir=game.getWaiting().plateau.tir(convCoordToTab(content[0]))
                    if tir[0]:
                        await message.add_reaction(dictReact[tir[1]])
                        await messageO.add_reaction(dictReact[tir[1]])
                        if game.getWaiting().plateau.victoire():
                            await endGame(game)
                        else:
                            await game.J1.editMessage(game,True)
                            await game.J2.editMessage(game,True)
                            await game.message.edit(embed=game.createEmbedBN(False,game.getWaiting(),False))
                            if tir[1]==3:
                                game.J1.setPlay()
                                game.J2.setPlay()
                            game.temps=0
                    else:
                        await message.add_reaction("<:otNON:740174227998769172>")
                        await messageO.add_reaction("<:otNON:740174227998769172>")
                except AssertionError:
                    pass
            game.cheat=False
        if game.count>10:
            await game.J1.setMessage(game,False)
            await game.J2.setMessage(game,False)
            game.count=0

async def validPosition(user,message):
    if user.id in listeJoueurs:
        if listeJoueurs[user.id] not in listeJeux:
            return
        game=listeJeux[listeJoueurs[user.id]]
        joueur=getUser(game,user.id)

        if joueur.messageP.id!=message.id:
            return
        if not joueur.position:
            if await joueur.finishPosition():
                await joueur.user.send("<:otVERT:868535645897912330> Placements confirmés. Vous ne pouvez plus revenir en arrière.")
                await game.getOther(joueur).user.send("<:otVERT:868535645897912330> {0} a terminé ses placements.".format(joueur.nom))
    
        if game.J1.position and game.J2.position:
            await endPosition(game)

async def cancelGame(message,user,reaction):
    if message.id in listeJeux:
        game=listeJeux[message.id]
        if game.J1.id!=user.id and game.ping!=user.id:
            if user.bot==False:
                await reaction.remove(user)
            return
        del listeJoueurs[game.J1.id]
        game.playing=None
        await message.clear_reactions()
        await message.edit(embed=createEmbed("Bataille navale","Recherche annulée",0xad917b,"bataillenavale",user))
    else:
        if user.id not in listeJoueurs:
            return
        game=listeJeux[listeJoueurs[user.id]]
        if game.getPlaying().id==user.id:
            game.J1.setPlay()
            game.J2.setPlay()
        game.position=None
        await endGame(game)

async def endGame(game):
    listeJ=[game.J1,game.J2]
    for i in listeJ:
        await i.messageP.delete()
        await i.messageA.delete()
        await i.user.send(embed=game.createEmbedBN(True,i,True))
        await i.user.send(embed=game.createEmbedBN(True,game.getOther(i),True))
        await i.user.send("<:otVERT:868535645897912330> Victoire de {0} !".format(game.getPlaying().nom))
    exeStatsJeux(game.getPlaying().id,game.getWaiting().id,game.guild,"BatailleNavale",0)
    await game.message.channel.send(embed=game.createEmbedBN(True,game.getWaiting(),True))
    await game.message.channel.send(embed=game.createEmbedBN(True,game.getPlaying(),True))
    await game.message.channel.send("<:otVERT:868535645897912330> Victoire de {0} !".format(game.getPlaying().nom))
    await game.message.delete()
    del listeJoueurs[game.J1.id]
    del listeJoueurs[game.J2.id]
    game.playing=None
    await game.messAd.delete()

async def endPosition(game):
    game.temps=0
    game.count=int((game.J2.count+game.J1.count)/2)
    game.position=False
    game.playing=True
    await game.getWaiting().user.send("<:otORANGE:868538903584456745> Placements terminés ! \n__Votre adversaire commence à jouer.__\nPour attaquer, donnez une coordonnée d'une case. \nSi :white_circle: apparait, c'est que le tir est manqué. Si :red_circle: apparait, c'est que vous avez touché, et :orange_circle: si vous avez coulé. Par contre, si les coordonnées ne sont pas bonnes, <:otNON:740174227998769172> sera envoyé. Et si rien ne se passe, réessayez.\n**Quand vous touchez, vous rejouez.**")
    await game.getPlaying().user.send("<:otORANGE:868538903584456745> Placements terminés ! \n__C'est à vous de jouer.__\nPour attaquer, donnez une coordonnée d'une case. \nSi :white_circle: apparait, c'est que le tir est manqué. Si :red_circle: apparait, c'est que vous avez touché, et :orange_circle: si vous avez coulé. Par contre, si les coordonnées ne sont pas bonnes, <:otNON:740174227998769172> sera envoyé. Et si rien ne se passe, réessayez.\n**Quand vous touchez, vous rejouez.**")


def getUser(jeu,id):
    if jeu.J1.id==id:
        return jeu.J1
    else:
        return jeu.J2

def convCoordToTab(coord):
    dictX={"a":0,"b":1,"c":2,"d":3,"e":4,"f":5,"g":6,"h":7,"i":8,"j":9}
    try:
        assert int(coord[1:len(coord)])-1>=0 and int(coord[1:len(coord)])-1<=9
        return (int(coord[1:len(coord)])-1,dictX[coord[0]])
    except:
        raise AssertionError("Vos coordonnées {0} ne sont pas valides.".format(coord))

def convTabToCoord(tab,plateau):
    dictX={0:"A",1:"B",2:"C",3:"D",4:"E",5:"F",6:"G",7:"H",8:"I",9:"J"}
    if plateau[tab[0]][tab[1]] in (2,4):
        return "~~{0}{1}~~ ".format(dictX[tab[1]],tab[0]+1)
    else:
        return "{0}{1} ".format(dictX[tab[1]],tab[0]+1)





    
dictArgs={"pa":PorteAvion(),"cr":Croiseur(),"ct":ContreTorpilleur(),"sm":SousMarin(),"to":Torpilleur()}




# 0 : rien/vide/nada/NEANT
# 1 : bateau
# 2 : touché
# 3 : manqué (dans l'eau)
# 4 : coulé
