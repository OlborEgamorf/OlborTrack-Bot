lettres="ABCDEFGHIJKLMNOPQRSTUVWXYZ"

def formatageVoiceEphem(pattern,user,nb):
    
    pattern.replace("{user}",user.name)
    pattern.replace("{nb}",nb)
    if (nb-1)//26>0:
        pattern.replace("{lettre}","{0}{1}".format(lettres[(nb-1)%26],(nb-1)//26))
    else:
        pattern.replace("{lettre}",lettres[(nb-1)%26])    
    
    return pattern