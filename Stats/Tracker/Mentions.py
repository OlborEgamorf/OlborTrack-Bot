from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.Convertisseurs import inverse
from Stats.SQL.Execution import exeObj

def exeMentionsSQL(id,dictPing,guild,option):
    for i in dictPing:
        dictPing[i]=inverse(option,dictPing[i])
        exeObj(dictPing[i],i,id,True,guild,"Mentions")
        exeObj(dictPing[i],id,i,True,guild,"Mentionnes")