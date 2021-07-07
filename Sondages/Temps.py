### OBSOLETE, POLL A REFAIRE ENTIEREMENT

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
    assert mode.lower() in ("s","m","h","d"), "Je n'ai pas compris le temps que vous voulez mettre...\nLe temps doit être un nombre suivi de s (pour secondes), m (pour minutes), h (pour heures) ou d (pour jours).\nPour mettre un nombre à virgule, mettez un point à la place de la virgule. (2.5m ou lieu de 2,5m par exemple)"
    if mode.lower()=="m":
        somme=somme*60
    elif mode.lower()=="h":
        somme=somme*3600
    elif mode.lower()=="d":
        somme=somme*86400
    somme=round(somme,0)
    assert somme<2592000, "Pas plus de trente jours !"
    return int(somme)