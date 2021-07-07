import sqlite3
import os

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def connectSQL(guild,db,option,mois,annee):
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
    elif option=="Trivial":
        pathDir="SQL/OT/Trivial"
        path="SQL/OT/Trivial/{0}.db".format(db)
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



"""connexionCMD,curseurCMD=connectSQL(ctx.guild.id,"Commandes""Guild",None,None)
connexion,curseur=connectSQL(ctx.guild.id,option,"Stats",tableauMois[mois],annee)"""