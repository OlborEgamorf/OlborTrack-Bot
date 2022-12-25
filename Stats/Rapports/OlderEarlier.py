tableauMois={"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre","TO":"TOTAL","1":"janvier","2":"février","3":"mars","4":"avril","5":"mai","6":"juin","7":"juillet","8":"aout","9":"septembre","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12"}

def hierMAG(date,period,curseur):
    if period=="mois":
        hier=getOlderMois(tableauMois[date[0]],date[1],curseur)
    elif period=="annee":
        hier=getOlderAnnee(date[1],curseur)
    elif period=="global":
        hier=None
    return hier

def getOlderMois(mois,annee,curseur):
    etat=curseur.execute("SELECT Mois,Annee FROM firstM WHERE DateID < {0}{1} ORDER BY DateID DESC".format(annee,mois)).fetchone()
    if etat==None:
        return None
    return tableauMois[etat["Mois"]],etat["Annee"]

def getEarlierMois(mois,annee,curseur):
    etat=curseur.execute("SELECT Mois,Annee FROM firstM WHERE DateID > {0}{1} ORDER BY DateID ASC".format(annee,mois)).fetchone()
    if etat==None:
        return None
    return tableauMois[etat["Mois"]],etat["Annee"]

def getOlderAnnee(annee,curseur):
    etat=curseur.execute("SELECT Mois,Annee FROM firstA WHERE DateID < {0} ORDER BY DateID DESC".format(annee)).fetchone()
    if etat==None:
        return None
    return "to",etat["Annee"]

def getEarlierAnnee(annee,curseur):
    etat=curseur.execute("SELECT Mois,Annee FROM firstA WHERE DateID > {0} ORDER BY DateID ASC".format(annee)).fetchone()
    if etat==None:
        return None
    return "to",etat["Annee"]