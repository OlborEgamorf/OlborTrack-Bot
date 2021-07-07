from Stats.GetData.Outils import dichotomieTable, triIDTable
from Stats.GetData.Objets import Table
from Stats.GetData.Compteurs import compteurGD28

def creatorServ(listeServ,j,id,*idcreate):
    exe=dichotomieTable(listeServ,int(id))
    if exe[0]==True:
        listeServ[exe[1]].table.append({"Rank":j["Rank"],"ID":j["ID"],"Mois":j["Mois"],"Annee":j["Annee"],"Count":j["Count"]})
    else:
        newTable=Table("mois","Serv","Serv",idcreate)
        newTable.table.append({"Rank":j["Rank"],"ID":j["ID"],"Mois":j["Mois"],"Annee":j["Annee"],"Count":j["Count"]})
        listeServ.append(newTable)
        listeServ.sort(key=triIDTable)
    return listeServ

def primeAll(liste,id,jour,mois,annee,count):
    exe=dichotomieTable(liste,int(str(annee)+str(mois)+str(jour)))
    if exe[0]==True:
        compteurGD28(liste[exe[1]].table,"ID",count,id,0,0,mois,annee,"mois")
    else:
        newTable=Table("emotesM",mois,annee,annee,mois,jour)
        compteurGD28(newTable.table,"ID",count,id,0,0,mois,annee,"mois")
        liste.append(newTable)
        liste.sort(key=triIDTable)