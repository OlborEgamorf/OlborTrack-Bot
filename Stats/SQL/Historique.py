def histoSQL(base,count,id,date,chan):
    base.execute("CREATE TABLE IF NOT EXISTS histo{0} (ID BIGINT, IDComp BIGINT, Date INT, Count INT)".format(id))
    base.execute("INSERT INTO histo{0} VALUES({1},{2},{3},{4})".format(id,id,chan,date,count))

def histoSQLJeux(base,id,count,date,idriv,state):
    base.execute("CREATE TABLE IF NOT EXISTS histo{0} (ID BIGINT, IDComp BIGINT, Date TEXT, Count INT, Win TEXT)".format(id))
    base.execute("INSERT INTO histo{0} VALUES{1}".format(id,(id,idriv,date,count,state)))