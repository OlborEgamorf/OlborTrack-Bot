from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.Convertisseurs import inverse
from Stats.SQL.Execution import exeClassic, exeObj

def exeMentionsSQL(id,dictPing,guild,option):
    connexionGuild,curseurGuild=connectSQL(guild.id,"Guild","Guild",None,None)
    for i in dictPing:
        dictPing[i]=inverse(option,dictPing[i])
        exeClassic(dictPing[i],id,"Mentionne",curseurGuild,guild)
        exeClassic(dictPing[i],i,"Mentions",curseurGuild,guild)
        exeObj(dictPing[i],i,id,True,guild,"Mentions")
        exeObj(dictPing[i],id,i,True,guild,"Mentionne")