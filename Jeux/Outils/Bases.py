from random import randint

import discord
from Core.Fonctions.Embeds import createEmbed
from Core.Fonctions.GetNom import getTitre
from Jeux.Outils.Paris import Pari
from Stats.SQL.Execution import executeJeux
from Stats.SQL.ConnectSQL import connectSQL
from Titres.Carte import sendCarte
from Titres.Outils import gainCoins,getEmoteJeux,getColorJeux

dictTitres={"Tortues":"Course des tortues","TortuesDuo":"Course des tortues DUO","P4":"Puissance 4","Matrice":"Matrice","Morpion":"Morpion","TrivialVersus":"Trivial Versus","TrivialBR":"Trivial Battle Royale","TrivialParty":"Trivial Party"}


class JoueurBase():
    def __init__(self,user:discord.Member,interaction:discord.Interaction):
        self.user=user
        self.id=user.id
        self.nom=user.nick or user.name
        self.color=None
        self.titre=None
        self.emote=None
        self.interaction=interaction
        self.guild=interaction.guild_id

    def getPerso(self):
        connexion,curseur=connectSQL("OT")
        self.color=getColorJeux(self.id,curseur) or self.user.color.value
        self.titre=getTitre(curseur,self.id)
        self.emote=getEmoteJeux(self.id,curseur)

class JeuBase():
    def __init__(self,message:discord.Message,invoke:int,jeu:str,cross:bool):
        self.guilds=[message.guild.id]
        self.messages=[message]
        self.ids=[]
        self.joueurs=[]
        self.emotes={}
        self.invoke=invoke
        self.turn=0
        self.playing=False
        self.paris=None
        self.jeu=jeu
        self.cross=cross

    async def startGame(self,inGame:list,view,mini:int,maxi:int) -> bool:
        self.playing=True     

        if len(self.ids)<mini:
            for mess in self.messages:
                await mess.edit(embed=createEmbed(dictTitres[self.jeu],"Une minute s'est écoulée et pas assez de personnes n'ont répondu à l'invitation.",0xad917b,self.jeu.lower(),mess.guild),view=None)
            for i in self.ids:
                inGame.remove(i)
            return False

        elif len(self.ids)>maxi:
            for i in range(maxi-len(self.ids)):
                kick=self.joueurs.pop()
                self.ids.remove(kick.id)

        for i in self.joueurs:
            i.getPerso()

        for mess in self.messages:
            descip="<:otVERT:868535645897912330> La partie commence pour "
            for j in self.joueurs:
                if j.guild!=mess.guild.id:
                    descip+="{0}, ".format(j.titre)
                else:
                    descip+="<@{0}>, ".format(j.id)
            await mess.channel.send(descip[:-2],delete_after=20)
            self.thread=await mess.create_thread(name="Partie de {0} en cours !".format(self.jeu))
            
            await mess.edit(view=view)  

        self.turn=randint(0,len(self.joueurs)-1)
        self.paris=Pari(self.ids,self.jeu)

        return True

    def addPlayer(self,user:discord.Member,interaction:discord.Interaction):
        self.joueurs.append(JoueurBase(user,interaction))
        self.ids.append(user.id)

    async def stats(self,userWin:int,guild:discord.Guild):
        connexionOT,curseurOT=connectSQL("OT")
        
        for i in self.joueurs:
            if i.id==userWin:
                gainCoins(i.id,len(self.ids)*25+sum(self.paris.mises.values()))
                self.paris.distribParis(i.id)
                state="W"
            else:
                state="L"

            wins=executeJeux(self.jeu,i.id,guild,state,curseurOT)
        
            if state=="W":
                await sendCarte(i.user,self.jeu,wins,i.interaction.message.channel)

        count=0
        if len(self.guilds)!=1:
            for i in self.joueurs:
                if i.guild!=guild:
                    count+=1

            executeJeux("Cross",i.id,guild,state,curseurOT)

        connexionOT.commit()

class FakeGuild:
    def __init__(self):
        self.id="OT"

fake=FakeGuild()
