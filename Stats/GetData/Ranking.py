from Core.Fonctions.DichoTri import nombre
from Stats.GetData.Outils import dichotomieTable, triIDTable
from Stats.GetData.Objets import Table, UserEvol

def rankingEvolGD28(table,option,annee,mois,jour,listeUser):
    countTemp=0
    rankTemp=0
    for i in range(len(table)):
        if table[i]["Count"]==countTemp:
            table[i]["Rank"]=rankTemp
        else:
            countTemp=table[i]["Count"]
            rankTemp=i+1
            table[i]["Rank"]=rankTemp
        if table[i]["Rank"]<=150:
            exe=dichotomieTable(listeUser,int(table[i]["ID"]))
            if exe[0]==True:
                exeF=dichotomieTable(listeUser[exe[1]].mois,int(option))
                if exeF[0]==True:
                    evolGD28(listeUser[exe[1]].mois[exeF[1]].table,table,i,annee,mois,jour)
                else:
                    newTable=Table("evolMois",table[i]["Mois"],table[i]["Annee"],option)
                    evolGD28(newTable.table,table,i,annee,mois,jour)
                    listeUser[exe[1]].mois.append(newTable)
                    listeUser[exe[1]].mois.sort(key=triIDTable)
            else:
                newUser=UserEvol(table[i]["ID"])
                newTable=Table("evolMois",table[i]["Mois"],table[i]["Annee"],option)
                evolGD28(newTable.table,table,i,annee,mois,jour)
                newUser.mois.append(newTable)
                listeUser.append(newUser)
                listeUser.sort(key=triIDTable)
        else:
            table[i]["Evol"]=0

def evolGD28(tableMove,table,i,annee,mois,jour):
    tableMove.append({"Rank":table[i]["Rank"],"ID":table[i]["ID"],"Jour":jour,"Mois":mois,"Annee":annee,"DateID":"{0}{1}{2}".format(annee,mois,jour),"Count":table[i]["Count"],"Evol":0})
    pos=len(tableMove)-1
    tableMove[pos]["Evol"]=int(tableMove[pos-1]["Rank"])-int(tableMove[pos]["Rank"])
    table[i]["Evol"]=int(tableMove[pos-1]["Rank"])-int(tableMove[pos]["Rank"])
