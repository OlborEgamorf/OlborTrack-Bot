import calendar

import numpy as np
import pandas as pd
import seaborn as sns
from Core.Fonctions.GetNom import getNomGraph
from Core.Fonctions.GraphTheme import setThemeGraph
from Core.Fonctions.TempsVoice import formatCount
from matplotlib import pyplot as plt
from Stats.SQL.ConnectSQL import connectSQL

tableauMois={"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre","TO":"TOTAL","1":"janvier","2":"février","3":"mars","4":"avril","5":"mai","6":"juin","7":"juillet","8":"aout","9":"septembre","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12"}
listeTitres={"Messages":"nombre de messages envoyés","Salons":"nombre de messages envoyés","Freq":"nombre de messages envoyés","Emotes":"nombre d'emotes utilisées","Reactions":"nombre de réactions utilisées","Voice":"temps passé en vocal","Voicechan":"temps passé en vocal"}

async def graphHeat(ligne,ctx,bot,option,guildOT):
    listeHeat=[]
    mask=[]
    labels=[]
    mois=tableauMois[ligne["Args1"]]
    annee=ligne["Args2"]
    anneeDate="20{0}".format(annee)
    obj="" if ligne["Args3"]=="None" else ligne["Args3"]
    connexion,curseur=connectSQL(ctx.guild.id)
    setThemeGraph(plt)
    if obj=="":
        dates=curseur.execute("SELECT DISTINCT Jour FROM ranks WHERE Mois='{0}' AND Annee='{1}' AND Type='{2}'".format(mois,annee,option)).fetchall()
    else:
        dates=curseur.execute("SELECT DISTINCT Jour FROM ranks WHERE Mois='{0}' AND Annee='{1}' AND Type='{2}' AND ID={3}".format(mois,annee,option,obj)).fetchall()
    calendrier=calendar.monthrange(int(anneeDate),int(mois))

    if ligne["Commande"]=="roles" and ligne["Args4"]!="None":
        descip=""
        members=ctx.guild.get_role(int(ligne["Args4"])).members
        for i in members:
            descip+="ID={0} OR ".format(i.id)

    if calendrier[1]+calendrier[0]==36:
        stop=calendrier[1]+calendrier[0]+7
    else:
        stop=calendrier[1]+calendrier[0]
    for i in range(1,stop,7):
        listeHeat.append([0]*7)
        labels.append([""]*7)
        mask.append([False]*7)
        if i==1:
            for j in range(calendrier[0]):
                mask[0][j]=True
    
    if (calendrier[0]+calendrier[1])%7!=0:
        for i in range((calendrier[0]+calendrier[1])%7,7):
            mask[len(listeHeat)-1][i]=True

    for i in dates:
        if ligne["Commande"]=="roles" and ligne["Args4"]!="None":
            if obj=="":
                somme=curseur.execute("SELECT SUM(Count) AS Total FROM ranks WHERE Jour='{0}' AND Mois='{1}' AND Annee='{2}' AND Type='{3}' AND ({4})".format(i["Jour"],mois,annee,option,descip[0:-3])).fetchone()["Total"]
            else:
                somme=curseur.execute("SELECT SUM(Count) AS Total FROM objs WHERE Jour='{0}' AND Mois='{1}' AND Annee='{2}' AND Type='{3}' AND IDComp={4} AND ({5})".format(i["Jour"],mois,annee,option,obj,descip[0:-3])).fetchone()["Total"]
        elif obj=="":
            somme=curseur.execute("SELECT SUM(Count) AS Total FROM ranks WHERE Jour='{0}' AND Mois='{1}' AND Annee='{2}' AND Type='{3}'".format(i["Jour"],mois,annee,option)).fetchone()["Total"]
        else:
            somme=curseur.execute("SELECT Count FROM ranks WHERE Jour='{0}' AND Mois='{1}' AND Annee='{2}' AND Type='{3}' AND ID={4}".format(i["Jour"],mois,annee,option,obj)).fetchone()["Count"]
        jour=calendar.weekday(int(anneeDate),int(mois),int(i["Jour"]))
        if calendrier[0]==0:
            semaine=(int(i["Jour"])+6-jour)//7-1
        else:
            semaine=(int(i["Jour"])+6-jour)//7
        listeHeat[semaine][jour]=somme
        labels[semaine][jour]="{0}/{1}/{2}\n{3}".format(i["Jour"],mois,annee,formatCount(option,somme))
    
    df = pd.DataFrame(listeHeat, columns=["Lundi","Mardi","Mercredi","Jeudi","Vendredi","Samedi","Dimanche"])
    midpoint = (df.values.max() - df.values.min()) / 2
    sns.heatmap(df, annot_kws={"size": 8.5},cmap="YlGnBu",fmt="",center=midpoint,square=True,mask=np.array(mask),xticklabels=True,yticklabels=False,cbar_kws={"shrink": 0.80}, annot=np.array(labels))

    titre="Calendrier {0} {1} {2} par jour".format(ligne["Args1"],anneeDate,listeTitres[option])
    if obj!="":
        titre+="\n{0}".format(getNomGraph(ctx,bot,option,int(obj)))
    if ligne["Commande"]=="roles" and ligne["Args4"]!="None":
        titre+="\n{0}".format(getNomGraph(ctx,bot,"Roles",int(ligne["Args4"])))
    plt.title(titre)

    plt.xticks(rotation=0)
    plt.tight_layout()
    plt.savefig("Graphs/otGraph.png")#, bbox_inches="tight")
    plt.clf()
