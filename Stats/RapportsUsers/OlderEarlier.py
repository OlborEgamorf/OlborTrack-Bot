from Core.Fonctions.GetTable import getTablePerso
from Stats.SQL.ConnectSQL import connectSQL

tableauMois={"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre","TO":"TOTAL","1":"janvier","2":"février","3":"mars","4":"avril","5":"mai","6":"juin","7":"juillet","8":"aout","9":"septembre","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12"}

def hierMAG(date,period,guild,option,user):
    if period=="mois":
        hier=getOlderMois(tableauMois[date[0]],date[1],guild,option,user)
    elif period=="annee":
        hier=getOlderAnnee(date[1],guild,option,user)
    elif period=="global":
        hier=None
    return hier

def getOlderJour(jour,mois,annee,curseur,option,user):
    etat=curseur.execute("SELECT Jour,Mois,Annee FROM objs WHERE DateID < {0}{1}{2} AND Type='{3}' AND ID={4} ORDER BY DateID DESC".format(annee,mois,jour,option,user)).fetchone()
    if etat==None:
        return None
    return etat["Jour"],etat["Mois"],etat["Annee"]

def getEarlierJour(jour,mois,annee,curseur,option,user):
    etat=curseur.execute("SELECT Jour,Mois,Annee FROM objs WHERE DateID > {0}{1}{2} AND Type='{3}' AND ID={4} ORDER BY DateID ASC".format(annee,mois,jour,option,user)).fetchone()
    if etat==None:
        return None
    return etat["Jour"],etat["Mois"],etat["Annee"]

def getOlderMois(mois,annee,guild,option,user):
    curseur=connectSQL(guild.id,"Messages","Stats","GL",None)[1]
    etat=curseur.execute("SELECT Mois,Annee, Annee || '' || Mois AS DateID FROM persoM{0} WHERE DateID < '{1}{2}' ORDER BY DateID DESC".format(user,annee,mois)).fetchone()
    if etat==None:
        return None
    return tableauMois[etat["Mois"]],etat["Annee"]

def getEarlierMois(mois,annee,guild,option,user):
    curseur=connectSQL(guild.id,"Messages","Stats","GL",None)[1]
    etat=curseur.execute("SELECT Mois,Annee, Annee || '' || Mois AS DateID FROM persoM{0} WHERE DateID > '{1}{2}' ORDER BY DateID ASC".format(user,annee,mois)).fetchone()
    if etat==None:
        return None
    return tableauMois[etat["Mois"]],etat["Annee"]

def getOlderAnnee(annee,guild,option,user):
    etat=getTablePerso(guild.id,"Messages",user,False,"A","countDesc")
    etat=list(filter(lambda x:x["Annee"]<annee and x["Annee"]!="GL", etat))
    etat.sort(key=lambda x:x["Annee"], reverse=True)
    if etat==[]:
        return None
    return "to",etat[0]["Annee"]

def getEarlierAnnee(annee,guild,option,user):
    etat=getTablePerso(guild.id,"Messages",user,False,"A","countDesc")
    etat=list(filter(lambda x:x["Annee"]>annee and x["Annee"]!="GL", etat))
    etat.sort(key=lambda x:x["Annee"])
    if etat==[]:
        return None
    return "to",etat[0]["Annee"]