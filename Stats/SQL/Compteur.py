from Stats.SQL.Ranking import rankingSQL
from Stats.SQL.ConnectSQL import connectSQL

typeCreate={1:"(Rank INT, ID BIGINT PRIMARY KEY, Mois TEXT, Annee TEXT, Count INT, Evol INT)",2:"(Rank INT, ID BIGINT PRIMARY KEY, IDComp BIGINT, Mois TEXT, Annee TEXT, Count INT)",3:"(Rank INT, ID INT PRIMARY KEY, Jour TEXT, Mois TEXT, Annee TEXT, Count INT)",4:"(Rank INT, ID BIGINT PRIMARY KEY, Mois TEXT, Annee TEXT, W INT, L INT, Count INT, Evol INT)",5:"(Rank INT, ID BIGINT PRIMARY KEY, IDComp BIGINT, Mois TEXT, Annee TEXT, W INT, L INT, Count INT, Evol INT)"}

def compteurSQL(base,table,id,insert,count,date,period,perso,obj,evol,crea,baseGL):
    base.execute("CREATE TABLE IF NOT EXISTS {0} {1}".format(table,typeCreate[crea]))
    etat=base.execute("SELECT Count,Rank,ID FROM {0} WHERE ID= {1}".format(table,id)).fetchone()
    if etat==None:
        base.execute("INSERT INTO {0} VALUES {1}".format(table,insert))
        countB,countN,rank=0,count,0
    else:
        countB,rank=etat["Count"],etat["Rank"]
        countN=countB+count
        base.execute("UPDATE {0} SET Count= {1} WHERE ID={2}".format(table,countN,id))
        
    return rankingSQL(base,table,countB,countN,id,rank,date,period,perso,obj,evol,baseGL)


def compteurTrivialS(id,insert,count):
    connexion,curseur=connectSQL("OT","ranks","Trivial",None,None)
    curseur.execute("CREATE TABLE IF NOT EXISTS trivialStreak {0}".format(typeCreate[2]))
    etat=curseur.execute("SELECT Count,Rank,ID FROM trivialStreak WHERE ID= {0}".format(id)).fetchone()
    if etat==None:
        curseur.execute("INSERT INTO trivialStreak VALUES {0}".format(insert))
        countB,countN,rank=0,count,0
    else:
        if count<=etat["Count"]:
            return False,0,0
        countB,rank=etat["Count"],etat["Rank"]
        curseur.execute("UPDATE trivialStreak SET Count= {0} WHERE ID={1}".format(count,id))
        
    rankingSQL(curseur,"trivialStreak",countB,count,id,rank,None,None,None,None,None,None)
    connexion.commit()
    return True,count,countB