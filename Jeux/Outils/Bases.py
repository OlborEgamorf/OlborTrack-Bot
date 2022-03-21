from random import randint

import discord
from Core.Fonctions.Embeds import createEmbed
from Core.Fonctions.GetNom import getTitre
from Core.Fonctions.Unpin import pin
from Jeux.Outils.Paris import Pari
from Stats.SQL.ConnectSQL import connectSQL
from Stats.SQL.Execution import exeClassic, exeJeuxSQL, exeObj
from Titres.Carte import sendCarte
from Titres.Couleur import getColorJeux
from Titres.Emote import getEmoteJeux
from Titres.Outils import gainCoins

dictTitres={"Tortues":"Course des tortues","TortuesDuo":"Course des tortues DUO","P4":"Puissance 4","Matrice":"Matrice","Morpion":"Morpion","TrivialVersus":"Trivial Versus","TrivialBR":"Trivial Battle Royale","TrivialParty":"Trivial Party"}


class JoueurBase():
    def __init__(self,user:discord.Member,message:discord.Message):
        self.user=user
        self.id=user.id
        self.nom=user.nick or user.name
        self.color=None
        self.titre=None
        self.emote=None
        self.message=message
        self.guild=message.guild.id

    def getPerso(self):
        connexion,curseur=connectSQL("OT","Titres","Titres",None,None)
        self.color=getColorJeux(self.id) or self.user.color.value
        self.titre=getTitre(curseur,self.id)
        self.emote=getEmoteJeux(self.id)

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

    async def startGame(self,inGame:list,emotes:list,mini:int) -> bool:
        self.playing=True
        for mess in self.messages:
            await mess.clear_reactions()        

        if len(self.ids)<mini:
            for mess in self.messages:
                await mess.edit(embed=createEmbed(dictTitres[self.jeu],"Une minute s'est écoulée et pas assez de personnes n'ont répondu à l'invitation.",0xad917b,self.jeu.lower(),mess.guild))
            for i in self.ids:
                inGame.remove(i)
            return False

        for i in self.joueurs:
            i.getPerso()

        for mess in self.messages:
            descip="<:otVERT:868535645897912330> La partie va bientôt commencer pour "
            for j in self.joueurs:
                if j.guild!=mess.guild.id:
                    descip+="{0}, ".format(j.titre)
                else:
                    descip+="<@{0}>, ".format(j.id)
            await mess.channel.send(descip[:-2])
            await pin(mess)

            for i in emotes:
                await mess.add_reaction(i)
            await mess.add_reaction("<:otCOINS:873226814527520809>")

        self.turn=randint(0,len(self.joueurs)-1)
        self.paris=Pari(self.ids,self.jeu)
        return True

    def addPlayer(self,user:discord.Member,message:discord.Message):
        self.joueurs.append(JoueurBase(user,message))
        self.ids.append(user.id)

    async def stats(self,userWin:int,guild:discord.Guild):
        connexionGuild,curseurGuild=connectSQL(guild,"Guild","Guild",None,None)
        connexionOT,curseurOT=connectSQL("OT","Guild","Guild",None,None)
        
        for i in self.joueurs:
            if i.id==userWin:
                gainCoins(i.id,len(self.ids)*25+sum(self.paris.mises.values()))
                self.paris.distribParis(i.id)
                state="W"
            else:
                state="L"
            if len(self.guilds)==1:
                exeJeuxSQL(i.id,None,state,guild,curseurGuild,self.jeu,None)
            wins=exeJeuxSQL(i.id,None,state,"OT",curseurOT,self.jeu,None)
            if state=="W":
                await sendCarte(i.user,self.jeu,wins,i.message.channel)

        count=0
        if len(self.guilds)!=1:
            for i in self.joueurs:
                if i.guild!=guild:
                    count+=1
            exeClassic(count,guild,"Cross",curseurOT,fake)
            exeObj(count,guild,userWin,True,fake,"Cross")

        connexionGuild.commit()
        connexionOT.commit()

class FakeGuild:
    def __init__(self):
        self.id="OT"

fake=FakeGuild()
