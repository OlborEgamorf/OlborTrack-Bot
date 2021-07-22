import pandas as pd
from math import pi
from matplotlib import pyplot as plt
from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.GraphTheme import setThemeGraph
from Core.Fonctions.GetNom import getNomGraph
from Core.Fonctions.VoiceAxe import voiceAxe

async def graphSpiderCompare(ligne,ctx,bot,option,guildOT):
    setThemeGraph(plt)
    plt.subplots(figsize=(6.4,4.8))
    connexion,curseur=connectSQL(ctx.guild.id,option,"Stats",ligne["Args2"],ligne["Args3"])
    table=curseur.execute("SELECT * FROM perso{0}{1}{2} ORDER BY Count DESC LIMIT 10".format(ligne["Args2"],ligne["Args3"],ligne["AuthorID"])).fetchall()
    
    listeCount=[]
    dictValues={}
    listeNext,listeNextTitre=[],[]
    for i in table:
        listeCount.append(i["Count"])
        if i["Count"]==0:
            continue
        nom=getNomGraph(ctx,bot,option,i["ID"])
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