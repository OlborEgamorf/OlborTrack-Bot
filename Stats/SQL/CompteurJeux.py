from Stats.SQL.Ranking import rankingSQL

typeCreate={1:"(Rank INT, ID BIGINT PRIMARY KEY, Mois TEXT, Annee TEXT, Count INT, Evol INT)",2:"(Rank INT, ID BIGINT PRIMARY KEY, IDComp BIGINT, Mois TEXT, Annee TEXT, Count INT)",3:"(Rank INT, ID INT PRIMARY KEY, Jour TEXT, Mois TEXT, Annee TEXT, Count INT)",4:"(Rank INT, ID BIGINT PRIMARY KEY, Mois TEXT, Annee TEXT, W INT, L INT, Count INT, Evol INT)",5:"(Rank INT, ID BIGINT PRIMARY KEY, IDComp BIGINT, Mois TEXT, Annee TEXT, W INT, L INT, Count INT, Evol INT)"}

def compteurJeuxSQL(base,table,id,insert,count,date,period,obj,state,crea,baseGL):
    base.execute("CREATE TABLE IF NOT EXISTS {0} {1}".format(table,typeCreate[crea]))
    base.execute("SELECT Count,Rank,ID,{0} FROM {1} WHERE ID= {2}".format(state,table,id))
    etat=base.fetchone()
    if etat==None:
        base.execute("INSERT INTO {0} VALUES {1}".format(table,insert))
        countB,countN,rank,winlose=0,count,0,0
    else:
        countB,rank,winlose=etat["Count"],etat["Rank"],etat[state]
        base.execute("UPDATE {0} SET Count= {1}, {2}={3} WHERE ID={4}".format(table,count+countB,state,winlose+1,id))
        countN=countB+count
    if obj==False:
        rankingSQL(base,table,countB,countN,id,rank,date,period,obj,True,baseGL)
    else:
        rankingSQL(base,table,countB,countN,id,rank,date,period,obj,False,baseGL)