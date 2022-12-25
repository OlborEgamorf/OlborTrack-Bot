import sqlite3
import mysql.connector


def connectSQL(guild):
    try:
        cnx = mysql.connector.connect(user='root', password='root',
                                host='localhost',
                                database="guild_"+str(guild),autocommit=False)
        cursor = CustomCursor(cnx)
    except:
        cnx = mysql.connector.connect(user='root', password='root',
                                host='localhost')
        cursor = CustomCursor(cnx)
        cursor.execute("CREATE DATABASE guild_{0}".format(guild))
        cnx.commit()
        cnx,cursor=connectSQL(guild)
    return cnx, cursor


class MySQLResponse():
    def __init__(self,cursor):
        keywords=cursor.column_names
        liste=[]
        try:
            for i in cursor:
                temp=list(map(lambda x:x, i))
                liste.append({keywords[i]:temp[i] for i in range(len(keywords))})
        except:
            pass
        self.fetch=liste
    
    def fetchone(self):
        if len(self.fetch)==0:
            return None
        return self.fetch[0]
    
    def fetchall(self):
        return self.fetch


class CustomCursor(mysql.connector.cursor_cext.CMySQLCursorBuffered):
    def __init__(self,connection):
        super().__init__(connection)

    def execute(self,operation) -> MySQLResponse:
        super().execute(operation)
        return MySQLResponse(self)

import os
def connectSQLOLD(guild,db,option,mois,annee):
    if option=="Guild":
        pathDir="SQL/{0}/Guild".format(guild)
        path="SQL/{0}/Guild/{1}.db".format(guild,db)
    elif db in ("Voice","Voicechan"):
        if mois in ("GL","glob") or annee in ("GL","glob"):
            pathDir="SQL/{0}/Voice/GL".format(guild)
            path="SQL/{0}/Voice/GL/{1}.db".format(guild,db)
        else:
            pathDir="SQL/{0}/Voice/{1}/{2}".format(guild,annee,mois.upper())
            path="SQL/{0}/Voice/{1}/{2}/{3}.db".format(guild,annee,mois.upper(),db)
    elif option=="Jeux":
        if mois in ("GL","glob") or annee in ("GL","glob"):
            pathDir="SQL/{0}/Jeux/GL".format(guild)
            path="SQL/{0}/Jeux/GL/{1}.db".format(guild,db)
        else:
            pathDir="SQL/{0}/Jeux/{1}/{2}".format(guild,annee,mois.upper())
            path="SQL/{0}/Jeux/{1}/{2}/{3}.db".format(guild,annee,mois.upper(),db)
    elif option=="Focus":
        if mois in ("GL","glob") or annee in ("GL","glob"):
            pathDir="SQL/Focus/{0}/GL".format(guild)
            path="SQL/Focus/{0}/GL/{1}.db".format(guild,db)
        else:
            pathDir="SQL/Focus/{0}/{1}/{2}".format(guild,annee,mois.upper())
            path="SQL/Focus/{0}/{1}/{2}/{3}.db".format(guild,annee,mois.upper(),db)
    elif option in ("Trivial","Titres"):
        pathDir="SQL/OT/{0}".format(option)
        path="SQL/OT/{0}/{1}.db".format(option,db)
    elif mois in ("GL","glob") or annee in ("GL","glob"):
        pathDir="SQL/{0}/GL".format(guild)
        path="SQL/{0}/GL/{1}.db".format(guild,db)
    else:
        pathDir="SQL/{0}/{1}/{2}".format(guild,annee,mois.upper())
        path="SQL/{0}/{1}/{2}/{3}.db".format(guild,annee,mois.upper(),db)
    
    if not os.path.exists(pathDir):
        os.makedirs(pathDir)
    connexion = sqlite3.connect(path)

    connexion.row_factory = dict_factory
    curseur = connexion.cursor()
    return connexion,curseur

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

"""connexionCMD,curseurCMD=connectSQL(ctx.guild.id,"Commandes""Guild",None,None)
connexion,curseur=connectSQL(ctx.guild.id,option,"Stats",tableauMois[mois],annee)"""