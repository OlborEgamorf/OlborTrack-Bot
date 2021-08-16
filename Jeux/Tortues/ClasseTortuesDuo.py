import discord
from Core.Fonctions.AuteurIcon import auteur
from Jeux.Tortues.ClassesAutres import Pile
from Jeux.Tortues.ClasseTortues import JeuTortues, Tortue
from Stats.SQL.ConnectSQL import connectSQL
from Stats.SQL.Execution import exeJeuxSQL
from Titres.Outils import gainCoins

dictEmote={0:"<:otBlank:828934808200937492>","rouge":"<:OTTrouge:860119157495693343>","verte":"<:OTTvert:860119157331853333>","bleue":"<:OTTbleu:860119157491892255>","jaune":"<:OTTjaune:860119157688631316>","violette":"<:OTTviolet:860119157672247326>","last":"*dernière tortue*","multi":"*au choix*"}
dictColor={"bleue":0x00CCFF,"violette":0x993366,"rouge":0xFF0000,"verte":0x77B255,"jaune":0xFFFF00}

class TortueDuo(Tortue):
    def __init__(self,couleur):
        super().__init__(couleur)
        self.equipe=0

    def setEquipe(self,equipe):
        self.equipe=equipe

class JeuTortuesDuo(JeuTortues):
    def __init__(self,guild,user):
        super().__init__(guild,user)
        self.tortues=[TortueDuo("bleue"),TortueDuo("verte"),TortueDuo("jaune"),TortueDuo("rouge"),TortueDuo("violette")]
        self.equipe={1:[],2:[]}
        self.score={1:0,2:0}
        self.plateau=[Pile() for i in range(10)]
        for i in self.tortues:
            self.plateau[0].empiler(i)
    
    def embedWin(self):
        descip=""
        play=False
        for i in self.score:
            if self.score[i]==2:
                embed=discord.Embed(title="Victoire de {0} et {1} !".format(self.equipe[i][0].name,self.equipe[i][1].name), description="Ils étaient les tortues {0} et {1} ! {2} {3}".format(self.equipe[i][0].couleur,self.equipe[i][1].couleur,dictEmote[self.equipe[i][0].couleur],dictEmote[self.equipe[i][1].couleur]), color=dictColor[self.equipe[i][0].couleur])

        for i in self.joueurs:
            descip+="{0} : <@{1}>\n".format(dictEmote[i.couleur],i.userid)
        
        embed.add_field(name="<:otCOINS:873226814527520809> gagnés par chacun des gagnants",value="{0} <:otCOINS:873226814527520809>".format(75+sum(self.mises.values())/2))

        embed=auteur(self.guild.id,self.guild.name,self.guild.icon,embed,"guild")
        embed.set_footer(text="OT!tortues")
        embed.description+="\n\n"+descip
        return embed

    def getWinner(self):
        already=True
        cont=len(self.plateau[9])
        temp=Pile()
        for j in range(cont):
            temp.empiler(self.plateau[9].depiler())
        cel=temp.contenu
        while cel is not None:
            win=cel.valeur
            if not cel.valeur.fini:
                already=False
                cel.valeur.fini=True
                break 
            cel=cel.suivante
        for j in range(cont):
            self.plateau[9].empiler(temp.depiler())
        if already:
            return None
        return win
    
    def stats(self,team):
        connexionGuild,curseurGuild=connectSQL(self.guild.id,"Guild","Guild",None,None)
        connexionOT,curseurOT=connectSQL("OT","Guild","Guild",None,None)
        for i in self.joueurs:
            if i.equipe==team:
                gainCoins(i.userid,75+sum(self.mises.values())/2)
                count,state=2,"W"
            else:
                count,state=-1,"L"
            exeJeuxSQL(i.userid,None,state,self.guild.id,curseurGuild,count,"TortuesDuo",None)
            exeJeuxSQL(i.userid,None,state,"OT",curseurOT,count,"TortuesDuo",None)
        connexionGuild.commit()
        connexionOT.commit()