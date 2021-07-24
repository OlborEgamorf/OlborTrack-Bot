from matplotlib import pyplot as plt
import pandas as pd
from Stats.SQL.ConnectSQL import connectSQL
from math import inf
from Core.Fonctions.VoiceAxe import voiceAxe
from Core.Fonctions.GraphTheme import setThemeGraph
from Core.Fonctions.GetTable import collapseEvol, getTableDay
from Core.Fonctions.GetNom import getNomGraph

tableauMois={"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre","TO":"TO","1":"janvier","2":"février","3":"mars","4":"avril","5":"mai","6":"juin","7":"juillet","8":"aout","9":"septembre","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","glob":"GL","to":"TO"}
dictTitle={"Messages":"membre","Voice":"membre","Mots":"membres","Salons":"salon","Emotes":"emote","Reactions":"réaction","Voicechan":"salon","Freq":"heure"}
colorOT=(110/256,200/256,250/256,1)

async def graphEvol(ligne,ctx,bot,option,guildOT):
    plt.subplots(figsize=(6.4,4.8))
    listeX,listeY,listeR=[],[],[]
    setThemeGraph(plt)
    mois,annee=ligne["Args1"],ligne["Args2"]
    if ligne["Commande"]=="day":
        connexion,curseur=connectSQL(ctx.guild.id,option,"Stats","GL","")
        table=getTableDay(curseur,mois,annee,"dateAsc")
        for i in table:
            i["Evol"]=0
    else:
        connexion,curseur=connectSQL(ctx.guild.id,option,"Stats",tableauMois[mois],annee)
        table=curseur.execute("SELECT * FROM evol{0}{1}{2} ORDER BY DateID ASC".format(mois,annee,ligne["Args3"])).fetchall()
    collapse=collapseEvol(table)
    dates=[]
    for i in collapse:
        dates.append(i["DateID"])
    listeM=[True for i in range(len(table))]
    for i in range(len(table)):
        listeX.append("{0}/{1}/{2}".format(table[i]["Jour"],table[i]["Mois"],table[i]["Annee"]))
        listeY.append(table[i]["Count"])
        listeR.append(table[i]["Rank"])
        if len(table)>31:
            if table[i]["DateID"] not in dates:
                listeM[i]=False
    
    voiceAxe(option,listeY,plt,"y")
    
    df=pd.DataFrame({"Date": listeX, "Count": listeY})

    if ligne["Commande"]=="evol":
        nom,color=getNomColor(ctx,bot,option,ligne["Args3"])
    else:
        nom,color="Jours d'activité sur le serveur",colorOT
    
    listeTX,listeTY,listeL,listeTR=[],[],[],[]
    for i in range(len(listeM)):
        if listeM[i]==True:
            listeL.append(i)
            listeTX.append(listeX[i])
            listeTY.append(listeY[i])
            listeTR.append(listeR[i])
    
    if ligne["Commande"]=="evol":
        for i in range(len(listeL)):
            plt.text(x=listeL[i], y=listeTY[i], s="{0}e".format(listeTR[i]), size=8)

    plt.xlabel("Date")
    plt.plot("Date", "Count", data=df, linestyle='-', marker='o',color=color,markevery=listeM)
    plt.xticks(listeL,listeTX,rotation=45)
    titreEvol(mois,annee,nom,"")
    plt.tight_layout()
    plt.savefig("Graphs/otGraph")
    plt.clf()
    plt.close()


async def graphEvolAA(ligne,ctx,bot,option,guildOT):
    plt.subplots(figsize=(6.4,4.8))
    listeX,listeY,listeT=[],[],[]
    setThemeGraph(plt)
    mois,annee=ligne["Args1"],ligne["Args2"]
    connexion,curseur=connectSQL(ctx.guild.id,option,"Stats",tableauMois[mois],annee)
    table=curseur.execute("SELECT * FROM evol{0}{1}{2} ORDER BY DateID ASC".format(mois,annee,ligne["Args3"])).fetchall()
    mini=curseur.execute("SELECT MIN(Count) AS Min FROM evol{0}{1}{2} ORDER BY DateID ASC".format(mois,annee,ligne["Args3"])).fetchone()["Min"]

    for i in range(len(table)):
        listeY.append(table[i]["Count"])
        absData(mois,table,i,listeX,listeT)
    
    div=voiceAxe(option,listeY,plt,"y")
    mini=round(mini/div,2)

    df=pd.DataFrame({"Date": listeX, "Count": listeY})

    connexion,curseur=connectSQL(ctx.guild.id,option,"Stats","GL","")
    if ligne["Args1"]=="to":
        tableDemain=curseur.execute("SELECT Mois, Annee FROM persoA{0} WHERE Annee>'{1}' AND Annee<>'GL' ORDER BY Annee ASC".format(ligne["Args3"],annee)).fetchone()
        tableHier=curseur.execute("SELECT Mois, Annee FROM persoA{0} WHERE Annee<'{1}' AND Annee<>'GL' ORDER BY Annee DESC".format(ligne["Args3"],annee)).fetchone()
    else:
        tableDemain=curseur.execute("SELECT Mois, Annee, Annee || '' || Mois AS DateID FROM persoM{0} WHERE DateID>'{1}{2}' ORDER BY DateID ASC".format(ligne["Args3"],annee,tableauMois[mois])).fetchone()
        tableHier=curseur.execute("SELECT Mois, Annee, Annee || '' || Mois AS DateID FROM persoM{0} WHERE DateID<'{1}{2}' ORDER BY DateID DESC".format(ligne["Args3"],annee,tableauMois[mois])).fetchone()

    nom,color=getNomColor(ctx,bot,option,ligne["Args3"])

    if tableDemain!=None:
        listeX2,listeY2=[],[]
        connexion,curseur=connectSQL(ctx.guild.id,option,"Stats",tableDemain["Mois"],tableDemain["Annee"])
        mini=min(mini,round(curseur.execute("SELECT MIN(Count) AS Min FROM evol{0}{1}{2} ORDER BY DateID ASC".format(tableauMois[tableDemain["Mois"]],tableDemain["Annee"],ligne["Args3"])).fetchone()["Min"]/div,2))
        demain=curseur.execute("SELECT * FROM evol{0}{1}{2} ORDER BY DateID ASC".format(tableauMois[tableDemain["Mois"]],tableDemain["Annee"],ligne["Args3"])).fetchall()
        for i in range(len(demain)):
            listeY2.append(round(demain[i]["Count"]/div,2))
            absData(mois,demain,i,listeX2,listeT)
        df2=pd.DataFrame({"Date": listeX2, "Count": listeY2})
    
    if tableHier!=None:
        listeX3,listeY3=[],[]
        connexion,curseur=connectSQL(ctx.guild.id,option,"Stats",tableHier["Mois"],tableHier["Annee"])
        mini=min(mini,round(curseur.execute("SELECT MIN(Count) AS Min FROM evol{0}{1}{2} ORDER BY DateID ASC".format(tableauMois[tableHier["Mois"]],tableHier["Annee"],ligne["Args3"])).fetchone()["Min"]/div,2))
        hier=curseur.execute("SELECT * FROM evol{0}{1}{2} ORDER BY DateID ASC".format(tableauMois[tableHier["Mois"]],tableHier["Annee"],ligne["Args3"])).fetchall()
        for i in range(len(hier)):
            listeY3.append(round(hier[i]["Count"]/div,2))
            absData(mois,hier,i,listeX3,listeT)
        df3=pd.DataFrame({"Date": listeX3, "Count": listeY3})
    
    if div==1:
        mini=int(mini)
    listeT.sort()
    dfDate=setMin(mois,listeT,mini)

    if tableHier!=None:
        plt.plot("Date", "Count", data=df3, linestyle='--', marker='',color="indianred",label="{0} 20{1}".format(tableauMois[tableHier["Mois"]],tableHier["Annee"]))
    plt.plot("Date", "Count", data=df, linestyle='-', marker='',color=color,label="{0} 20{1}".format(mois,annee))
    if tableDemain!=None:
        plt.plot("Date", "Count", data=df2, linestyle='--', marker='',color="mediumpurple",label="{0} 20{1}".format(tableauMois[tableDemain["Mois"]],tableDemain["Annee"]))
    
    titreEvol(mois,annee,nom,"comparée avec périodes avant et après")

    if mois=="to":
        listeDates,listeXD,temp=[],[],0
        for i in range(len(listeT)):
            if listeT[i][0:2]!=temp:
                listeDates.append("{0}/{1}".format(listeT[i][2:4],listeT[i][0:2]))
                listeXD.append(i)
                temp=listeT[i][0:2]
        plt.xticks(listeXD,listeDates,rotation=45)
    
    plt.xlabel("Date")
    plt.tight_layout()
    plt.legend()
    plt.savefig("Graphs/otGraph")
    plt.clf()


async def graphEvolBest(ligne,ctx,bot,option,guildOT):
    plt.subplots(figsize=(6.4,4.8))
    listeX,listeY,listeT=[],[],[]
    setThemeGraph(plt)
    mois,annee=ligne["Args1"],ligne["Args2"]
    connexion,curseur=connectSQL(ctx.guild.id,option,"Stats",tableauMois[mois],annee)
    table=curseur.execute("SELECT * FROM evol{0}{1}{2} ORDER BY DateID ASC".format(mois,annee,ligne["Args3"])).fetchall()
    mini=curseur.execute("SELECT MIN(Count) AS Min FROM evol{0}{1}{2} ORDER BY DateID ASC".format(mois,annee,ligne["Args3"])).fetchone()["Min"]
    for i in range(len(table)):
        listeY.append(table[i]["Count"])
        absData(mois,table,i,listeX,listeT)
    
    div=voiceAxe(option,listeY,plt,"y")
    mini=round(mini/div,2)

    df=pd.DataFrame({"Date": listeX, "Count": listeY})

    connexion,curseur=connectSQL(ctx.guild.id,option,"Stats","GL","")
    if ligne["Args1"]=="to":
        tableMeilleur=curseur.execute("SELECT Mois, Annee FROM persoA{0} WHERE Annee<>'GL' AND Annee<>'{1}' ORDER BY Count DESC".format(ligne["Args3"],annee)).fetchone()
    else:
        tableMeilleur=curseur.execute("SELECT Mois, Annee, Annee || '' || Mois AS DateID FROM persoM{0} WHERE DateID<>'{1}{2}' ORDER BY Count DESC".format(ligne["Args3"],annee,tableauMois[mois])).fetchone()

    nom,color=getNomColor(ctx,bot,option,ligne["Args3"])
    
    if tableMeilleur!=None:
        listeX2,listeY2=[],[]
        connexion,curseur=connectSQL(ctx.guild.id,option,"Stats",tableMeilleur["Mois"],tableMeilleur["Annee"])
        mini=min(mini,round(curseur.execute("SELECT MIN(Count) AS Min FROM evol{0}{1}{2} ORDER BY DateID ASC".format(tableauMois[tableMeilleur["Mois"]],tableMeilleur["Annee"],ligne["Args3"])).fetchone()["Min"]/div,2))
        tableM=curseur.execute("SELECT * FROM evol{0}{1}{2} ORDER BY DateID ASC".format(tableauMois[tableMeilleur["Mois"]],tableMeilleur["Annee"],ligne["Args3"])).fetchall()
        for i in range(len(tableM)):
            listeY2.append(round(tableM[i]["Count"]/div,2))
            absData(mois,tableM,i,listeX2,listeT)
        df2=pd.DataFrame({"Date": listeX2, "Count": listeY2})
    
    if div==1:
        mini=int(mini)

    listeT.sort()
    dfDate=setMin(mois,listeT,mini)
    plt.plot("Date", "Count", data=df, linestyle='-', marker='',color=color,label="{0} 20{1}".format(mois,annee))
    if tableMeilleur!=None:
        plt.plot("Date", "Count", data=df2, linestyle='--', marker='',color="mediumpurple",label="{0} 20{1}".format(tableauMois[tableMeilleur["Mois"]],tableMeilleur["Annee"]))
    
    titreEvol(mois,annee,nom,"comparée avec meilleure période personnelle")

    if mois=="to":
        listeDates,listeXD,temp=[],[],0
        for i in range(len(listeT)):
            if listeT[i][0:2]!=temp:
                listeDates.append("{0}/{1}".format(listeT[i][2:4],listeT[i][0:2]))
                listeXD.append(i)
                temp=listeT[i][0:2]
        plt.xticks(listeXD,listeDates,rotation=45)

    plt.xlabel("Date")
    plt.tight_layout()
    plt.legend()
    plt.savefig("Graphs/otGraph")
    plt.clf()


async def graphEvolAutour(ligne,ctx,bot,option,guildOT):
    plt.subplots(figsize=(6.4,4.8))
    colorsBasic=[colorOT,"green","red","gold"]
    listeX,listeY,listeT=[],[],[]
    setThemeGraph(plt)
    mois,annee=ligne["Args1"],ligne["Args2"]
    connexion,curseur=connectSQL(ctx.guild.id,option,"Stats",tableauMois[mois],annee)
    table=curseur.execute("SELECT * FROM evol{0}{1}{2} ORDER BY DateID ASC".format(mois,annee,ligne["Args3"])).fetchall()
    mini=curseur.execute("SELECT MIN(Count) AS Min FROM evol{0}{1}{2} ORDER BY DateID ASC".format(mois,annee,ligne["Args3"])).fetchone()["Min"]
    rank=table[len(table)-1]["Rank"]

    for i in range(len(table)):
        listeY.append(table[i]["Count"])
        absData(mois,table,i,listeX,listeT)

    div=voiceAxe(option,listeY,plt,"y")
    mini=round(mini/div,2)
    df=pd.DataFrame({"Date": listeX, "Count": listeY})
    tableRank=curseur.execute("SELECT * FROM {0}{1} WHERE Rank>={2} AND Rank<={3} AND ID<>{4}".format(mois,annee,rank-2,rank+2,ligne["Args3"])).fetchall()

    listeXO,listeYO=[[] for i in range(len(tableRank))],[[] for i in range(len(tableRank))]
    for i in range(len(tableRank)):
        evol=curseur.execute("SELECT * FROM evol{0}{1}{2} ORDER BY DateID ASC".format(mois,annee,tableRank[i]["ID"])).fetchall()
        mini=min(mini,round(curseur.execute("SELECT MIN(Count) AS Min FROM evol{0}{1}{2} ORDER BY DateID ASC".format(mois,annee,tableRank[i]["ID"])).fetchone()["Min"]/div,2))
        for j in range(len(evol)):
            listeYO[i].append(round(evol[j]["Count"]/div,2))
            absData(mois,evol,j,listeXO[i],listeT)
    
    if div==1:
        mini=int(mini)
    listeT.sort()
    dfDate=setMin(mois,listeT,mini)
    dictLine={1:"--",2:"-.",3:"."}

    listeColor=[]
    for i in range(len(tableRank)):
        if option in ("Salons","Voicechan"):
            if guildOT.chan[tableRank[i]["ID"]]["Hide"]:
                continue
        elif option in ("Messages","Mots","Voice"):
            if guildOT.users[tableRank[i]["ID"]]["Hide"]:
                continue 
        df2=pd.DataFrame({"Date": listeXO[i], "Count": listeYO[i]})
        user=ctx.guild.get_member(tableRank[i]["ID"])
        if user!=None:
            listeColor.append((user.color.r/256,user.color.g/256,user.color.b/256,1))
            plt.plot("Date", "Count", data=df2, linestyle=dictLine[listeColor.count((user.color.r/256,user.color.g/256,user.color.b/256,1))], marker="", color=(user.color.r/256,user.color.g/256,user.color.b/256,1),label=user.name)
        else:
            try:
                nom=getNomGraph(ctx,bot,option,tableRank[i]["ID"])
            except:
                if option in ("Messages","Mots","Voice"):
                    nom="Ancien membre"
                else:
                    nom="??"
            plt.plot("Date", "Count", data=df2, linestyle='--', marker='',color=colorsBasic[i],label=nom)
    
    nom,color=getNomColor(ctx,bot,option,ligne["Args3"])
    plt.plot("Date", "Count", data=df, linestyle='-', marker='',color=color,label=nom)
    
    titreEvol(mois,annee,nom,"comparée avec {0}s autour".format(dictTitle[option]))

    listeDates,listeXD,temp=[],[],0
    if mois=="to":
        for i in range(len(listeT)):
            if listeT[i][0:2]!=temp:
                listeDates.append("{0}/{1}".format(listeT[i][2:4],listeT[i][0:2]))
                listeXD.append(i)
                temp=listeT[i][0:2]
        plt.xticks(listeXD,listeDates,rotation=45)
    elif mois=="glob":
        for i in range(len(listeT)):
            if listeT[i][0:2]!=temp:
                listeDates.append("{0}/{1}/{2}".format(listeT[i][4:6],listeT[i][2:4],listeT[i][0:2]))
                listeXD.append(i)
                temp=listeT[i][0:2]
        plt.xticks(listeXD,listeDates,rotation=45)

    plt.xlabel("Date")
    plt.tight_layout()
    plt.legend()
    plt.savefig("Graphs/otGraph")
    plt.clf()

async def graphEvolBestUser(ligne,ctx,bot,option,guildOT):
    plt.subplots(figsize=(6.4,4.8))
    listeX,listeY,listeT=[],[],[]
    setThemeGraph(plt)
    mois,annee=ligne["Args1"],ligne["Args2"]
    connexion,curseur=connectSQL(ctx.guild.id,option,"Stats",tableauMois[mois],annee)
    table=curseur.execute("SELECT * FROM evol{0}{1}{2} ORDER BY DateID ASC".format(mois,annee,ligne["Args3"])).fetchall()
    mini=curseur.execute("SELECT MIN(Count) AS Min FROM evol{0}{1}{2} ORDER BY DateID ASC".format(mois,annee,ligne["Args3"])).fetchone()["Min"]
    rank=table[len(table)-1]["Rank"]

    for i in range(len(table)):
        listeY.append(table[i]["Count"])
        absData(mois,table,i,listeX,listeT)
    div=voiceAxe(option,listeY,plt,"y")
    mini=round(mini/div,2)

    df=pd.DataFrame({"Date": listeX, "Count": listeY})
    if rank==1:
        tableRank=curseur.execute("SELECT * FROM {0}{1} WHERE Rank=2".format(mois,annee)).fetchone()
    else:
        tableRank=curseur.execute("SELECT * FROM {0}{1} WHERE Rank=1".format(mois,annee)).fetchone()

    listeXO,listeYO=[],[]
    if tableRank!=None:
        evol=curseur.execute("SELECT * FROM evol{0}{1}{2} ORDER BY DateID ASC".format(mois,annee,tableRank["ID"])).fetchall()
        mini=min(mini,round(curseur.execute("SELECT MIN(Count) AS Min FROM evol{0}{1}{2} ORDER BY DateID ASC".format(mois,annee,tableRank["ID"])).fetchone()["Min"]/div,2))
        for i in range(len(evol)):
            listeYO.append(round(evol[i]["Count"]/div,2))
            absData(mois,evol,i,listeXO,listeT)
        df2=pd.DataFrame({"Date": listeXO, "Count": listeYO})
    
    if div==1:
        mini=int(mini)
    listeT.sort()
    dfDate=setMin(mois,listeT,mini)

    nom,color=getNomColor(ctx,bot,option,ligne["Args3"])
    plt.plot("Date", "Count", data=df, linestyle='-', marker='',color=color,label=nom)

    if tableRank!=None:
        try:
            if option in ("Salons","Voicechan"):
                assert not guildOT.chan[tableRank["ID"]]["Hide"]    
            elif option in ("Messages","Mots","Voice"):
                assert not guildOT.users[tableRank["ID"]]["Hide"]
            user=ctx.guild.get_member(tableRank["ID"])
            if user!=None:
                plt.plot("Date", "Count", data=df2, linestyle='--', marker='',color=(user.color.r/256,user.color.g/256,user.color.b/256,1),label=user.name)
            else:
                try:
                    nom2=getNomGraph(ctx,bot,option,tableRank["ID"])
                except:
                    if option in ("Messages","Mots","Voice"):
                        nom2="Ancien membre"
                    else:
                        nom2="??"
                plt.plot("Date", "Count", data=df2, linestyle='--', marker='',color=colorOT,label=nom2)
        except AssertionError:
            pass
    
    if rank==1:
        titreEvol(mois,annee,nom,"comparée avec deuxième meilleur {0} sur la période".format(dictTitle[option]))
    else:
        titreEvol(mois,annee,nom,"comparée avec meilleur {0} sur la période".format(dictTitle[option]))

    listeDates,listeXD,temp=[],[],0
    if mois=="to":
        for i in range(len(listeT)):
            if listeT[i][0:2]!=temp:
                listeDates.append("{0}/{1}".format(listeT[i][2:4],listeT[i][0:2]))
                listeXD.append(i)
                temp=listeT[i][0:2]
        plt.xticks(listeXD,listeDates,rotation=45)
    elif mois=="glob":
        for i in range(len(listeT)):
            if listeT[i][0:2]!=temp:
                listeDates.append("{0}/{1}/{2}".format(listeT[i][4:6],listeT[i][2:4],listeT[i][0:2]))
                listeXD.append(i)
                temp=listeT[i][0:2]
        plt.xticks(listeXD,listeDates,rotation=45)

    plt.xlabel("Date")
    plt.tight_layout()
    plt.legend()
    plt.savefig("Graphs/otGraph")
    plt.clf()


async def graphEvolRank(ligne,ctx,bot,option,guildOT):
    plt.subplots(figsize=(6.4,4.8))
    listeX,listeY,listeR=[],[],[]
    setThemeGraph(plt)
    mois,annee=ligne["Args1"],ligne["Args2"]
    connexion,curseur=connectSQL(ctx.guild.id,option,"Stats",tableauMois[mois],annee)
    table=curseur.execute("SELECT * FROM evol{0}{1}{2} ORDER BY DateID ASC".format(mois,annee,ligne["Args3"])).fetchall()
    collapse=collapseEvol(table)
    dates=[]
    for i in collapse:
        dates.append(i["DateID"])
    listeM=[True for i in range(len(table))]
    for i in range(len(table)):
        listeX.append("{0}/{1}/{2}".format(table[i]["Jour"],table[i]["Mois"],table[i]["Annee"]))
        listeY.append(table[i]["Rank"])
        if len(table)>31:
            if table[i]["DateID"] not in dates:
                listeM[i]=False
    
    df=pd.DataFrame({"Date": listeX, "Count": listeY})

    nom,color=getNomColor(ctx,bot,option,ligne["Args3"])
    
    listeTX,listeL=[],[]
    for i in range(len(listeM)):
        if listeM[i]==True:
            listeL.append(i)
            listeTX.append(listeX[i])

    plt.xlabel("Date")
    plt.ylabel("Rang") 
    plt.plot("Date", "Count", data=df, linestyle='-', marker='o',color=color,markevery=listeM)
    plt.xticks(listeL,listeTX,rotation=45)
    titreEvol(mois,annee,nom,"du rang")
    plt.tight_layout()
    plt.savefig("Graphs/otGraph")
    plt.clf()

async def graphEvolJoursAA(ligne,ctx,bot,option,guildOT):
    plt.subplots(figsize=(6.4,4.8))
    listeX,listeY,listeT=[],[],[]
    setThemeGraph(plt)
    mois,annee=ligne["Args1"],ligne["Args2"]
    connexion,curseur=connectSQL(ctx.guild.id,option,"Stats","GL","")
    table=getTableDay(curseur,mois,annee,"dateAsc")
    mini=curseur.execute("SELECT MIN(Count) AS Min FROM dayRank").fetchone()["Min"]

    for i in range(len(table)):
        listeY.append(table[i]["Count"])
        absData(mois,table,i,listeX,listeT)
    
    div=voiceAxe(option,listeY,plt,"y")
    mini=round(mini/div,2)

    df=pd.DataFrame({"Date": listeX, "Count": listeY})

    if ligne["Args1"]=="to":
        tableDemain=curseur.execute("SELECT Mois, Annee FROM firstA WHERE Annee>'{0}' AND Annee<>'GL' ORDER BY Annee ASC".format(annee)).fetchone()
        tableHier=curseur.execute("SELECT Mois, Annee FROM firstA WHERE Annee<'{0}' AND Annee<>'GL' ORDER BY Annee DESC".format(annee)).fetchone()
    else:
        tableDemain=curseur.execute("SELECT Mois, Annee, Annee || '' || Mois AS DateID FROM firstM WHERE DateID>'{0}{1}' ORDER BY DateID ASC".format(annee,mois)).fetchone()
        tableHier=curseur.execute("SELECT Mois, Annee, Annee || '' || Mois AS DateID FROM firstM WHERE DateID<'{0}{1}' ORDER BY DateID DESC".format(annee,mois)).fetchone()

    nom,color="Jours d'activité sur le serveur",colorOT

    if tableDemain!=None:
        listeX2,listeY2=[],[]
        demain=getTableDay(curseur,tableDemain["Mois"],tableDemain["Annee"],"dateAsc")
        for i in range(len(demain)):
            listeY2.append(round(demain[i]["Count"]/div,2))
            absData(mois,demain,i,listeX2,listeT)
        df2=pd.DataFrame({"Date": listeX2, "Count": listeY2})
    
    if tableHier!=None:
        listeX3,listeY3=[],[]
        hier=getTableDay(curseur,tableHier["Mois"],tableHier["Annee"],"dateAsc")
        for i in range(len(hier)):
            listeY3.append(round(hier[i]["Count"]/div,2))
            absData(mois,hier,i,listeX3,listeT)
        df3=pd.DataFrame({"Date": listeX3, "Count": listeY3})
    
    if div==1:
        mini=int(mini)
    listeT.sort()
    dfDate=setMin(mois,listeT,mini)

    if tableHier!=None:
        plt.plot("Date", "Count", data=df3, linestyle='--', marker='',color="indianred",label="{0} 20{1}".format(tableauMois[tableHier["Mois"]],tableHier["Annee"]))
    plt.plot("Date", "Count", data=df, linestyle='-', marker='',color=color,label="{0} 20{1}".format(tableauMois[mois],annee))
    if tableDemain!=None:
        plt.plot("Date", "Count", data=df2, linestyle='--', marker='',color="mediumpurple",label="{0} 20{1}".format(tableauMois[tableDemain["Mois"]],tableDemain["Annee"]))
    
    titreEvol(mois,annee,nom,"comparée avec périodes avant et après")

    if mois=="to":
        listeDates,listeXD,temp=[],[],0
        for i in range(len(listeT)):
            if listeT[i][0:2]!=temp:
                listeDates.append("{0}/{1}".format(listeT[i][2:4],listeT[i][0:2]))
                listeXD.append(i)
                temp=listeT[i][0:2]
        plt.xticks(listeXD,listeDates,rotation=45)
    
    plt.xlabel("Date")
    plt.tight_layout()
    plt.legend()
    plt.savefig("Graphs/otGraph")
    plt.clf()

def getNomColor(ctx,bot,option,author):
    if option in ("Voice","Messages","Mots"):
        try:
            user=ctx.guild.get_member(int(author))
            nom,color=user.name,(user.color.r/256,user.color.g/256,user.color.b/256,1)
        except:
            nom,color="Ancien membre",colorOT
    else:
        try:
            nom,color=getNomGraph(ctx,bot,option,int(author)),colorOT
        except:
            nom,color="??",colorOT
    if len(nom)>15:
        nom=nom[0:15]+"..."
    return nom,color

def absData(mois,table,i,listeX,listeT):
    if mois=="to":
        listeX.append("{0}/{1}".format(table[i]["Jour"],table[i]["Mois"]))
        if "{0}{1}".format(table[i]["Mois"],table[i]["Jour"]) not in listeT:
            listeT.append("{0}{1}".format(table[i]["Mois"],table[i]["Jour"]))
    elif mois=="glob":
        listeX.append("{0}/{1}/{2}".format(table[i]["Jour"],table[i]["Mois"],table[i]["Annee"]))
        if table[i]["DateID"] not in listeT:
            listeT.append(table[i]["DateID"])
    else:
        listeX.append(table[i]["Jour"])
        if table[i]["Jour"] not in listeT:
            listeT.append(table[i]["Jour"])

def setMin(mois,listeT,mini):
    if mois=="to":
        dfDate=pd.DataFrame({"Date": ["{0}/{1}".format(i[2:4],i[0:2]) for i in listeT], "Count": [mini//1.5 for i in range(len(listeT))]})
    elif mois=="glob":
        dfDate=pd.DataFrame({"Date": ["{0}/{1}/{2}".format(i[4:6],i[2:4],i[0:2]) for i in listeT], "Count": [mini//1.5 for i in range(len(listeT))]})
    else:
        dfDate=pd.DataFrame({"Date": listeT, "Count": [mini//1.5 for i in range(len(listeT))]})
    plt.plot("Date", "Count", data=dfDate, linestyle='', label="")

def titreEvol(mois,annee,nom,option):
    if mois=="glob":
        plt.title("Évolution globale {0}\n{1}".format(option,nom),fontsize=10)
    elif mois=="to":
        plt.title("Évolution 20{0} {1}\n{2}".format(annee,option,nom),fontsize=10)
    else:
        plt.title("Évolution {0} 20{1} {2}\n{3}".format(mois,annee,option,nom),fontsize=10)