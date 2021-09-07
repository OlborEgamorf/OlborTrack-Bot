from Core.Fonctions.GraphTheme import setThemeGraph
from matplotlib import pyplot as plt
from Stats.SQL.ConnectSQL import connectSQL
import sqlite3
from Core.Fonctions.GetNom import getNomGraph
from Core.Fonctions.VoiceAxe import voiceAxe
import pandas as pd

tableauMois={"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre","TO":"TOTAL","1":"janvier","2":"février","3":"mars","4":"avril","5":"mai","6":"juin","7":"juillet","8":"aout","9":"septembre","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","to":"to"}
dictColor={"light":"grey","dark":(200/256, 210/256, 227/256)}
colorOT=(110/256,200/256,250/256,1)
dictOption={"tortues":"Tortues","tortuesduo":"TortuesDuo","trivialversus":"TrivialVersus","trivialbr":"TrivialBR","trivialparty":"TrivialParty","p4":"P4","bataillenavale":"BatailleNavale"}

async def graphScatterUsers(ligne,ctx,bot,option,guildOT):
    theme=setThemeGraph(plt)
    fig,ax=plt.subplots(figsize=(6.4,4.8))
    listeX,listeY,listeXU,listeYU=[],[],[],[]
    listeN=[]
    count=0
    obj="" if ligne["Args3"]=="None" else ligne["Args3"]
    if ligne["Commande"]=="jeux":
        connexion,curseur=connectSQL(ligne["Args3"],dictOption[option],"Jeux",tableauMois[ligne["Args1"]],ligne["Args2"])
        obj=""
    else:
        connexion,curseur=connectSQL(ctx.guild.id,option,"Stats",tableauMois[ligne["Args1"]],ligne["Args2"])
    table=curseur.execute("SELECT * FROM {0}{1}{2} WHERE Rank<=15 ORDER BY Rank ASC LIMIT 15".format(ligne["Args1"],ligne["Args2"],obj)).fetchall()
    table.reverse()
    
    if ligne["Commande"]=="jeux":
        connexion,curseur=connectSQL(ligne["Args3"],dictOption[option],"Jeux","GL","")
    else:
        connexion,curseur=connectSQL(ctx.guild.id,option,"Stats","GL","")
    for i in range(len(table)):
        if option in ("Salons","Voicechan") and obj=="":
            if guildOT.chan[table[i]["ID"]]["Hide"]:
                count+=1
                continue
        elif option in ("Messages","Mots","Voice","Voicechan") or obj!="":
            if guildOT.users[table[i]["ID"]]["Hide"]:
                count+=1
                continue 
        listeX.append(i+1)
        listeY.append(table[i]["Count"])
        try:
            if ligne["Args1"]=="to":
                tablePerso=curseur.execute("SELECT * FROM persoA{0}{1} WHERE Annee<>'GL'".format(table[i]["ID"],obj)).fetchall()
            else:
                tablePerso=curseur.execute("SELECT * FROM persoM{0}{1}".format(table[i]["ID"],obj)).fetchall()
            for j in tablePerso:
                listeXU.append(i+1)
                listeYU.append(j["Count"])
        except sqlite3.OperationalError:
            pass

        try:
            if ligne["Commande"]=="jeux":
                listeN.append(getNomGraph(ctx,bot,option,table[i]["ID"]))
            elif option in ("Messages","Mots","Voice","Voicechan") or obj!="":
                nom=getNomGraph(ctx,bot,"Messages",table[i]["ID"]).name
                nom=nom if len(nom)<=15 else "{0}...".format(nom[0:15])
                listeN.append(nom)
            else:
                listeN.append(getNomGraph(ctx,bot,option,table[i]["ID"]))
        except:
            listeN.append("??")

    div=voiceAxe(option,listeY,plt,"x")
    if option in ("Voice","Voicechan"):
        for i in range(len(listeYU)):
            listeYU[i]=round(listeYU[i]/div,2)

    dfMois=pd.DataFrame({'Rank': listeX, "Count":listeY})
    dfOther=pd.DataFrame({'Rank': listeXU, "Count":listeYU})
    
    plt.plot("Count", "Rank", data=dfOther, linestyle="", marker="o", markersize=3, color=dictColor[theme], alpha=0.4, label="Autre mois")
    plt.plot("Count", "Rank", data=dfMois, linestyle="", marker="o", markersize=3, color="red", label="{0} 20{1}".format(ligne["Args1"],ligne["Args2"]))

    plt.yticks([i+1 for i in range(len(table)-count)], listeN)
    plt.xlim(left=0)

    if obj=="" or ligne["Commande"]=="jeux":
        plt.title("Compteur par personne - {0}".format(option))
    else:
        plt.title("Compteur par personne - {0}\n{1}".format(option,getNomGraph(ctx,bot,option,int(obj))))
    plt.legend(frameon=True)
    plt.tight_layout()
    plt.savefig("Graphs/otGraph")
    plt.clf()