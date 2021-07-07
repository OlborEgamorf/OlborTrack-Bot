def animateGraph(i,*fargs):
    ranks,barcollection,graphiqueOT,plt=fargs
    maxi=0
    if i>=len(graphiqueOT):
        pass
    else:
        ligne=graphiqueOT[i]
        if i%30==0:
            date=str(ligne[0]["date"])
            plt.title("Classement au {0}/{1}/{2}".format(date[4:6],date[2:4],date[0:2]))
        if i!=0:
            if getRankList(ligne)!=getRankList(graphiqueOT[i-1]):
                labels=setlabel(ligne,ranks)
                plt.yticks(labels[1], labels[0],va="baseline")
        else:
            labels=setlabel(ligne,ranks)
            plt.yticks(labels[1], labels[0],va="baseline")
    
        for j, b in enumerate(barcollection):
            if i!=0:
                if graphiqueOT[i-1][j]["y"]!=ligne[j]["y"]:
                    b.set_width(ligne[j]["y"])
                if graphiqueOT[i-1][j]["x"]!=ligne[j]["x"]:
                    b.set_y(ligne[j]["x"])
            else:
                b.set_width(ligne[j]["y"])
                b.set_y(ligne[j]["x"])
            maxi=max(maxi,ligne[j]["y"])
        plt.xlim(0,maxi+maxi*0.12)

def setlabel(liste,i):
    listeN=[]
    listeP=[]
    for j in liste:
        if j["x"]<i+1:
            listeN.append(j["name"])
            listeP.append(j["x"])
    return listeN, listeP

def getRankList(liste):
    return [h["x"] for h in liste]