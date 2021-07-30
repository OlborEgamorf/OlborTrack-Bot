############################################################################

 #######  #########     #########       #######
#       #     #                 #            #     Olbor Track Bot    
#       #     #                 #           #      Créé par OlborEgamorf  
#       #     #         #########          #       Puissance 4
#       #     #         #                 #                  
 #######      #         ############# #  #                         

############################################################################

import discord
import asyncio
import sys 
sys.path.append('OT3/Fonctions')
sys.path.append('OT3/Exe')
from random import randint
from Stats.Tracker.Jeux import exeStatsJeux
from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.Embeds import createEmbed, embedAssert, exeErrorExcept
listeJoueurs=[]
listeJeux={}

embedPerm=discord.Embed(title="<:otRED:718392916061716481> Permission manquante", description="Je ne peux retirer votre réaction ! Donnez moi la permission 'gestion des messages' pour ne plus voir ce message.",color=0xff0000)
embedPerm.set_footer(text="Permission")
emotes=["<:ot1:705766186909958185>","<:ot2:705766186989912154>","<:ot3:705766186930929685>","<:ot4:705766186947706934>","<:ot5:705766186713088042>","<:ot6:705766187182850148>","<:ot7:705766187115741246>","<:otANNULER:811242376625782785>"]
dictCo={705766186909958185:0,705766186989912154:1,705766186930929685:2,705766186947706934:3,705766186713088042:4,705766187182850148:5,705766187115741246:6}
#####


class JoueurP4:
    def __init__(self,user,num):
        self.id=user.id
        self.nom=user.name
        self.color=user.color.value
        self.avatar=user.avatar
        self.play=False
        self.numero=num
    
    def setPlay(self):
        if self.play==True:
            self.play=False
        else:
            self.play=True

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
    def __init__(self,guild,message):
        self.id=message.id
        self.guild=guild
        self.message=message
        self.J1=None
        self.J2=None
        self.temps=0
        self.tab=TabP4()
        self.cheat=False
        self.tours=0
        self.playing=False
        self.ping=False
        self.messAd=None
    
    def addPlayer(self,user,player):
        if player==1:
            self.J1=JoueurP4(user,1)
        else:
            self.J2=JoueurP4(user,2)

    def setTurn(self):
        if randint(1,2)==1:
            self.J1.setPlay()
        else:
            self.J2.setPlay()

    async def timerLoad(self):
        await asyncio.sleep(300)
        if self.playing==False:
            embedP4=discord.Embed(title="Pas d'adversaire trouvé !", description="5 minutes se sont écoulées et personne n'a répondu à l'invitation.", color=0xad917b)
            embedP4.set_footer(text="OT!p4")
            listeJoueurs.remove(self.J1.id)
            await self.message.clear_reactions()
            await self.message.edit(embed=embedP4)
        del listeJeux[self.id]
    
    async def start(self):
        self.playing=True
        while self.temps<90 and self.playing==True:
            await asyncio.sleep(1)
            self.temps+=1
            if self.temps==75:
                if self.J1.play==True:
                    await self.message.channel.send("<:otORANGE:718396570755661884> plus que 15 secondes <@"+str(self.J1.id)+"> !")
                else:
                    await self.message.channel.send("<:otORANGE:718396570755661884> plus que 15 secondes <@"+str(self.J2.id)+"> !")
        if self.playing==True:
            self.J1.setPlay()
            self.J2.setPlay()
            listeJoueurs.remove(self.J1.id)
            listeJoueurs.remove(self.J2.id)
            self.playing=None
            await self.message.clear_reactions()
            await self.message.edit(embed=self.createEmbedP4("Victoire par forfait de "+self.getPlaying().nom))
            exeStatsJeux(self.getPlaying().id,self.getWaiting().id,self.guild,"P4",self.tours)
            await self.messAd.delete()

    def getColor(self):
        return self.getPlaying().color

    def getPlaying(self):
        if self.J1.play==True:
            return self.J1
        else:
            return self.J2
    
    def getWaiting(self):
        if self.J1.play==True:
            return self.J2
        else:
            return self.J1

    def createEmbedP4(self,titre):
        embed=discord.Embed(title=titre,description=self.affichageTab(),color=self.getColor())
        auteur(self.getPlaying().id,self.getPlaying().nom,self.getPlaying().avatar,embed,"user")
        embed.set_footer(text="OT!p4")
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

async def createGameP4(ctx,args,client):
    try:
        assert ctx.author.id not in listeJoueurs, "Vous êtes déjà dans une partie !"
        if len(ctx.message.mentions)>0:
            assert ctx.message.mentions[0].bot==False, "Vous ne pouvez pas jouer contre un robot !"
            assert ctx.message.mentions[0]!=ctx.author, "Vous voulez vraiment vous défier vous même ?"
            assert ctx.message.mentions[0].id not in listeJoueurs, "La personne défiée est déjà dans une partie !"
            descip="<@"+str(ctx.message.mentions[0].id)+"> est défié par <@"+str(ctx.author.id)+"> pour une partie de puissance 4 !\n<@"+str(ctx.message.mentions[0].id)+"> doit appuyer sur la réaction <:otVALIDER:772766033996021761> pour accepter ou <:otANNULER:811242376625782785> pour refuser ou annuler le défi."
        else:
            descip="Appuyez sur la réaction <:otVALIDER:772766033996021761> pour défier <@"+str(ctx.author.id)+"> au puissance 4. La personne qui a demandé la partie peut cliquer sur <:otANNULER:811242376625782785> pour annuler la recherche."
        message=await ctx.send(embed=createEmbed("Puissance 4",descip,0xad917b,ctx.invoked_with.lower(),ctx.author))
        listeJeux[message.id]=JeuP4(ctx.guild.id,message)
        listeJeux[message.id].addPlayer(ctx.author,1)
        if len(ctx.message.mentions)>0:
            listeJeux[message.id].ping=ctx.message.mentions[0].id
        listeJoueurs.append(ctx.author.id)
        client.loop.create_task(listeJeux[message.id].timerLoad())
        await message.add_reaction("<:otVALIDER:772766033996021761>")
        await message.add_reaction("<:otANNULER:811242376625782785>")
    except AssertionError as er:
        await ctx.send(embed=embedAssert(str(er)))
    except:
        await ctx.send(embed=await exeErrorExcept(ctx,client,args))

async def joinGameP4(message,user,reaction,client):
    if message.id not in listeJeux:
        return
    if user.id in listeJoueurs or user.bot==True or (listeJeux[message.id].ping!=False and listeJeux[message.id].ping!=user.id):
        if user.bot==False:
            await reaction.remove(user)
        return
    listeJoueurs.append(user.id)
    listeJeux[message.id].addPlayer(user,2)
    listeJeux[message.id].setTurn()
    client.loop.create_task(listeJeux[message.id].start())
    await message.channel.send("<:otVERT:868535645897912330> Le challenge de <@{0}> a été relevé !".format(listeJeux[message.id].J1.id))
    await message.clear_reactions()
    await message.edit(embed=listeJeux[message.id].createEmbedP4(listeJeux[message.id].J1.nom+" VS "+listeJeux[message.id].J2.nom))
    for i in emotes:
        await message.add_reaction(i)
    listeJeux[message.id].messAd=await client.get_channel(870598360296488980).send("{0} - {1} : partie OT!p4 débutée".format(message.guild.name,message.guild.id))

async def playGameP4(message,user,reaction):
    if message.id not in listeJeux:
        return
    if (listeJeux[message.id].J1.id!=user.id and listeJeux[message.id].J2.id!=user.id) or listeJeux[message.id].cheat==True:
        if user.bot==False:
            await reaction.remove(user)
        return
    if (listeJeux[message.id].J1.id==user.id and listeJeux[message.id].J1.play==True) or (listeJeux[message.id].J2.id==user.id and listeJeux[message.id].J2.play==True):
        listeJeux[message.id].cheat=True
        add=listeJeux[message.id].tab.addJeton(dictCo[reaction.emoji.id],listeJeux[message.id].getPlaying().numero)
        if add[0]==True:
            if listeJeux[message.id].tab.checkTab(add[1],add[2],listeJeux[message.id].getPlaying().numero)==True:
                await message.clear_reactions()
                await message.edit(embed=listeJeux[message.id].createEmbedP4("Victoire de "+listeJeux[message.id].getPlaying().nom))
                listeJoueurs.remove(listeJeux[message.id].J1.id)
                listeJoueurs.remove(listeJeux[message.id].J2.id)
                listeJeux[message.id].playing=None
                exeStatsJeux(listeJeux[message.id].getPlaying().id,listeJeux[message.id].getWaiting().id,listeJeux[message.id].guild,"P4",listeJeux[message.id].tours)
                await listeJeux[message.id].messAd.delete()
            else:
                if listeJeux[message.id].tab.checkNul()==True:
                    await message.clear_reactions()
                    await message.edit(embed=listeJeux[message.id].createEmbedP4("Match nul !"))
                    listeJoueurs.remove(listeJeux[message.id].J1.id)
                    listeJoueurs.remove(listeJeux[message.id].J2.id)
                    listeJeux[message.id].playing=None
                    await listeJeux[message.id].messAd.delete()
                else:
                    listeJeux[message.id].J1.setPlay()
                    listeJeux[message.id].J2.setPlay()
                    listeJeux[message.id].temps=0
                    listeJeux[message.id].tours+=1
                    await message.edit(embed=listeJeux[message.id].createEmbedP4(listeJeux[message.id].J1.nom+" VS "+listeJeux[message.id].J2.nom))
                    await reaction.remove(user)
        else:
            await reaction.remove(user)
        listeJeux[message.id].cheat=False
    else:
        await reaction.remove(user)

async def abandonP4(message,user,reaction):
    if message.id not in listeJeux:
        return
    if listeJeux[message.id].playing==True:
        if listeJeux[message.id].J1.id!=user.id and listeJeux[message.id].J2.id!=user.id:
            if user.bot==False:
                await reaction.remove(user)
            return
        if listeJeux[message.id].getPlaying().id==user.id:
            listeJeux[message.id].J1.setPlay()
            listeJeux[message.id].J2.setPlay()
        listeJoueurs.remove(listeJeux[message.id].J1.id)
        listeJoueurs.remove(listeJeux[message.id].J2.id)
        listeJeux[message.id].playing=None
        await message.clear_reactions()
        await message.edit(embed=listeJeux[message.id].createEmbedP4("Victoire par forfait de "+listeJeux[message.id].getPlaying().nom))
        await listeJeux[message.id].messAd.delete()
        exeStatsJeux(listeJeux[message.id].getPlaying().id,listeJeux[message.id].getWaiting().id,listeJeux[message.id].guild,"P4",listeJeux[message.id].tours)
    else:
        if listeJeux[message.id].J1.id!=user.id and listeJeux[message.id].ping!=user.id:
            if user.bot==False:
                await reaction.remove(user)
            return
        embedP4=discord.Embed(title="Défi annulé", description="La recherche de partie a été annulée.", color=0xad917b)
        embedP4.set_footer(text="OT!p4")
        listeJoueurs.remove(listeJeux[message.id].J1.id)
        listeJeux[message.id].playing=None
        await message.clear_reactions()
        await message.edit(embed=embedP4)