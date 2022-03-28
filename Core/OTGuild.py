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
    def __init__(self,id,get):
        self.id=id
        self.chan=None
        self.users=None
        self.mcmd=None
        self.mstats=None
        self.stats=True
        self.gd=False

        if get:
            connexion,curseur=connectSQL(self.id,"Guild","Guild",None,None)
            self.getHBM(curseur)
            self.getPerms(curseur)
            self.getStats(curseur)

    def getStats(self,curseur=None):
        if curseur==None:
            connexion,curseur=connectSQL(self.id,"Guild","Guild",None,None)
        self.stats=curseur.execute("SELECT * FROM stats").fetchone()["Active"]

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

class OTGuildCMD(OTGuild):
    def __init__(self,id,get):
        super().__init__(id,get)
        self.wikinsfw=None
        self.twitch=[]
        self.yt=[]
        self.snipe=OTSnipe()
        self.starlist={}
        self.stardict={}
        self.voicehub={}
        self.voiceephem=[]
        self.twitter=[]
        self.bv=None
        self.ad=None
        self.auto=None
        self.anniv=None

        if get:
            connexion,curseur=connectSQL(self.id,"Guild","Guild",None,None)
            self.getStar(curseur)
            self.getAuto(curseur)
            self.getWikiNSFW(curseur)
            self.getTwitch(curseur)
            self.getYouTube(curseur)
            self.getHubs()
            self.getChans()
            self.getBV(curseur)
            self.getAnniv()
            self.getTwitter(curseur)
            self.getDynIcon(curseur)

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

    def getYouTube(self,curseur=None):
        if curseur==None:
            connexion,curseur=connectSQL(self.id,"Guild","Guild",None,None)
        self.yt=[]
        for i in curseur.execute("SELECT * FROM youtube").fetchall():
            self.yt.append(OTYouTube(i))
    
    def getTwitter(self,curseur=None):
        if curseur==None:
            connexion,curseur=connectSQL(self.id,"Guild","Guild",None,None)
        self.twitter=[]
        for i in curseur.execute("SELECT * FROM twitter").fetchall():
            self.twitter.append(OTTwitter(i))

    def getHubs(self,curseur=None):
        self.voicehub={}
        if curseur==None:
            connexion,curseur=connectSQL(self.id,"VoiceEphem","Guild",None,None)
        for i in curseur.execute("SELECT * FROM hub").fetchall():
            self.voicehub[i["ID"]]=OTHub(i)
    
    def getChans(self,curseur=None):
        self.voiceephem=[]
        if curseur==None:
            connexion,curseur=connectSQL(self.id,"VoiceEphem","Guild",None,None)
        for i in curseur.execute("SELECT * FROM salons").fetchall():
            self.voiceephem.append(i["IDChannel"])

    def getBV(self,curseur=None):
        self.bv=None
        self.ad=None
        if curseur==None:
            connexion,curseur=connectSQL(self.id,"Guild","Guild",None,None)
        if curseur.execute("SELECT * FROM etatBVAD WHERE Type='BV'").fetchone()["Statut"]==True:
            self.bv=curseur.execute("SELECT * FROM etatBVAD WHERE Type='BV'").fetchone()["Salon"]
        if curseur.execute("SELECT * FROM etatBVAD WHERE Type='AD'").fetchone()["Statut"]==True:
            self.ad=curseur.execute("SELECT * FROM etatBVAD WHERE Type='AD'").fetchone()["Salon"]

    def getAnniv(self,curseur=None):
        self.anniv=None
        if curseur==None:
            connexion,curseur=connectSQL(self.id,"Guild","Guild",None,None)
        anniv=curseur.execute("SELECT * FROM etatAnniv").fetchone()
        if anniv["Statut"]==True:
            self.anniv=OTAnniv(anniv)

    def getDynIcon(self,curseur=None):
        if curseur==None:
            connexion,curseur=connectSQL(self.id,"Guild","Guild",None,None)
        dyn=curseur.execute("SELECT * FROM etatPP").fetchone()
        if dyn["Statut"]==True:
            self.dynicon=dyn["Salon"]
        else:
            self.dynicon=None

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

class OTYouTube:
    def __init__(self,infos):
        self.chaine=infos["Chaine"]
        self.salon=infos["Salon"]
        self.descip=infos["Descip"]
        self.last=infos["LastID"]
        self.numero=infos["Nombre"]

class OTTwitter:
    def __init__(self,infos):
        self.compte=infos["Compte"]
        self.salon=infos["Salon"]
        self.descip=infos["Descip"]
        self.last=infos["LastID"]
        self.numero=infos["Nombre"]
        self.nom=infos["Nom"]

class OTAnniv:
    def __init__(self,anniv):
        self.chan=anniv["Salon"]
        self.descip=anniv["Message"]

class OTHub:
    def __init__(self,hub):
        self.limite=hub["Limite"]
        self.pattern=hub["Pattern"]