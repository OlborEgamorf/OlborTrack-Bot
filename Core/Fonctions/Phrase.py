def createPhrase(args:list) -> str:
    """Formate une liste de str pour en faire une phrase sans ' , pour que l'insertion dans les bases de données se fasse sans casse.
    Entrée : 
        args : liste de mots qui forme une phrase
    Sortie :
        descip : la phrase reconstituée"""
    descip=""
    for i in args:
        mot=""
        for lettre in i:
            if lettre=="'":
                mot+="’"
            else:
                mot+=lettre
        descip+=mot+" "
    return descip