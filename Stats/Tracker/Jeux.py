from time import time
from Stats.SQL.ConnectSQL import connectSQL
from Stats.SQL.Execution import exeClassic, exeJeuxSQL, exeObj


def exeStatsJeux(idW,idL,guild,option,tours,statut):
    connexionGuild,curseurGuild=connectSQL(guild,"Guild","Guild",None,None)
    connexionOT,curseurOT=connectSQL("OT","Guild","Guild",None,None)

    if statut=="abandon":
        exeJeuxSQL(idL,idW,"L",guild,curseurGuild,-1,option,tours)
        exeJeuxSQL(idL,idW,"L","OT",curseurOT,-1,option,tours)
    else:
        exeJeuxSQL(idW,idL,"W",guild,curseurGuild,2,option,tours)
        countW=exeJeuxSQL(idW,idL,"W","OT",curseurOT,2,option,tours)
        exeJeuxSQL(idL,idW,"L",guild,curseurGuild,-1,option,tours)
        exeJeuxSQL(idL,idW,"L","OT",curseurOT,-1,option,tours)

    connexionGuild.commit()
    connexionOT.commit()
    if "countW" in locals():
        return countW


def statsServ(game,win):
    connexionOT,curseurOT=connectSQL("OT","Guild","Guild",None,None)
    count=0
    guild=game.memguild[win]
    for i in game.memguild.values():
        if i!=guild:
            count+=1
    exeClassic(count,guild,"Cross",curseurOT,fake)
    exeObj(count,guild,win,True,fake,"Cross")
    connexionOT.commit()


class FakeGuild:
    def __init__(self):
        self.id="OT"

fake=FakeGuild()