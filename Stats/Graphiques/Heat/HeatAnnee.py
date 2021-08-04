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

async def graphHeatAnnee(ligne,ctx,bot,option,guildOT):
    listeMois=["Janvier","Février","Mars","Avril","Mai","Juin","Juillet","Aout","Septembre","Octobre","Novembre","Décembre"]
    listeHeat=[[0]*31 for i in range(12)]
    mask=[[False]*31 for i in range(12)]
    labels=[[""]*31 for i in range(12)]
    annee=ligne["Args2"]
    anneeDate=int("20{0}".format(annee))
    obj="" if ligne["Args3"]=="None" else ligne["Args3"]
    setThemeGraph(plt)
    connexion,curseur=connectSQL(ctx.guild.id,"Rapports","Stats","GL","")

    if ligne["Commande"]=="roles" and ligne["Args4"]!="None":
        descip=""
        members=ctx.guild.get_role(int(ligne["Args4"])).members
        for i in members:
            descip+="ID={0} OR ".format(i.id)
    
    for i in range(12):
        calendrier=calendar.monthrange(anneeDate,i+1)
        
        for j in range(31+(calendrier[1]-31),31):
            mask[i][j]=True

        try:
            mois=tableauMois[listeMois[i].lower()]            
            if obj=="":
                dates=curseur.execute("SELECT DISTINCT Jour FROM ranks WHERE Mois='{0}' AND Annee='{1}' AND Type='{2}'".format(mois,annee,option)).fetchall()
            else:
                dates=curseur.execute("SELECT DISTINCT Jour FROM ranks WHERE Mois='{0}' AND Annee='{1}' AND Type='{2}' AND ID={3}".format(mois,annee,option,obj)).fetchall()
            for j in dates:
                if ligne["Commande"]=="roles" and ligne["Args4"]!="None":
                    if obj=="":
                        somme=curseur.execute("SELECT SUM(Count) AS Total FROM ranks WHERE Jour='{0}' AND Mois='{1}' AND Annee='{2}' AND Type='{3}' AND ({4})".format(j["Jour"],mois,annee,option,descip[0:-3])).fetchone()["Total"]
                    else:
                        somme=curseur.execute("SELECT SUM(Count) AS Total FROM objs WHERE Jour='{0}' AND Mois='{1}' AND Annee='{2}' AND Type='{3}' AND IDComp={4} AND ({5})".format(j["Jour"],mois,annee,option,obj,descip[0:-3])).fetchone()["Total"]
                elif obj=="":
                    somme=curseur.execute("SELECT SUM(Count) AS Total FROM ranks WHERE Jour='{0}' AND Mois='{1}' AND Annee='{2}' AND Type='{3}'".format(j["Jour"],mois,annee,option)).fetchone()["Total"]
                else:
                    somme=curseur.execute("SELECT Count FROM ranks WHERE Jour='{0}' AND Mois='{1}' AND Annee='{2}' AND Type='{3}' AND ID={4}".format(j["Jour"],mois,annee,option,obj)).fetchone()["Count"]
                jour=int(j["Jour"])-1
                listeHeat[i][jour]=somme
                labels[i][jour]=formatCount(option,somme)
                if option in ("Voice","Voicechan"):
                    if len(labels[i][jour].split(" "))>=3:
                        descip=""
                        for z in range(len(labels[i][jour].split(" "))):
                            if z==2:
                                descip+="\n"
                            descip+=labels[i][jour].split(" ")[z]+" "
                        labels[i][jour]=descip
        except:
            pass
    
    i=0
    while i!=len(listeHeat):
        if listeHeat[i].count(0)==31:
            del listeHeat[i]
            del mask[i]
            del listeMois[i]
            del labels[i]
        else:
            i+=1

    df = pd.DataFrame(listeHeat, columns=[i+1 for i in range(31)],index=listeMois)
    midpoint = (df.values.max() - df.values.min()) / 2
    sns.heatmap(df, annot=np.array(labels),annot_kws={"size": 9},cmap="YlGnBu",fmt="",center=midpoint,square=True,mask=np.array(mask),xticklabels=True,yticklabels=True,cbar_kws={"shrink": len(listeMois)*0.65/12})

    titre="Calendrier {0} {1} chaque jour".format(anneeDate,listeTitres[option])
    if obj!="":
        titre+="\n{0}".format(getNomGraph(ctx,bot,option,int(obj)))
    if ligne["Commande"]=="roles" and ligne["Args4"]!="None":
        titre+="\n{0}".format(getNomGraph(ctx,bot,"Roles",int(ligne["Args4"])))
    plt.title(titre)

    plt.xticks(rotation=0)
    plt.gcf().set_size_inches(24, 13)
    plt.savefig("Graphs/otGraph.png", bbox_inches="tight")
    plt.clf()
