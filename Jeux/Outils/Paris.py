from Stats.SQL.ConnectSQL import connectSQL
from Titres.Outils import gainCoins


class Pari:
    def __init__(self,ids,option):
        self.ids=ids
        self.mises={}
        self.cotes={}
        self.paris={}
        self.parissomme={}
        self.option=option
        self.ouvert=True
        self.setMises()
        self.setCotes()

    def setMises(self):
        for i in self.ids:
            self.mises[i]=0
    
    def setCotes(self):
        points={}
        victoires={}
        defaites={}
        connexion,curseur=connectSQL("OT")
        for i in self.ids:
            user=curseur.execute("SELECT * FROM glob WHERE ID={0}".format(i)).fetchone()
            if user==None:
                self.cotes[i]=None
            else:
                if user["Count"]>0:
                    points[i]=user["Count"]
                else:
                    points[i]=0
                victoires[i]=user["W"]
                defaites[i]=user["L"]
        somme=sum(points.values())
        if somme>0:
            for i in self.ids:
                if i in self.cotes:
                    continue
                if points[i]>0:
                    if defaites[i]>0:
                        self.cotes[i]=round((somme/points[i])-(victoires[i]/defaites[i]/2),2)
                    else:
                        self.cotes[i]=round((somme/points[i])-(victoires[i]/2),2)
                else:
                    if defaites[i]>0:
                        self.cotes[i]=round(4-(victoires[i]/defaites[i]*2),2)
                    else:
                        self.cotes[i]=round(4-(victoires[i]*2),2)
        else:
            for i in self.ids:
                if i in self.cotes:
                    continue
                if victoires[i]==0:
                    self.cotes[i]=2+0.1*defaites[i]
                else:
                    self.cotes[i]=round(2+defaites[i]/victoires[i]/10,2)
        for i in self.cotes:
            if self.cotes[i]!=None:
                if self.cotes[i]>4:
                    self.cotes[i]=4
                if self.cotes[i]<1.1:
                    self.cotes[i]=1.1

    def distribParis(self,win):
        for i in self.paris:
            if self.paris[i]==win:
                gainCoins(i,self.parissomme[i]*self.cotes[win])
