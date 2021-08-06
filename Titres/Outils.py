from Stats.SQL.ConnectSQL import connectSQL
from random import randint

def setMarketPlace():
    connexion,curseur=connectSQL("OT","Titres","Titres",None,None)
    for i in curseur.execute("SELECT * FROM marketplace").fetchall():
        if i["Stock"]!=0:
            curseur.execute("UPDATE titres SET Stock=Stock+{0} WHERE ID={1}".format(i["Stock"],i["ID"]))
        curseur.execute("DELETE FROM marketplace WHERE ID={0}".format(i["ID"]))
    
    if randint(0,5)==3:
        if curseur.execute("SELECT * FROM titres WHERE Rareté=3 AND Stock=1").fetchall()!=[]:
            unique=curseur.execute("SELECT ID FROM titres WHERE Rareté=3 AND Stock=1 ORDER BY RANDOM()").fetchone()
            curseur.execute("UPDATE titres SET Stock=0 WHERE ID={0}".format(unique["ID"]))
            curseur.execute("INSERT INTO marketplace VALUES({0},1)".format(unique["ID"]))
    
    if curseur.execute("SELECT * FROM titres WHERE Rareté=2 AND Stock<>0").fetchall()!=[]:
        legend=curseur.execute("SELECT ID,Stock FROM titres WHERE Rareté=2 AND Stock<>0 ORDER BY RANDOM() LIMIT 3").fetchall()
        for i in legend:
            if i["Stock"]<3:
                curseur.execute("UPDATE titres SET Stock=0 WHERE ID={0}".format(i["ID"]))
                curseur.execute("INSERT INTO marketplace VALUES({0},{1})".format(i["ID"],i["Stock"]))
            else:
                curseur.execute("UPDATE titres SET Stock=Stock-3 WHERE ID={0}".format(i["ID"]))
                curseur.execute("INSERT INTO marketplace VALUES({0},3)".format(i["ID"]))
    
    if curseur.execute("SELECT * FROM titres WHERE Rareté=1 AND Stock<>0").fetchall()!=[]:
        legend=curseur.execute("SELECT ID,Stock FROM titres WHERE Rareté=1 AND Stock<>0 ORDER BY RANDOM() LIMIT 7").fetchall()
        for i in legend:
            if i["Stock"]<10:
                curseur.execute("UPDATE titres SET Stock=0 WHERE ID={0}".format(i["ID"]))
                curseur.execute("INSERT INTO marketplace VALUES({0},{1})".format(i["ID"],i["Stock"]))
            else:
                curseur.execute("UPDATE titres SET Stock=Stock-10 WHERE ID={0}".format(i["ID"]))
                curseur.execute("INSERT INTO marketplace VALUES({0},10)".format(i["ID"]))

    connexion.commit()

def createAccount(connexion,curseur):
    curseur.execute("CREATE TABLE IF NOT EXISTS titresUser (ID INT, Nom TEXT, Rareté INT, PRIMARY KEY(ID))")
    curseur.execute("CREATE TABLE IF NOT EXISTS coins (Coins INT)")
    curseur.execute("INSERT INTO coins VALUES(0)")
    connexion.commit()