from Stats.SQL.ConnectSQL import connectSQL
from Stats.SQL.Execution import exeJeuxSQL


def exeStatsJeux(idW,idL,guild,option,tours,statut):
    connexionGuild,curseurGuild=connectSQL(guild,"Guild","Guild",None,None)
    connexionOT,curseurOT=connectSQL("OT","Guild","Guild",None,None)

    if statut=="abandon":
        exeJeuxSQL(idL,idW,"L",guild,curseurGuild,option,tours)
        exeJeuxSQL(idL,idW,"L","OT",curseurOT,option,tours)
    else:
        exeJeuxSQL(idW,idL,"W",guild,curseurGuild,option,tours)
        countW=exeJeuxSQL(idW,idL,"W","OT",curseurOT,option,tours)
        exeJeuxSQL(idL,idW,"L",guild,curseurGuild,option,tours)
        exeJeuxSQL(idL,idW,"L","OT",curseurOT,option,tours)

    connexionGuild.commit()
    connexionOT.commit()
    if "countW" in locals():
        return countW