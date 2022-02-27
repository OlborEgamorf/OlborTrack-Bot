import datetime
import time
from Core.Fonctions.Convertisseurs import convZero

dictLimite={"01":31,"02":28,"03":31,"04":30,"05":31,"06":30,"07":31,"08":31,"09":30,"10":31,"11":30,"12":31}

def gestionTemps(tempo):
    mode=tempo[-1]
    assert mode.lower() in ("s","m","h","j"), "Vous devez baliser les périodes avec s (pour secondes), m (pour minutes), h (pour heures) ou j (pour jours)."
    tempo=tempo.lower()
    listeBalise=["s","m","h","j"]
    listeMulti={"s":1,"m":60,"h":3600,"j":86400}
    balise=0
    count=0
    for i in range(len(tempo)):
        if tempo[i] in listeBalise:
            try:
                count+=listeMulti[tempo[i]]*float(tempo[balise:i])
                balise=i+1
            except:
                raise AssertionError("Je n'ai pas compris le temps que vous voulez mettre...\nLe temps doit être balisé avec s (pour secondes), m (pour minutes), h (pour heures) ou j (pour jours).\nPour mettre un nombre à virgule, mettez un point à la place de la virgule. (2.5m ou lieu de 2,5m par exemple)")
    assert count<7776000, "Vous ne pouvez pas configurer plus de 90 jours !"
    assert count>4, "Vous devez mettre plus de 4 secondes !"
    return int(count)

def footerTime(temps):
    '''Timer de la commande OT!polltime.\n
    Temps est un int, le nombre de secondes que la tache doit tenir.'''
    return datetime.datetime.fromtimestamp(time.time()+temps).strftime('%d/%m/%Y - %H:%M:%S')