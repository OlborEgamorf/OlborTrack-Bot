
import sys

import matplotlib.patches as mpatches
from Core.Fonctions.GetNom import getNomGraph
from Core.Fonctions.GraphTheme import setThemeGraph
from Core.Fonctions.VoiceAxe import voiceAxe
from matplotlib import pyplot as plt
import matplotlib.patches
from Stats.SQL.ConnectSQL import connectSQL

colorOT=(110/256,200/256,250/256,1)
tableauMois={"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre","TO":"TOTAL","1":"janvier","2":"février","3":"mars","4":"avril","5":"mai","6":"juin","7":"juillet","8":"aout","9":"septembre","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12"}

def graphGroupedCompare(ligne,ctx,option,bot,guildOT):
    colors={ligne["AuthorID"]:colorOT,int(ligne["Args4"]):colorOT}
    noms={ligne["AuthorID"]:"Ancien membre",int(ligne["Args4"]):"Ancien membre"}
    author,table=ligne["AuthorID"],ligne["AuthorID"]
    connexion,curseur=connectSQL(ctx.guild.id,option,"Stats",ligne["Args2"],ligne["Args3"])
    table=curseur.execute("SELECT * FROM perso{0}{1}{2} ORDER BY Count DESC LIMIT 10".format(ligne["Args2"],ligne["Args3"],ligne["AuthorID"])).fetchall()
    listeX,listeY,listeSN,listeSX,listeA=[],[],[],[],[]
    pos=0
    setThemeGraph(plt)
    plt.subplots(figsize=(6.4,4.8))
    for i in range(len(table)):
        center=0
        listeX.append(pos)
        listeY.append(table[i]["Count"])
        listeA.append(author)
        pos+=1
        center+=1

        count=curseur.execute("SELECT * FROM perso{0}{1}{2} WHERE ID={3}".format(ligne["Args2"],ligne["Args3"],ligne["Args4"],table[i]["ID"])).fetchone()
        if count!=None:
            listeY.append(count["Count"])
            listeA.append(int(ligne["Args4"]))
            listeX.append(pos)
            pos+=1
            center+=1

        listeSX.append(pos-center//2-1)
        listeSN.append(getNomGraph(ctx,bot,option,table[i]["ID"]))
        pos+=0.75

    voiceAxe(option,listeY,plt,"y")
    user1=ctx.guild.get_member(author)
    user2=ctx.guild.get_member(int(ligne["Args4"]))

    if user1!=None:
        colors[user1.id]=(user1.color.r/256,user1.color.g/256,user1.color.b/256,1)
        noms[user1.id]=user1.name
    if user2!=None:
        colors[user2.id]=(user2.color.r/256,user2.color.g/256,user2.color.b/256,1)
        noms[user2.id]=user2.name

    if colors[ligne["AuthorID"]]==colors[int(ligne["Args4"])]:
        colors[int(ligne["Args4"])]=(colors[int(ligne["Args4"])][0],colors[int(ligne["Args4"])][1],colors[int(ligne["Args4"])][2],0.5)

    plt.bar(listeX, listeY, color=[colors[i] for i in listeA], width=1, edgecolor='white')
    plt.xticks(listeSX, listeSN,rotation=45)
    plt.xlabel("Mois")

    for i in range(len(listeY)):
        plt.text(x=listeX[i], y=listeY[i], s=listeY[i], size=8, ha="center")

    plt.legend([matplotlib.patches.Patch(color=colors[ligne["AuthorID"]]),matplotlib.patches.Patch(color=colors[int(ligne["Args4"])])],[noms[ligne["AuthorID"]],noms[int(ligne["Args4"])]])

    plt.title("Groupement comparaison\n{0} - {1}/{2}".format(option,ligne["Args2"],ligne["Args3"]))
    plt.tight_layout()
    plt.savefig("Graphs/otGraph")
    plt.clf()