from Core.Fonctions.Embeds import createEmbed, embedAssert, exeErrorExcept
import asyncio
import discord
from random import randint
from Core.Fonctions.AuteurIcon import auteur
from Stats.Tracker.Jeux import exeStatsJeux
from Titres.Outils import gainCoins

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
        self.mises={}
        self.emotes={}
        self.guild=guild
        self.tab=TabP4()
        self.tours=0
        self.playing=False
        self.invoke=user
    
    def addPlayer(self,user):
        self.joueurs.append(JoueurP4(user))

    def createEmbedP4(self,turn):
        embed=discord.Embed(title="Au tour de {0}".format(self.joueurs[turn].nom),description=self.affichageTab(),color=self.joueurs[turn].color)
        auteur(self.joueurs[turn].id,self.joueurs[turn].nom,self.joueurs[turn].avatar,embed,"user")
        embed.set_footer(text="OT!p4")
        embed.add_field(name="Joueurs",value="<@{0}> : <:otP1:726164724882079854>\n<@{1}> : <:otP2:726165146229145610>".format(self.joueurs[0].id,self.joueurs[1].id))
        if sum(self.mises.values())!=0:
            descip=""
            for i in self.mises:
                if self.mises[i]!=0:
                    descip+="<@{0}> : {1} <:otCOINS:873226814527520809>\n".format(i,self.mises[i])
            embed.add_field(name="Mises d'OT Coins",value=descip)
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
            embed.add_field(name="<:otCOINS:873226814527520809> gagnés",value="{0} <:otCOINS:873226814527520809>".format(50+sum(self.mises.values())))

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


async def startGameP4(ctx,bot,inGame,gamesP4):
    try:
        assert ctx.author.id not in inGame, "Terminez votre partie en cours avant de lancer ou rejoindre une partie."
        game=JeuP4(ctx.guild,ctx.author.id)
        game.ids.append(ctx.author.id)
        game.mises[ctx.author.id]=0
        inGame.append(ctx.author.id)
        message=await ctx.send(embed=createEmbed("Puissance 4","Appuyez sur la réaction <:otVALIDER:772766033996021761> pour défier <@{0}> au Puissance 4.\nL'objectif est d'aligner 4 jetons de votre couleur dans n'importe quel sens (horizontallement, verticalement ou diagonalement) en premier !\nLes réactions allant de <:ot1:705766186909958185> à <:ot7:705766187115741246> représentent les colonnes où vous pouvez placer votre jeton. Cliquez sur l'une d'entre elles et le jeton apparaîtra !\nLa personne qui a demandé la partie peut cliquer sur <:otANNULER:811242376625782785> pour se retirer de la partie.".format(ctx.author.id),0xad917b,ctx.invoked_with.lower(),ctx.guild))
        gamesP4[message.id]=game

        await message.add_reaction("<:otVALIDER:772766033996021761>")
        await message.add_reaction("<:otANNULER:811242376625782785>")

        for i in range(60):
            if not game.playing:
                await asyncio.sleep(1)
            else:
                break
        
        game.playing=True
        await message.clear_reactions()
        if len(game.ids)<2:
            await message.edit(embed=createEmbed("Puissance 4","Une minute s'est écoulée et personne n'a répondu à l'invitation.",0xad917b,ctx.invoked_with.lower(),ctx.guild))
            for i in game.ids:
                inGame.remove(i)
                return
        for i in game.ids:
            game.addPlayer(ctx.guild.get_member(i))
        descip="<:otVERT:868535645897912330> La partie commence "
        for i in game.joueurs:
            descip+="<@{0}> ".format(i.id)
        await message.channel.send(descip)
        gamesP4[message.id]=game
        try:
            await message.pin()
        except:
            pass
        for i in emotes:
            await message.add_reaction(i)
        await message.add_reaction("<:otCOINS:873226814527520809>")
        messAd=await bot.get_channel(870598360296488980).send("{0} - {1} : partie OT!p4 débutée\n2 joueurs".format(ctx.guild.name,ctx.guild.id))

        turn=randint(0,1)
        while game.playing:
            await message.edit(embed=game.createEmbedP4(turn))
            add=await game.play(turn,message,bot)
            if add[0]==True:
                if game.tab.checkTab(add[1],add[2],turn+1)==True:
                    await message.clear_reactions()
                    await message.edit(embed=game.createEmbedP4(turn))
                    if turn==0: lose=1
                    else: lose=0
                    exeStatsJeux(game.joueurs[turn].id,game.joueurs[lose].id,game.guild.id,"P4",game.tours,"win")
                    gainCoins(game.joueurs[turn].id,50+sum(game.mises.values()))
                    await message.channel.send(embed=game.embedWin(turn,False))
                    game.playing=False
                else:
                    if game.tab.checkNul()==True:
                        await message.clear_reactions()
                        await message.edit(embed=game.createEmbedP4(turn))
                        await message.channel.send(embed=game.embedWin(turn,True))
                        game.playing=False
                    else:
                        game.tours+=1      
                        for i in range(7):
                            if game.tab.tableau[0][i]!=0:
                                await message.clear_reaction(emotes[i])
            turn+=1
            if turn==len(game.joueurs):
                turn=0
        if "messAd" in locals():
            await messAd.delete()
    except AssertionError as er:
        await ctx.send(embed=embedAssert(er))
        return
    except:
        await ctx.send(embed=await exeErrorExcept(ctx,bot,""))
        try:
            await message.unpin()
        except:
            pass
    for i in game.ids:
        inGame.remove(i)
    del gamesP4[message.id]