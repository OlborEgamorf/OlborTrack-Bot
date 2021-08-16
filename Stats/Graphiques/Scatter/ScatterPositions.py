from Core.Fonctions.GraphTheme import setThemeGraph
from matplotlib import pyplot as plt
from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.VoiceAxe import voiceAxe
import pandas as pd
import sqlite3
from Core.Fonctions.GetNom import getNomGraph

tableauMois={"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre","TO":"TOTAL","1":"janvier","2":"février","3":"mars","4":"avril","5":"mai","6":"juin","7":"juillet","8":"aout","9":"septembre","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","to":"to"}
dictColor={"light":"grey","dark":(200/256, 210/256, 227/256)}
colorOT=(110/256,200/256,250/256,1)
dictOption={"tortues":"Tortues","tortuesduo":"TortuesDuo","trivialversus":"TrivialVersus","trivialbr":"TrivialBR","trivialparty":"TrivialParty","p4":"P4","bataillenavale":"BatailleNavale"}

async def graphScatter(ligne,ctx,bot,option,guildOT):
    theme=setThemeGraph(plt)
    plt.subplots(figsize=(6.4,4.8))
    listeX,listeY=[],[]
    listeTick=[]
    obj="" if ligne["Args3"]=="None" else ligne["Args3"]
    if ligne["Commande"]=="jeux":
        connexion,curseur=connectSQL(ligne["Args3"],dictOption[option],"Jeux",tableauMois[ligne["Args1"]],ligne["Args2"])
        obj=""
    else:
        connexion,curseur=connectSQL(ctx.guild.id,option,"Stats",tableauMois[ligne["Args1"]],ligne["Args2"])
    mois=curseur.execute("SELECT * FROM {0}{1}{2} WHERE Rank<=15".format(ligne["Args1"],ligne["Args2"],obj)).fetchall()
    
    for i in mois:
        if option in ("Salons","Voicechan") and obj=="":
            if guildOT.chan[i["ID"]]["Hide"]:
                continue
        elif option in ("Messages","Mots","Voice") or obj!="":
            if guildOT.users[i["ID"]]["Hide"]:
                continue 
        listeX.append(i["Rank"])
        listeY.append(i["Count"])
    
    div=voiceAxe(option,listeY,plt,"y")
    dfMois=pd.DataFrame({'Rank': listeX, "Count":listeY})

    listeX,listeY=[],[]

    if ligne["Commande"]=="jeux":
        connexion,curseur=connectSQL(ligne["Args3"],dictOption[option],"Jeux","GL","")
    else:
        connexion,curseur=connectSQL(ctx.guild.id,option,"Stats","GL","")
        
    if ligne["Args1"]=="to":
        allMois=curseur.execute("SELECT Mois,Annee FROM firstA").fetchall()
        labelO="Autre année"
    else:
        allMois=curseur.execute("SELECT Mois,Annee FROM firstM").fetchall()
        labelO="Autre mois"
    for i in allMois:
        try:
            if ligne["Commande"]=="jeux":
                connexion,curseur=connectSQL(ligne["Args3"],dictOption[option],"Jeux",i["Mois"],i["Annee"])
            else:
                connexion,curseur=connectSQL(ctx.guild.id,option,"Stats",i["Mois"],i["Annee"])
            for j in curseur.execute("SELECT * FROM {0}{1}{2} WHERE Rank<=15".format(tableauMois[i["Mois"].lower()],i["Annee"],obj)).fetchall():
                listeX.append(j["Rank"])
                listeY.append(j["Count"])
                if j["Rank"] not in listeTick:
                    listeTick.append(j["Rank"])
        except sqlite3.OperationalError:
            pass
    
    if option in ("Voice","Voicechan"):
        for i in range(len(listeY)):
            listeY[i]=round(listeY[i]/div,2)
    dfOther=pd.DataFrame({'Rank': listeX, "Count":listeY})
    
    plt.plot("Rank", "Count", data=dfOther, linestyle="", marker="o", markersize=3, color=dictColor[theme], alpha=0.4, label=labelO)
    plt.plot("Rank", "Count", data=dfMois, linestyle="", marker="o", markersize=3, color="red", label="{0} 20{1}".format(ligne["Args1"],ligne["Args2"]))

    listeTick.sort()
    listeL=["{0}e".format(i) for i in range(1,len(listeTick)+1)]
    plt.xticks(listeTick, listeL)
    plt.xlabel("Rang")
    if obj=="":
        plt.title("Compteur par rang - {0}".format(option))
    else:
        plt.title("Compteur par rang - {0}\n{1}".format(option,getNomGraph(ctx,bot,option,int(obj))))
    plt.legend()
    plt.tight_layout()
    plt.savefig("Graphs/otGraph")
    plt.clf()