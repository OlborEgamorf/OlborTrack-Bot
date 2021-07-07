def evolSQL(base,table,rank,count,id,date):
    if rank<=150:
        table="evol"+table+str(id)
        base.execute("CREATE TABLE IF NOT EXISTS {0} (Rank INT, ID BIGINT, Jour TEXT, Mois TEXT, Annee TEXT, DateID TEXT, Count INT, Evol INT, PRIMARY KEY(Jour,Mois,Annee))".format(table))
        etat=base.execute("SELECT * FROM {0} WHERE Jour='{1}' AND Mois='{2}' AND Annee='{3}'".format(table,date[0],date[1],date[2])).fetchone()
        if etat==None:
            base.execute("INSERT INTO {0} VALUES {1}".format(table,(rank,id,date[0],date[1],date[2],date[2]+date[1]+date[0],count,0)))
        rankB=base.execute("SELECT Rank FROM {0} WHERE DateID != {1} ORDER BY DateID DESC".format(table,date[2]+date[1]+date[0])).fetchone()
        if rankB!=None:
            rankB=rankB["Rank"]
            base.execute("UPDATE {0} SET Count={1}, Rank={2}, Evol={3} WHERE Jour='{4}' AND Mois='{5}' AND Annee='{6}'".format(table,count,rank,rankB-rank,date[0],date[1],date[2]))
            evol=rankB-rank
        else:
            base.execute("UPDATE {0} SET Count={1}, Rank={2} WHERE Jour='{3}' AND Mois='{4}' AND Annee='{5}'".format(table,count,rank,date[0],date[1],date[2]))
            evol=0
        return evol
    return 0