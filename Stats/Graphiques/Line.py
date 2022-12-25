from math import inf

import pandas as pd
from Core.Fonctions.GetNom import getNomGraph, getTitre
from Core.Fonctions.GraphTheme import setThemeGraph
from Core.Fonctions.VoiceAxe import voiceAxe
from matplotlib import pyplot as plt
from Core.Fonctions.GetTable import getTablePerso
from Stats.SQL.ConnectSQL import connectSQL

tableauMois={"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre","TO":"TOTAL","1":"janvier","2":"février","3":"mars","4":"avril","5":"mai","6":"juin","7":"juillet","8":"aout","9":"septembre","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","glob":"GL","to":"TO"}
colorOT=(110/256,200/256,250/256,1)
dictOption={"tortues":"Tortues","tortuesduo":"TortuesDuo","trivialversus":"TrivialVersus","trivialbr":"TrivialBR","trivialparty":"TrivialParty","p4":"P4","bataillenavale":"BatailleNavale"}

async def graphLine(ligne,ctx,bot,option,guildOT):
    colorsBasic=[colorOT,"green","red"]
    plt.subplots(figsize=(6.4,4.8))
    setThemeGraph(plt)
    obj=ligne["Args3"] if ligne["Args3"]!="None" else ""
    if ligne["Commande"]=="jeux":
        connexion,curseur=connectSQL(ligne["Args3"])
        obj=""
    else:
        connexion,curseur=connectSQL(ctx.guild.id)
    table=curseur.execute("SELECT * FROM {0}{1}{2} ORDER BY Rank ASC".format(ligne["Args1"],ligne["Args2"],obj)).fetchall()

    if obj=="":
        old10=curseur.execute("SELECT * FROM firstM WHERE DateID<={0}{1} ORDER BY DateID DESC".format(ligne["Args2"],tableauMois[ligne["Args1"]])).fetchall()
    else:
        less=ligne["Args2"]+tableauMois[ligne["Args1"]]
        old10=getTablePerso(ctx.guild.id,option,obj,False,"M","periodDesc")
        old10=list(filter(lambda x:x["Annee"]+x["Mois"]<less,old10))
    old10=old10[0:10] if len(old10)>10 else old10

    listeDates=[]
    listeX,listeY,listeR,listeP=[[],[],[]],[[],[],[]],[[],[],[]],[[],[],[]]
    mini=inf

    stop=3 if len(table)>3 else len(table)
    for i in range(stop-1,-1,-1):
        for j in range(len(old10)-1,-1,-1):
            count=curseur.execute("SELECT Count,Rank FROM {0}{1}{2} WHERE ID={3}".format(tableauMois[old10[j]["Mois"]],old10[j]["Annee"],obj,table[i]["ID"])).fetchone()
            if count!=None:
                if old10[j]["DateID"] not in listeDates:
                    listeDates.append(old10[j]["DateID"])
                listeX[i].append("{0}/{1}".format(old10[j]["Mois"],old10[j]["Annee"]))
                listeY[i].append(count["Count"])
                listeP[i].append(old10[j]["DateID"])
                listeR[i].append(count["Rank"])
                mini=min(count["Count"],mini)

    
    div=voiceAxe(option,listeY[0],plt,"y")
    if option in ("Voice","Voicechan"):
        for i in range(1,stop):
            for j in range(len(listeY[i])):
                listeY[i][j]=round(listeY[i][j]/div,2)
        mini=round(mini/div,2)

    listeDates.sort()
    dfDate=pd.DataFrame({"Date": ["{0}/{1}".format(str(i)[2:4],str(i)[0:2]) for i in listeDates], "Count": [mini//1.5 for i in range(len(listeDates))]})
    plt.plot("Date", "Count", data=dfDate, linestyle='', label="")
    listeColors=[]
    dictLine={1:"-",2:"--",3:"-."}

    connexion,curseur=connectSQL("OT")
    for i in range(stop):
        if ligne["Commande"]=="jeux":
            df=pd.DataFrame({"Date": listeX[i], "Count": listeY[i]})
            color=curseur.execute("SELECT * FROM couleurs WHERE ID={0}".format(table[i]["ID"])).fetchone()
            if color==None:
                color={"R":110,"G":200,"B":250}
            nom=getTitre(curseur,table[i]["ID"])
            listeColors.append((color["R"]/256,color["G"]/256,color["B"]/256,1))
            plt.plot("Date", "Count", data=df, linestyle=dictLine[listeColors.count((color["R"]/256,color["G"]/256,color["B"]/256,1))], marker='o',color=(color["R"]/256,color["G"]/256,color["B"]/256,1),label=nom)
        else:
            if option in ("Salons","Voicechan") and obj=="":
                if guildOT.chan[table[i]["ID"]]["Hide"]:
                    continue
            elif option in ("Messages","Mots","Voice") or obj!="":
                if guildOT.users[table[i]["ID"]]["Hide"]:
                    continue 
            df=pd.DataFrame({"Date": listeX[i], "Count": listeY[i]})
            user=ctx.guild.get_member(table[i]["ID"])
            if user!=None:
                listeColors.append((user.color.r/256,user.color.g/256,user.color.b/256,1))
                plt.plot("Date", "Count", data=df, linestyle=dictLine[listeColors.count((user.color.r/256,user.color.g/256,user.color.b/256,1))], marker='o',color=(user.color.r/256,user.color.g/256,user.color.b/256,1),label=user.name)
            else:
                try:
                    nom=getNomGraph(ctx,bot,option,table[i]["ID"])
                except:
                    nom="Ancien membre"
                plt.plot("Date", "Count", data=df, linestyle='-', marker='o',color=colorsBasic[i],label=nom)
        for j in range(len(listeY[i])):
            plt.text(x=listeDates.index(listeP[i][j]), y=listeY[i][j], s="{0}e".format(listeR[i][j]),size=10)

    titre="Evolution du top 3 de {0} 20{1}".format(ligne["Args1"],ligne["Args2"])
    if obj!="":
        titre+="\n{0}".format(getNomGraph(ctx,bot,option,int(obj)))
       
    plt.legend()
    plt.xlabel("Date")
    plt.title(titre)
    plt.tight_layout()
    plt.savefig("Graphs/otGraph")
    plt.clf()
