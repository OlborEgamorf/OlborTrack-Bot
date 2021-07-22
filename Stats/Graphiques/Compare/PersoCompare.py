from matplotlib import pyplot as plt
import pandas as pd
from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.GraphTheme import setThemeGraph
from Core.Fonctions.DichoTri import triPeriod
from Core.Fonctions.GetNom import getNomGraph
from Core.Fonctions.VoiceAxe import voiceAxe
colorOT=(110/256,200/256,250/256,1)

def graphPersoComp(ligne,ctx,option,bot,period,guildOT,categ):
    connexion,curseur=connectSQL(ctx.guild.id,option,"Stats","GL","")
    user1,user2=ligne["AuthorID"],ligne["Args2"]
    obj=ligne["Args3"]
    if obj=="None":
        obj=""
    plt.subplots(figsize=(6.4,4.8))
    theme=setThemeGraph(plt)
    if period=="mois":
        table=triPeriod(curseur,"persoM{0}{1}".format(user1,obj),"periodAsc")
        table2=triPeriod(curseur,"persoM{0}{1}".format(user2,obj),"periodAsc")
    else:
        table=curseur.execute("SELECT * FROM persoA{0}{1} WHERE Annee<>'GL' ORDER BY Annee ASC".format(user1,obj)).fetchall()
        table2=curseur.execute("SELECT * FROM persoA{0}{1} WHERE Annee<>'GL' ORDER BY Annee ASC".format(user2,obj)).fetchall()
    listeX,listeY=[[],[]],[[],[]]
    tables=[table,table2]
    users=[user1,user2]
    somme=0
    dictLine={1:"-",2:"--"}
    listeColor=[]
    colorsBasic=[colorOT,"gold"]

    for z in range(2):
        for i in tables[z]:
            dictY={"Compteur":i["Count"],"Rang":i["Rank"]}
            listeX[z].append("{0}/{1}".format(i["Mois"],i["Annee"]))
            listeY[z].append(dictY[categ])
    
        user=getNomGraph(ctx,bot,option,int(users[z]))

        if z==0:
            div=voiceAxe(option,listeY[z],plt,"y")
        else:
            for i in range(len(listeY[z])):
                listeY[z][i]=round(listeY[z][i]/div,2)
        
        df=pd.DataFrame({'date': listeX[z], categ: listeY[z]})
        if user==None:
            plt.plot('date', categ, data=df, linestyle='-', marker='o',color=colorsBasic[z],label="Ancien membre")
        else:
            listeColor.append((user.color.r/256,user.color.g/256,user.color.b/256,1))
            plt.plot('date', categ, data=df, linestyle=dictLine[listeColor.count((user.color.r/256,user.color.g/256,user.color.b/256,1))], marker='o',color=(user.color.r/256,user.color.g/256,user.color.b/256,1),label=user.name)

    plt.legend()
    plt.xlabel("Date")
    plt.ylabel(categ)
    plt.xticks(rotation=90)
    plt.tight_layout()
    plt.savefig("Graphs/otGraph")
    plt.clf()