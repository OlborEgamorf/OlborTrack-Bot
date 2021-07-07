import pandas as pd
from math import pi
from matplotlib import pyplot as plt

def graphSpider(table,id,color,name):
    dictValues={"Culture":[],"Divertissement":[],"Sciences":[],"Mythologie":[],"Sport":[],"Géographie":[],"Histoire":[],"Politique":[],"Art":[],"Célébrités":[],"Animaux":[],"Véhicules":[],"nom":["nom" for i in range(len(table))]}
    listeNext=[]
    listeNextTitre=[]
    for j in table:
        for i in j:
            dictValues[i["Categ"]].append(float(i["Exp"]))
            if listeNext.count(int(i["Next"]))==0:
                listeNext.append(int(i["Next"]))
                listeNextTitre.append("Nv. "+str(int(i["Niveau"])+1))
    for i in table[0]:
        if sum(dictValues[i["Categ"]])==0:
            del dictValues[i["Categ"]]

    df=pd.DataFrame(dictValues)

    angles = [n / float(len(dictValues)-1) * 2 * pi for n in range(len(dictValues)-1)]
    angles += angles[:1]

    ax = plt.subplot(111, polar=True)
    plt.xticks(angles[:-1], dictValues, color='grey', size=8)
    ax.set_rlabel_position(0)
    plt.yticks(listeNext, listeNextTitre, color="grey", size=7)
    plt.ylim(0,max(listeNext)+10)

    for i in range(len(table)):
        values=df.loc[i].drop('nom').values.flatten().tolist()
        values += values[:1]
        ax.plot(angles, values, linewidth=1, color=(color[i].r/256,color[i].g/256,color[i].b/256,1), linestyle='solid', label=name[i])
        ax.fill(angles, values, (), alpha=0.1)

    plt.title("Toile OT!trivia")
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    plt.tight_layout()
    plt.savefig("CSV/Graphs/"+str(id)+".png")
    plt.clf()
    return "CSV/Graphs/"+str(id)+".png"