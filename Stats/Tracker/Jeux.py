from time import time
from Stats.SQL.ConnectSQL import connectSQL
from Stats.SQL.Execution import exeJeuxSQL

def exeStatsJeux(idW,idL,guild,option,tours):
    temps=time()

    connexionGuild,curseurGuild=connectSQL(guild,"Guild","Guild",None,None)
    connexionOT,curseurOT=connectSQL("OT","Guild","Guild",None,None)

    exeJeuxSQL(idW,idL,"W",guild,curseurGuild,2,option,tours)
    exeJeuxSQL(idW,idL,"W","OT",curseurOT,2,option,tours)
    exeJeuxSQL(idL,idW,"L",guild,curseurGuild,-1,option,tours)
    exeJeuxSQL(idL,idW,"L","OT",curseurOT,-1,option,tours)

    connexionGuild.commit()
    connexionOT.commit()
    print(time()-temps)