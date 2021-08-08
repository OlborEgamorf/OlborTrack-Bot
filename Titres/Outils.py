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

def dailyCoins():
    dictRank={5:2,4:4,3:6,2:8,1:10}
    liste=["P4","BatailleNavale","Tortues","TortuesDuo","TrivialVersus","TrivialParty","TrivialBR"]
    for i in liste:
        connexion,curseur=connectSQL("OT",i,"Jeux","GL","")
        for j in curseur.execute("SELECT * FROM glob WHERE Rank<=5").fetchall():
            gainCoins(j["ID"],dictRank[j["Rank"]]) 


async def monthlyTitles(mois,annee,bot):
    dictTitres={"P4":"des Puissants","BatailleNavale":"des Mers","Tortues":"des Tortues","TortuesDuo":"de la Co-Op","TrivialVersus":"des Questions","TrivialParty":"de la Fête","TrivialBR":"de la Survie"}
    dictID={"P4":144,"BatailleNavale":147,"Tortues":141,"TortuesDuo":150,"TrivialVersus":156,"TrivialParty":159,"TrivialBR":153}
    liste=["P4","BatailleNavale","Tortues","TortuesDuo","TrivialVersus","TrivialParty","TrivialBR"]
    for i in liste:
        print(i)
        connexion,curseur=connectSQL("OT",i,"Jeux",mois,annee)
        try:
            for j in curseur.execute("SELECT * FROM {0}{1} WHERE Rank=1".format(tableauMois[mois].lower(),annee)).fetchall():
                connexionUser,curseurUser=connectSQL("OT",j["ID"],"Titres",None,None)
                try:
                    curseurUser.execute("INSERT INTO titresUser VALUES({0},'Prince {1}',0)".format(dictID[i],dictTitres[i]))
                    user=bot.get_user(j["ID"])
                    await user.send(embed=createEmbed("Bravo !","Vous avez terminé **1er** du classement du **{0}** le mois dernier !\nVous avez donc droit au titre exclusif **Prince {1}** !\nVous pouvez l'équiper avec la commande *OT!titre set {2}*, et consulter votre liste de titres avec *OT!titre perso*.".format(i,dictTitres[i],dictID[i]),0xf58d1d,"titre",user))
                except:
                    pass
                connexionUser.commit()
        except sqlite3.OperationalError:
            pass

        connexion,curseur=connectSQL("OT",i,"Jeux","GL","")
        connexionTitre,curseurTitre=connectSQL("OT","Titres","Titres",None,None)
        rank1=curseur.execute("SELECT * FROM glob WHERE Rank=1").fetchone()
        old=curseurTitre.execute("SELECT * FROM monthly WHERE Jeu='{0}'".format(i)).fetchone()
        if rank1["ID"]!=old["ID"]:
            print(rank1["ID"])
            connexionUser,curseurUser=connectSQL("OT",rank1["ID"],"Titres",None,None)
            createAccount(connexionUser,curseurUser)
            curseurUser.execute("INSERT INTO titresUser VALUES({0},'L’Empereur {1}',0)".format(dictID[i]+2,dictTitres[i]))
            connexionUser.commit()

            connexionUser,curseurUser=connectSQL("OT",old["ID"],"Titres",None,None)
            createAccount(connexionUser,curseurUser)
            curseurUser.execute("DELETE FROM titresUser WHERE ID={0}".format(dictID[i]+2))
            if curseurTitre.execute("SELECT * FROM active WHERE MembreID={0}".format(old["ID"])).fetchone()!=None:
                if curseurTitre.execute("SELECT * FROM active WHERE MembreID={0}".format(old["ID"])).fetchone()["TitreID"]==dictID[i]+2:
                    curseurTitre.execute("UPDATE active SET TitreID=8 WHERE MembreID={0}".format(old["ID"]))
            connexionUser.commit()

            curseurTitre.execute("UPDATE monthly SET ID={0} WHERE Jeu='{1}'".format(rank1["ID"],i))
            connexionTitre.commit()

            try:
                user=bot.get_user(rank1["ID"])
                #await user.send(embed=createEmbed("Bravo !","Vous êtes actuellement **1er** du classement GÉNÉRAL du **{0}** !!\nVous avez donc droit au titre exclusif **Empereur {1}** pour un mois !\nDéfendez votre place pendant tout le mois pour le garder !\nVous pouvez l'équiper avec la commande *OT!titre set {2}*, et consulter votre liste de titres avec *OT!titre perso*.".format(i,dictTitres[i],dictID[i]),0xf58d1d,user))
            except:
                pass