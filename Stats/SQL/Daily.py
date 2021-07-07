tableauMois={"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre","TO":"TOTAL"}
from Stats.SQL.Evolutions import evolSQL
from Stats.SQL.ConnectSQL import connectSQL

def dailySQL(id,date,nom,curseurGuild,guild):
    curseurGuild.execute("CREATE TABLE IF NOT EXISTS logJour (Objet TEXT PRIMARY KEY, Date INT)")
    etat=curseurGuild.execute("SELECT * FROM logJour WHERE Date={0}".format(id)).fetchone()
    if etat==None:
        curseurGuild.execute("DROP TABLE logJour")
        curseurGuild.execute("CREATE TABLE IF NOT EXISTS logJour (Objet TEXT, Date INT)")
    etat=curseurGuild.execute("SELECT * FROM logJour WHERE Objet='{0}'".format(nom)).fetchone()
    if etat==None:
        curseurGuild.execute("INSERT INTO logJour VALUES('{0}',{1})".format(nom,id))
        db=nom
        if type(nom)!=int:
            nom=""
        
        tables=[tableauMois[date[1]]+date[2]+str(nom),"to"+date[2]+str(nom),"glob"+str(nom)]
        curseurs=[(date[1],date[2]),("TO",date[2]),("GL","")]
        for j in range(3):
            connexion,base=connectSQL(guild,db,"Stats",curseurs[j][0],curseurs[j][1])
            for i in base.execute("SELECT * FROM {0} WHERE Rank<=150".format(tables[j])).fetchall():
                evol=evolSQL(base,tables[j],i["Rank"],i["Count"],i["ID"],date)
                base.execute("UPDATE {0} SET Evol={1} WHERE ID={2}".format(tables[j],evol,i["ID"]))
            connexion.commit()