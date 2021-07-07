import sqlite3

import discord
from Core.Fonctions.DichoTri import dichotomieID, nombre, triID
from Core.Fonctions.RankingClassic import rankingClassic

dictTriArg={"countAsc":"Count","rankAsc":"Rank","countDesc":"Count","rankDesc":"Rank","dateAsc":"DateID","dateDesc":"DateID","periodAsc":"None","periodDesc":"None","moyDesc":"Moyenne","nombreDesc":"Nombre"}
dictTriSens={"countAsc":"ASC","rankAsc":"ASC","countDesc":"DESC","rankDesc":"DESC","dateAsc":"ASC","dateDesc":"DESC","periodAsc":"None","periodDesc":"None","moyDesc":"DESC","nombreDesc":"DESC"}

def getTableDay(curseur:sqlite3.Cursor,mois:str,annee:str,tri:str) -> list:
    """Permet d'extraire une liste des jours d'activité selon les critères de période que l'on veut.
    Entrées : 
        curseur : curseur pour accéder à la base de données
        mois : mois de la période voulue
        annee : année de la période voulue
        tri : comment la liste doit être triée
    Sortie :
        la liste qui répond à nos critères, renvoyée par la requête SQL"""
    if mois=="glob":
        return curseur.execute("SELECT * FROM dayRank ORDER BY {0} {1}".format(dictTriArg[tri],dictTriSens[tri])).fetchall()
    elif mois=="to":
        return curseur.execute("SELECT * FROM dayRank WHERE Annee={0} ORDER BY {1} {2}".format(annee,dictTriArg[tri],dictTriSens[tri])).fetchall()
    else:
        return curseur.execute("SELECT * FROM dayRank WHERE Mois={0} AND Annee={1} ORDER BY {2} {3}".format(mois,annee,dictTriArg[tri],dictTriSens[tri])).fetchall()

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
