def tempsVoice(nb:int) -> str:
    """Permet de formater un nombre en unité de temps, pour les statistiques vocales."""
    if int(nb)<60:
        count=str(nb)+"s"
    elif int(nb)<3600:
        count=str(int(nb)//60)+"m "+str(int(nb)%60)+"s"
    elif int(nb)<86400:
        count=str(int(nb)//3600)+"h "+str(int(nb)%3600//60)+"m "+str(int(nb)%3600%60)+"s"
    else:
        count=str(int(nb)//86400)+"j "+str(int(nb)%86400//3600)+"h "+str(int(nb)%86400%3600//60)+"m "+str(int(nb)%86400%3600%60)+"s"
    return count

def formatCount(option:str,count:int) -> str:
    """Permet de décider en fonction de l'option donnée de s'il faut formater en unité de temps ou non."""
    if option in ("Voice","Voicechan"):
        return tempsVoice(count)
    return count