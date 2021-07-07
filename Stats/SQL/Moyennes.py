def moySQL(base,option,date,period,count,id):
    base.execute("CREATE TABLE IF NOT EXISTS time{0} (ID INT PRIMARY KEY)".format(option+str(id)))
    base.execute("CREATE TABLE IF NOT EXISTS moy{0} (ID BIGINT, Type TEXT, Mois TEXT, Annee TEXT, Nombre INT, Count INT, Moyenne INT, PRIMARY KEY(Mois,Annee))".format(option+str(id)))
    etat=base.execute("SELECT * FROM time{0} WHERE ID={1}".format(option+str(id),date)).fetchone()
    search=base.execute("SELECT * FROM moy{0} WHERE Mois='{1}' AND Annee='{2}'".format(option+str(id),period[0],period[1])).fetchone()
    if etat==None:
        base.execute("INSERT INTO time{0} VALUES ({1})".format(option+str(id),date))
        if search==None:
            base.execute("INSERT INTO moy{0} VALUES {1}".format(option+str(id),(id,option,period[0],period[1],1,count,count)))
        else:
            base.execute("UPDATE moy{0} SET Count={1}, Nombre={2}, Moyenne={3} WHERE Mois='{4}' AND Annee='{5}'".format(option+str(id),count+search["Count"],search["Nombre"]+1,(count+search["Count"])/(search["Nombre"]+1),period[0],period[1]))
    else:
        base.execute("UPDATE moy{0} SET Count={1}, Moyenne={2} WHERE Mois='{3}' AND Annee='{4}'".format(option+str(id),count+search["Count"],(count+search["Count"])/(search["Nombre"]),period[0],period[1]))