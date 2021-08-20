import discord
from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.GetNom import getTitre
from Stats.SQL.ConnectSQL import connectSQL
from Stats.SQL.EmoteDetector import emoteDetector
from Titres.Couleur import getColorJeux
from Titres.Emote import getEmoteJeux
from Jeux.P4 import JeuP4, JoueurP4


class JeuP4Cross(JeuP4):
    def __init__(self, guild, user):
        self.guilds=[]
        self.messages=[]
        self.memguild={}
        self.messguild={}
        self.guildmess={}
        self.memmess={}
        self.emotesCustom={}
        super().__init__(guild, user)
    
    def addPlayer(self,user):
        self.joueurs.append(JoueurP4Cross(user))

    def createEmbedP4(self,user,guild):
        if self.memguild[user.id]==guild:
            embed=discord.Embed(title="Au tour de {0}".format(user.nom),description=self.affichageTab())
            auteur(user.id,user.nom,user.avatar,embed,"user")
        else:
            embed=discord.Embed(title="Au tour de {0}".format(user.titre),description=self.affichageTab())
            if user.emote!=None:
                embed.set_author(name=user.titre,icon_url="https://cdn.discordapp.com/emojis/{0}.png".format(emoteDetector(user.emote)[0]))
            else:
                embed=auteur(699728606493933650,user.titre,None,embed,"user")
        embed.set_footer(text="OT!p4cross")

        descip=""
        if self.memguild[self.joueurs[0].id]==guild:
            descip="<@{0}> : <:otP1:726164724882079854>\n".format(self.joueurs[0].id)
        else:
            descip="{0} : <:otP1:726164724882079854>\n".format(self.joueurs[0].titre)

        if self.memguild[self.joueurs[1].id]==guild:
            descip+="<@{0}> : <:otP2:726165146229145610>".format(self.joueurs[1].id)
        else:
            descip+="{0} : <:otP2:726165146229145610>".format(self.joueurs[1].titre)

        embed.add_field(name="Joueurs",value=descip)
        if sum(self.mises.values())!=0:
            descip=""
            for i in self.joueurs:
                if self.mises[i.id]!=0:
                    if self.memguild[i.id]==guild:
                        descip+="<@{0}> : {1} <:otCOINS:873226814527520809>\n".format(i.id,self.mises[i.id])
                    else:
                        descip+="{0} : {1} <:otCOINS:873226814527520809>\n".format(i.titre,self.mises[i.id])
            embed.add_field(name="Mises d'OT Coins",value=descip)
        
        if user.color!=None:
            embed.color=user.color
        return embed

    def embedWin(self,win,nul,guild):
        if nul==True:
            embed=discord.Embed(title="Match nul !", description="Le tableau est bloqué, et personne n'a gagné !", color=0xad917b)
        else:
            if self.memguild[self.joueurs[win].id]==guild:
                embed=discord.Embed(title="Victoire de {0}".format(self.joueurs[win].nom), description="Bravo à lui/elle !")
                embed=auteur(self.joueurs[win].id,self.joueurs[win].nom,self.joueurs[win].avatar,embed,"user")
            else:
                embed=discord.Embed(title="Victoire de {0}".format(self.joueurs[win].titre), description="Bravo à lui/elle !")
                if self.joueurs[win].emote!=None:
                    embed.set_author(name=self.joueurs[win].titre,icon_url="https://cdn.discordapp.com/emojis/{0}.png".format(emoteDetector(self.joueurs[win].emote)[0]))
                else:
                    embed=auteur(699728606493933650,self.joueurs[win].titre,None,embed,"user")
            embed.add_field(name="<:otCOINS:873226814527520809> gagnés",value="{0} <:otCOINS:873226814527520809>".format(50+sum(self.mises.values())))

        embed.set_footer(text="OT!p4cross")
        if self.joueurs[win].color!=None:
            embed.color=self.joueurs[win].color

        return embed

class JoueurP4Cross(JoueurP4):
    def __init__(self, user):
        self.titre=None
        self.emote=None
        super().__init__(user)
        self.setColorTitre()
    
    def setColorTitre(self):
        connexion,curseur=connectSQL("OT","Titres","Titres",None,None)
        self.color=getColorJeux(self.id)
        self.titre=getTitre(curseur,self.id)
        self.emote=getEmoteJeux(self.id)
