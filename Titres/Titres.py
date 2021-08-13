from Stats.SQL.ConnectSQL import connectSQL
from random import randint
from Core.Fonctions.Embeds import createEmbed, embedAssert
import asyncio
from Titres.Outils import titresJeux, titresTrivial

dictValue={1:300,2:800,3:5000}
dictSell={1:150,2:400,3:2500}








    
    
def simulation():
    connexionS,curseurS=connectSQL("OT","Simu","Titres",None,None)
    liste=["Tortues","Tortuesduo","TrivialVersus","TrivialParty","TrivialBR","P4","BatailleNavale"]
    listeC={"Tortues":75,"Tortuesduo":100,"TrivialVersus":75,"TrivialParty":150,"TrivialBR":150,"P4":50,"BatailleNavale":50}
    for i in liste:
        connexion,curseur=connectSQL("OT",i,"Jeux","GL","")
        for j in curseur.execute("SELECT * FROM glob").fetchall():
            if curseurS.execute("SELECT * FROM Simu WHERE ID={0}".format(j["ID"])).fetchone()==None:
                curseurS.execute("INSERT INTO Simu VALUES({0},0)".format(j["ID"]))
            curseurS.execute("UPDATE Simu SET Coins=Coins+{0} WHERE ID={1}".format(listeC[i]*j["W"],j["ID"]))
            if j["W"]>=5:
                titresJeux(5,i,j["ID"])
            if j["W"]>=10:
                titresJeux(10,i,j["ID"])
    
    connexion,curseur=connectSQL("OT","ranks","Trivial",None,None)
    for j in curseur.execute("SELECT * FROM trivial12").fetchall():
        if curseurS.execute("SELECT * FROM Simu WHERE ID={0}".format(j["ID"])).fetchone()==None:
            curseurS.execute("INSERT INTO Simu VALUES({0},0)".format(j["ID"]))
        curseurS.execute("UPDATE Simu SET Coins=Coins+{0} WHERE ID={1}".format(j["Count"],j["ID"]))
        connexionUser,curseurUser=connectSQL("OT",j["ID"],"Trivial",None,None)
        for h in curseurUser.execute("SELECT * FROM trivial{0}".format(j["ID"])).fetchall():
            if h["Niveau"]>=5:
                titresTrivial(5,h["IDCateg"],j["ID"])
            if h["Niveau"]>=10:
                titresTrivial(10,h["IDCateg"],j["ID"])

    
    connexionS.commit()

