import asyncio
from random import choice, randint

import discord
from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.Embeds import createEmbed
from Core.Fonctions.WebRequest import getAvatar
from PIL import Image, ImageDraw, ImageFont
from Stats.SQL.ConnectSQL import connectSQL
from Stats.SQL.Execution import exeJeuxSQL
from Titres.Carte import sendCarte
from Titres.Outils import gainCoins

from Jeux.Outils.Bases import JeuBase, JoueurBase
from Outils.Bienvenue.Manipulation import squaretoround

dictColor={1:0xFF4600,2:0x5C99EC}
montage=(((125,45),(475,45),(825,45),(1175,45),(1525,45)),((125,293),(475,293),(825,293),(1175,293),(1525,293)),((125,541),(475,541),(825,541),(1175,541),(1525,541)),((125,789),(475,789),(825,789),(1175,789),(1525,789)),((125,1037),(475,1037),(825,1037),(1175,1037),(1525,1037)))

class Mot:
    def __init__(self,mot):
        self.x=0
        self.y=0
        self.mot=mot
        self.equipe=None
        self.find=False
        self.findplayer=None

    def setFind(self,joueur):
        self.find=True
        self.findplayer=joueur

    def setCoords(self,x,y,equipe):
        self.x=x
        self.y=y
        self.equipe=equipe

class JoueurCN(JoueurBase):
    def __init__(self,user,equipe,role):
        super().__init__(user)
        self.equipe=equipe
        self.role=role
   

class JeuCodeNames(JeuBase):
    def __init__(self,message,user):
        super().__init__(message,user,"CodeNames",False)
        self.plateau=[]
        self.equipe={1:[],2:[]}

    def addPlayer(self,user,role):
        dictEquipe={893548469309038633:1,893548469229346896:1,893548469212561468:2,893548468822495263:2}
        dictRole={893548469309038633:"mj",893548469229346896:"dev",893548469212561468:"mj",893548468822495263:"dev"}
        joueur=JoueurCN(user,dictEquipe[role],dictRole[role])
        self.joueurs.append(joueur)
        self.equipe[dictEquipe[role]].append(joueur)
    
    def embedEnd(self,win):
        descip=""
        embed=discord.Embed(title="Victoire de {0} et {1} !".format(self.equipe[win][0].name,self.equipe[win][1].name), description="Ils ont réussi à déviner tous les mots !", color=dictColor[win])

        for i in self.joueurs:
            dictRole={"mj":"maitre du jeu","dev":"devineur"}
            dictEquipe={1:"rouge",2:"bleue"}
            descip+="<@{0}> : équipe {1}, {2}\n".format(i.id,dictEquipe[i.equipe],dictRole[i.role])
        
        embed.add_field(name="<:otCOINS:873226814527520809> gagnés par chacun des gagnants",value="{0} <:otCOINS:873226814527520809>".format(75+sum(self.mises.values())/2))

        embed=auteur(self.guild.id,self.guild.name,self.guild.icon,embed,"guild")
        embed.set_footer(text="OT!codenames")
        embed.description+="\n\n"+descip
        return embed
    
    async def stats(self,team,chan):
        connexionGuild,curseurGuild=connectSQL(self.guild.id,"Guild","Guild",None,None)
        connexionOT,curseurOT=connectSQL("OT","Guild","Guild",None,None)
        for i in self.joueurs:
            if i.equipe==team:
                gainCoins(i.id,75+sum(self.paris.mises.values())/2)
                state="W"
            else:
                state="L"
            exeJeuxSQL(i.id,None,state,self.guild.id,curseurGuild,"CodeNames",None)
            wins=exeJeuxSQL(i.id,None,state,"OT",curseurOT,"CodeNames",None)
            if state=="W":
                await sendCarte(i.user,"CodeNames",wins,False,chan)
        connexionGuild.commit()
        connexionOT.commit()

    async def startGame(self,message,inGame,ctx,mini,bot):
        if await super().startGame(ctx,bot,inGame,[],mini):
            self.message=self.messages[0]
            self.guild=self.guilds[0]
            dictChoix={893548469309038633:"Equipe rouge, maitre du jeu",893548469229346896:"Equipe rouge, devineur",893548469212561468:"Equipe bleue, maître du jeu",893548468822495263:"Equipe bleue, devineur"}
            dictEmote={893548469309038633:"<:otRouge1:893548469309038633>",893548469229346896:"<:otRouge2:893548469229346896>",893548469212561468:"<:otBleu1:893548469212561468>",893548468822495263:"<:otBleu2:893548468822495263>"}
            mess=await message.channel.send(embed=createEmbed("Code Names","Chacun votre tour, vous allez choisir votre équipe et votre rôle !\nVous pouvez vous mettre d'accord à l'avance sur les équipes ! Vous aurez chacun 15 secondes pour choisir, sinon le choix sera aléatoire.\n\n- <:otRouge1:893548469309038633> : Equipe rouge, maître du jeu\n- <:otRouge2:893548469229346896> : Equipe rouge, devineur\n- <:otBleu1:893548469212561468> : Equipe bleue, maître du jeu\n- <:otBleu2:893548468822495263> : Equipe bleue, devineur",0xad917b,ctx.invoked_with.lower(),ctx.guild))
            for j in ("<:otRouge1:893548469309038633>","<:otRouge2:893548469229346896>","<:otBleu1:893548469212561468>","<:otBleu2:893548468822495263>"):
                await mess.add_reaction(j)
            liste=[893548469309038633,893548469229346896,893548469212561468,893548468822495263]
            for i in self.ids:
                try:
                    user=ctx.guild.get_member(i)
                    await getAvatar(user)
                    squaretoround(user.id)
                    messUser=await message.channel.send("<:otVERT:868535645897912330> <@{0}>, c'est à vous de choisir".format(i))
                    def check(reaction,user):
                        if type(reaction.emoji)==str:
                            return False
                        return reaction.message.id==mess.id and user.id==i and reaction.emoji.id in liste
                    
                    reaction,user=await bot.wait_for('reaction_add', check=check, timeout=15)
                    role=reaction.emoji.id
                except asyncio.TimeoutError:
                    role=choice(liste)
                liste.remove(role)
                await messUser.edit(content="<:otVERT:868535645897912330> <@{0}>, a choisi {1}".format(i,dictChoix[role]))
                await mess.clear_reaction(dictEmote[role])
                self.addPlayer(user,role)
                if role in (893548469309038633,893548469212561468):
                    try:
                        await user.send("<:otVERT:868535645897912330> Vous m'avez bel et bien autorisé à vous envoyer des messages privés, vous êtes dans la partie !")
                    except:
                        await message.channel.send("<:otROUGE:868535622237818910> <@{0}> vous devez m'autoriser à vous envoyer des messages privés ! Modifiez vos paramètres de confidentialité sur ce serveur avant le début de la partie !".format(user.id))
            
            self.turn=self.generateGame()
            self.showPlateau(True)
            self.showPlateau(False)
            for i in self.joueurs:
                if i.role=="mj":
                    await i.user.send(file=discord.File("Images/Plateau{0}True.png".format(self.guild.id)),embed=self.embedMJ(i.equipe,i.user),content="Vous avez 2 minutes pour réfléchir...")
            message=await message.channel.send(file=discord.File("Images/Plateau{0}False.png".format(self.guild.id)),embed=self.embedCompo())
            await asyncio.sleep(120)
            return True
        return False

    def fermeture(self):
        self.paris.ouvert=False

    def generateGame(self):
        connexion,curseur=connectSQL("OT","Codenames","Titres",None,None)
        liste=curseur.execute("SELECT Mots FROM code ORDER BY RANDOM() ASC LIMIT 60").fetchall()
        mots=[]
        final=[]
        for i in liste:
            mots.append(i["Mots"])
        for i in range(25):
            mot=choice(mots)
            final.append(mot)
            curseur.execute("UPDATE code SET Usage=Usage+1 WHERE Mots='{0}'".format(mot))
            mots.remove(mot)
        connexion.commit()
        for i in final:
            self.plateau.append(Mot(i))

        turn=randint(1,2)
        
        listeCoords=[[x,y] for x in range(5) for y in range(5)]
        liste=[0]*7+[1]*8+[2]*8+[3]+[turn]
        for i in range(25):
            coord=choice(listeCoords)
            listeCoords.remove(coord)
            self.plateau[i].setCoords(coord[0],coord[1],liste[i])

        return turn

    def showPlateau(self,mj):
        fond=Image.open("Images/CodeNames/VIDE.png")
        barre=Image.open("Images/CodeNames/BARRE.png")
        for i in self.plateau:
            carte=self.createCarte(i,mj)
            fond.paste(carte,montage[i.x][i.y],mask=carte)
            if i.find:
                fond.paste(barre,montage[i.x][i.y],mask=barre)
        fond.save("Images/Plateau{0}{1}.png".format(self.guild.id,mj))

    def createCarte(self,mot,mj):
        if mj or mot.find:
            if mot.equipe==0:
                carte=Image.open("Images/CodeNames/CarteNeutreW.png")
            elif mot.equipe==1:
                carte=Image.open("Images/CodeNames/CarteRouge.png")
            elif mot.equipe==2:
                carte=Image.open("Images/CodeNames/CarteBleue.png")
            else:
                carte=Image.open("Images/CodeNames/CarteNoire.png")
        else:
            carte=Image.open("Images/CodeNames/CarteNeutreW.png")
        font = ImageFont.truetype("Font/RobotoCondensed-Regular.ttf", 20)
        fontBig = ImageFont.truetype("Font/RobotoCondensed-Regular.ttf", 39)
        draw=ImageDraw.Draw(carte)
        if mot.findplayer!=None:
            imPP=Image.open("PNG/Round{0}.png".format(mot.findplayer.id))
            imPP=imPP.resize((62,62))
            carte.paste(imPP,(18,18),mask=imPP)
            draw.text((100,50),mot.findplayer.name,(255,255,255),font=font,anchor="lm")
        draw.text((165,152),mot.mot,(255,255,255),font=fontBig,anchor="mm")
        return carte

    def checkWin(self):
        count1,count2=0,0
        for i in self.plateau:
            if i.equipe==3 and i.findplayer!=None:
                return 1 if i.findplayer.equipe==2 else 2
            elif i.findplayer==None:
                if i.equipe==1:
                    count1+=1
                elif i.equipe==2:
                    count2+=1
            
        if count1==0:
            return 1
        elif count2==0:
            return 2
        return None

    def embedMJ(self,equipe,user):
        descip1,descip2="",""
        for i in self.plateau:
            if i.find:
                sup="~~"
            else:
                sup=""
            if i.equipe==3:
                noir=i.mot
            elif i.equipe==1:
                descip1+="{1}{0}{1}, ".format(i.mot,sup)
            elif i.equipe==2:
                descip2+="{1}{0}{1}, ".format(i.mot,sup)
        embed=discord.Embed(title="Mots à faire deviner",color=dictColor[equipe])
        embed.add_field(name="MOT INTERDIT",value=noir,inline=False)
        if equipe==1:
            embed.add_field(name="Vos mots",value=descip1[:-2],inline=False)
            embed.add_field(name="Mots de l'équipe bleue",value=descip2[:-2],inline=False)
        else:
            embed.add_field(name="Vos mots",value=descip2[:-2],inline=False)
            embed.add_field(name="Mots de l'équipe rouge",value=descip1[:-2],inline=False)
        embed.set_footer(text="OT!codenames")
        embed=auteur(user.id,user.name,user.avatar,embed,"user")
        return embed

    def embedCompo(self):
        embed=discord.Embed(title="Début de la partie !",description="Les maîtres du jeu ont 2 minutes pour réfléchir à leurs combinaisons !",color=0xad917b)
        dictRole={"mj":"maitre du jeu","dev":"devineur"}
        for i in ((1,"rouge"),(2,"bleue")):
            descip=""
            for j in self.equipe[i[0]]:
                descip+="<@{0}> : {1}\n".format(j.id,dictRole[j.role])
            embed.add_field(name="Equipe {0}".format(i[1]),value=descip)
        embed.set_footer(text="OT!codenames")
        embed=auteur(self.guild.id,self.guild.name,self.guild.icon,embed,"guild")
        return embed

    async def boucle(self,bot):
        while self.playing:
            for i in self.equipe[self.turn]:
                if i.role=="mj":
                    if not begin:
                        await i.user.send(file=discord.File("Images/Plateau{0}True.png".format(self.guild.id)),embed=self.embedMJ(i.equipe,i.user))
                    mj=i.user
                else:
                    joueur=i

            def check(mess):
                try:
                    assert mess.author.id==mj.id
                    assert mess.channel.type==discord.ChannelType.private
                    content=mess.content.split(" ")
                    assert len(content)>=2
                    valid=True
                    for i in self.plateau:
                        if i.mot.lower()==content[0].lower():
                            valid=False
                            break
                    assert valid
                    nb=int(content[1][0])
                except AssertionError:
                    return False
                return True
            
            await mj.send(embed=createEmbed("C'est votre tour !","Vous devez faire deviner des mots à votre coéquipier !\nVous avez une minute pour me donner un mot indice et le nombre de mots que vous voulez faire deviner avec.\nVous pouvez mettre un '+' juste après le nombre pour laisser votre partenaire en deviner plus !",dictColor[self.turn],"codenames",mj))
            try:
                mess=await bot.wait_for("message",check=check,timeout=60)
            except asyncio.TimeoutError:
                await mj.send("<:otROUGE:868535622237818910> Temps écoulé, votre tour est passé.")
                await self.message.channel.send("<:otROUGE:868535622237818910> <@{0}> a mis trop de temps. Le tour est passé.".format(mj.id))
                self.turn+=1
                if self.turn==3:
                    self.turn=1
                continue

            content=mess.content.split(" ")
            mot,nb,plus=content[0],int(content[1][0]),(len(content[1])>=2 and content[1][1]=="+")

            embed=createEmbed("Devinez !","C'est à vous de deviner les mots !\nCliquez sur <:otVALIDER:772766033996021761> pour faire vos propositions. Elles démareront automatiquement dans 1 minute et 30 secondes",dictColor[self.turn],"codenames",joueur.user)
            embed.add_field(name="Indice",value=mot,inline=True)
            embed.add_field(name="Nombre de mots",value=nb,inline=True)
            embed.add_field(name="Mots supplémentaires",value=str(plus),inline=True)
            messGuess=await self.message.channel.send(embed=embed,content="<@{0}>".format(joueur.userid))
            await messGuess.add_reaction("<:otVALIDER:772766033996021761>")

            def check(react,user):
                if type(react.emoji)==str:
                        return False
                return user.id==joueur.userid and react.message.id==messGuess.id and react.emoji.id==772766033996021761

            try:
                await bot.wait_for("reaction_add",check=check,timeout=90)
            except asyncio.TimeoutError:
                pass

            guess=True
            nombre=0
            await self.message.channel.send("<:otVERT:868535645897912330> Ecrivez à quel mot vous pensez ! Vous avez 20 secondes par mot.")
            while guess and (nombre!=nb or plus):

                def check(mess):
                    try:
                        assert mess.author.id==joueur.userid
                        content=mess.content.split()
                        valid=False
                        for i in self.plateau:
                            if i.mot.lower()==content[0].lower():
                                return True
                    except:
                        return False
                    return False

                try:
                    mess=await bot.wait_for("message",check=check,timeout=20)
                except asyncio.TimeoutError:
                    break
                mot=mess.content.split()[0].lower()
                for i in self.plateau:
                    if i.mot.lower()==mot:
                        i.setFind(joueur)
                        if i.equipe!=self.turn:
                            guess=False
                        else:
                            await mess.add_reaction("<:otOUI:726840394150707282>")
                
                nombre+=1
            
            self.showPlateau(True)
            self.showPlateau(False)
            begin=False
            win=self.checkWin()
            if win!=None:
                self.playing=False
                embed=self.embedWin(win)
                await self.message.channel.send(embed=embed)
                await self.message.channel.send(file=discord.File("Images/Plateau{0}True.png".format(self.guild.id)))
                await self.stats(win,self.message.channel)
                for j in range(2):
                    self.paris.distribParis(self.equipe[win][j].userid)
            else:
                await self.message.channel.send(file=discord.File("Images/Plateau{0}False.png".format(self.guild.id)),content="<:otVERT:868535645897912330> Voici le nouveau plan de jeu !")
            
            self.fermeture()
            
            self.turn+=1
            if self.turn==3:
                self.turn=1
