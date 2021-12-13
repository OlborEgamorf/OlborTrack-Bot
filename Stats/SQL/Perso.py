def persoSQL(base,id,idComp,rank,count,date):
    base.execute("CREATE TABLE IF NOT EXISTS {0} (Rank INT, ID BIGINT PRIMARY KEY, IDComp BIGINT, Mois TEXT, Annee TEXT, Count INT)".format("perso"+date[0]+date[1]+str(idComp)))
    base.execute("SELECT Count,Rank,ID FROM {0} WHERE ID={1}".format("perso"+date[0]+date[1]+str(idComp),id))
    etat=base.fetchone()
    if etat==None:
        try:
            base.execute("INSERT INTO {0} VALUES {1}".format("perso"+date[0]+date[1]+str(idComp),(rank,id,idComp,date[0],date[1],count)))
        except:
            base.execute("DROP TABLE {0}".format("perso"+date[0]+date[1]+str(idComp)))
    else:
        base.execute("UPDATE {0} SET Count= {1}, Rank={2} WHERE ID={3}".format("perso"+date[0]+date[1]+str(idComp),count,rank,id))  