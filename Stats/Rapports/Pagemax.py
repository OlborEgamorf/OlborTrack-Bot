tableauMois={"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre","TO":"TOTAL","1":"janvier","2":"février","3":"mars","4":"avril","5":"mai","6":"juin","7":"juillet","8":"aout","9":"septembre","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","to":"TO","glob":"GL"}

def pagemaxHome(curseur,mois,annee,period):
    listeOptions=[]
    if period=="mois":
        table=curseur.execute("SELECT DISTINCT Type FROM ranks WHERE Mois='{0}' AND Annee='{1}' ORDER BY Type ASC".format(tableauMois[mois],annee)).fetchall()
    elif period=="annee":
        table=curseur.execute("SELECT DISTINCT Type FROM ranks WHERE Annee='{0}' ORDER BY Type ASC".format(annee)).fetchall()
    else:
        table=curseur.execute("SELECT DISTINCT Type FROM ranks ORDER BY Type ASC").fetchall()
    for i in table:
        if i["Type"] not in ("Divers","Mots"):
            listeOptions.append(i["Type"])
    pagemax=len(listeOptions)+2
    return pagemax,listeOptions

def pagemaxSpeJour(curseur,jour,mois,annee,option):
    nb=len(curseur.execute("SELECT DISTINCT IDComp FROM objs WHERE Jour='{0}' AND Mois='{1}' AND Annee='{2}' AND Type='{3}'".format(jour,mois,annee,option)).fetchall())
    if nb%5==0:
        nb=nb//5
    else:
        nb=nb//5+1
    pagemax=nb if nb<5 else 4
    pagemax+=4
    return pagemax


def pagemaxSpeMois(curseur,mois,annee):
    nb=curseur.execute("SELECT COUNT() AS Nombre FROM {0}{1}".format(mois,annee)).fetchone()["Nombre"]
    if nb%5==0:
        nb=nb//5
    else:
        nb=nb//5+1
    pagemax=nb if nb<5 else 4
    pagemax+=4
    return pagemax