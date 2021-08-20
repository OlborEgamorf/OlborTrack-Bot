from Stats.SQL.ConnectSQL import connectSQL
from random import randint
from Core.Fonctions.Embeds import createEmbed, embedAssert
import asyncio
from Titres.Outils import gainCoins, titresJeux, titresTrivial

dictValue={1:300,2:800,3:5000}
dictSell={1:150,2:400,3:2500}



def simulation():
    liste=["Tortues","TortuesDuo","TrivialVersus","TrivialParty","TrivialBR","P4"]
    listeC={"Tortues":75,"TortuesDuo":100,"TrivialVersus":75,"TrivialParty":150,"TrivialBR":150,"P4":50,"BatailleNavale":50}
    for i in liste:
        connexion,curseur=connectSQL("OT",i,"Jeux","GL","")
        for j in curseur.execute("SELECT * FROM glob").fetchall():
            gainCoins(j["ID"],listeC[i]*j["W"])
            if j["W"]>=5:
                try:
                    titresJeux(5,i,j["ID"])
                except:
                    pass
            if j["W"]>=10:
                try:
                    titresJeux(10,i,j["ID"])
                except:
                    pass
    
    connexion,curseur=connectSQL("OT","ranks","Trivial",None,None)
    for j in curseur.execute("SELECT * FROM trivial12").fetchall():
        gainCoins(j["ID"],j["Count"])
        connexionUser,curseurUser=connectSQL("OT",j["ID"],"Trivial",None,None)
        for h in curseurUser.execute("SELECT * FROM trivial{0}".format(j["ID"])).fetchall():
            if h["Niveau"]>=5:
                try:
                    titresTrivial(5,h["IDCateg"],j["ID"])
                except:
                    pass
            if h["Niveau"]>=10:
                try:
                    titresTrivial(10,h["IDCateg"],j["ID"])
                except:
                    pass