from random import choice
import sqlite3

from Stats.SQL.ConnectSQL import CustomCursor, connectSQL

dictTriArg={"countAsc":"Count","rankAsc":"Rank","countDesc":"Count","rankDesc":"Rank","dateAsc":"DateID","dateDesc":"DateID","periodAsc":"None","periodDesc":"None","moyDesc":"Moyenne","nombreDesc":"Nombre"}
dictTriSens={"countAsc":"ASC","rankAsc":"ASC","countDesc":"DESC","rankDesc":"DESC","dateAsc":"ASC","dateDesc":"DESC","periodAsc":"None","periodDesc":"None","moyDesc":"DESC","nombreDesc":"DESC"}
tableauMois={"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre","TO":"to","1":"janvier","2":"février","3":"mars","4":"avril","5":"mai","6":"juin","7":"juillet","8":"aout","9":"septembre","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","to":"to","glob":"GL","GL":"glob"}

def getTableDay(curseur:sqlite3.Cursor,mois:str,annee:str,tri:str) -> list:
    """Permet d'extraire une liste des jours d'activité selon les critères de période que l'on veut.
    Entrées : 
        curseur : curseur pour accéder à la base de données
        mois : mois de la période voulue
        annee : année de la période voulue
        tri : comment la liste doit être triée
    Sortie :
        la liste qui répond à nos critères, renvoyée par la requête SQL"""
    if mois.lower()=="glob":
        return curseur.execute("SELECT *, Annee || '' || Mois || '' || Jour AS DateID FROM dayRank ORDER BY {0} {1}".format(dictTriArg[tri],dictTriSens[tri])).fetchall()
    elif mois.lower()=="to":
        return curseur.execute("SELECT *, Annee || '' || Mois || '' || Jour AS DateID FROM dayRank WHERE Annee='{0}' ORDER BY {1} {2}".format(annee,dictTriArg[tri],dictTriSens[tri])).fetchall()
    else:
        return curseur.execute("SELECT *, Annee || '' || Mois || '' || Jour AS DateID FROM dayRank WHERE Mois='{0}' AND Annee='{1}' ORDER BY {2} {3}".format(mois,annee,dictTriArg[tri],dictTriSens[tri])).fetchall()

def getTableSV(curseur:sqlite3.Cursor,option:str,id:int) -> list:
    """Permet d'obtenir la liste des phrases SavezVous d'une personne, ou toutes, en fonction de l'option.
    Entrées :
        curseur : curseur pour accéder à la base de données
        option : option de la commade (list ou modo)
        id : l'ID de la personne, si option==list
    Sortie :
        la liste qui répond à nos critères, renvoyée par la requête SQL"""
    if option=="list":
        return curseur.execute("SELECT * FROM savezvous WHERE ID={0}".format(id)).fetchall()
    return curseur.execute("SELECT * FROM savezvous").fetchall()

def collapseEvol(table:list) -> list:
    """Permet d'écraser une table évol pour ne faire ressortir que les dates importantes si la table est trop grande : changement de rang et changement de mois
    Entrée : 
        table : la table évol à écraser
    Sortie :
        table si len(table)<=31, sinon newTable, la table écrasée"""
    newTable=[table[0]]
    temp=(table[0]["Mois"],table[0]["Annee"])
    if len(table)>31:
        for i in range(1,len(table)-1):
            if table[i]["Evol"]!=0 or temp!=(table[i]["Mois"],table[i]["Annee"]):
                newTable.append(table[i])
                temp=(table[i]["Mois"],table[i]["Annee"])
        newTable.append(table[i+1])
        return newTable
    return table

def getTablePeriods(curseur,option,id,period,column,tri):
    liste=[]

    if period == "M":
        liste = curseur.execute(f"SELECT {column}, SUM(Count) AS Final, Mois, Annee, RANK() OVER (partition by Mois,Annee ORDER BY SUM(Count) DESC) AS 'Rank' FROM {option}_ranks GROUP BY {column}, Mois, Annee").fetchall()
    else:
        liste = curseur.execute(f"SELECT {column}, SUM(Count) AS Final, Annee, RANK() OVER (partition by Annee ORDER BY SUM(Count) DESC) AS 'Rank' FROM {option}_ranks GROUP BY {column}, Annee").fetchall()
        for i in liste:
            i["Mois"] = "TO"

    liste = list(filter(lambda x:x[column] == id, liste))
    
    if tri=="countDesc":
        liste.sort(key=lambda x:x["Final"],reverse=True)
    elif tri=="periodAsc":
        liste.sort(key=lambda x:x["Annee"]+x["Mois"])
    elif tri=="periodDesc":
        liste.sort(key=lambda x:x["Annee"]+x["Mois"],reverse=True)
    elif tri=="rankAsc":
        liste.sort(key=lambda x:x["Rank"])
    elif tri=="random":
        if liste!=[]:
            liste=choice(liste)
        else:
            liste=None

    return liste

def getTablePeriodsInter(curseur,option,id,obj,period,column,tri):
    liste=[]

    if period == "M":
        liste = curseur.execute(f"SELECT User, {column}, SUM(Count) AS Final, Mois, Annee, RANK() OVER (partition by {column}, Mois, Annee ORDER BY SUM(Count) DESC) AS 'Rank' FROM {option}_ranks WHERE {column} = {obj} GROUP BY User, Mois, Annee").fetchall()
    else:
        liste = curseur.execute(f"SELECT User, {column}, SUM(Count) AS Final, Annee, RANK() OVER (partition by {column}, Annee ORDER BY SUM(Count) DESC) AS 'Rank' FROM {option}_ranks WHERE {column} = {obj} GROUP BY User, Annee").fetchall()
        for i in liste:
            i["Mois"] = "TO"

    liste = list(filter(lambda x:x[column] == id, liste))
    
    if tri=="countDesc":
        liste.sort(key=lambda x:x["Final"],reverse=True)
    elif tri=="periodAsc":
        liste.sort(key=lambda x:x["Annee"]+x["Mois"])
    elif tri=="periodDesc":
        liste.sort(key=lambda x:x["Annee"]+x["Mois"],reverse=True)
    elif tri=="rankAsc":
        liste.sort(key=lambda x:x["Rank"])
    elif tri=="random":
        if liste!=[]:
            liste=choice(liste)
        else:
            liste=None

    return liste

def getTablePerso(curseur,option,id,mois,annee,column):
    if mois != "None":
        liste = curseur.execute(f"SELECT User, {column}, SUM(Count) AS Final, Mois, Annee, RANK() OVER (partition by {column}, Mois, Annee ORDER BY SUM(Count) DESC) AS 'Rank' FROM {option}_ranks WHERE Mois='{mois}' AND Annee='{annee}' GROUP BY Salon, User").fetchall()
    elif annee != "None":
        liste = curseur.execute(f"SELECT User, {column}, SUM(Count) AS Final, Annee, RANK() OVER (partition by {column}, Annee ORDER BY SUM(Count) DESC) AS 'Rank' FROM {option}_ranks WHERE Annee='{annee}' GROUP BY Salon, User").fetchall()
    else:
        liste = curseur.execute(f"SELECT User, {column}, SUM(Count) AS Final, RANK() OVER (partition by {column} ORDER BY SUM(Count) DESC) AS 'Rank' FROM {option}_ranks GROUP BY Salon, User").fetchall()

    return list(filter(lambda x:x[column] == id, liste))
    

def getTableRanks(curseur:CustomCursor,option:str,mois:str,annee:str,column:str,obj:int,dateMax=300000) -> list:
    if obj == None:
        strObj = ""
    else:
        strObj = "AND Salon={0}".format(obj)

    if mois != "None":
        return curseur.execute("SELECT {0}, SUM(Count) AS Final, RANK() OVER (ORDER BY SUM(Count) DESC) AS 'Rank' FROM {1}_ranks WHERE Mois='{2}' AND Annee='{3}' AND DateID<{4} {5} GROUP BY {0}".format(column,option,mois,annee,dateMax,strObj)).fetchall()
    elif annee != "None":
        return curseur.execute("SELECT {0}, SUM(Count) AS Final, RANK() OVER (ORDER BY SUM(Count) DESC) AS 'Rank' FROM {1}_ranks WHERE Annee='{2}' AND DateID<{3} {4} GROUP BY {0}".format(column,option,annee,dateMax,strObj)).fetchall()
    else:
        return curseur.execute("SELECT {0}, SUM(Count) AS Final, RANK() OVER (ORDER BY SUM(Count) DESC) AS 'Rank' FROM {1}_ranks WHERE DateID<{2} {3} GROUP BY {0}".format(column,option,dateMax,strObj)).fetchall()

def getTableRanksJeux(curseur:CustomCursor,option:str,mois:str,annee:str,guild=None,dateMax=300000):
    if guild == None:
        strObj = ""
    else:
        strObj = "AND Guild={0}".format(guild)

    if mois != "None":
        return curseur.execute("SELECT User, SUM(Count) AS Final, SUM(W) AS WFinal, SUM(L) AS LFinal, RANK() OVER (ORDER BY SUM(Count) DESC) AS 'Rank' FROM {0}_ranks WHERE Mois='{1}' AND Annee='{2}' AND DateID<{3} {4} GROUP BY User".format(option,mois,annee,dateMax,strObj)).fetchall()
    elif annee != "None":
        return curseur.execute("SELECT User, SUM(Count) AS Final, RANK() OVER (ORDER BY SUM(Count) DESC) AS 'Rank' FROM {0}_ranks WHERE Annee='{1}' AND DateID<{2} {3} GROUP BY User".format(option,annee,dateMax,strObj)).fetchall()
    else:
        return curseur.execute("SELECT User, SUM(Count) AS Final, RANK() OVER (ORDER BY SUM(Count) DESC) AS 'Rank' FROM {0}_ranks WHERE DateID<{1} {2} GROUP BY User".format(option,dateMax,strObj)).fetchall()
