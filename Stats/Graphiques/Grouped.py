import sys

import matplotlib.patches as mpatches
from Core.Fonctions.GetNom import getNomGraph
from Core.Fonctions.GraphTheme import setThemeGraph
from Core.Fonctions.VoiceAxe import voiceAxe
from matplotlib import pyplot as plt
from Stats.SQL.ConnectSQL import connectSQL

tableauMois={"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre","TO":"TOTAL","1":"janvier","2":"février","3":"mars","4":"avril","5":"mai","6":"juin","7":"juillet","8":"aout","9":"septembre","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12"}

def graphGroupedMois(ligne,ctx,option,bot,guildOT):
    connexion,curseur=connectSQL(ctx.guild.id,option,"Stats","GL","")
    colors={"15":"grey","16":"pink","17":"purple","18":"orange","19":"green","20":"red","21":"blue"}
    author,table=ligne["AuthorID"],ligne["AuthorID"]
    if ligne["Args1"]!="None":
        table="{0}{1}".format(ligne["AuthorID"],ligne["Args1"])
    annees=curseur.execute("SELECT DISTINCT Annee FROM persoM{0} ORDER BY Annee ASC".format(table)).fetchall()
    mois=curseur.execute("SELECT DISTINCT Mois FROM persoM{0} ORDER BY Mois ASC".format(table)).fetchall()
    listeX,listeY,listeC,listeSN,listeSX,listeA=[],[],[],[],[],[]
    pos=0
    setThemeGraph(plt)
    plt.subplots(figsize=(6.4,4.8))
    for i in range(len(mois)):
        center=0
        for j in range(len(annees)):
            count=curseur.execute("SELECT * FROM persoM{0} WHERE Mois='{1}' AND Annee='{2}'".format(table,mois[i]["Mois"],annees[j]["Annee"])).fetchone()
            if count==None:
                continue
            else:
                listeY.append(count["Count"])
            listeX.append(pos)
            listeA.append(annees[j]["Annee"])
            pos+=1
            center+=1
        listeSX.append(pos-center//2-1)
        listeSN.append(tableauMois[mois[i]["Mois"]])
        pos+=0.75

    voiceAxe(option,listeY,plt,"y")
    for i in range(len(listeA)):
        plt.text(x=listeX[i], y=listeY[i], s="20{0}".format(listeA[i]), size=5, fontproperties="italic", ha="center") 

    plt.bar(listeX, listeY, color=[colors[i] for i in listeA], width=1, edgecolor='white') #,label='20{0}'.format(annees[i]["Annee"]))
    plt.xticks(listeSX, listeSN,rotation=45)
    plt.xlabel("Mois")
    
    if option in ("Messages","Voice","Mots") or ligne["Args1"]!="None":
        nom=getNomGraph(ctx,bot,"Messages",author)
        try:
            nom=nom.name
        except:
            nom="Ancien membre"
    else:
        nom=getNomGraph(ctx,bot,option,author)
    
    titre="{0} - Mois groupés".format(nom)
    if ligne["Args1"]!="None":
        titre+="\n{0}".format(getNomGraph(ctx,bot,option,int(ligne["Args1"])))

    plt.title(titre)
    plt.tight_layout()
    plt.savefig("Graphs/otGraph")
    plt.clf()