from Stats.SQL.ConnectSQL import connectSQL
from Stats.GetData.Outils import dichotomieTable
from Stats.GetData.Ecriture import ecritureSQL

def agregatorMoy(times,tableA,tableM,guild):
    if tableA==[] or tableM==[]:
        return
    connexion,curseur=connectSQL(guild.id,"Moyennes","Stats","GL","")
    for i in times:
        exe=dichotomieTable(tableM,i["ID"])
        if exe[0]==True:
            moyH,moyJ,moyM=[],[],[]
            plageA,plageM,plageJ=[],[],[]
            ecritureSQL("timeHeure{0}".format(i["ID"]),i["Plages"],curseur,8)
            for j in tableM[exe[1]].table:
                count=0
                plage=[]
                for z in i["Plages"]:
                    if z.startswith("{0}{1}".format(j["Annee"],j["Mois"])):
                        count+=1
                        if z[0:6] not in plage:
                            plage.append(z[0:6])
                        if z[0:4] not in plageM:
                            plageM.append(z[0:4])
                        if z[0:2] not in plageA:
                            plageA.append(z[0:2])
                plageJ+=plage.copy()
                moyH.append({"ID":i["ID"],"Type":"Heure","Mois":j["Mois"],"Annee":j["Annee"],"Nombre":count,"Count":j["Count"],"Moyenne":j["Count"]/count})
                moyJ.append({"ID":i["ID"],"Type":"Jour","Mois":j["Mois"],"Annee":j["Annee"],"Nombre":len(plage),"Count":j["Count"],"Moyenne":j["Count"]/len(plage)})
            ecritureSQL("timeJour{0}".format(i["ID"]),plageJ,curseur,8)
            ecritureSQL("timeMois{0}".format(i["ID"]),plageM,curseur,8)
            ecritureSQL("timeAnnee{0}".format(i["ID"]),plageA,curseur,8)
            ecritureSQL("moyHeure{0}".format(i["ID"]),moyH,curseur,9)
            ecritureSQL("moyJour{0}".format(i["ID"]),moyJ,curseur,9)
        exe=dichotomieTable(tableA,i["ID"])
        if exe[0]==True:
            for j in tableA[exe[1]].table:
                if j["Annee"]=="GL":
                    ecritureSQL("moyAnnee{0}".format(i["ID"]),[{"ID":i["ID"],"Type":"Annee","Mois":"TO","Annee":"GL","Nombre":len(plageA),"Count":j["Count"],"Moyenne":j["Count"]/len(plageA)}],curseur,9)
                else:
                    count=0
                    for z in plageM:
                        if z[0:2]==j["Annee"]:
                            count+=1
                    moyM.append({"ID":i["ID"],"Type":"Mois","Mois":"TO","Annee":j["Annee"],"Nombre":count,"Count":j["Count"],"Moyenne":j["Count"]/count})
            ecritureSQL("moyMois{0}".format(i["ID"]),moyM,curseur,9)
    connexion.commit()
    return