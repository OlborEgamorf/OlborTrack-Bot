from Stats.SQL.ConnectSQL import connectSQL
from Titres.Outils import createAccount, gainCoins
from Core.Fonctions.Embeds import createEmbed
import sqlite3
import asyncio

tableauMois={"01":"Janvier","02":"Février","03":"Mars","04":"Avril","05":"Mai","06":"Juin","07":"Juillet","08":"Aout","09":"Septembre","10":"Octobre","11":"Novembre","12":"Décembre","TO":"Année","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","glob":"GL","to":"TO"}

def dailyCoins():
    dictRank={5:2,4:4,3:6,2:8,1:10}
    liste=["P4","BatailleNavale","Tortues","TortuesDuo","TrivialVersus","TrivialParty","TrivialBR","Matrice"]
    for i in liste:
        connexion,curseur=connectSQL("OT",i,"Jeux","GL","")
        try:
            for j in curseur.execute("SELECT * FROM glob WHERE Rank<=5").fetchall():
                gainCoins(j["ID"],dictRank[j["Rank"]]) 
        except:
            pass


async def monthlyTitles(mois,annee,bot):
    dictCoins={3:50,2:100,1:200}
    dictTitres={"P4":"des Puissants","BatailleNavale":"des Mers","Tortues":"des Tortues","TortuesDuo":"de la Co-Op","TrivialVersus":"des Questions","TrivialParty":"de la Fête","TrivialBR":"de la Survie","Matrice":"de la Matrice"}
    dictID={"P4":76,"BatailleNavale":11,"Tortues":90,"TortuesDuo":95,"TrivialVersus":136,"TrivialParty":131,"TrivialBR":126,"Matrice":168}
    liste=["P4","BatailleNavale","Tortues","TortuesDuo","TrivialVersus","TrivialParty","TrivialBR","Matrice"]
    for i in liste:
        connexion,curseur=connectSQL("OT",i,"Jeux",mois,annee)
        try:
            for j in curseur.execute("SELECT * FROM {0}{1} WHERE Rank=1".format(tableauMois[mois].lower(),annee)).fetchall():
                connexionUser,curseurUser=connectSQL("OT",j["ID"],"Titres",None,None)
                try:
                    curseurUser.execute("INSERT INTO titresUser VALUES({0},'Prince {1}',0)".format(dictID[i],dictTitres[i]))
                    user=bot.get_user(j["ID"])
                    await user.send(embed=createEmbed("Bravo !","Vous avez terminé **1er** du classement du **{0}** lors du mois de {1}/{2} !\nVous avez donc droit au titre exclusif **Prince {3}** !\nVous pouvez l'équiper avec la commande *OT!titre set {4}*, et consulter votre liste de titres avec *OT!titre perso*.".format(i,mois,annee,dictTitres[i],dictID[i]),0xf58d1d,"titre",user))
                except:
                    pass
                connexionUser.commit()
            for j in curseur.execute("SELECT * FROM {0}{1} WHERE Rank<=3".format(tableauMois[mois].lower(),annee)).fetchall():
                gainCoins(j["ID"],dictCoins[j["Rank"]])
        except sqlite3.OperationalError:
            pass
        

        connexion,curseur=connectSQL("OT",i,"Jeux","GL","")
        connexionTitre,curseurTitre=connectSQL("OT","Titres","Titres",None,None)
        try:
            rank1=curseur.execute("SELECT * FROM glob WHERE Rank=1").fetchone()
        except:
            continue
        else:
            old=curseurTitre.execute("SELECT * FROM monthly WHERE Jeu='{0}'".format(i)).fetchone()
            if rank1["ID"]!=old["ID"]:
                connexionUser,curseurUser=connectSQL("OT",rank1["ID"],"Titres",None,None)
                createAccount(connexionUser,curseurUser)
                try:
                    curseurUser.execute("INSERT INTO titresUser VALUES({0},'L’Empereur {1}',0)".format(dictID[i]+2,dictTitres[i]))
                except:
                    pass
                connexionUser.commit()

                connexionUser,curseurUser=connectSQL("OT",old["ID"],"Titres",None,None)
                createAccount(connexionUser,curseurUser)
                curseurUser.execute("DELETE FROM titresUser WHERE ID={0}".format(dictID[i]+2))
                if curseurTitre.execute("SELECT * FROM active WHERE MembreID={0}".format(old["ID"])).fetchone()!=None:
                    if curseurTitre.execute("SELECT * FROM active WHERE MembreID={0}".format(old["ID"])).fetchone()["TitreID"]==dictID[i]+2:
                        curseurTitre.execute("UPDATE active SET TitreID=73 WHERE MembreID={0}".format(old["ID"]))
                connexionUser.commit()

                curseurTitre.execute("UPDATE monthly SET ID={0} WHERE Jeu='{1}'".format(rank1["ID"],i))
                connexionTitre.commit()

                try:
                    user=bot.get_user(rank1["ID"])
                    await user.send(embed=createEmbed("Bravo !","Vous êtes actuellement **1er** du classement GÉNÉRAL du **{0}** !!\nVous avez donc droit au titre exclusif **L’Empereur {1}** pour un mois !\nDéfendez votre place pendant tout le mois pour le garder !\nVous pouvez l'équiper avec la commande *OT!titre set {2}*, et consulter votre liste de titres avec *OT!titre perso*.".format(i,dictTitres[i],dictID[i]),0xf58d1d,user))
                except:
                    pass


async def annualyTitles(annee,bot):
    dictCoins={3:250,2:500,1:1000}
    dictTitres={"P4":"des Puissants","BatailleNavale":"des Mers","Tortues":"des Tortues","TortuesDuo":"de la Co-Op","TrivialVersus":"des Questions","TrivialParty":"de la Fête","TrivialBR":"de la Survie","Matrice":"de la Matrice"}
    dictID={"P4":77,"BatailleNavale":12,"Tortues":91,"TortuesDuo":96,"TrivialVersus":137,"TrivialParty":132,"TrivialBR":127,"Matrice":169}
    liste=["P4","BatailleNavale","Tortues","TortuesDuo","TrivialVersus","TrivialParty","TrivialBR","Matrice"]
    for i in liste:
        connexion,curseur=connectSQL("OT",i,"Jeux","TO",annee)
        try:
            for j in curseur.execute("SELECT * FROM to{0} WHERE Rank=1".format(annee)).fetchall():
                connexionUser,curseurUser=connectSQL("OT",j["ID"],"Titres",None,None)
                try:
                    curseurUser.execute("INSERT INTO titresUser VALUES({0},'Le Roi {1}',0)".format(dictID[i],dictTitres[i]))
                    user=bot.get_user(j["ID"])
                    await user.send(embed=createEmbed("Bravo !","Vous avez terminé **1er** du classement du **{0}** lors de l'année **20{1}** !\nVous avez donc droit au titre exclusif **Le Roi {2}** !\nVous pouvez l'équiper avec la commande *OT!titre set {3}*, et consulter votre liste de titres avec *OT!titre perso*.".format(i,annee,dictTitres[i],dictID[i]),0xf58d1d,"titre",user))
                except:
                    pass
                connexionUser.commit()
            for j in curseur.execute("SELECT * FROM to{0} WHERE Rank<=3".format(annee)).fetchall():
                gainCoins(j["ID"],dictCoins[j["Rank"]])
        except sqlite3.OperationalError:
            pass


async def badgesSimu(mois,annee,bot):
    dictValue={3:1,2:2,1:3}
    liste=["P4","BatailleNavale","Tortues","TortuesDuo","TrivialVersus","TrivialParty","TrivialBR","Matrice"]
    for i in liste:
        connexion,curseur=connectSQL("OT",i,"Jeux",mois,annee)
        try:
            for j in curseur.execute("SELECT * FROM {0}{1} WHERE Rank<=3".format(tableauMois[mois].lower(),annee)).fetchall():
                connexionUser,curseurUser=connectSQL("OT",j["ID"],"Titres",None,None)
                try:
                    curseurUser.execute("CREATE TABLE IF NOT EXISTS badges (Type TEXT, Période TEXT, Rang INT, Valeur INT, PRIMARY KEY(Type,Période,Rang))")
                    curseurUser.execute("INSERT INTO badges VALUES('{0}','{1}',{2},{3})".format(i,"mois",j["Rank"],dictValue[j["Rank"]]))
                    #curseurUser.execute("DROP TABLE badges")
                    connexionUser.commit()
                except sqlite3.IntegrityError:
                    pass
        except sqlite3.OperationalError:
            pass
        

        connexion,curseur=connectSQL("OT",i,"Jeux","GL","")
        try:
            for j in curseur.execute("SELECT * FROM glob WHERE Rank<=3").fetchall():
                connexionUser,curseurUser=connectSQL("OT",j["ID"],"Titres",None,None)
                try:
                    curseurUser.execute("CREATE TABLE IF NOT EXISTS badges (Type TEXT, Période TEXT, Rang INT, Valeur INT, PRIMARY KEY(Type,Période,Rang))")
                    curseurUser.execute("INSERT INTO badges VALUES('{0}','{1}',{2},{3})".format(i,"global",j["Rank"],100+dictValue[j["Rank"]]))
                    #curseurUser.execute("DROP TABLE badges")
                    connexionUser.commit()
                except sqlite3.IntegrityError:
                    pass
        except sqlite3.OperationalError:
            pass

        connexion,curseur=connectSQL("OT",i,"Jeux","TO",annee)
        try:
            for j in curseur.execute("SELECT * FROM to{0} WHERE Rank<=3".format(annee)).fetchall():
                connexionUser,curseurUser=connectSQL("OT",j["ID"],"Titres",None,None)
                try:
                    curseurUser.execute("CREATE TABLE IF NOT EXISTS badges (Type TEXT, Période TEXT, Rang INT, Valeur INT, PRIMARY KEY(Type,Période,Rang))")
                    curseurUser.execute("INSERT INTO badges VALUES('{0}','{1}',{2},{3})".format(i,"annee",j["Rank"],10+dictValue[j["Rank"]]))
                    #curseurUser.execute("DROP TABLE badges")
                    connexionUser.commit()
                except sqlite3.IntegrityError:
                    pass
        except sqlite3.OperationalError:
            pass
    
    for i in (128523828329578496,236142110355488768,422708715419074561,385108888330043393,233322552167104512,254731377013030914,417676325227331585,309320824891113473,520243182924070915,375632632244994048,216578161289330691,520243182924070915,309032693499297802):
        try:
            connexionUser,curseurUser=connectSQL("OT",i,"Titres",None,None)
            curseurUser.execute("CREATE TABLE IF NOT EXISTS badges (Type TEXT, Période TEXT, Rang INT, Valeur INT, PRIMARY KEY(Type,Période,Rang))")
            curseurUser.execute("INSERT INTO badges VALUES('{0}','{1}',{2},{3})".format("Special","VIP",0,0))
            connexionUser.commit()
        except sqlite3.IntegrityError:
            pass
    
    for i in (128523828329578496,151803910514933760,410535340542001172,774688029956243457,258593598860165120,227800236356009987,319931472058515476,417676325227331585,254731377013030914,233322552167104512,385108888330043393):
        try:
            connexionUser,curseurUser=connectSQL("OT",i,"Titres",None,None)
            curseurUser.execute("CREATE TABLE IF NOT EXISTS badges (Type TEXT, Période TEXT, Rang INT, Valeur INT, PRIMARY KEY(Type,Période,Rang))")
            curseurUser.execute("INSERT INTO badges VALUES('{0}','{1}',{2},{3})".format("Special","Testeur",0,0))
            connexionUser.commit()
        except sqlite3.IntegrityError:
            pass


"""listeDates=[("06","20"),("07","20"),("08","20"),("09","20"),("10","20"),("11","20"),("12","20"),("01","21"),("02","21"),("03","21"),("04","21"),("05","21"),("06","21"),("07","21"),("08","21")]
for i in listeDates:
    asyncio.run(badgesSimu(i[0],i[1],None))"""