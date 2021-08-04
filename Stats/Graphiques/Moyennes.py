from matplotlib import pyplot as plt
import pandas as pd
from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.GraphTheme import setThemeGraph
from Core.Fonctions.GetNom import getNomGraph
from Core.Fonctions.VoiceAxe import voiceAxe
import os
import numpy as np
import seaborn as sns
colorOT=(110/256,200/256,250/256,1)

tableauMois={"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre","TO":"TOTAL","1":"janvier","2":"février","3":"mars","4":"avril","5":"mai","6":"juin","7":"juillet","8":"aout","9":"septembre","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12"}

def graphPersoMoy(ligne,ctx,option,bot,period,guildOT,curseur):
    author,nomTable=ligne["AuthorID"],ligne["AuthorID"]
    if ligne["Args1"]!="None":
        nomTable="{0}{1}".format(ligne["AuthorID"],ligne["Args1"])
    plt.subplots(figsize=(6.4,4.8))
    theme=setThemeGraph(plt)
    if period=="mois":
        table=curseur.execute("SELECT *, Annee || '' || Mois AS DateID FROM moy{0}{1} ORDER BY DateID ASC".format(option,ligne["AuthorID"])).fetchall()
    else:
        table=curseur.execute("SELECT * FROM moy{0}{1} ORDER BY Annee ASC".format(option,ligne["AuthorID"])).fetchall()
    listeX,listeY=[],[]
    somme=0

    for i in table:
        listeX.append("{0}/{1}".format(i["Mois"],i["Annee"]))
        listeY.append(round(i["Moyenne"],2))
    
    user=getNomGraph(ctx,bot,"Messages",author)

    df=pd.DataFrame({'date': listeX, "Moyennes": listeY})
    if user==None:
        plt.plot('date', "Moyennes", data=df, linestyle='-', marker='o',color=colorOT)
        plt.title("Ancien membre - Moyennes messages envoyés par {0}".format(option.lower()),fontsize=12)
    else:
        plt.plot('date', "Moyennes", data=df, linestyle='-', marker='o',color=(user.color.r/256,user.color.g/256,user.color.b/256,1))
        plt.title("{0} - Moyennes messages envoyés par {1}".format(user.name,option.lower()),fontsize=12)
    
    for i in range(len(listeX)):
        plt.text(x=i, y=listeY[i], s=listeY[i],size=8) 

    for i in listeY:
        somme+=i
    dictColor={"light":"black","dark":"white"}
    df2=pd.DataFrame({'date': listeX, 'moy': [somme/len(table) for i in range(len(listeX))]})
    plt.plot("date","moy",data=df2, linestyle="--", color=dictColor[theme],label="Moyenne globale ({0})".format(round(somme/len(table),2)))
    plt.legend()
    plt.xlabel("Date")
    plt.ylabel("Moyennes")

    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig("Graphs/otGraph")
    plt.clf()

def graphGroupedMoy(ligne,ctx,option,bot,guildOT,curseur):
    colors={"15":"grey","16":"pink","17":"purple","18":"orange","19":"green","20":"red","21":"blue"}
    author=ligne["AuthorID"]
    annees=curseur.execute("SELECT DISTINCT Annee FROM moy{0}{1} ORDER BY Annee ASC".format(option,author)).fetchall()
    mois=curseur.execute("SELECT DISTINCT Mois FROM moy{0}{1} ORDER BY Mois ASC".format(option,author)).fetchall()
    listeX,listeY,listeC,listeSN,listeSX,listeA=[],[],[],[],[],[]
    pos=0
    setThemeGraph(plt)
    plt.subplots(figsize=(6.4,4.8))
    for i in range(len(mois)):
        center=0
        for j in range(len(annees)):
            count=curseur.execute("SELECT * FROM moy{0}{1} WHERE Mois='{2}' AND Annee='{3}'".format(option,author,mois[i]["Mois"],annees[j]["Annee"])).fetchone()
            if count==None:
                continue
            else:
                listeY.append(round(count["Moyenne"],2))
            listeX.append(pos)
            listeA.append(annees[j]["Annee"])
            pos+=1
            center+=1
        listeSX.append(pos-center//2-1)
        listeSN.append(tableauMois[mois[i]["Mois"]])
        pos+=0.75

    plt.ylabel("Moyennes")
    for i in range(len(listeA)):
        plt.text(x=listeX[i], y=listeY[i], s="20{0}".format(listeA[i]), size=5, fontproperties="italic", ha="center") 

    plt.bar(listeX, listeY, color=[colors[i] for i in listeA], width=1, edgecolor='white')
    plt.xticks(listeSX, listeSN,rotation=45)
    plt.xlabel("Mois")
    
    nom=getNomGraph(ctx,bot,"Messages",author)
    try:
        nom=nom.name
    except:
        nom="Ancien membre"

    plt.title("{0} - Mois groupés moyennes messages envoyés par {1}".format(nom,option))
    plt.tight_layout()
    plt.savefig("Graphs/otGraph")
    plt.clf()

async def graphHeatMoy(ligne,ctx,bot,option,guildOT,curseur):
    author=ligne["AuthorID"]
    setThemeGraph(plt)
    dates=curseur.execute("SELECT DISTINCT Annee FROM moy{0}{1} ORDER BY Annee ASC".format(option,author)).fetchall()
    listeHeat=[[0]*12 for i in range(len(dates))]
    labels=[[""]*12 for i in range(len(dates))]
    listeMois=["Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Aout","Septembre","Octobre","Novembre","Décembre"]

    for i in range(len(dates)):
        for j in range(12):
            mois=tableauMois[listeMois[j].lower()]
            try:
                assert os.path.exists("SQL/{0}/{1}/{2}".format(ctx.guild.id,dates[i]["Annee"],mois))
                somme=round(curseur.execute("SELECT * FROM moy{0}{1} WHERE Mois='{2}' AND Annee='{3}'".format(option,author,mois,dates[i]["Annee"])).fetchone()["Moyenne"],2)
                if somme==None:
                    listeHeat[i][j]=0
                else:
                    listeHeat[i][j]=somme
                    labels[i][j]=somme
            except:
                listeHeat[i][j]=0

    df = pd.DataFrame(listeHeat, index=["20{0}".format(dates[i]["Annee"]) for i in range(len(dates))],columns=listeMois)
    midpoint = (df.values.max() - df.values.min()) / 2
    sns.heatmap(df, annot=np.array(labels),annot_kws={"size": 15},cmap="YlGnBu",fmt="",center=midpoint,square=True,xticklabels=True,yticklabels=True,cbar_kws={"shrink": 0.5})

    plt.title("Calendrier global moyenne messages envoyés {0} chaque mois".format(option.lower()))

    plt.xticks(rotation=0)
    plt.yticks(rotation=0)
    plt.gcf().set_size_inches(32, 18)
    plt.savefig("Graphs/otGraph",bbox_inches="tight")
    plt.clf()