import sqlite3

import discord
from Core.Fonctions.DichoTri import dichotomieID, nombre, triID
from Core.Fonctions.RankingClassic import rankingClassic
from Stats.SQL.ConnectSQL import connectSQL

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

def getTableRoles(curseur:sqlite3.Cursor,guild:discord.Guild,nom:str,tri:str) -> list:
    """Permet d'obtenir le classement des rôles pour une table donnée
    Entrées :
        curseur : curseur pour accéder à la base de données
        guild : le serveur d'où vient la commande
        nom : le nom de la table
        tri : comment la liste doit être triée 
    Sortie :
        tableRole : le classement des rôles"""
    table=curseur.execute("SELECT * FROM {0}".format(nom)).fetchall()
    tableRole=[]
    for i in table:
        user=guild.get_member(i["ID"])
        if user!=None:
            for j in user.roles:
                if j.id==guild.id:
                    continue
                exe=dichotomieID(tableRole,j.id,"ID")
                if exe[0]==True:
                    tableRole[exe[1]]["Count"]+=i["Count"]
                else:
                    tableRole.append({"Rank":0,"ID":j.id,"Count":i["Count"],"Mois":i["Mois"],"Annee":i["Annee"]})
                    tableRole.sort(key=triID)
    rankingClassic(tableRole)
    if tri=="countAsc":
        tableRole.sort(key=nombre)
    return tableRole

def getTableRolesMem(curseur:sqlite3.Cursor,guild:discord.Guild,id:int,nom:str,tri:str) -> list:
    """Permet d'obtenir le classement des membres ayant un certain rôles pour une table donnée
    Entrées :
        curseur : curseur pour accéder à la base de données
        guild : le serveur d'où vient la commande
        id : l'ID du rôle
        nom : le nom de la table
        tri : comment la liste doit être triée 
    Sortie :
        newTable : le classement des membres ayant le rôle"""
    table=curseur.execute("SELECT * FROM {0}".format(nom)).fetchall()
    newTable=[]
    membres=[]
    role=guild.get_role(id)
    for i in role.members:
        membres.append(i.id)
    for i in table:
        if i["ID"] in membres:
            newTable.append(i)
    if tri=="countDesc":
        newTable.sort(key=nombre,reverse=True)
    else:
        newTable.sort(key=nombre)
    return newTable

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

def getTablePerso(guild,option,id,idobj,period,tri):
    liste=[]
    connectionF,curseurF=connectSQL(guild,option,"Stats","GL","")
    for i in curseurF.execute("SELECT Mois,Annee FROM first{0}".format(period)).fetchall():
        try:
            connection,curseur=connectSQL(guild,option,"Stats",i["Mois"],i["Annee"])
            if not idobj:
                stat=curseur.execute("SELECT Rank,Count,Mois,Annee,ID FROM {0}{1} WHERE ID={2}".format(tableauMois[i["Mois"]],i["Annee"],id)).fetchone()
            else:
                stat=curseur.execute("SELECT Rank,Count,Mois,Annee,ID FROM perso{0}{1}{2} WHERE ID={3}".format(i["Mois"],i["Annee"],id,idobj)).fetchone()
            if stat!=None:
                liste.append(stat)
        except:
            pass
    if tri=="countDesc":
        liste.sort(key=lambda x:x["Count"],reverse=True)
    elif tri=="periodAsc":
        liste.sort(key=lambda x:x["Annee"]+x["Mois"])
    elif tri=="periodDesc":
        liste.sort(key=lambda x:x["Annee"]+x["Mois"],reverse=True)
    elif tri=="rankAsc":
        liste.sort(key=lambda x:x["Rank"])
    return liste
