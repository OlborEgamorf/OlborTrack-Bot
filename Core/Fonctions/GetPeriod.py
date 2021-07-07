def getAnnee(arg:list) -> int:
    """Cette fonction permet d'extraire une année sous forme AA de la liste des arguments d'une commande
    Entrée : 
        arg : la liste des arguments
    Sortie :
        argE : l'année cherchée"""
    if len(arg)>2:
        try:
            argE=arg.split("[")[1]
            argE=arg.split("]")[0]
        except:
            argE=arg
        argE=argE[len(argE)-2:len(argE)]
    else:
        argE=arg
    return int(argE)

def getMois(arg:str) -> str:
    """Cette fonction permet d'extraire un mois  de la liste des arguments d'une commandeEntrée : 
        arg : la liste des arguments
    Sortie :
        le mois cherché"""
    if arg in ("1","01","janvier"):
        return "janvier"
    elif arg in ("2","02","fevrier","février"):
        return "février"
    elif arg in ("3","03","mars"):
        return "mars"
    elif arg in ("4","04","avril"):
        return "avril"
    elif arg in ("5","05","mai"):
        return "mai"
    elif arg in ("6","06","juin"):
        return "juin"
    elif arg in ("7","07","juillet"):
        return "juillet"
    elif arg in ("8","08","aout","août"):
        return "aout"
    elif arg in ("9","09","septembre"):
        return "septembre"
    elif arg in ("10","octobre"):
        return "octobre"
    elif arg in ("11","novembre"):
        return "novembre"
    elif arg in ("12","décembre","decembre"):
        return "décembre"