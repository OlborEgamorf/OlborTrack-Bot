import discord
from Core.Fonctions.AuteurIcon import auteur
from Jeux.Tortues.ClassesAutres import Pile
from Jeux.CrossServeur.ClasseTortuesCross import JeuTortuesCross, TortueCross
from Stats.SQL.ConnectSQL import connectSQL
from Stats.SQL.Execution import exeJeuxSQL
from Titres.Outils import gainCoins
from Titres.Carte import newCarte

dictEmote={0:"<:otBlank:828934808200937492>","rouge":"<:OTTrouge:860119157495693343>","verte":"<:OTTvert:860119157331853333>","bleue":"<:OTTbleu:860119157491892255>","jaune":"<:OTTjaune:860119157688631316>","violette":"<:OTTviolet:860119157672247326>","last":"*dernière tortue*","multi":"*au choix*"}
dictColor={"bleue":0x00CCFF,"violette":0x993366,"rouge":0xFF0000,"verte":0x77B255,"jaune":0xFFFF00}

class TortueDuoCross(TortueCross):
    def __init__(self,couleur):
        super().__init__(couleur)
        self.equipe=0

    def setEquipe(self,equipe):
        self.equipe=equipe

class JeuTortuesDuoCross(JeuTortuesCross):
    def __init__(self,guild,user):
        super().__init__(guild,user)
        self.tortues=[TortueDuoCross("bleue"),TortueDuoCross("verte"),TortueDuoCross("jaune"),TortueDuoCross("rouge"),TortueDuoCross("violette")]
        self.equipe={1:[],2:[]}
        self.score={1:0,2:0}
        self.plateau=[Pile() for i in range(10)]
        for i in self.tortues:
            self.plateau[0].empiler(i)
    
    def embedWin(self,guild,bot):
        descip=""
        play=False
        for i in self.score:
            if self.score[i]==2:
                if self.memguild[self.equipe[i][0].userid]==guild:
                    nameP1=self.equipe[i][0].name
                else:
                    nameP1=self.equipe[i][0].titre

                if self.memguild[self.equipe[i][1].userid]==guild:
                    nameP2=self.equipe[i][1].name
                else:
                    nameP2=self.equipe[i][1].titre

                embed=discord.Embed(title="Victoire de {0} et {1} !".format(nameP1,nameP2), description="Ils étaient les tortues {0} et {1} ! {2} {3}".format(self.equipe[i][0].couleur,self.equipe[i][1].couleur,dictEmote[self.equipe[i][0].couleur],dictEmote[self.equipe[i][1].couleur]), color=dictColor[self.equipe[i][0].couleur])

        for i in self.joueurs:
            if self.memguild[i.userid]==guild:
                descip+="{0} : <@{1}>\n".format(dictEmote[i.couleur],i.userid)
            else:
                descip+="{0} : {1}\n".format(dictEmote[i.couleur],i.titre)
        
        embed.add_field(name="<:otCOINS:873226814527520809> gagnés par chacun des gagnants",value="{0} <:otCOINS:873226814527520809>".format(75+sum(self.paris.mises.values())/2))

        embed=auteur(bot.user,None,None,embed,"olbor")
        embed.set_footer(text="OT!tortuesduocross")
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
    
    async def stats(self,team):
        connexionOT,curseurOT=connectSQL("OT","Guild","Guild",None,None)
        for i in self.joueurs:
            if i.equipe==team:
                gainCoins(i.userid,75+sum(self.paris.mises.values())/2)
                count,state=2,"W"
            else:
                count,state=-1,"L"
            wins=exeJeuxSQL(i.userid,None,state,"OT",curseurOT,count,"TortuesDuo",None)
            if state=="W":
                await newCarte(i.user,"TortuesDuo",wins,"cross")
                for j in self.messages:
                    await j.channel.send(file=discord.File("Images/ExFond/{0}.png".format(i.userid)))
        connexionOT.commit()
