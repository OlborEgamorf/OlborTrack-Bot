import asyncio
from random import choice, randint

import discord
from Core.Fonctions.AuteurIcon import auteurJeux
from Core.Fonctions.Embeds import createEmbed
from Core.Fonctions.Unpin import unpin

from Jeux.Outils.Bases import JeuBase, JoueurBase

listeCouleurs=("rouge","jaune","bleue","verte","violette")
dictEmote={0:"<:otBlank:828934808200937492>","rouge":"<:OTTrouge:860119157495693343>","verte":"<:OTTvert:860119157331853333>","bleue":"<:OTTbleu:860119157491892255>","jaune":"<:OTTjaune:860119157688631316>","violette":"<:OTTviolet:860119157672247326>","last":"*dernière tortue*","multi":"*au choix*"}
dictColor={"bleue":0x00CCFF,"violette":0x993366,"rouge":0xFF0000,"verte":0x77B255,"jaune":0xFFFF00}
choix={705766186909958185:0,705766186989912154:1,705766186930929685:2,705766186947706934:3,705766186713088042:4,860119157491892255:"bleue",860119157688631316:"jaune",860119157495693343:"rouge",860119157331853333:"verte",860119157672247326:"violette"}
emotes=["<:ot1:705766186909958185>","<:ot2:705766186989912154>","<:ot3:705766186930929685>","<:ot4:705766186947706934>","<:ot5:705766186713088042>","<:OTTbleu:860119157491892255>", "<:OTTjaune:860119157688631316>", "<:OTTrouge:860119157495693343>", "<:OTTvert:860119157331853333>", "<:OTTviolet:860119157672247326>"]

class JoueurTortue(JoueurBase):
    def __init__(self,user,message,tortue):
        super().__init__(user,message)
        self.couleur=tortue
        self.jeu=[]
        self.fini=False
    
    def pioche(self,listeCartes):
        carte=randint(0,len(listeCartes)-1)
        self.jeu.append(listeCartes.pop(carte))
    
    def __str__(self):
        return self.couleur

class FakeTortue:
    def __init__(self,couleur):
        self.couleur=couleur
        self.user=None
        self.id=None
        self.nom=None
        self.guild=None
        self.message=None

class JeuTortues(JeuBase):
    def __init__(self,message,user,jeu,cross):
        super().__init__(message,user,jeu,cross)
        self.tortues=["bleue","verte","jaune","rouge","violette"]
        self.historique={}
        self.plateau=[Pile() for i in range(10)]
        self.cartes=[Carte(i,1) for i in listeCouleurs]*5+[Carte(i,2) for i in listeCouleurs]+[Carte(i,-1) for i in listeCouleurs]*2+[Carte("multi",1) for i in range(5)]+[Carte("last",1) for i in range(3)]+[Carte("last",2) for i in range(2)]+[Carte("multi",-1) for i in range(2)]
        for i in self.tortues:
            self.plateau[0].empiler(i)

    def embedGame(self,user:JoueurTortue,guild:int):
        
        liste=[[0 for i in range(10)] for j in range(5)]
        descip=""
        for j in range(len(self.plateau)):
            i=5-len(self.plateau[j])
            cel=self.plateau[j].contenu
            while cel is not None:
                liste[i][j]=cel.valeur
                cel=cel.suivante 
                i+=1
        for i in range(5):
            for j in range(10):
                if j==9 and liste[i][j]==0:
                    descip+="<:OTTarrivee:860185134895726622>"
                else:
                    descip+=dictEmote[liste[i][j]]
            descip+="\n"

        if user.guild==guild:
            embed=createEmbed("Course de tortues",descip,user.color,self.jeu.lower(),user.user)
        else:
            embed=createEmbed("Course de tortues",descip,user.color,self.jeu.lower(),None)
            auteurJeux(user,embed)

        for i in self.joueurs:
            if i.id==user.id:
                sup="__"
            else:
                sup=""
            descip=""
            for j in range(len(i.jeu)):
                if i.jeu[j].valeur>0:
                    form="+{0}".format(i.jeu[j].valeur)
                else:
                    form=i.jeu[j].valeur
                descip+="{0} : {1} {2}\n".format(emotes[j],form,dictEmote[i.jeu[j].couleur])
            if i.id in self.historique:
                if self.historique[i.id].valeur>0:
                    form="+{0}".format(self.historique[i.id].valeur)
                else:
                    form=self.historique[i.id].valeur
                descip+="Dernier coup : {0} {1}".format(form,dictEmote[self.historique[i.id].couleur])
            if self.paris.ouvert and i.guild==guild:
                if self.paris.cotes[i.id]!=None:
                    mise="\nCôte : {0} ".format(self.paris.cotes[i.id])
                else:
                    mise=""
            else:
                if self.paris.mises[i.id]!=0:
                    mise="\nMise : {0} <:otCOINS:873226814527520809>".format(self.paris.mises[i.id])
                else:
                    mise=""
            if i.emote==None:
                emote=""
            else:
                emote=i.emote
            if i.guild==guild:
                embed.add_field(name="{0} {2}Cartes de {1}{2}{3}".format(emote,i.nom,sup,mise),value=descip)
            else:
                embed.add_field(name="{0} {2}Cartes de {1}{2}{3}".format(emote,i.titre,sup,mise),value=descip)

        return embed
                
    def mouvement(self,couleur,valeur):
        if couleur=="last":
            i=0
            while self.plateau[i].est_vide():
                i+=1
            if i==0:
                cel=self.plateau[i].contenu
                liste=[]
                while cel is not None:
                    liste.append(cel.valeur)
                    cel=cel.suivante
                choix=choice(liste)
                self.mouvement(choix,valeur)
                return
            else:
                count=len(self.plateau[i])
        else:
            for i in range(len(self.plateau)):
                cel=self.plateau[i].contenu
                count=0
                while cel is not None:
                    count+=1
                    if cel.valeur==couleur:
                        break
                    cel=cel.suivante
                if cel!=None:
                    if cel.valeur==couleur:
                        break  
        if i==0:
            if valeur<0:
                pass 
            else:
                temp=Pile()
                for j in range(count-1):
                    temp.empiler(self.plateau[i].depiler())
                self.plateau[i+valeur].empiler(self.plateau[i].depiler())
                cel=temp.contenu
                while cel is not None:
                    self.plateau[i].empiler(cel.valeur)
                    cel=cel.suivante
        elif i==9:
            return False
        else:
            if i+valeur<0:
                stop=0
            elif i+valeur>9:
                stop=9
            else:
                stop=i+valeur
            temp=Pile()
            for j in range(count):
                temp.empiler(self.plateau[i].depiler())
            for j in range(count):
                self.plateau[stop].empiler(temp.depiler())
            
            if stop==9:
                return True
        return False

    def giveCards(self):
        for i in self.joueurs:
            for j in range(5):
                carte=randint(0,len(self.cartes)-1)
                i.jeu.append(self.cartes.pop(carte))
    
    def addPlayer(self,user,message):
        tortue=choice(self.tortues)
        self.tortues.remove(tortue)
        self.joueurs.append(JoueurTortue(user,message,tortue))
        self.ids.append(user.id)

    def getWinner(self):
        cel=self.plateau[9].contenu
        win=cel.valeur
        while cel is not None:
            win=cel.valeur
            cel=cel.suivante
        winID=list(filter(lambda x:x.couleur==win, self.joueurs))
        if len(winID)==0:
            return FakeTortue(win)
        return winID[0]

    def embedEnd(self,win,guild):
        descip=""
        for i in self.joueurs:
            if i.guild==guild:
                descip+="{0} : <@{1}>\n".format(dictEmote[i.couleur],i.id)
            else:
                descip+="{0} : {1}\n".format(dictEmote[i.couleur],i.titre)

        if type(win)==FakeTortue: 
            embed=createEmbed("Personne n'a gagné !","La tortue {0} n'était jouée par personne ! {1}\n\n{2}".format(win.couleur,dictEmote[win.couleur],descip),dictColor[win.couleur],"tortues",None)
        else:
            if win.guild==guild:
                embed=createEmbed("Victoire de {0}".format(win.nom),"Il/elle était la tortue {0} ! {1}\n\n{2}".format(win.couleur,dictEmote[win.couleur],descip),dictColor[win.couleur],"tortues",win.user)
            else:
                embed=createEmbed("Victoire de {0}".format(win.titre),"Il/elle était la tortue {0} ! {1}\n\n{2}".format(win.couleur,dictEmote[win.couleur],descip),dictColor[win.couleur],"tortues",None)
                auteurJeux(win,embed)
            embed.add_field(name="<:otCOINS:873226814527520809> gagnés",value="{0} <:otCOINS:873226814527520809>".format(len(self.ids)*25+sum(self.paris.mises.values())))

        embed.set_footer(text="OT!tortues")
        return embed

    async def startGame(self,inGame,emotes,mini):
        listeDel=[]
        for i in self.joueurs:
            try:
                await i.user.send("<:otVERT:868535645897912330> Je vais vous donner votre tortue dans un instant... La partie démarre...")
            except discord.Forbidden:
                await i.message.channel.send("<:otROUGE:868535622237818910> <@{0}> n'a pas activé ses messages privés, je ne peux pas lui communiquer sa tortue et ne jouera donc pas la partie.".format(i.id))
                inGame.remove(i.id)
                listeDel.append(i)
        for i in listeDel:
            self.ids.remove(i.id)
            self.joueurs.remove(i)
            
        start=await super().startGame(inGame,emotes,mini)

        if start:
            await self.sendTortues()
            for mess in self.messages:
                await mess.channel.send("<:otVERT:868535645897912330> Vos couleurs de tortues ont été envoyées par message privé !")
        return start

    async def sendTortues(self):
        for i in self.joueurs:
            await i.user.send(embed=createEmbed("Course des tortues : {0}".format(i.couleur),"Votre couleur est : {0} {1}".format(i.couleur,dictEmote[i.couleur]),dictColor[i.couleur],"tortues",i.user))
        self.giveCards()

    def fermeture(self):
        if not self.plateau[4].est_vide() or not self.plateau[5].est_vide():
            self.paris.ouvert=False

    async def play(self,bot,message):

        def check(reaction,user):
            if type(reaction.emoji)==str:
                return False
            return reaction.emoji.id in (705766186909958185,705766186989912154,705766186930929685,705766186947706934,705766186713088042) and reaction.message.id==message.id and self.joueurs[self.turn].id==user.id

        try:
            reaction,user=await bot.wait_for('reaction_add', check=check, timeout=40)
            await reaction.remove(user)
        except asyncio.exceptions.TimeoutError:
            carte=self.joueurs[self.turn].jeu[randint(0,4)]
            couleur,valeur=carte.couleur,carte.valeur
            if couleur=="multi":
                couleur=choice(listeCouleurs)
        else:
            if self.joueurs[self.turn].jeu[choix[reaction.emoji.id]].couleur=="multi":
                carte=self.joueurs[self.turn].jeu[choix[reaction.emoji.id]]
                valeur=carte.valeur
                eff=await message.channel.send("<@{0}>, choisissez une tortue avec les réactions <:OTTbleu:860119157491892255> <:OTTjaune:860119157688631316> <:OTTrouge:860119157495693343> <:OTTvert:860119157331853333> <:OTTviolet:860119157672247326>.".format(self.joueurs[self.turn].id))

                def check(reaction,user):
                    if type(reaction.emoji)==str:
                        return False
                    return reaction.emoji.id in (860119157491892255,860119157688631316,860119157495693343,860119157331853333,860119157672247326) and reaction.message.id==message.id and self.joueurs[self.turn].id==user.id
                try:
                    reaction,user=await bot.wait_for('reaction_add', check=check, timeout=30)
                    await reaction.remove(user)
                except asyncio.exceptions.TimeoutError:
                    couleur=choice(listeCouleurs)
                else:
                    couleur=choix[reaction.emoji.id]
                await eff.delete()
                    
            else:
                carte=self.joueurs[self.turn].jeu[choix[reaction.emoji.id]]
                couleur,valeur=carte.couleur,carte.valeur

        self.historique[self.joueurs[self.turn].id]=carte
        return couleur,valeur,carte
        
    async def boucle(self,bot):

        while self.playing:
            for mess in self.messages:
                await mess.edit(embed=self.embedGame(self.joueurs[self.turn],mess.guild.id))
            couleur,valeur,carte=await self.play(bot,self.joueurs[self.turn].message)
        
            if self.mouvement(couleur,valeur):    
                win=self.getWinner()        
                self.playing=False
                if type(win)==FakeTortue:
                    await self.stats(win.id,self.guilds[0])
                else:
                    await self.stats(win.id,win.guild)
                for mess in self.messages:
                    await mess.edit(embed=self.embedGame(self.joueurs[self.turn],mess.guild.id))
                    await mess.reply(embed=self.embedEnd(win,mess.guild.id))
                    await mess.clear_reactions()
                    await unpin(mess)

            self.fermeture()
            self.joueurs[self.turn].jeu.remove(carte)
            self.joueurs[self.turn].pioche(self.cartes)
            self.turn+=1
            if self.turn==len(self.joueurs):
                self.turn=0
            if len(self.cartes)==0:
                self.cartes=[Carte(i,1) for i in listeCouleurs]*5+[Carte(i,2) for i in listeCouleurs]+[Carte(i,-1) for i in listeCouleurs]*2+[Carte("multi",1) for i in range(5)]+[Carte("last",1) for i in range(3)]+[Carte("last",2) for i in range(2)]+[Carte("multi",-1) for i in range(2)]



class Carte:
    def __init__(self,couleur,valeur):
        self.couleur=couleur
        self.valeur=valeur

class Cellule:
    def __init__(self,v,s):
        self.valeur=v
        self.suivante=s

class Pile:
    def __init__(self):
        self.contenu=None
    def est_vide(self):
        return self.contenu is None
    def empiler(self,v):
        self.contenu=Cellule(v,self.contenu)
    def depiler(self):
        if self.est_vide():
            raise IndexError("La liste est vide")
        v=self.contenu.valeur
        self.contenu=self.contenu.suivante
        return v     
    def __len__(self):
        count=0
        cel=self.contenu
        while cel is not None:
            count+=1
            cel=cel.suivante
        return count
