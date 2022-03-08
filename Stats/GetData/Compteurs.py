from Core.Fonctions.DichoTri import dichotomieID
from Stats.GetData.Ranking import rankingEvolGD28

def comptSortEvol(table,id,mois,annee,option,listeUser,tableBase,comp):
    for j in tableBase:
        if comp=="":
            compteurGD28(table,"ID",j["Count"],j["ID"],0,0,mois,annee,"mois")
        else:
            compteurGD28(table,"ID",j["Count"],j["ID"],comp,0,mois,annee,"chan")
    if comp=="":
        table.sort(key=lambda x:x["Count"],reverse=True)
        rankingEvolGD28(table,option,str(id)[0:2],str(id)[2:4],str(id)[4:6],listeUser)
        table.sort(key=lambda x:x["ID"])

def compteurGD28(table,search,numb,id,id2,id3,mois,annee,option):
    etat=dichotomieID(table,int(id),search)
    add=etat[0]
    place=etat[1]
    if add==True:
        table[place]["Count"]=int(table[place]["Count"])+numb
    else:
        if option=="mois":
            table.append({"Rank":0,"ID":id,"Mois":mois,"Annee":annee,"Count":numb})
        elif option=="day":
            table.append({"Rank":0,"ID":id,"Jour":id2,"Mois":mois,"Annee":annee,"Count":numb})
        elif option=="chan":
            table.append({"Rank":id3,"ID":id,"UserID":id2,"Mois":mois,"Annee":annee,"Count":numb})
    table.sort(key=lambda x:x["ID"])
    return