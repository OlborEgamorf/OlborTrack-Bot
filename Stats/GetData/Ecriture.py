typeCreate={1:"(Rank INT, ID BIGINT PRIMARY KEY, Mois TEXT, Annee TEXT, Count INT, Evol INT)",2:"(Rank INT, ID BIGINT PRIMARY KEY, IDComp BIGINT, Mois TEXT, Annee TEXT, Count INT)",3:"(Rank INT, ID INT PRIMARY KEY, Count INT)",4:"(Rank INT, ID BIGINT, Jour TEXT, Mois TEXT, Annee TEXT, DateID TEXT, Count INT, Evol INT, PRIMARY KEY(Jour,Mois,Annee))",5:"(Rank INT, ID BIGINT, Mois TEXT, Annee TEXT, Count INT,PRIMARY KEY(Mois,Annee))",6:"(Rank INT, ID BIGINT PRIMARY KEY, IDComp BIGINT, Mois TEXT, Annee TEXT, Count INT)",7:"(Rank INT, Mois TEXT, Annee TEXT, Count INT, PRIMARY KEY(Mois,Annee))",8:"(ID INT PRIMARY KEY)",9:"(ID BIGINT, Type TEXT, Mois TEXT, Annee TEXT, Nombre INT, Count INT, Moyenne INT, PRIMARY KEY(Mois,Annee))",10:"(Rank INT, ID INT PRIMARY KEY, Jour TEXT, Mois TEXT, Annee TEXT, Count INT)",11:"(Rank INT, ID BIGINT, Jour TEXT, Mois TEXT, Annee TEXT, DateID INT, Count INT, Type TEXT, PRIMARY KEY(Jour,Mois,Annee,ID,Type))",12:"(Rank INT, ID BIGINT, IDComp BIGINT, Jour TEXT, Mois TEXT, Annee TEXT, DateID INT, Count INT, Type TEXT, PRIMARY KEY(Jour,Mois,Annee,ID,Type,IDComp))",13:"(Rank INT, ID BIGINT, Jour TEXT, Mois TEXT, Annee TEXT, DateID INT, Periode TEXT, Count INT, Evol INT, Type TEXT, PRIMARY KEY(Jour,Mois,Annee,ID,Type,Periode))"}
typeMany={1:"(?,?,?,?,?,?)",2:"(?,?,?,?,?,?)",3:"(?,?,?)",4:"(?,?,?,?,?,?,?,?)",5:"(?,?,?,?,?)",6:"(?,?,?,?,?,?)",7:"(?,?,?,?)",8:"(?)",9:"(?,?,?,?,?,?,?)",10:"(?,?,?,?,?,?)",11:"(?,?,?,?,?,?,?,?)",12:"(?,?,?,?,?,?,?,?,?)",13:"(?,?,?,?,?,?,?,?,?,?)"}

def ecritureSQL(table,liste,curseur,num):
    curseur.execute("DROP TABLE IF EXISTS {0}".format(table))
    curseur.execute("CREATE TABLE IF NOT EXISTS {0} {1}".format(table,typeCreate[num]))
    if type(liste[0])==dict:
        many=[tuple(i.values()) for i in liste]
    else:
        many=[(i,) for i in liste]
    curseur.executemany("INSERT INTO {0} VALUES {1}".format(table,typeMany[num]),many)

def ecritureSQLRapport(obj,liste,curseur,jour,mois,annee,option):
    if obj=="":
        table,num="ranks",11
        stop=len(liste)
    elif obj in ("Mois","Annee","Global"):
        table,num="archives",13
        liste.sort(key=lambda x:x["Count"],reverse=True)
        stop=10 if len(liste)>10 else len(liste)
    else:
        table,num="objs",12
        stop=len(liste)
    curseur.execute("CREATE TABLE IF NOT EXISTS {0} {1}".format(table,typeCreate[num]))
    many=[]
    for i in range(stop):
        if table=="ranks":
            many.append((liste[i]["Rank"],liste[i]["ID"],jour,mois,annee,int(annee+mois+jour),liste[i]["Count"],option))
        elif table=="archives":
            many.append((liste[i]["Rank"],liste[i]["ID"],jour,mois,annee,int(annee+mois+jour),obj,liste[i]["Count"],liste[i]["Evol"],option))
        else:
            many.append((liste[i]["Rank"],liste[i]["ID"],obj,jour,mois,annee,int(annee+mois+jour),liste[i]["Count"],option))
    curseur.executemany("INSERT INTO {0} VALUES {1}".format(table,typeMany[num]),many)
    if table=="archives":
        liste.sort(key=lambda x:x["ID"])