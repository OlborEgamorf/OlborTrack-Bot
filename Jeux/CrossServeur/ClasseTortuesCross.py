from Titres.Couleur import getColorJeux
from Titres.Emote import getEmoteJeux
from Stats.SQL.EmoteDetector import emoteDetector
from Core.Fonctions.GetNom import getTitre
from Core.Fonctions.Embeds import createEmbed
from Stats.SQL.ConnectSQL import connectSQL
import discord
from random import choice
from Core.Fonctions.AuteurIcon import auteur
from Jeux.Tortues.ClasseTortues import JeuTortues, Tortue
from Stats.SQL.Execution import exeJeuxSQL

dictEmote={0:"<:otBlank:828934808200937492>","rouge":"<:OTTrouge:860119157495693343>","verte":"<:OTTvert:860119157331853333>","bleue":"<:OTTbleu:860119157491892255>","jaune":"<:OTTjaune:860119157688631316>","violette":"<:OTTviolet:860119157672247326>","last":"*dernière tortue*","multi":"*au choix*"}
dictColor={"bleue":0x00CCFF,"violette":0x993366,"rouge":0xFF0000,"verte":0x77B255,"jaune":0xFFFF00}

class JeuTortuesCross(JeuTortues):

    def __init__(self, guild, user):
        self.guilds=[]
        self.messages=[]
        self.memguild={}
        self.messguild={}
        self.guildmess={}
        self.memmess={}
        self.emotesCustom={}
        super().__init__(guild, user)
        self.tortues=[TortueCross("bleue"),TortueCross("verte"),TortueCross("jaune"),TortueCross("rouge"),TortueCross("violette")]

    async def checkPlayers(self,inGame,bot,mini):
        for i in self.memguild:
            if self.memguild[i] not in self.guilds:
                self.guilds.append(self.memguild[i])
        for i in self.memmess:
            if self.memmess[i] not in self.messages:
                self.messages.append(self.memmess[i])

        if len(self.ids)<mini:
            for message in self.messages:
                await message.edit(embed=createEmbed("Course des tortues","Une minute s'est écoulée et pas assez de personnes n'ont répondu à l'invitation.",0xad917b,"tortues",bot.user))
                for i in self.ids:
                    inGame.remove(i)
                return False
        else:
            listeDel=[]
            connexion,curseur=connectSQL("OT","Titres","Titres",None,None)
            for i in self.ids:
                user=bot.get_user(i)
                try:
                    await user.send("<:otVERT:868535645897912330> Vous m'avez bel et bien autorisé à vous envoyer des messages privés, vous êtes dans la partie !")
                    self.addPlayer(user,curseur)
                except discord.Forbidden:
                    await self.memmess[i].channel.send("<:otROUGE:868535622237818910> <@{0}> n'a pas activé ses messages privés, je ne peux pas lui communiquer sa tortue et ne jouera donc pas la partie.".format(i))
                    inGame.remove(i)
                    listeDel.append(i)
            for i in listeDel:
                self.ids.remove(i)
            
            if len(self.ids)<2:
                for message in self.messages:
                    await message.edit(embed=createEmbed("Course des tortues","Sur les joueurs qui ont voulu rejoindre la partie, pas assez ont activé leurs messages privés pour recevoir leur couleur. La partie est annulée.",0xad917b,"tortues",bot.user))
                for i in self.ids:
                    inGame.remove(i)
                return False
        return True

    def addPlayer(self,user,curseur):
        tortue=choice(self.tortues)
        self.tortues.remove(tortue)
        titre=getTitre(curseur,user.id)
        tortue.setPlayer(user,titre)
        self.joueurs.append(tortue)

    def embedGame(self,user,guild):
        embed=super().embedGame(user.user)
        if self.memguild[user.userid]!=guild:
            if self.emotesCustom[user.userid]!=None:
                embed.set_author(name="Au tour de {0}".format(user.titre),icon_url="https://cdn.discordapp.com/emojis/{0}.png".format(emoteDetector(self.emotesCustom[user.userid])[0]))
            else:
                embed=auteur(699728606493933650,"Au tour de {0}".format(user.titre),None,embed,"user")
        for i in range(len(self.joueurs)):
            if self.memguild[self.joueurs[i].userid]!=guild:
                sup=""
                if user.userid==self.joueurs[i].userid:
                    sup="__"
                if self.emotesCustom[self.joueurs[i].userid]!=None:
                    embed.set_field_at(index=i,name="{2}{0} Cartes de {1}{2}".format(self.emotesCustom[self.joueurs[i].userid],self.joueurs[i].titre,sup),value=embed.fields[i].value,inline=True)
                else:
                    embed.set_field_at(index=i,name="{1}Cartes de {0}{1}".format(self.joueurs[i].titre,sup),value=embed.fields[i].value,inline=True)
        if user.colorUser!=None:
            embed.color=user.colorUser
        return embed

    def embedWin(self,win,guild):
        descip=""
        play=False
        for i in self.joueurs:
            if self.memguild[i.userid]==guild:
                if i.couleur==win:
                    embed=discord.Embed(title="Victoire de {0}".format(i.name), description="Il/elle était la tortue {0} ! {1}".format(win,dictEmote[win]), color=dictColor[win])
                    embed=auteur(i.userid,i.name,i.user.avatar,embed,"user")
                    play=True
                    embed.add_field(name="<:otCOINS:873226814527520809> gagnés par {0}".format(i.name),value="{0} <:otCOINS:873226814527520809>".format(len(self.ids)*25+sum(self.mises.values())))
                descip+="{0} : <@{1}>\n".format(dictEmote[i.couleur],i.userid)
            else:
                if i.couleur==win:
                    embed=discord.Embed(title="Victoire de {0}".format(i.titre), description="Il/elle était la tortue {0} ! {1}".format(win,dictEmote[win]), color=dictColor[win])
                    if self.emotesCustom[i.userid]!=None:
                        embed.set_author(name=i.titre,icon_url="https://cdn.discordapp.com/emojis/{0}.png".format(emoteDetector(self.emotesCustom[i.userid])[0]))
                    else:
                        embed=auteur(699728606493933650,i.titre,None,embed,"user")
                    play=True
                    embed.add_field(name="<:otCOINS:873226814527520809> gagnés par {0}".format(i.titre),value="{0} <:otCOINS:873226814527520809>".format(len(self.ids)*25+sum(self.mises.values())))
                descip+="{0} : {1}\n".format(dictEmote[i.couleur],i.titre)

        if play==False: 
            embed=discord.Embed(title="Personne n'a gagné !", description="La tortue {0} n'était jouée par personne ! {1}".format(win,dictEmote[win]), color=dictColor[win])
        embed.set_footer(text="OT!tortues")
        embed.description+="\n\n"+descip
        return embed

    async def emotesUser(self,bot):
        await super().emotesUser(bot)
        for i in self.joueurs:
            emote=getEmoteJeux(i.userid)
            self.emotesCustom[i.userid]=emote



class TortueCross(Tortue):

    def __init__(self, couleur):
        self.titre=None
        self.colorUser=None
        super().__init__(couleur)

    def setPlayer(self,user,titre):
        super().setPlayer(user)
        self.colorUser=getColorJeux(user.id)
        self.titre=titre