lettres="ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def formatageVoiceEphem(pattern,user,nb):
    if pattern=="default":
        return "Salon de {0}".format(user.name)
    new=""
    membre=pattern.split("{user}")
    longMembre=len(membre)
    for i in range(longMembre):
        new+=membre[i]
        if i!=longMembre-1:
            new+="{0}".format(user.name)
    
    newN=""
    nbSalon=new.split("{nb}")
    longNb=len(nbSalon)
    for i in range(longNb):
        newN+=nbSalon[i]
        if i!=longNb-1:
            newN+="{0}".format(nb)

    newG=""
    lettre=newN.split("{lettre}")
    longLettre=len(lettre)
    for i in range(longLettre):
        newG+=lettre[i]
        if i!=longLettre-1:
            if (nb-1)//26>0:
                newG+="{0}{1}".format(lettres[(nb-1)%26],(nb-1)//26)
            else:
                newG+="{0}".format(lettres[(nb-1)%26])
    
    return newG