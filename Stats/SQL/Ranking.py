from Stats.SQL.First import firstSQL
from Stats.SQL.Periods import periodsSQL
from Stats.SQL.Perso import persoSQL
from Stats.SQL.Evolutions import evolSQL

def rankingSQL(base,table,countB,countN,id,baseRank,date,period,perso,obj,evol,baseGL):
    rank=base.execute("SELECT COUNT() AS nombre FROM {0} WHERE Count> {1}".format(table,countN)).fetchone()["nombre"]
    equal=base.execute("SELECT COUNT() AS nombre FROM {0} WHERE Rank= {1}".format(table,baseRank)).fetchone()["nombre"]
    newRank=rank+1

    if obj==True:
        idObj=base.execute("SELECT IDComp FROM {0} WHERE ID= {1}".format(table,id)).fetchone()["IDComp"]
    else:
        if obj==False and newRank==1:
            firstSQL(baseGL,id,countN,period)
        idObj=None
    evolRank=rankingPlus(base,table,perso,id,rank+1,countN,period,date,obj,idObj,baseGL)

    if newRank!=baseRank or equal!=0:
        if evol==True and evolRank!=None:
            base.execute("UPDATE {0} SET Rank= {1}, Evol={2} WHERE ID = {3}".format(table,newRank,evolRank,id))
        else:
            base.execute("UPDATE {0} SET Rank= {1} WHERE ID = {2}".format(table,newRank,id))
        countE=countN
        if baseRank==0:
            exe="SELECT * FROM {0} WHERE Count<= {1} ORDER BY Count DESC".format(table,countN)
        elif countN>=countB:
            exe="SELECT * FROM {0} WHERE Count<= {1} AND Count>= {2} ORDER BY Count DESC".format(table,countN,countB)
        else:
            newRank=baseRank
            exe="SELECT * FROM {0} WHERE Count>= {1} AND Count<= {2} ORDER BY Count DESC".format(table,countN,countB)

        etat=base.execute(exe).fetchall()
        for i in range(len(etat)):
            if etat[i]["ID"]!=id:
                if etat[i]["Count"]==countN:
                    newRank=rank+1
                elif etat[i]["Count"]!=countE:
                    if countN>=countB:
                        newRank=rank+i+1
                    else:
                        newRank=baseRank+i
                    countE=etat[i]["Count"]
                if evol==True:
                    if obj==True:
                        evolRank=rankingPlus(base,table,perso,etat[i]["ID"],newRank,countE,period,date,obj,etat[i]["IDComp"],baseGL)
                    else:
                        evolRank=rankingPlus(base,table,perso,etat[i]["ID"],newRank,countE,period,date,obj,None,baseGL)
                    base.execute("UPDATE {0} SET Rank= {1}, Evol={2} WHERE ID = {3}".format(table,newRank,evolRank,etat[i]["ID"]))  
                else:
                    base.execute("UPDATE {0} SET Rank= {1} WHERE ID = {2}".format(table,newRank,etat[i]["ID"]))   
                if obj==False and newRank==1:
                    firstSQL(baseGL,etat[i]["ID"],countE,period)
        return base.execute(exe).fetchall()
    return [{"ID":id,"Rank":baseRank}]

def rankingPlus(base,table,perso,id,rank,countN,period,date,obj,idObj,baseGL):
    if obj==False:
        periodsSQL(baseGL,perso,id,rank,countN,period)
        evol=evolSQL(base,table,rank,countN,id,date)
    elif obj==True:
        periodsSQL(baseGL,perso,str(id)+str(idObj),rank,countN,period)
        persoSQL(base,idObj,id,rank,countN,period)
        evol=None
    else:
        evol=None
    return evol