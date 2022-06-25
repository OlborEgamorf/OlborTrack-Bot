from Stats.SQL.ConnectSQL import connectSQL

def addChan(guild,chan):
    connexion,curseur=connectSQL(guild.id,"Guild","Guild",None,None)
    curseur.execute("INSERT INTO chans VALUES({0},{1},{2},{3},{4})".format(chan.id,False,False,False,False))
    connexion.commit()
    guild.getHBM()

def delChan(guild,chan):
    connexion,curseur=connectSQL(guild.id,"Guild","Guild",None,None)
    curseur.execute("DELETE FROM chans WHERE ID={0}".format(chan.id))
    connexion.commit()
    guild.getHBM()