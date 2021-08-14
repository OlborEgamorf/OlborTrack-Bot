import asyncio
from random import choice, randint

import discord
from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.Embeds import createEmbed
from Jeux.Tortues.ClassesAutres import Carte, Pile
from Stats.SQL.ConnectSQL import connectSQL
from Stats.SQL.Execution import exeJeuxSQL
from Titres.Outils import gainCoins

listeCouleurs=("rouge","jaune","bleue","verte","violette")
dictEmote={0:"<:otBlank:828934808200937492>","rouge":"<:OTTrouge:860119157495693343>","verte":"<:OTTvert:860119157331853333>","bleue":"<:OTTbleu:860119157491892255>","jaune":"<:OTTjaune:860119157688631316>","violette":"<:OTTviolet:860119157672247326>","last":"*dernière tortue*","multi":"*au choix*"}
dictColor={"bleue":0x00CCFF,"violette":0x993366,"rouge":0xFF0000,"verte":0x77B255,"jaune":0xFFFF00}
choix={705766186909958185:0,705766186989912154:1,705766186930929685:2,705766186947706934:3,705766186713088042:4,860119157491892255:"bleue",860119157688631316:"jaune",860119157495693343:"rouge",860119157331853333:"verte",860119157672247326:"violette"}
emotes=["<:ot1:705766186909958185>","<:ot2:705766186989912154>","<:ot3:705766186930929685>","<:ot4:705766186947706934>","<:ot5:705766186713088042>","<:OTTbleu:860119157491892255>", "<:OTTjaune:860119157688631316>", "<:OTTrouge:860119157495693343>", "<:OTTvert:860119157331853333>", "<:OTTviolet:860119157672247326>"]

class Tortue:
    def __init__(self,couleur):
        self.couleur=couleur
        self.user=None
        self.userid=None
        self.name=None
        self.fini=False
        self.jeu=[]
        
    def setPlayer(self,user):
        self.user=user
        self.userid=user.id
        self.name=user.name
    
    def pioche(self,listeCartes):
        carte=randint(0,len(listeCartes)-1)
        self.jeu.append(listeCartes.pop(carte))
    
    def __str__(self):
        return self.couleur


class JeuTortues:
    def __init__(self,guild,user):
        self.joueurs=[]
        self.tortues=[Tortue("bleue"),Tortue("verte"),Tortue("jaune"),Tortue("rouge"),Tortue("violette")]
        self.ids=[]
        self.historique={}
        self.emotes={}
        self.plateau=[Pile() for i in range(10)]
        self.cartes=[Carte(i,1) for i in listeCouleurs]*5+[Carte(i,2) for i in listeCouleurs]+[Carte(i,-1) for i in listeCouleurs]*2+[Carte("multi",1) for i in range(5)]+[Carte("last",1) for i in range(3)]+[Carte("last",2) for i in range(2)]+[Carte("multi",-1) for i in range(2)]
        self.playing=False
        self.guild=guild
        for i in self.tortues:
            self.plateau[5].empiler(i)
        self.invoke=user

    def embedGame(self,user):
        embed=discord.Embed(title="Course de tortues",color=user.color.value)
        embed=auteur(user.id,"Au tour de {0}".format(user.name),user.avatar,embed,"user")
        embed.set_footer(text="OT!tortues")
        liste=[[0 for i in range(10)] for j in range(5)]
        descip=""
        for j in range(len(self.plateau)):
            i=5-len(self.plateau[j])
            cel=self.plateau[j].contenu
            while cel is not None:
                liste[i][j]=cel.valeur.couleur
                cel=cel.suivante 
                i+=1
        for i in range(5):
            for j in range(10):
                if j==9 and liste[i][j]==0:
                    descip+="<:OTTarrivee:860185134895726622>"
                else:
                    descip+=dictEmote[liste[i][j]]
            descip+="\n"
        embed.description=descip

        for i in self.joueurs:
            if i.userid==user.id:
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
            if i.userid in self.historique:
                if self.historique[i.userid].valeur>0:
                    form="+{0}".format(self.historique[i.userid].valeur)
                else:
                    form=self.historique[i.userid].valeur
                descip+="Dernier coup : {0} {1}".format(form,dictEmote[self.historique[i.userid].couleur])
            embed.add_field(name="{0} {2}Cartes de {1}{2}".format(self.emotes[i.userid],i.user.name,sup),value=descip)
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
                    liste.append(cel.valeur.couleur)
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
                    if cel.valeur.couleur==couleur:
                        break
                    cel=cel.suivante
                if cel!=None:
                    if cel.valeur.couleur==couleur:
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
    
    def addPlayer(self,user):
        tortue=choice(self.tortues)
        self.tortues.remove(tortue)
        tortue.setPlayer(user)
        self.joueurs.append(tortue)

    async def emotesUser(self,bot):
        idServ=[759688015676309525,759690251521622016,776417458386763778,776417488698212383]
        for i in self.joueurs:
            for j in range(4):
                try:
                    emote=await bot.get_guild(idServ[j]).create_custom_emoji(name=i.name.split(" ")[0],image=await i.user.avatar_url_as(size=128).read(),roles=None,reason=None)
                    break
                except:
                    if j==3:
                        emote="<:otBlank:828934808200937492>"
            self.emotes[i.userid]=emote

    async def delEmotes(self):
        for i in self.ids:
            if self.emotes[i]!="<:otBlank:828934808200937492>":
                await self.emotes[i].delete()

    def getWinner(self):
        cel=self.plateau[9].contenu
        win=cel.valeur.couleur
        while cel is not None:
            win=cel.valeur.couleur
            cel=cel.suivante
        return win

    def embedWin(self,win):
        descip=""
        play=False
        for i in self.joueurs:
            if i.couleur==win:
                embed=discord.Embed(title="Victoire de {0}".format(i.name), description="Il/elle était la tortue {0} ! {1}".format(win,dictEmote[win]), color=dictColor[win])
                embed=auteur(i.userid,i.name,i.user.avatar,embed,"user")
                play=True
                embed.add_field(name="<:otCOINS:873226814527520809> gagnés par {0}".format(i.name),value="{0} <:otCOINS:873226814527520809>".format(len(self.ids)*25))
            descip+="{0} : <@{1}>\n".format(dictEmote[i.couleur],i.userid)

        if play==False: 
            embed=discord.Embed(title="Personne n'a gagné !", description="La tortue {0} n'était jouée par personne ! {1}".format(win,dictEmote[win]), color=dictColor[win])
        embed.set_footer(text="OT!tortues")
        embed.description+="\n\n"+descip
        return embed

    def stats(self,win):
        connexionGuild,curseurGuild=connectSQL(self.guild.id,"Guild","Guild",None,None)
        connexionOT,curseurOT=connectSQL("OT","Guild","Guild",None,None)
        for i in self.joueurs:
            if i.couleur==win:
                gainCoins(i.userid,len(self.ids)*25)
                count,state=2,"W"
            else:
                count,state=-1,"L"
            exeJeuxSQL(i.userid,None,state,self.guild.id,curseurGuild,count,"Tortues",None)
            exeJeuxSQL(i.userid,None,state,"OT",curseurOT,count,"Tortues",None)
        connexionGuild.commit()
        connexionOT.commit()

    async def checkPlayers(self,message,inGame,ctx,mini):
        if len(self.ids)<mini:
            await message.edit(embed=createEmbed("Course des tortues","Une minute s'est écoulée et pas assez de personnes n'ont répondu à l'invitation.",0xad917b,ctx.invoked_with.lower(),ctx.guild))
            for i in self.ids:
                inGame.remove(i)
            return False
        else:
            listeDel=[]
            for i in self.ids:
                user=ctx.guild.get_member(i)
                try:
                    await user.send("<:otVERT:868535645897912330> Vous m'avez bel et bien autorisé à vous envoyer des messages privés, vous êtes dans la partie !")
                    self.addPlayer(user)
                except discord.Forbidden:
                    await ctx.send("<:otROUGE:868535622237818910> <@{0}> n'a pas activé ses messages privés, je ne peux pas lui communiquer sa tortue et ne jouera donc pas la partie.".format(i))
                    inGame.remove(i)
                    listeDel.append(i)
            for i in listeDel:
                self.ids.remove(i)
            
            if len(self.ids)<2:
                await message.edit(embed=createEmbed("Course des tortues","Sur les joueurs qui ont voulu rejoindre la partie, pas assez ont activé leurs messages privés pour recevoir leur couleur. La partie est annulée.",0xad917b,ctx.invoked_with.lower(),ctx.guild))
                for i in self.ids:
                    inGame.remove(i)
                return False
        return True

    async def play(self,turn,message,bot):

        def check(reaction,user):
            if type(reaction.emoji)==str:
                return False
            return reaction.emoji.id in (705766186909958185,705766186989912154,705766186930929685,705766186947706934,705766186713088042) and reaction.message.id==message.id and self.joueurs[turn].userid==user.id

        try:
            reaction,user=await bot.wait_for('reaction_add', check=check, timeout=40)
            await reaction.remove(user)
        except asyncio.exceptions.TimeoutError:
            carte=self.joueurs[turn].jeu[randint(0,4)]
            couleur,valeur=carte.couleur,carte.valeur
            if couleur=="multi":
                couleur=choice(listeCouleurs)
        else:
            if self.joueurs[turn].jeu[choix[reaction.emoji.id]].couleur=="multi":
                carte=self.joueurs[turn].jeu[choix[reaction.emoji.id]]
                valeur=carte.valeur
                eff=await message.channel.send("<@{0}>, choisissez une tortue avec les réactions <:OTTbleu:860119157491892255> <:OTTjaune:860119157688631316> <:OTTrouge:860119157495693343> <:OTTvert:860119157331853333> <:OTTviolet:860119157672247326>.".format(self.joueurs[turn].userid))

                def check(reaction,user):
                    if type(reaction.emoji)==str:
                        return False
                    return reaction.emoji.id in (860119157491892255,860119157688631316,860119157495693343,860119157331853333,860119157672247326) and reaction.message.id==message.id and self.joueurs[turn].userid==user.id
                try:
                    reaction,user=await bot.wait_for('reaction_add', check=check, timeout=30)
                    await reaction.remove(user)
                except asyncio.exceptions.TimeoutError:
                    couleur=choice(listeCouleurs)
                else:
                    couleur=choix[reaction.emoji.id]
                await eff.delete()
                    
            else:
                carte=self.joueurs[turn].jeu[choix[reaction.emoji.id]]
                couleur,valeur=carte.couleur,carte.valeur

        self.historique[self.joueurs[turn].userid]=carte
        return couleur,valeur,carte
