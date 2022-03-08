from Core.Fonctions.DichoTri import dichotomieID
from Core.Fonctions.RankingClassic import rankingClassic
from Stats.Graphiques.Evol import getNomColor
from Stats.SQL.ConnectSQL import connectSQL

tableauSiom={"janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","TOTAL":"TO",":":":","00":"00","01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre"}

def createEvol(ctx,bot,ligne,option):
    listeMois=[]
    connexion,curseur=connectSQL(ctx.guild.id,"Rapports","Stats","GL","")
    dates=curseur.execute("SELECT DISTINCT Jour FROM ranks WHERE Mois='{0}' AND Annee='{1}' AND Type='{2}' ORDER BY Jour ASC".format(tableauSiom[ligne["Args1"]],ligne["Args2"],option)).fetchall()
    for i in dates:
        table=curseur.execute("SELECT * FROM ranks WHERE Mois='{0}' AND Annee='{1}' AND Type='{2}' AND Jour='{3}' ORDER BY Rank ASC".format(tableauSiom[ligne["Args1"]],ligne["Args2"],option,i["Jour"])).fetchall()
        listeMois.append(table.copy())
    return listeMois

def createDict(listeMois,client,ctx,option,guildOT):
    dictGraph={}
    listeAll=[]
    listeRank=[]
    listeNC=[]
    
    for i in range(len(listeMois)):
        if len(listeMois[i])>15:
            borne=15
        else:
            borne=len(listeMois[i])
        for h in range(borne):
            if option in ("Messages","Mots","Voice"):
                print(listeMois[i][h]["ID"])
                if guildOT.users[listeMois[i][h]["ID"]]["Hide"]:
                    print("oui")
                    continue
            elif option in ("Salons","Voicechan"):
                if guildOT.chan[listeMois[i][h]["ID"]]["Hide"]:
                    continue
            if listeMois[i][h]["ID"] not in listeAll:
                listeAll.append(listeMois[i][h]["ID"])
    for i in listeAll:
        listeNC.append(getNomColor(ctx,client,option,i))
    ranks=16 if len(listeAll)>15 else len(listeAll)+1
    for i in range(len(listeMois)):
        listeMois[i].sort(key=lambda x:x["ID"])
        if i==0:
            listeRank=listeMois[0].copy()
            for h in range(len(listeAll)):
                exe=dichotomieID(listeMois[i],listeAll[h],"ID")
                nom,color=listeNC[h]
                for j in range(30):
                    if j not in dictGraph:
                        dictGraph[j]=[]
                    if exe[0]==True:
                        dictGraph[j].append({"x":listeMois[i][exe[1]]["Rank"],"y":float(int(listeMois[i][exe[1]]["Count"]/30*(j+1))),"color":color,"name":nom,"date":listeRank[0]["DateID"]})
                    else:
                        dictGraph[j].append({"x":16,"y":0,"color":color,"name":nom})
        else:
            listeOld=[]
            for h in listeRank:
                listeOld.append(h.copy())
            listeRank.sort(key=lambda x:x["ID"])
            for h in listeMois[i]:
                exe=dichotomieID(listeRank,h["ID"],"ID")
                if exe[0]==True:
                    listeRank[exe[1]]["Count"]+=h["Count"]
                else:
                    listeRank.append(h)
                    listeRank.sort(key=lambda x:x["ID"])
            rankingClassic(listeRank)
            listeRank.sort(key=lambda x:x["ID"])

            for h in range(len(listeAll)):
                exeB=dichotomieID(listeOld,listeAll[h],"ID")
                exeA=dichotomieID(listeRank,listeAll[h],"ID")
                nom,color=listeNC[h]
                for j in range(30):
                    if i*30+j not in dictGraph:
                        dictGraph[i*30+j]=[]
                    if exeA[0]==True:
                        if listeRank[exeA[1]]["Rank"]>15 and exeB[0]==False:
                            dictGraph[i*30+j].append({"x":ranks,"y":float(int(listeRank[exeA[1]]["Count"]/30*(30-j))),"color":color,"name":nom})
                        elif exeB[0]==True:
                            dictGraph[i*30+j].append({"x":float(listeOld[exeB[1]]["Rank"]+(listeRank[exeA[1]]["Rank"]-listeOld[exeB[1]]["Rank"])/30*(j+1)),"y":float(listeOld[exeB[1]]["Count"]+(listeRank[exeA[1]]["Count"]-listeOld[exeB[1]]["Count"])/30*(j+1)),"color":color,"name":nom})
                        else:
                            dictGraph[i*30+j].append({"x":float(16+(listeRank[exeA[1]]["Rank"]-16)/30*(j+1)),"y":float(int(listeRank[exeA[1]]["Count"])/30*(j+1)),"color":color,"name":nom})
                    else: 
                        dictGraph[i*30+j].append({"x":ranks,"y":0,"color":color,"name":nom})
                    if h==0 and j==0:
                        dictGraph[i*30+j][h]["date"]=listeMois[i][0]["DateID"]
    return dictGraph
