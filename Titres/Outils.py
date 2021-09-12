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
    curseur.execute("CREATE TABLE IF NOT EXISTS badges (Type TEXT, Période TEXT, Rang INT, Valeur INT, PRIMARY KEY(Type,Période,Rang))")
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
        dict5ID={0:122,1:100,2:102,3:104,4:106,5:108,6:110,7:112,8:114,9:116,10:118,11:120,12:98}
        curseurUser.execute("INSERT INTO titresUser VALUES({0},'{1}',0)".format(dict5ID[categ],dict5[categ]))
    else:
        dict10={0:"Connaisseur",1:"Réalisateur",2:"Virologue",3:"Légende",4:"Athlète",5:"Cartographe",6:"Historique",7:"Ministre",8:"Chef d’Oeuvre",9:"Star",10:"Requin",11:"Bolide",12:"Encyclopédie"}
        dict10ID={0:123,1:101,2:103,3:105,4:107,5:109,6:111,7:113,8:115,9:117,10:119,11:121,12:99}
        curseurUser.execute("INSERT INTO titresUser VALUES({0},'{1}',0)".format(dict10ID[categ],dict10[categ]))
    connexionUser.commit()

def titresJeux(wins,option,user):
    connexionUser,curseurUser=connectSQL("OT",user,"Titres",None,None)
    if wins==5:
        dict5={"P4":"Aligné","BatailleNavale":"Navire","Tortues":"Empilé","TortuesDuo":"Équipier","TrivialVersus":"Vainqueur","TrivialParty":"Fêtard","TrivialBR":"Vivant","Matrice":"Inversé"}
        dict5ID={"P4":74,"BatailleNavale":9,"Tortues":88,"TortuesDuo":93,"TrivialVersus":134,"TrivialParty":129,"TrivialBR":124,"Matrice":166}
        curseurUser.execute("INSERT INTO titresUser VALUES({0},'{1}',0)".format(dict5ID[option],dict5[option]))
    else:
        dict10={"P4":"Puissance 10","BatailleNavale":"Flotte Armée","Tortues":"Tortue de Sport","TortuesDuo":"Co-Pilote","TrivialVersus":"Médaillé","TrivialParty":"Bourré","TrivialBR":"Survivant","Matrice":"Matrixé"}
        dict10ID={"P4":75,"BatailleNavale":10,"Tortues":89,"TortuesDuo":94,"TrivialVersus":135,"TrivialParty":130,"TrivialBR":125,"Matrice":167}
        curseurUser.execute("INSERT INTO titresUser VALUES({0},'{1}',0)".format(dict10ID[option],dict10[option]))
    connexionUser.commit()

def changeIDs():
    connexion,curseur=connectSQL("OT","Titres","Titres",None,None)
    liste=curseur.execute("SELECT * FROM titres ORDER BY Collection ASC").fetchall()
    for i in range(len(liste)):
        curseur.execute("UPDATE titres SET ID={0} WHERE Nom='{1}'".format(i+1,liste[i]["Nom"]))
    connexion.commit()