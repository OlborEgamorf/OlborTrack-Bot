def firstSQL(base,id,count,period):
    if period[1]=="GL":
        return
    if period[0]=="TO":
        detail="A"
    else:
        detail="M"
    base.execute("CREATE TABLE IF NOT EXISTS first{0} (ID BIGINT, Mois TEXT, Annee TEXT, DateID INT, Count INT, PRIMARY KEY(Mois,Annee))".format(detail))
    etat=base.execute("SELECT * FROM first{0} WHERE Mois='{1}' AND Annee='{2}'".format(detail,period[0],period[1])).fetchone()
    if etat==None:
        if period[0]=="TO":
            base.execute("INSERT INTO firstA VALUES {0}".format((id,period[0],period[1],period[1],count)))
        else:
            base.execute("INSERT INTO firstM VALUES {0}".format((id,period[0],period[1],period[1]+period[0],count)))
    else:
        base.execute("UPDATE first{0} SET Count={1}, ID={2} WHERE Mois='{3}' AND Annee='{4}'".format(detail,count,id,period[0],period[1]))