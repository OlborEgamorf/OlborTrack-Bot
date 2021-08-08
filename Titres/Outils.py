from Stats.SQL.ConnectSQL import connectSQL
from random import randint
from Core.Fonctions.Embeds import createEmbed
import sqlite3

tableauMois={"01":"Janvier","02":"Février","03":"Mars","04":"Avril","05":"Mai","06":"Juin","07":"Juillet","08":"Aout","09":"Septembre","10":"Octobre","11":"Novembre","12":"Décembre","TO":"Année","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","glob":"GL","to":"TO"}

def setMarketPlace():
    connexion,curseur=connectSQL("OT","Titres","Titres",None,None)
    for i in curseur.execute("SELECT * FROM marketplace").fetchall():
        if i["Stock"]!=0:
            curseur.execute("UPDATE titres SET Stock=Stock+{0} WHERE ID={1}".format(i["Stock"],i["ID"]))
        curseur.execute("DELETE FROM marketplace WHERE ID={0}".format(i["ID"]))
    
    if randint(0,5)==3:
        if curseur.execute("SELECT * FROM titres WHERE Rareté=3 AND Stock=1").fetchall()!=[]:
            unique=curseur.execute("SELECT ID FROM titres WHERE Rareté=3 AND Stock=1 ORDER BY RANDOM()").fetchone()
            curseur.execute("UPDATE titres SET Stock=0, Known=True WHERE ID={0}".format(unique["ID"]))
            curseur.execute("INSERT INTO marketplace VALUES({0},1,True)".format(unique["ID"]))
    
    if curseur.execute("SELECT * FROM titres WHERE Rareté=2 AND Stock<>0").fetchall()!=[]:
        legend=curseur.execute("SELECT ID,Stock FROM titres WHERE Rareté=2 AND Stock<>0 ORDER BY RANDOM() LIMIT 3").fetchall()
        for i in legend:
            if i["Stock"]<3:
                curseur.execute("UPDATE titres SET Stock=0, Known=True WHERE ID={0}".format(i["ID"]))
                curseur.execute("INSERT INTO marketplace VALUES({0},{1},True)".format(i["ID"],i["Stock"]))
            else:
                curseur.execute("UPDATE titres SET Stock=Stock-3, Known=True WHERE ID={0}".format(i["ID"]))
                curseur.execute("INSERT INTO marketplace VALUES({0},3,True)".format(i["ID"]))
    
    if curseur.execute("SELECT * FROM titres WHERE Rareté=1 AND Stock<>0").fetchall()!=[]:
        legend=curseur.execute("SELECT ID,Stock FROM titres WHERE Rareté=1 AND Stock<>0 ORDER BY RANDOM() LIMIT 7").fetchall()
        for i in legend:
            if i["Stock"]<10:
                curseur.execute("UPDATE titres SET Stock=0, Known=True WHERE ID={0}".format(i["ID"]))
                curseur.execute("INSERT INTO marketplace VALUES({0},{1},True)".format(i["ID"],i["Stock"]))
            else:
                curseur.execute("UPDATE titres SET Stock=Stock-10, Known=True WHERE ID={0}".format(i["ID"]))
                curseur.execute("INSERT INTO marketplace VALUES({0},10,True)".format(i["ID"]))

    connexion.commit()

def createAccount(connexion,curseur):
    curseur.execute("CREATE TABLE IF NOT EXISTS titresUser (ID INT, Nom TEXT, Rareté INT, PRIMARY KEY(ID))")
    curseur.execute("CREATE TABLE IF NOT EXISTS coins (Coins INT)")
    if curseur.execute("SELECT * FROM coins").fetchone()==None:
        curseur.execute("INSERT INTO coins VALUES(0)")
    connexion.commit()

def gainCoins(user,coins):
    connexion,curseur=connectSQL("OT",user,"Titres",None,None)
    createAccount(connexion,curseur)
    curseur.execute("UPDATE coins SET Coins=Coins+{0}".format(coins))
    connexion.commit()

def titresTrivial(niveau,categ,user):
    connexionUser,curseurUser=connectSQL("OT",user,"Titres",None,None)
    if niveau==5:
        dict5={0:"Cultivé",1:"Diverti",2:"Scientifique",3:"Mythe",4:"Sportif",5:"Géographe",6:"Historien",7:"Député",8:"Artiste",9:"Célèbre",10:"Lion",11:"Mécano",12:"Cerveau"}
        dict5ID={0:162,1:11,2:13,3:15,4:17,5:19,6:21,7:23,8:25,9:27,10:29,11:31,12:9}
        curseurUser.execute("INSERT INTO titresUser VALUES({0},'{1}',0)".format(dict5ID[categ],dict5[categ]))
    else:
        dict10={0:"Connaisseur",1:"Réalisateur",2:"Virologue",3:"Légende",4:"Athlète",5:"Cartographe",6:"Historique",7:"Ministre",8:"Chef d’Oeuvre",9:"Star",10:"Requin",11:"Bolide",12:"Encyclopédie"}
        dict10ID={0:163,1:12,2:14,3:16,4:18,5:20,6:22,7:24,8:26,9:28,10:30,11:32,12:10}
        curseurUser.execute("INSERT INTO titresUser VALUES({0},'{1}',0)".format(dict10ID[categ],dict10[categ]))
    connexionUser.commit()

def titresJeux(wins,option,user):
    connexionUser,curseurUser=connectSQL("OT",user,"Titres",None,None)
    if wins==5:
        dict5={"P4":"Aligné","BatailleNavale":"Navire","Tortues":"Empilé","TortuesDuo":"Équipier","TrivialVersus":"Vainqueur","TrivialParty":"Fêtard","TrivialBR":"Vivant"}
        dict5ID={"P4":39,"BatailleNavale":45,"Tortues":41,"TortuesDuo":43,"TrivialVersus":33,"TrivialParty":35,"TrivialBR":37}
        curseurUser.execute("INSERT INTO titresUser VALUES({0},'{1}',0)".format(dict5ID[option],dict5[option]))
    else:
        dict10={"P4":"Puissance 10","BatailleNavale":"Flotte Armée","Tortues":"Tortue de Sport","TortuesDuo":"Co-Pilote","TrivialVersus":"Médaillé","TrivialParty":"Bourré","TrivialBR":"Survivant"}
        dict10ID={"P4":40,"BatailleNavale":46,"Tortues":42,"TortuesDuo":44,"TrivialVersus":34,"TrivialParty":36,"TrivialBR":38}
        curseurUser.execute("INSERT INTO titresUser VALUES({0},'{1}',0)".format(dict10ID[option],dict10[option]))
    connexionUser.commit()

def getTitre(curseur,user):
    total=""
    custom=curseur.execute("SELECT Custom FROM custom WHERE ID={0}".format(user)).fetchone()
    titre=curseur.execute("SELECT titres.Nom FROM active JOIN titres ON active.TitreID=titres.ID WHERE MembreID={0}".format(user)).fetchone()
    if custom!=None:
        total+="{0}, ".format(custom["Custom"])
    if titre==None:
        total+="Inconnu"
    else:
        total+=titre["Nom"]
    return total