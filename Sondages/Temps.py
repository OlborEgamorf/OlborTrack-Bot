from Core.Fonctions.Convertisseurs import convZero
from time import strftime

dictLimite={"01":31,"02":28,"03":31,"04":30,"05":31,"06":30,"07":31,"08":31,"09":30,"10":31,"11":30,"12":31}

def gestionTemps(tempo):
    mode=tempo[len(tempo)-1]
    somme=""
    add=True
    for i in range(len(tempo)-1):
        somme=somme+tempo[i]
    try:
        somme=float(somme)
    except:
        add=False
    assert add==True, "Je n'ai pas compris le temps que vous voulez mettre...\nLe temps doit être un nombre suivi de s (pour secondes), m (pour minutes), h (pour heures) ou d (pour jours).\nPour mettre un nombre à virgule, mettez un point à la place de la virgule. (2.5m ou lieu de 2,5m par exemple)"
    assert somme>=0, "Je ne peux pas remonter dans le temps !"
    assert mode.lower() in ("s","m","h","d"), "Je n'ai pas compris le temps que vous voulez mettre...\nLe temps doit être un nombre suivi de s (pour secondes), m (pour minutes), h (pour heures) ou j (pour jours).\nPour mettre un nombre à virgule, mettez un point à la place de la virgule. (2.5m ou lieu de 2,5m par exemple)"
    if mode.lower()=="m":
        somme=somme*60
    elif mode.lower()=="h":
        somme=somme*3600
    elif mode.lower()=="j":
        somme=somme*86400
    somme=round(somme,0)
    assert somme<2592000, "Pas plus de trente jours !"
    return int(somme)


def footerTime(temps):
    '''Timer de la commande OT!polltime.\n
    Temps est un int, le nombre de secondes que la tache doit tenir.'''
    jours=(int(strftime("%d"))+temps//86400)
    if jours>dictLimite[strftime("%m")]:
        jours=jours-dictLimite[strftime("%m")]
        mois=int(strftime("%m"))+1
    else:
        mois=strftime("%m")
    minutes=(int(strftime("%M"))+temps//60)%60
    if (int(strftime("%M"))+temps//60)//60>0:
        heures=(int(strftime("%H")))+(int(strftime("%M"))+temps//60)//60%24
    else:
        heures=strftime("%H")
    secondes=(int(strftime("%S"))+temps)%60
    heures=convZero(heures)
    minutes=convZero(minutes)
    jours=convZero(jours)
    mois=convZero(mois)
    secondes=convZero(secondes)
    textFoot="Fin : "+str(jours)+"/"+str(mois)+" - "+str(heures)+":"+str(minutes)+":"+str(secondes)
    return textFoot