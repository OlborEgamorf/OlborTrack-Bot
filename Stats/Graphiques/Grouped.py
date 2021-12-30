from Core.Fonctions.GetNom import getNomGraph
from Core.Fonctions.GetTable import getTablePerso
from Core.Fonctions.GraphTheme import setThemeGraph
from Core.Fonctions.VoiceAxe import voiceAxe
from matplotlib import pyplot as plt

tableauMois={"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre","TO":"TOTAL","1":"janvier","2":"février","3":"mars","4":"avril","5":"mai","6":"juin","7":"juillet","8":"aout","9":"septembre","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12"}

def graphGroupedMois(ligne,ctx,option,bot):
    colors={"15":"grey","16":"pink","17":"purple","18":"orange","19":"green","20":"red","21":"blue"}
    author=ligne["AuthorID"]
    if ligne["Args1"]=="None":
        table=getTablePerso(ctx.guild.id,option,author,False,"M","periodAsc")
    else:
        table=getTablePerso(ctx.guild.id,option,author,ligne["Args1"],"M","periodAsc")
    annees,mois=[],[]
    for i in table:
        if i["Mois"] not in mois:
            mois.append(i["Mois"])
        if i["Annee"] not in annees:
            annees.append(i["Annee"]) 
    annees.sort()
    mois.sort()
    dictTable={i["Annee"]+i["Mois"]:i for i in table}
    listeX,listeY,listeSN,listeSX,listeA=[],[],[],[],[]
    pos=0
    setThemeGraph(plt)
    plt.subplots(figsize=(6.4,4.8))
    for i in mois:
        center=0
        for j in annees:
            try:
                count=dictTable[j+i]
            except:
                continue
            listeY.append(count["Count"])
            listeX.append(pos)
            listeA.append(j)
            pos+=1
            center+=1
        listeSX.append(pos-center//2-1)
        listeSN.append(tableauMois[i])
        pos+=0.75

    voiceAxe(option,listeY,plt,"y")
    for i in range(len(listeA)):
        plt.text(x=listeX[i], y=listeY[i], s="20{0}".format(listeA[i]), size=5, fontproperties="italic", ha="center") 

    plt.bar(listeX, listeY, color=[colors[i] for i in listeA], width=1, edgecolor='white')
    plt.xticks(listeSX, listeSN,rotation=45)
    plt.xlabel("Mois")
    
    if option in ("Messages","Mots","Voice","Mentions","Mentionne") or ligne["Args1"]!="None":
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
