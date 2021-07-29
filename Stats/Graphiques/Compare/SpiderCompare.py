import pandas as pd
from math import pi
from matplotlib import pyplot as plt
from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.GraphTheme import setThemeGraph
from Core.Fonctions.GetNom import getNomGraph
from Core.Fonctions.VoiceAxe import voiceAxe
colorOT=(110/256,200/256,250/256,1)
tableauMois={"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre","TO":"TOTAL","1":"janvier","2":"février","3":"mars","4":"avril","5":"mai","6":"juin","7":"juillet","8":"aout","9":"septembre","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","to":"TO","glob":"GL"}

async def graphSpiderCompare(ligne,ctx,bot,option,guildOT,curseur):
    setThemeGraph(plt)
    plt.subplots(figsize=(6.4,4.8))
    table=curseur.execute("SELECT * FROM perso{0}{1}{2} ORDER BY Count DESC LIMIT 10".format(ligne["Args2"],ligne["Args3"],ligne["AuthorID"])).fetchall()
    
    listeCount=[]
    dictValues={}
    listeNext,listeNextTitre=[],[]
    for i in table:
        listeCount.append(i["Count"])
        if i["Count"]==0:
            continue
        try:
            nom=getNomGraph(ctx,bot,option,i["ID"])
        except:
            nom=i["ID"]
        if nom not in dictValues:
            dictValues[nom]=[]
        dictValues[nom].append(i["Count"])
        count=curseur.execute("SELECT * FROM perso{0}{1}{2} WHERE ID={3}".format(ligne["Args2"],ligne["Args3"],ligne["Args4"],i["ID"])).fetchone()
        if count!=None:
            dictValues[nom].append(count["Count"])
        else:
            dictValues[nom].append(0)
    
    div=voiceAxe(option,listeCount,plt,"x")
    for i in dictValues:
        for j in range(len(dictValues[i])):
            dictValues[i][j]=round(dictValues[i][j]/div,2)
    
    dictValues["nom"]=["nom","nom"]
    df=pd.DataFrame(dictValues)
    liste=list(dictValues.keys())
    liste.remove("nom")
    angles = [n / float(len(dictValues)-1) * 2 * pi for n in range(len(dictValues)-1)]
    angles += angles[:1]

    ax = plt.subplot(111, polar=True)
    plt.xticks(angles[:-1], liste, color='grey', size=8)
    
    users=[ligne["AuthorID"],int(ligne["Args4"])]
    for i in range(2):
        user=ctx.guild.get_member(users[i])
        if user!=None:
            color=(user.color.r/256,user.color.g/256,user.color.b/256,1)
            nom=user.name
        else:
            color=(110/256,200/256,250/256,1)
            nom="Ancien membre"

        values=df.loc[i].drop("nom").values.flatten().tolist()
        values += values[:1]
        ax.plot(angles, values, linewidth=1, color=color, linestyle='solid', label=nom)
        ax.fill(angles, values, (), alpha=0.1)

    plt.title("Toile comparaison\n{0} - {1}/{2}".format(option,ligne["Args2"],ligne["Args3"]))
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    plt.tight_layout()
    plt.savefig("Graphs/otGraph")
    plt.clf()


async def graphSpiderComparePerso(ligne,ctx,bot,option,guildOT):
    setThemeGraph(plt)
    plt.subplots(figsize=(6.4,4.8))
    liste1=ligne["Args1"].split(" ")
    liste2=ligne["Args2"].split(" ")
    colors=[colorOT,"green"]
    
    author=ligne["AuthorID"]
    obj=ligne["Args3"]
    if obj=="None":
        obj=""
    tempOption=option
    if obj!="":
        if option=="Voicechan":
            option="Voice"
        else:
            option="Messages"

    if ligne["Commande"]=="compareServ":
        noms=["{0}/{1}".format(tableauMois[liste1[0]],liste1[1]),"{0}/{1}".format(tableauMois[liste2[0]],liste2[1])]
        connexion1,curseur1=connectSQL(ctx.guild.id,tempOption,"Stats",tableauMois[liste1[0]],liste1[1])
        connexion2,curseur2=connectSQL(ctx.guild.id,tempOption,"Stats",tableauMois[liste2[0]],liste2[1])
        table=curseur1.execute("SELECT * FROM {0}{1}{2} ORDER BY Count DESC LIMIT 10".format(liste1[0],liste1[1],obj)).fetchall()
    else:
        noms=["{0}/{1}".format(liste1[0],liste1[1]),"{0}/{1}".format(liste2[0],liste2[1])]
        connexion1,curseur1=connectSQL(ctx.guild.id,option,"Stats",liste1[0],liste1[1])
        connexion2,curseur2=connectSQL(ctx.guild.id,option,"Stats",liste2[0],liste2[1])
        table=curseur1.execute("SELECT * FROM perso{0}{1}{2} ORDER BY Count DESC LIMIT 10".format(liste1[0],liste1[1],author)).fetchall()
    
    listeCount=[]
    dictValues={}
    listeNext,listeNextTitre=[],[]
    for i in table:
        listeCount.append(i["Count"])
        if i["Count"]==0:
            continue
        try:
            nom=getNomGraph(ctx,bot,option,i["ID"])
            if obj!="" or option in ("Messages","Voice","Mots"):
                nom=nom.name
            if len(nom)>15:
                nom=nom[0:15]+"..."
        except:
            nom=i["ID"]
        if nom not in dictValues:
            dictValues[nom]=[]
        dictValues[nom].append(i["Count"])
        if ligne["Commande"]=="compareServ":
            count=curseur2.execute("SELECT * FROM {0}{1}{2} WHERE ID={3}".format(liste2[0],liste2[1],obj,i["ID"])).fetchone()
        else:
            count=curseur2.execute("SELECT * FROM perso{0}{1}{2} WHERE ID={3}".format(liste2[0],liste2[1],author,i["ID"])).fetchone()
        if count!=None:
            dictValues[nom].append(count["Count"])
        else:
            dictValues[nom].append(0)
    
    div=voiceAxe(option,listeCount,plt,"x")
    for i in dictValues:
        for j in range(len(dictValues[i])):
            dictValues[i][j]=round(dictValues[i][j]/div,2)
    
    dictValues["nom"]=["nom","nom"]
    df=pd.DataFrame(dictValues)
    liste=list(dictValues.keys())
    liste.remove("nom")
    angles = [n / float(len(dictValues)-1) * 2 * pi for n in range(len(dictValues)-1)]
    angles += angles[:1]

    ax = plt.subplot(111, polar=True)
    plt.xticks(angles[:-1], liste, color='grey', size=8)
    
    for i in range(2):

        values=df.loc[i].drop("nom").values.flatten().tolist()
        values += values[:1]
        ax.plot(angles, values, linewidth=1, color=colors[i], linestyle='solid', label=noms[i])
        ax.fill(angles, values, (), alpha=0.1)

    plt.title("Toile comparaison\n{0}".format(option))
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    plt.tight_layout()
    plt.savefig("Graphs/otGraph")
    plt.clf()