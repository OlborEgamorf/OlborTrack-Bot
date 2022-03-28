dictPage={"+":1,"-":-1,None:0}

def setMax(nb:int) -> int:
    """Détermine le nombre maximal de pages pour une commande. Une page contient au maximum 15 éléments.
    Entrée : 

            nb : le nombre d'éléments au total
    Sortie :

            le nombre de page maximal"""
    if nb%15==0:
        return nb//15
    return nb//15+1

def setPage(page:int,pagemax:int,turn:(str or None)) -> int:
    """Détermine quelle est la page après un changement de page.

    Entrées :

            page : la page actuelle
            pagemax : le nombre de page maximal
            turn : action de changement de page ('+', '-' ou None)
    Sortie :

            la nouvelle page"""
    page+=dictPage[turn]
    if page==0:
        return pagemax
    elif page>pagemax:
        return 1 
    return page
