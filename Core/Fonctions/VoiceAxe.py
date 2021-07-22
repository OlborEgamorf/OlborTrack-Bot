dictNameAxis={"Messages":"Messages","Salons":"Messages","Freq":"Messages","Mots":"Mots","Emotes":"Utilisations","Reactions":"Utilisations","Mentions":"Mentions","Mentionne":"Mentions","Divers":"Nombre"}

def voiceAxe(option:str,listeY:list,plt,xy:str) -> int:
    """Pour les graphiques, décide s'il faut convertir les valeurs d'un des axes en minutes, heures ou jours si l'option est une stat vocale. Détermine aussi le nom de l'axe.
    
    Entrées :

            option : l'option du graphique
            listeY : les valeurs sur l'axe
            plt : pyplot
            xy : l'axe à changer
            
    Sortie :
            
            div : si d'autres valeurs sont à modifier, renvoie le diviseur à appliquer"""
    if option in ("Voice","Voicechan"):
        maxi=max(listeY)
        if maxi<60:
            mesure="(en secondes)"
            div=1
        elif maxi<3600:
            mesure="(en minutes)"
            div=60
        elif maxi<86400:
            mesure="(en heures)"
            div=3600
        else:
            mesure="(en jours)"
            div=86400
        for i in range(len(listeY)):
            listeY[i]=round(listeY[i]/div,2)
        if xy=="x":
            plt.xlabel("Temps passé en vocal {0}".format(mesure))
        else:
            plt.ylabel("Temps passé en vocal {0}".format(mesure))
    else:
        if xy=="x":
            plt.xlabel(dictNameAxis[option])
        else:
            plt.ylabel(dictNameAxis[option])
        div=1
    return div