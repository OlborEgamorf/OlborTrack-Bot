from Stats.SQL.ConnectSQL import connectSQL

def leaveUser(guild,user,state):
    connexion,curseur=connectSQL(guild.id,"Guild","Guild",None,None)
    if curseur.execute("SELECT * FROM users WHERE ID={0}".format(user.id))==None:
        curseur.execute("INSERT INTO users VALUES({0},{1},{2},{3})".format(user.id,False,False,False))
    curseur.execute("UPDATE users SET Leave={0} WHERE ID={1}".format(state,user.id))
    connexion.commit()
    guild.getHBM()