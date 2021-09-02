from Stats.SQL.ConnectSQL import connectSQL
from Titres.Outils import createAccount, gainCoins
from Core.Fonctions.Embeds import createEmbed
import sqlite3

tableauMois={"01":"Janvier","02":"Février","03":"Mars","04":"Avril","05":"Mai","06":"Juin","07":"Juillet","08":"Aout","09":"Septembre","10":"Octobre","11":"Novembre","12":"Décembre","TO":"Année","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","glob":"GL","to":"TO"}

def dailyCoins():
    dictRank={5:2,4:4,3:6,2:8,1:10}
    liste=["P4","BatailleNavale","Tortues","TortuesDuo","TrivialVersus","TrivialParty","TrivialBR"]
    for i in liste:
        connexion,curseur=connectSQL("OT",i,"Jeux","GL","")
        try:
            for j in curseur.execute("SELECT * FROM glob WHERE Rank<=5").fetchall():
                gainCoins(j["ID"],dictRank[j["Rank"]]) 
        except:
            pass


async def monthlyTitles(mois,annee,bot):
    dictCoins={3:50,2:100,1:200}
    dictTitres={"P4":"des Puissants","BatailleNavale":"des Mers","Tortues":"des Tortues","TortuesDuo":"de la Co-Op","TrivialVersus":"des Questions","TrivialParty":"de la Fête","TrivialBR":"de la Survie"}
    dictID={"P4":76,"BatailleNavale":11,"Tortues":90,"TortuesDuo":95,"TrivialVersus":136,"TrivialParty":131,"TrivialBR":126}
    liste=["P4","BatailleNavale","Tortues","TortuesDuo","TrivialVersus","TrivialParty","TrivialBR"]
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
    dictTitres={"P4":"des Puissants","BatailleNavale":"des Mers","Tortues":"des Tortues","TortuesDuo":"de la Co-Op","TrivialVersus":"des Questions","TrivialParty":"de la Fête","TrivialBR":"de la Survie"}
    dictID={"P4":77,"BatailleNavale":12,"Tortues":91,"TortuesDuo":96,"TrivialVersus":137,"TrivialParty":132,"TrivialBR":127}
    liste=["P4","BatailleNavale","Tortues","TortuesDuo","TrivialVersus","TrivialParty","TrivialBR"]
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