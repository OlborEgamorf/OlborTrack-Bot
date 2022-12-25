from Stats.SQL.Execution import executeStats, executeStatsObj
from Core.Fonctions.Convertisseurs import inverse

dictTrivia={"Images":3,"GIFs":2,"Fichiers":1,"Liens":4,"Réponse":5,"Réactions":6,"Edits":7,"Emotes":8,"Messages":9,"Mots":10,"Vocal":11,"Stickers":12}

def exeDiversSQL(user,salon,dicDivers,option,curseur):
    for i in dicDivers:
        if dicDivers[i]!=0:
            dicDivers[i]=inverse(option,dicDivers[i])
            executeStatsObj("divers",user,salon,dictTrivia[i],dicDivers[i],curseur)