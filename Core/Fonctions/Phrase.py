def createPhrase(text:(str or list)) -> str:
    """Formate une liste de str pour en faire une phrase sans ' , pour que l'insertion dans les bases de données se fasse sans casse.
    Entrée : 
        args : liste de mots qui forme une phrase
    Sortie :
        descip : la phrase reconstituée"""
    if type(text) in (list, tuple):
        text=" ".join(text)
    return text.replace("'","’")