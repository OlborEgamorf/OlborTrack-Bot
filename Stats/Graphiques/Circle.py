from matplotlib import pyplot as plt
import pandas as pd
import circlify
from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.GraphTheme import setThemeGraph
from Core.Fonctions.GetTable import getTableRoles, getTableRolesMem
from Core.Fonctions.GetNom import getNomGraph
from Core.Fonctions.TempsVoice import tempsVoice
colorOT=(110/256,200/256,250/256,1)
tableauMois={"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre","TO":"TOTAL","1":"janvier","2":"février","3":"mars","4":"avril","5":"mai","6":"juin","7":"juillet","8":"aout","9":"septembre","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","glob":"GL","to":"TO"}

async def graphCircle(ligne,ctx,bot,option,guildOT):
    setThemeGraph(plt)
    fig, ax = plt.subplots(figsize=(6.4,6.4))
    listeX,listeY,listeC=[],[],[]
    obj=ligne["Args3"] if ligne["Args3"]!="None" else ""
    if ligne["Commande"]=="perso":
        connexion,curseur=connectSQL(ctx.guild.id,option,"Stats",ligne["Args1"],ligne["Args2"])
        table=curseur.execute("SELECT * FROM perso{0}{1}{2} WHERE Count>0 ORDER BY Count DESC LIMIT 100".format(ligne["Args1"],ligne["Args2"],ligne["AuthorID"])).fetchall()
        table.reverse()
    elif ligne["Commande"]=="roles":
        connexion,curseur=connectSQL(ctx.guild.id,option,"Stats",tableauMois[ligne["Args1"]],ligne["Args2"])
        obj="" if ligne["Args3"]=="None" else ligne["Args3"]
        if ligne["Args4"]=="None":
            table=getTableRoles(curseur,ctx.guild,"{0}{1}{2}".format(ligne["Args1"],ligne["Args2"],obj),ligne["Tri"])
        else:
            table=getTableRolesMem(curseur,ctx.guild,int(ligne["Args4"]),"{0}{1}{2}".format(ligne["Args1"],ligne["Args2"],obj),ligne["Tri"])
        table.reverse()
        if len(table)>15:
            table=table[0:15]
    else:
        connexion,curseur=connectSQL(ctx.guild.id,option,"Stats",tableauMois[ligne["Args1"]],ligne["Args2"])
        table=curseur.execute("SELECT * FROM {0}{1}{2} WHERE Rank<=100 AND Count>0 ORDER BY Rank DESC".format(ligne["Args1"],ligne["Args2"],obj)).fetchall()
    delete=0
    for i in range(len(table)):
        listeX.append(table[i]["Count"])
        listeC.append(colorOT)
        try:
            if ligne["Commande"]=="roles" and ligne["Args4"]=="None":
                role=ctx.guild.get_role(table[i]["ID"])
                listeC[i]=(role.color.r/256,role.color.g/256,role.color.b/256,1)
                if len(role.name)<=15:
                    listeY.append("{0}".format(role.name))
                else:
                    listeY.append("{0}...".format(role.name[0:15]))
            elif option in ("Salons","Voicechan") and obj=="":
                if guildOT.chan[table[i]["ID"]]["Hide"]:
                    del listeX[i]
                    del listeC[i]
                    delete+=1
                else:
                    listeY.append(getNomGraph(ctx,bot,option,table[i]["ID"]))
            elif option in ("Messages","Mots","Voice") or obj!="":
                if guildOT.users[table[i]["ID"]]["Hide"]:
                    del listeX[i]
                    del listeC[i]
                    delete+=1
                elif guildOT.users[table[i]["ID"]]["Leave"]:
                    if table[i]["Rank"]>15:
                        listeY.append("??")
                    else:
                        listeY.append("Ancien membre")
                else:
                    user=getNomGraph(ctx,bot,"Messages",table[i]["ID"])
                    listeC[i]=(user.color.r/256,user.color.g/256,user.color.b/256,1)
                    if table[i]["Rank"]>15:
                        listeY.append("??")
                    else:
                        listeY.append(user.name) 
            else:
                listeY.append(getNomGraph(ctx,bot,option,table[i]["ID"]))  
            if len(listeY[i-delete])>15:
                listeY[i-delete]="{0}...".format(listeY[i-delete][0:15])     
        except:
            listeY.append("??")

    df=pd.DataFrame({"Noms":listeY,"Valeurs":listeX,"Couleurs":listeC})

    circles = circlify.circlify(df['Valeurs'].tolist(), show_enclosure=False, target_enclosure=circlify.Circle(x=0, y=0, r=1))
    lim = max(max(abs(circle.x) + circle.r, abs(circle.y) + circle.r,) for circle in circles)
    ax.axis('off')
    plt.xlim(-lim, lim)
    plt.ylim(-lim, lim)
    for circle,nom,count,color in zip(circles,df["Noms"],df["Valeurs"],df["Couleurs"]):
        x, y, r = circle
        ax.add_patch(plt.Circle((x, y), r, linewidth=2, fill=True, facecolor=color, edgecolor="black"))
        if nom!="??":
            if option in ("Voice","Voicechan"):
                plt.annotate("{0}\n{1}".format(nom,tempsVoice(count)),(x,y),va="center",ha="center")
            else:
                plt.annotate("{0}\n{1}".format(nom,count),(x,y),va="center",ha="center")

    if table[0]["Annee"]=="GL":
        titre="Bulles global - {0} - {1}".format(ctx.guild.name,option)   
    else:
        titre="Bulles {0} 20{1} - {2} - {3}".format(tableauMois[table[0]["Mois"]],table[0]["Annee"],ctx.guild.name,option)
    
    if obj not in ("None",""):
        titre+="\n{0}".format(getNomGraph(ctx,bot,option,int(obj)))
    if ligne["Commande"]=="roles" and ligne["Args4"]!="None":
        titre+="\n{0}".format(getNomGraph(ctx,bot,"Roles",int(ligne["Args4"])))
    elif ligne["Args4"]!="None":
        titre+="\n{0}".format(getNomGraph(ctx,bot,"Messages",int(ligne["AuthorID"])))

    plt.title(titre)
    plt.tight_layout()
    plt.savefig("Graphs/otGraph")
    plt.clf()