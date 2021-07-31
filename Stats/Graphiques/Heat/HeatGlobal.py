import numpy as np
import pandas as pd
import seaborn as sns
from Core.Fonctions.GetNom import getNomGraph
from Core.Fonctions.GraphTheme import setThemeGraph
from Core.Fonctions.TempsVoice import formatCount
from matplotlib import pyplot as plt
from Stats.SQL.ConnectSQL import connectSQL
import os

tableauMois={"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre","TO":"TOTAL","1":"janvier","2":"février","3":"mars","4":"avril","5":"mai","6":"juin","7":"juillet","8":"aout","9":"septembre","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12"}
listeTitres={"Messages":"nombre de messages envoyés","Salons":"nombre de messages envoyés","Freq":"nombre de messages envoyés","Emotes":"nombre d'emotes utilisées","Reactions":"nombre de réactions utilisées","Voice":"temps passé en vocal","Voicechan":"temps passé en vocal","Divers":"nombre d'occurences de la statistique diverse"}

async def graphHeatGlobal(ligne,ctx,bot,option,guildOT):
    connexion,curseur=connectSQL(ctx.guild.id,option,"Stats","GL","")
    obj="" if ligne["Args3"]=="None" else ligne["Args3"]
    setThemeGraph(plt)
    if ligne["Commande"]=="periodsInter":
        dates=curseur.execute("SELECT DISTINCT Annee FROM persoA{0}{1} WHERE Annee<>'GL' ORDER BY Annee ASC".format(ligne["AuthorID"],ligne["Args1"])).fetchall()
    elif obj=="":
        dates=curseur.execute("SELECT DISTINCT Annee FROM firstA ORDER BY Annee ASC").fetchall()
    else:
        dates=curseur.execute("SELECT DISTINCT Annee FROM persoA{0} WHERE Annee<>'GL' ORDER BY Annee ASC".format(obj)).fetchall()
    listeHeat=[[0]*12 for i in range(len(dates))]
    labels=[[""]*12 for i in range(len(dates))]
    listeMois=["Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Aout","Septembre","Octobre","Novembre","Décembre"]
    connexion,curseur=connectSQL(ctx.guild.id,"Rapports","Stats","GL","")

    if ligne["Commande"]=="roles" and ligne["Args4"]!="None":
        descip=""
        members=ctx.guild.get_role(int(ligne["Args4"])).members
        for i in members:
            descip+="ID={0} OR ".format(i.id)

    for i in range(len(dates)):
        for j in range(12):
            mois=tableauMois[listeMois[j].lower()]
            try:
                assert os.path.exists("SQL/{0}/{1}/{2}".format(ctx.guild.id,dates[i]["Annee"],mois))
                if ligne["Commande"]=="periodsInter":
                    somme=curseur.execute("SELECT SUM(Count) AS Total FROM objs WHERE Mois='{0}' AND Annee='{1}' AND Type='{2}' AND ID={3} AND IDComp={4}".format(mois,dates[i]["Annee"],option,ligne["AuthorID"],ligne["Args1"])).fetchone()["Total"]
                elif ligne["Commande"]=="roles" and ligne["Args4"]!="None":
                    if obj=="":
                        somme=curseur.execute("SELECT SUM(Count) AS Total FROM ranks WHERE Mois='{0}' AND Annee='{1}' AND Type='{2}' AND ({3})".format(mois,dates[i]["Annee"],option,descip[0:-3])).fetchone()["Total"]
                    else:
                        somme=curseur.execute("SELECT SUM(Count) AS Total FROM objs WHERE Mois='{0}' AND Annee='{1}' AND Type='{2}' AND IDComp={3} AND ({4})".format(mois,dates[i]["Annee"],option,obj,descip[0:-3])).fetchone()["Total"]
                elif obj=="":
                    somme=curseur.execute("SELECT SUM(Count) AS Total FROM ranks WHERE Mois='{0}' AND Annee='{1}' AND Type='{2}'".format(mois,dates[i]["Annee"],option)).fetchone()["Total"]
                else:
                    somme=curseur.execute("SELECT SUM(Count) AS Total FROM ranks WHERE Mois='{0}' AND Annee='{1}' AND Type='{2}' AND ID={3}".format(mois,dates[i]["Annee"],option,obj)).fetchone()["Total"]
                if somme==None:
                    listeHeat[i][j]=0
                else:
                    listeHeat[i][j]=somme
                    labels[i][j]=formatCount(option,somme)
            except:
                listeHeat[i][j]=0

    df = pd.DataFrame(listeHeat, index=["20{0}".format(dates[i]["Annee"]) for i in range(len(dates))],columns=listeMois)
    midpoint = (df.values.max() - df.values.min()) / 2
    sns.heatmap(df, annot=np.array(labels),annot_kws={"size": 15},cmap="YlGnBu",fmt="",center=midpoint,square=True,xticklabels=True,yticklabels=True,cbar_kws={"shrink": 0.5})

    titre="Calendrier global {0} chaque mois".format(listeTitres[option])
    if ligne["Commande"]=="periodsInter":
        titre+="\n{0}".format(getNomGraph(ctx,bot,option,int(ligne["Args1"])))
    if obj!="":
        titre+="\n{0}".format(getNomGraph(ctx,bot,option,int(obj)))
    if ligne["Commande"]=="roles" and ligne["Args4"]!="None":
        titre+="\n{0}".format(getNomGraph(ctx,bot,"Roles",int(ligne["Args4"])))
    plt.title(titre)

    plt.xticks(rotation=0)
    plt.yticks(rotation=0)
    plt.gcf().set_size_inches(16, 9)
    plt.savefig("Graphs/otGraph",bbox_inches="tight")
    plt.clf()