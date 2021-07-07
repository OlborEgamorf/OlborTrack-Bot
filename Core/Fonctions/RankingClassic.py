from Core.Fonctions.DichoTri import nombre 

def rankingClassic(table:list):
    """Cette fonction effectue un classement de type 'classique' d'une table donnée.
    Entrée :
        table : la liste de dictionnaires formant la table à classer"""
    table.sort(key=nombre,reverse=True)
    countTemp=0
    rankTemp=0
    for i in range(len(table)):
        if table[i]["Count"]==countTemp:
            table[i]["Rank"]=rankTemp
        else:
            countTemp=table[i]["Count"]
            rankTemp=i+1
            table[i]["Rank"]=rankTemp