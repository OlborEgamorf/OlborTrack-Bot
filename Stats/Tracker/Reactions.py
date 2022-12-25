from Core.Fonctions.Convertisseurs import inverse
from Stats.SQL.ConnectSQL import connectSQL
from Stats.SQL.Execution import executeStatsObj
from Stats.SQL.Verification import verifExecSQL

class SimulID:
    def __init__(self,id):
        self.id=id
        self.bot=False

async def exeReactClient(option,channel,react,user,guild):
    user,channel=SimulID(user),SimulID(channel)
    if verifExecSQL(guild,channel,user)==False or bool(guild.mstats[3]["Statut"])==False:
        return

    connexion,curseur=connectSQL(guild)
    
    if len(react.name)==1:
        executeStatsObj("reactions",user,channel,ord(react.name),inverse(option,1),curseur)
    elif react.id==None:
        pass
    else:
        executeStatsObj("reactions",user,channel,react.id,inverse(option,1),curseur)
    
    connexion.commit()
