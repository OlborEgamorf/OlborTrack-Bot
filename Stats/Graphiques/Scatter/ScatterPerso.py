import sqlite3

import pandas as pd
from Core.Fonctions.GetNom import getNomGraph
from Core.Fonctions.GraphTheme import setThemeGraph
from matplotlib import pyplot as plt
from Stats.SQL.ConnectSQL import connectSQL

tableauMois={"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre","TO":"TOTAL","1":"janvier","2":"février","3":"mars","4":"avril","5":"mai","6":"juin","7":"juillet","8":"aout","9":"septembre","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","to":"to"}

async def graphScatterPerso(ligne,ctx,bot,option,guildOT):
    setThemeGraph(plt)
    fig,ax=plt.subplots(figsize=(6.4,4.8))
    listeX,listeY,listeXU,listeYU=[],[],[],[]
    listeN=[]
    count=0
    connexion,curseur=connectSQL(ctx.guild.id,option,"Stats",ligne["Args1"],ligne["Args2"])
    table=curseur.execute("SELECT * FROM perso{0}{1}{2} ORDER BY Count DESC LIMIT 15".format(ligne["Args1"],ligne["Args2"],ligne["AuthorID"])).fetchall()
    table.reverse()
    connexion,curseur=connectSQL(ctx.guild.id,option,"Stats","GL","")
    for i in range(len(table)):
        if option in ("Salons","Voicechan"):
            if guildOT.chan[table[i]["ID"]]["Hide"]:
                count+=1
                continue
        listeX.append(i+1-count)
        listeY.append(table[i]["Count"])
        try:
            if ligne["Args1"]=="TO":
                tablePerso=curseur.execute("SELECT * FROM persoA{0}{1} WHERE Annee<>'GL'".format(ligne["AuthorID"],table[i]["ID"])).fetchall()
            else:
                tablePerso=curseur.execute("SELECT * FROM persoM{0}{1}".format(ligne["AuthorID"],table[i]["ID"])).fetchall()
            for j in tablePerso:
                listeXU.append(i+1-count)
                listeYU.append(j["Count"])
        except sqlite3.OperationalError:
            pass

        try:
            listeN.append(getNomGraph(ctx,bot,option,table[i]["ID"]))
        except:
            listeN.append("??")

    dfMois=pd.DataFrame({'Rank': listeX, "Count":listeY})
    dfOther=pd.DataFrame({'Rank': listeXU, "Count":listeYU})
    
    plt.plot("Count", "Rank", data=dfOther, linestyle="", marker="o", markersize=3, color="grey", alpha=0.4, label="Autre mois")
    plt.plot("Count", "Rank", data=dfMois, linestyle="", marker="o", markersize=3, color="red", label="{0} 20{1}".format(tableauMois[ligne["Args1"]],ligne["Args2"]))

    plt.yticks([i+1 for i in range(len(table)-count)], listeN)
    plt.xlabel("Compteur")
    plt.xlim(left=0)
    try:
        nom=getNomGraph(ctx,bot,"Messages",int(ligne["AuthorID"])).name
    except:
        nom="Ancien membre"
    plt.title("Compteur par {0}\n{1}".format(option,nom))
    plt.legend(frameon=True)
    plt.tight_layout()
    plt.savefig("Graphs/otGraph")
    plt.clf()
