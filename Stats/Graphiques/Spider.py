import pandas as pd
from math import pi
from matplotlib import pyplot as plt
from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.GraphTheme import setThemeGraph

async def graphSpider(ligne,ctx,option,bot,guildOT):
    setThemeGraph(plt)
    plt.subplots(figsize=(6.4,4.8))
    connexion,curseur=connectSQL("OT",ligne["AuthorID"],"Trivial",None,None)
    table=curseur.execute("SELECT * FROM trivial{0} WHERE Categ<> 'Global'".format(ligne["AuthorID"])).fetchall()
    
    dictValues={}
    listeNext,listeNextTitre=[],[]
    for i in table:
        if int(i["Exp"])==0:
            continue
        dictValues[i["Categ"]]=[i["Exp"]]
        if listeNext.count(i["Next"])==0:
            listeNext.append(i["Next"])
            listeNextTitre.append("Nv. {0}".format(i["Niveau"]+1))
    dictValues["nom"]=["nom"]
    df=pd.DataFrame(dictValues)
    liste=list(dictValues.keys())
    liste.remove("nom")
    angles = [n / float(len(dictValues)-1) * 2 * pi for n in range(len(dictValues)-1)]
    angles += angles[:1]

    ax = plt.subplot(111, polar=True)
    plt.xticks(angles[:-1], liste, color='grey', size=8)
    ax.set_rlabel_position(0)
    plt.yticks(listeNext, listeNextTitre, color="grey", size=7)
    plt.ylim(0,max(listeNext)+10)
    
    user=ctx.guild.get_member(ligne["AuthorID"])
    if user!=None:
        plt.title("Toile OT!trivial\n{0}".format(user.name))
        color=(user.color.r/256,user.color.g/256,user.color.b/256,1)
    else:
        plt.title("Toile OT!trivial")
        color=(110/256,200/256,250/256,1)

    values=df.loc[0].drop("nom").values.flatten().tolist()
    values += values[:1]
    ax.plot(angles, values, linewidth=1, color=color, linestyle='solid', label="Exp")
    ax.fill(angles, values, (), alpha=0.1)

    
    plt.legend(loc='upper right', bbox_to_anchor=(0.1, 0.1))
    plt.tight_layout()
    plt.savefig("Graphs/otGraph")
    plt.clf()