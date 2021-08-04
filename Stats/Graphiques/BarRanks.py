from matplotlib import pyplot as plt
import matplotlib.image as mpimg
from time import strftime
from matplotlib.offsetbox import AnnotationBbox, OffsetImage
from colorthief import ColorThief
from Core.Fonctions.GraphTheme import setThemeGraph
from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.GetTable import getTableRoles, getTableRolesMem
from Core.Fonctions.GetNom import getNomGraph
from Core.Fonctions.WebRequest import getAvatar, getImage
from Core.Fonctions.VoiceAxe import voiceAxe
colorOT=(110/256,200/256,250/256,1)
tableauMois={"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre","TO":"TO","1":"janvier","2":"février","3":"mars","4":"avril","5":"mai","6":"juin","7":"juillet","8":"aout","9":"septembre","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","glob":"GL","to":"TO"}

async def graphRank(ligne,ctx,bot,option,guildOT):
    
    listeX,listeY,listeN,listeC=[],[],[],[]
    setThemeGraph(plt)
    fig,ax=plt.subplots()
    mois,annee,obj=ligne["Args1"],ligne["Args2"],ligne["Args3"]
    
    if ligne["Commande"]=="rank":
        connexion,curseur=connectSQL(ctx.guild.id,option,"Stats",tableauMois[mois],annee)
        if obj=="None":
            table=curseur.execute("SELECT * FROM {0}{1} WHERE Rank<=15 ORDER BY Rank DESC".format(mois,annee)).fetchall()
        else:
            table=curseur.execute("SELECT * FROM {0}{1}{2} WHERE Rank<=15 ORDER BY Rank DESC".format(mois,annee,obj)).fetchall()
        colorBase=colorOT
    elif ligne["Commande"]=="roles":
        connexion,curseur=connectSQL(ctx.guild.id,option,"Stats",tableauMois[mois],annee)
        obj="" if ligne["Args3"]=="None" else ligne["Args3"]
        if ligne["Args4"]=="None":
            table=getTableRoles(curseur,ctx.guild,"{0}{1}{2}".format(mois,annee,obj),ligne["Tri"])
        else:
            table=getTableRolesMem(curseur,ctx.guild,int(ligne["Args4"]),"{0}{1}{2}".format(mois,annee,obj),ligne["Tri"])
        table.reverse()
        if len(table)>15:
            table=table[0:15]
        colorBase=colorOT
    else:
        connexion,curseur=connectSQL(ctx.guild.id,option,"Stats",mois,annee)
        table=curseur.execute("SELECT * FROM perso{0}{1}{2} ORDER BY Count DESC LIMIT 15".format(mois,annee,ligne["AuthorID"])).fetchall()
        table.reverse()
        user=getNomGraph(ctx,bot,"Messages",ligne["AuthorID"])
        if user!=None:
            colorBase=(user.color.r/256,user.color.g/256,user.color.b/256,1)

    borne=len(table)
    listeL=[i for i in range(borne)]
    
    for i in range(borne):
        listeY.append(table[i]["Count"])
        listeC.append(colorBase)
        try:
            if ligne["Commande"]=="roles" and ligne["Args4"]=="None":
                role=ctx.guild.get_role(table[i]["ID"])
                listeC[i]=(role.color.r/256,role.color.g/256,role.color.b/256,1)
                if len(role.name)<=15:
                    listeN.append("{0}".format(role.name))
                else:
                    listeN.append("{0}...".format(role.name[0:15]))
            elif option in ("Salons","Emotes","Reactions","Voicechan") and obj=="None":
                if option in ("Emotes","Reactions"):
                    try:
                        open("PNG/{0}.png".format(table[i]["ID"]))
                    except:
                        await getImage(table[i]["ID"])
                    addImage(table,ax,i)
                    color=ColorThief("PNG/{0}.png".format(table[i]["ID"])).get_color(quality=1)
                    listeC[i]=(color[0]/256,color[1]/256,color[2]/256,1)
                    listeN.append("{0}".format(getNomGraph(ctx,bot,option,table[i]["ID"])))
                else:
                    if guildOT.chan[table[i]["ID"]]["Hide"]:
                        listeY[i]=0
                        listeN.append("")
                    else:
                        listeN.append(getNomGraph(ctx,bot,option,table[i]["ID"]))
            elif option in ("Messages","Mots","Voice","Mentions","Mentionne") or obj!="None":
                if guildOT.users[table[i]["ID"]]["Hide"]:
                    listeY[i]=0
                    listeN.append("")
                elif guildOT.users[table[i]["ID"]]["Leave"]:
                    listeN.append("Ancien membre")
                else:
                    user=getNomGraph(ctx,bot,"Messages",table[i]["ID"])
                    await getAvatar(user)
                    addImage(table,ax,i)
                    if len(user.name)<=15:
                        listeN.append("{0}".format(user.name))
                    else:
                        listeN.append("{0}...".format(user.name[0:15]))
                    listeC[i]=(user.color.r/256,user.color.g/256,user.color.b/256,1)
            else:
                listeN.append(getNomGraph(ctx,bot,option,table[i]["ID"]))
        except:
            listeN.append("??")
    
    voiceAxe(option,listeY,plt,"x")

    plt.barh(listeL, listeY, color=listeC,edgecolor="white")
    plt.yticks(listeL, listeN)
    
    if table[0]["Annee"]=="GL":
        titre="Classement global - {0} - {1}".format(ctx.guild.name,option)   
    else:
        titre="Classement {0} 20{1} - {2} - {3}".format(tableauMois[table[0]["Mois"]],table[0]["Annee"],ctx.guild.name,option)
    
    if obj not in ("None",""):
        titre+="\n{0}".format(getNomGraph(ctx,bot,option,int(obj)))
    if ligne["Commande"]=="roles" and ligne["Args4"]!="None":
        titre+="\n{0}".format(getNomGraph(ctx,bot,"Roles",int(ligne["Args4"])))

    plt.title(titre,fontsize=10)
    for i in range(borne):
        plt.text(x=listeY[i], y=listeL[i], s=listeY[i], size=8)

    plt.subplots_adjust(left=0.20)
    plt.tight_layout()
    plt.savefig("Graphs/otGraph")
    plt.clf()
    plt.close()

def addImage(table,ax,i):
    image = mpimg.imread("PNG/{0}.png".format(table[i]["ID"])) # Lecture
    imagebox = OffsetImage(image, zoom=1.5/len(table)) # Zoom
    ab = AnnotationBbox(imagebox, (0,i), frameon=False, box_alignment=(0,0.5)) # Coordonnées
    ax.add_artist(ab)
