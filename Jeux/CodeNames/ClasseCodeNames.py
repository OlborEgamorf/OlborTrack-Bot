import asyncio
from random import choice, randint

import discord
from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.Embeds import createEmbed
from Core.Fonctions.WebRequest import getAvatar
from Outils.Bienvenue.Manipulation import squaretoround
from PIL import Image, ImageDraw, ImageFont
from Stats.SQL.ConnectSQL import connectSQL
from Stats.SQL.Execution import exeJeuxSQL
from Titres.Carte import sendCarte
from Titres.Outils import gainCoins

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

class JoueurCN:
    def __init__(self,user,equipe,role):
        self.user=user
        self.userid=user.id
        self.name=user.name
        self.fini=False
        self.jeu=[]
        self.equipe=equipe
        self.role=role
   

class JeuCN:
    def __init__(self,guild,user):
        self.joueurs=[]
        self.ids=[]
        self.paris=None
        self.plateau=[]
        self.playing=False
        self.guild=guild
        self.invoke=user
        self.equipe={1:[],2:[]}

    def addPlayer(self,user,role):
        dictEquipe={893548469309038633:1,893548469229346896:1,893548469212561468:2,893548468822495263:2}
        dictRole={893548469309038633:"mj",893548469229346896:"dev",893548469212561468:"mj",893548468822495263:"dev"}
        joueur=JoueurCN(user,dictEquipe[role],dictRole[role])
        self.joueurs.append(joueur)
        self.equipe[dictEquipe[role]].append(joueur)
    
    def embedWin(self,win):
        descip=""
        play=False
        embed=discord.Embed(title="Victoire de {0} et {1} !".format(self.equipe[win][0].name,self.equipe[win][1].name), description="Ils ont réussi à déviner tous les mots !", color=dictColor[win])

        for i in self.joueurs:
            dictRole={"mj":"maitre du jeu","dev":"devineur"}
            dictEquipe={1:"rouge",2:"bleue"}
            descip+="<@{0}> : équipe {1}, {2}\n".format(i.userid,dictEquipe[i.equipe],dictRole[i.role])
        
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
                gainCoins(i.userid,75+sum(self.paris.mises.values())/2)
                count,state=2,"W"
            else:
                count,state=-1,"L"
            exeJeuxSQL(i.userid,None,state,self.guild.id,curseurGuild,count,"CodeNames",None)
            wins=exeJeuxSQL(i.userid,None,state,"OT",curseurOT,count,"CodeNames",None)
            if state=="W":
                await sendCarte(i.user,"CodeNames",wins,"classic",chan)
        connexionGuild.commit()
        connexionOT.commit()

    async def checkPlayers(self,message,inGame,ctx,mini,bot):
        if len(self.ids)<mini:
            await message.edit(embed=createEmbed("Code Names","Une minute s'est écoulée et pas assez de personnes n'ont répondu à l'invitation.",0xad917b,ctx.invoked_with.lower(),ctx.guild))
            for i in self.ids:
                inGame.remove(i)
            return False
        else:
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
        return True

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
            imPP=Image.open("PNG/Round{0}.png".format(mot.findplayer.userid))
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
                descip+="<@{0}> : {1}\n".format(j.userid,dictRole[j.role])
            embed.add_field(name="Equipe {0}".format(i[1]),value=descip)
        embed.set_footer(text="OT!codenames")
        embed=auteur(self.guild.id,self.guild.name,self.guild.icon,embed,"guild")
        return embed

            