def periodsSQL(base,table,id,rank,count,date):
    base.execute("CREATE TABLE IF NOT EXISTS {0} (Rank INT, ID BIGINT, Mois TEXT, Annee TEXT, Count INT,PRIMARY KEY(Mois,Annee))".format(table+str(id)))
    etat=base.execute("SELECT * FROM {0} WHERE Mois='{1}' AND Annee='{2}'".format(table+str(id),date[0],date[1])).fetchone()
    if etat==None:
        base.execute("INSERT INTO {0} VALUES {1}".format(table+str(id),(rank,id,date[0],date[1],count)))
    else:
        base.execute("UPDATE {0} SET Count={1}, Rank={2} WHERE Mois='{3}' AND Annee='{4}'".format(table+str(id),count,rank,date[0],date[1]))