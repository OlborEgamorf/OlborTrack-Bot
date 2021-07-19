from Stats.SQL.ConnectSQL import connectSQL

class OTGuild:
    """Cette classe permet de stocker des informations sur un serveur, afin de ne pas avoir à ouvrir sans cesse des bases de données récurentes.
    
    Est stocké : 
    
            - l'état des salons
            - l'état des membres
            - les tableaux configurés
            - les commandes automatiques
            - les modules
            - si la commande Wikipedia est NSFW
    
    Elle est accompagnée de méthodes pour récupérer ces informations et de deux autres classes pour faciliter le stockage."""
    def __init__(self,id):
        self.id=id
        self.chan=None
        self.users=None
        self.mcmd=None
        self.mstats=None
        self.wikinsfw=None
        self.stats=True
        self.gd=False
        self.twitch=[]
        self.snipe=OTSnipe()
        self.starlist={}
        self.stardict={}
        self.auto=None

        connexion,curseur=connectSQL(self.id,"Guild","Guild",None,None)
        self.getStar(curseur)
        self.getHBM(curseur)
        self.getPerms(curseur)
        self.getAuto(curseur)
        self.getWikiNSFW(curseur)
        self.getTwitch(curseur)
        self.getStats(curseur)
    
    def getStar(self,curseur=None):
        if curseur==None:
            connexion,curseur=connectSQL(self.id,"Guild","Guild",None,None)
        self.stardict={}
        self.starlist={}
        for i in curseur.execute("SELECT * FROM sb").fetchall():
            if i["ID"] not in self.starlist:
                self.starlist[i["ID"]]=[]
            self.starlist[i["ID"]].append(i["Nombre"])
            self.stardict[i["Nombre"]]=OTTableau(i)
    
    def getHBM(self,curseur=None):
        if curseur==None:
            connexion,curseur=connectSQL(self.id,"Guild","Guild",None,None)
        self.chan={}
        self.users={}
        for i in curseur.execute("SELECT * FROM chans").fetchall():
            self.chan[i["ID"]]=i
        for i in curseur.execute("SELECT * FROM users").fetchall():
            self.users[i["ID"]]=i
    
    def getPerms(self,curseur=None):
        if curseur==None:
            connexion,curseur=connectSQL(self.id,"Guild","Guild",None,None)
        self.mcmd=curseur.execute("SELECT * FROM modulesCMD").fetchall()
        self.mstats=curseur.execute("SELECT * FROM modulesStats").fetchall()
    
    def getAuto(self,curseur=None):
        if curseur==None:
            connexion,curseur=connectSQL(self.id,"Guild","Guild",None,None)
        self.auto=curseur.execute("SELECT * FROM auto").fetchall()
    
    def getWikiNSFW(self,curseur=None):
        if curseur==None:
            connexion,curseur=connectSQL(self.id,"Guild","Guild",None,None)
        self.wikinsfw=curseur.execute("SELECT * FROM wikinsfw").fetchone()["Active"]
    
    def getTwitch(self,curseur=None):
        if curseur==None:
            connexion,curseur=connectSQL(self.id,"Guild","Guild",None,None)
        self.twitch=[]
        for i in curseur.execute("SELECT * FROM twitch").fetchall():
            self.twitch.append(OTTwitch(i))

    def getStats(self,curseur=None):
        if curseur==None:
            connexion,curseur=connectSQL(self.id,"Guild","Guild",None,None)
        self.stats=curseur.execute("SELECT * FROM stats").fetchone()["Active"]

class OTTableau:
    def __init__(self,star):
        self.nombre=star["Nombre"]
        self.salon=star["Salon"]
        self.emote=star["Emote"]
        self.count=star["Count"]
        self.id=star["ID"]

class OTSnipe:
    def __init__(self):
        self.texte=None
        self.date=None
        self.id=None
    
    def setSnipe(self,texte,date,id):
        self.texte=texte
        self.date=date
        self.id=id

class OTTwitch:
    def __init__(self,infos):
        self.stream=infos["Stream"]
        self.salon=infos["Salon"]
        self.descip=infos["Descip"]
        self.sent=infos["Sent"]
        self.numero=infos["Nombre"]