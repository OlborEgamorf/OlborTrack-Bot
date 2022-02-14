from Stats.GetData.Objets import Table
from Core.Fonctions.RankingClassic import rankingClassic
from Stats.SQL.First import firstSQL
from Stats.GetData.Compteurs import comptSortEvol
from Stats.GetData.Ecriture import ecritureSQL, ecritureSQLRapport
from Stats.GetData.Createurs import creatorServ
from Stats.GetData.Outils import sommeTable
from Core.Fonctions.DichoTri import nombre
from Stats.SQL.ConnectSQL import connectSQL

tableauMois={"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre","TO":"TOTAL","1":"janvier","2":"février","3":"mars","4":"avril","5":"mai","6":"juin","7":"juillet","8":"aout","9":"septembre","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12"}


def agregatorEvol(liste,guild,autho,id,option,dictConnexion,dictCurseur,curRap):
    if liste==[]:
        return dictConnexion, dictCurseur
    listeUser=[]
    listeTempM,listeTempA=Table("mois",liste[0].mois,liste[0].annee,liste[0].annee,liste[0].mois),Table("mois","Total",liste[0].annee,liste[0].annee)
    period="{0}{1}".format(liste[0].mois,liste[0].annee)
    listeM,listeA,listeData=[],[],[]
    listeG=Table("global","TO","GL",guild.id)
    listeTotal=Table("total","Total","GLOBAL",guild.id)
    listePersoA,listePersoM=[],[]
    for i in liste:
        if listeTempM.mois!=i.mois or listeTempM.annee!=i.annee:
            rankingClassic(listeTempM.table)
            listeM.append(listeTempM)
            listeTempM=Table("mois",i.mois,i.annee,i.annee,i.mois)
            period="{0}{1}".format(i.mois,i.annee)
        if listeTempA.annee!=i.annee:
            rankingClassic(listeTempA.table)
            listeA.append(listeTempA)
            listeTempA=Table("mois","to",i.annee,i.annee)
        comptSortEvol(listeTempM.table,i.id,i.mois,i.annee,str(i.id)[0:4],listeUser,i.table,id)
        comptSortEvol(listeTempA.table,i.id,"TO",i.annee,str(i.id)[0:2],listeUser,i.table,id)
        comptSortEvol(listeG.table,i.id,"TO","GL","6969",listeUser,i.table,id)
        if option not in ("Mentions","Mentionne"):
            rankingClassic(i.table)
            ecritureSQLRapport(id,i.table,curRap,str(i.id)[4:6],str(i.id)[2:4],str(i.id)[0:2],option)
            if id=="" and option not in ("Divers","Mots"):
                ecritureSQLRapport("Mois",listeTempM.table,curRap,str(i.id)[4:6],str(i.id)[2:4],str(i.id)[0:2],option)
                ecritureSQLRapport("Annee",listeTempA.table,curRap,str(i.id)[4:6],str(i.id)[2:4],str(i.id)[0:2],option)
                ecritureSQLRapport("Global",listeG.table,curRap,str(i.id)[4:6],str(i.id)[2:4],str(i.id)[0:2],option)

    rankingClassic(listeTempM.table)
    rankingClassic(listeTempA.table)
    rankingClassic(listeG.table)
    listeM.append(listeTempM)
    listeA.append(listeTempA)

    for i in listeG.table:
        creatorServ(listePersoA,i,i["ID"],i["ID"])
    for i in listeA:
        for j in i.table:
            creatorServ(listePersoA,j,j["ID"],j["ID"])
    for i in listeM:
        for j in i.table:
            creatorServ(listePersoM,j,j["ID"],j["ID"])
        count=sommeTable(i.table)
        listeTotal.table.append({"Rank":0,"Mois":i.mois,"Annee":i.annee,"Count":count})
        listeData.append({"Mois":i.mois,"Annee":i.annee})
    listeTotal.table=rankingClassic(listeTotal.table)


    if autho==True:
        mode=1 if id=="" else 2
        if "GL" not in dictCurseur:
            dictConnexion["GL"],dictCurseur["GL"]=connectSQL(guild.id,option,"Stats","GL","")
        if not (option in ("Emotes","Reactions") and id!="" and sommeTable(listeG.table)<50):
            ecritureSQL("glob{0}".format(id),listeG.table,dictCurseur["GL"],mode)

        if id!="":
            for j in listeG.table:
                dictCurseur["GL"].execute("CREATE TABLE IF NOT EXISTS persoTOGL{0} (Rank INT, ID BIGINT PRIMARY KEY, IDComp BIGINT, Mois TEXT, Annee TEXT, Count INT)".format(j["ID"]))
                dictCurseur["GL"].execute("INSERT INTO persoTOGL{0} VALUES({1},{2},{3},'{4}','{5}',{6})".format(j["ID"],j["Rank"],id,j["ID"],"TO","GL",j["Count"]))
        
        if id=="":
            for i in listeM:
                firstSQL(dictCurseur["GL"],i.table[0]["ID"],i.table[0]["Count"],(i.mois,i.annee))
            for i in listeA:
                firstSQL(dictCurseur["GL"],i.table[0]["ID"],i.table[0]["Count"],("TO",i.annee))
            firstSQL(dictCurseur["GL"],listeG.table[0]["ID"],listeG.table[0]["Count"],"TO","GL")

        perso=True
        if id!="":
            if option in ("Emotes","Reactions") and dictCurseur["GL"].execute("SELECT Rank FROM glob WHERE ID={0}".format(id)).fetchone()["Rank"]>400:
                perso=False

        for i in listeUser:
            for j in i.mois:
                if j.id==6969:
                    ecritureSQL("evolglob{0}{1}".format(id,i.id),j.table,dictCurseur["GL"],4)

        for i in listeM:
            period="{0}{1}".format(i.mois,i.annee)
            if period not in dictCurseur:
                dictConnexion[period],dictCurseur[period]=connectSQL(guild.id,option,"Stats",i.mois,i.annee)
            if not (option in ("Emotes","Reactions") and id!="" and sommeTable(i.table)<10):
                ecritureSQL("{0}{1}{2}".format(tableauMois[str(i.idcomp[1])],i.idcomp[0],id),i.table,dictCurseur[period],mode)
            if id!="":
                for j in i.table:
                    dictCurseur[period].execute("CREATE TABLE IF NOT EXISTS perso{0}{1}{2} (Rank INT, ID BIGINT PRIMARY KEY, IDComp BIGINT, Mois TEXT, Annee TEXT, Count INT)".format(i.mois,i.annee,j["ID"]))
                    dictCurseur[period].execute("INSERT INTO perso{0}{1}{2} VALUES({3},{4},{5},'{6}','{7}',{8})".format(i.mois,i.annee,j["ID"],j["Rank"],id,j["ID"],i.mois,i.annee,j["Count"]))
            for z in listeUser:
                for j in z.mois:
                    if str(j.id)[2:4]==str(i.mois) and str(j.id)[0:2]==str(i.annee):
                        ecritureSQL("evol{0}{1}{2}{3}".format(tableauMois[str(j.id)[2:4]],str(j.id)[0:2],id,z.id),j.table,dictCurseur[period],4)
        del listeM

        for i in listeA:
            period="{0}{1}".format("TO",i.annee)
            if period not in dictCurseur:
                dictConnexion[period],dictCurseur[period]=connectSQL(guild.id,option,"Stats","TO",i.annee)
            if not (option in ("Emotes","Reactions") and id!="" and sommeTable(i.table)<25):
                ecritureSQL("to{0}{1}".format(i.idcomp[0],id),i.table,dictCurseur[period],mode)
            if id!="":
                for j in i.table:
                    dictCurseur[period].execute("CREATE TABLE IF NOT EXISTS persoTO{0}{1} (Rank INT, ID BIGINT PRIMARY KEY, IDComp BIGINT, Mois TEXT, Annee TEXT, Count INT)".format(i.annee,j["ID"]))
                    dictCurseur[period].execute("INSERT INTO persoTO{0}{1} VALUES({2},{3},{4},'{5}','{6}',{7})".format(i.annee,j["ID"],j["Rank"],id,j["ID"],"TO",i.annee,j["Count"]))
            for z in listeUser:
                for j in z.mois:
                    if str(j.annee)==str(i.annee) and j.mois=="TO":
                        ecritureSQL("evolto{0}{1}{2}".format(j.annee,id,z.id),j.table,dictCurseur[period],4)
        del listeA        

    if option=="Messages":
        return dictConnexion, dictCurseur, listePersoA,listePersoM,listeG
    else:
        del listePersoA,listePersoM,listeG
        return dictConnexion, dictCurseur