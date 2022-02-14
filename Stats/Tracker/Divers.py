from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.Convertisseurs import inverse
from Stats.SQL.Execution import exeClassic, exeObj

dictTrivia={"Images":3,"GIFs":2,"Fichiers":1,"Liens":4,"Réponse":5,"Réactions":6,"Edits":7,"Emotes":8,"Messages":9,"Mots":10,"Vocal":11,"Stickers":12}

def exeDiversSQL(id,dicDivers,option,guild,conG,curG):
    if conG==None and curG==None:
        conG,curG=connectSQL(guild.id,"Guild","Guild",None,None)
    for i in dicDivers:
        if dicDivers[i]!=0:
            dicDivers[i]=inverse(option,dicDivers[i])
            exeClassic(dicDivers[i],dictTrivia[i],"Divers",curG,guild)
            exeObj(dicDivers[i],dictTrivia[i],id,True,guild,"Divers")
    conG.commit()