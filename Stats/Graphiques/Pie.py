### CODE OBSOLETE : N'EST ACTUELLEMENT PLUS UTILISÉ

from matplotlib import pyplot as plt
from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.GraphTheme import setThemeGraph
from Core.Fonctions.GetNom import getNomGraph
colorOT=(110/256,200/256,250/256,1)
tableauMois={"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre","TO":"TOTAL","1":"janvier","2":"février","3":"mars","4":"avril","5":"mai","6":"juin","7":"juillet","8":"aout","9":"septembre","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","glob":"GL","to":"TO"}

async def graphPie(ligne,ctx,bot,option,guildOT):
    plt.subplots(figsize=(6.4,4.8))
    setThemeGraph(plt)
    connexion,curseur=connectSQL(ctx.guild.id,option,"Stats",tableauMois[ligne["Args1"]],ligne["Args2"])
    listeX,listeY,listeC=[],[],[]
    obj="" if ligne["Args3"]=="None" else ligne["Args3"]
    table=curseur.execute("SELECT * FROM {0}{1}{2} ORDER BY Rank ASC".format(ligne["Args1"],ligne["Args2"],obj)).fetchall()
    percent=int(round(15*len(table)/100,0))
    countPC,countO=0,0
    for i in range(percent):
        countPC+=table[i]["Count"]
    for i in range(percent,len(table)):
        countO+=table[i]["Count"]

    pcPC=100*round(countPC/(countPC+countO),2)
    pcO=100*round(countO/(countPC+countO),2)
    values=[countPC,countO]
    names=["Le top 15% représente\n {0}% des messages\n{1} membres\n{2} messages".format(pcPC,percent,countPC),"Les 85% restants\n{0}% des messages\n{1} membres\n{2} messages".format(pcO,len(table)-percent,countO)]
    plt.pie(values,labels=names,labeldistance=1.1,colors=[colorOT,"grey"])
    
    if table[0]["Annee"]=="GL":
        titre="Proportions global - {0} - {1}".format(ctx.guild.name,option)   
    else:
        titre="Proportions {0} 20{1} - {2} - {3}".format(tableauMois[table[0]["Mois"]],table[0]["Annee"],ctx.guild.name,option)
    
    if obj!="":
        titre+="\n{0}".format(getNomGraph(ctx,bot,option,int(obj)))

    plt.title(titre,fontsize=10)
    plt.tight_layout()
    plt.savefig("Graphs/otGraph")
    plt.clf()