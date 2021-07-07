import os
from Stats.SQL.ConnectSQL import connectSQL

def graphSQL(guild):
    connexion,curseur = connectSQL(guild.id,"Guild")
    curseur.execute("CREATE TABLE IF NOT EXISTS graphs (MessageID BIGINT, Graph1 TEXT, Graph2 TEXT, Graph3 TEXT, Graph4 TEXT, Graph5 TEXT, Graph6 TEXT, Graph7 TEXT, Page INT, PageMax INT)")
    connexion.commit()


def createDirSQL(guild):
    if not os.path.exists("SQL/{0}".format(guild.id)):
        os.makedirs("SQL/{0}".format(guild.id))
    connexion,curseur = connectSQL(guild.id,"Guild","Guild",None,None)

    
    curseur.execute("CREATE TABLE IF NOT EXISTS modulesStats (Module TEXT PRIMARY KEY, Statut BOOL)")
    listeN=["Salons","Moyennes","Freq","Reactions","Mentions","Voice","Mots","Roles","Emotes","Messages","Divers"]
    for i in listeN:
        try:
            curseur.execute("INSERT INTO modulesStats VALUES('{0}',True)".format(i))
        except:
            pass

    
    curseur.execute("CREATE TABLE IF NOT EXISTS modulesCMD (Module TEXT PRIMARY KEY, Statut BOOL)")
    listeC=["Stats","Sondages","Custom","Savezvous","Jeux","MAL","Wiki","Spotify","Geo"]
    for i in listeC:
        try:
            curseur.execute("INSERT INTO modulesCMD VALUES('{0}',{1})".format(i,True))
        except:
            pass

    curseur.execute("CREATE TABLE IF NOT EXISTS sbmessages (IDMess BIGINT, IDStar BIGINT, Nombre INT, PRIMARY KEY(IDMess,IDStar))")
    curseur.execute("CREATE TABLE IF NOT EXISTS savezvous (Texte TEXT, ID BIGINT, Image TEXT, Count INT)")
    curseur.execute("CREATE TABLE IF NOT EXISTS sb (Nombre INT, Salon BIGINT, Emote TEXT, ID BIGINT, Count INT, PRIMARY KEY(Salon,Emote))")

    curseur.execute("CREATE TABLE IF NOT EXISTS wikinsfw (Active BOOL PRIMARY KEY)")
    try:
        curseur.execute("INSERT INTO wikinsfw VALUES(True)")
    except:
        pass

    curseur.execute("CREATE TABLE IF NOT EXISTS chans (ID BIGINT PRIMARY KEY, Hide BOOL, Blind BOOL, Mute BOOL)")
    for i in guild.text_channels:
        if curseur.execute("SELECT * FROM chans WHERE ID={0}".format(i.id)).fetchone()==None:
            curseur.execute("INSERT INTO chans VALUES({0},{1},{2},{3})".format(i.id,False,False,False))
    for i in guild.voice_channels:
        if curseur.execute("SELECT * FROM chans WHERE ID={0}".format(i.id)).fetchone()==None:
            curseur.execute("INSERT INTO chans VALUES({0},{1},{2},{3})".format(i.id,False,False,False))
    
    curseur.execute("CREATE TABLE IF NOT EXISTS users (ID BIGINT PRIMARY KEY, Hide BOOL, Blind BOOL, Leave BOOL)")
    for i in guild.members:
        if curseur.execute("SELECT * FROM users WHERE ID={0}".format(i.id)).fetchone()==None:
            curseur.execute("INSERT INTO users VALUES({0},{1},{2},{3})".format(i.id,False,False,False))
    
    curseur.execute("CREATE TABLE IF NOT EXISTS sbmessages (IDMess BIGINT, IDStar BIGINT, Nombre INT, PRIMARY KEY(IDMess,IDStar))")

    
    curseur.execute("CREATE TABLE IF NOT EXISTS auto (Commande TEXT PRIMARY KEY, Salon BIGINT, Active BOOL)")
    listeA=["savezvous","nasaphoto","jour","mois","annee"]
    for i in listeA:
        try:
            curseur.execute("INSERT INTO auto VALUES('{0}',False,0)".format(i))
        except:
            pass

    
    connexion.commit()

    connexion,curseur = connectSQL(guild.id,"CustomCMD","Guild",None,None)
    curseur.execute("CREATE TABLE IF NOT EXISTS help (Nom TEXT PRIMARY KEY, Description TEXT)")
    curseur.execute("CREATE TABLE IF NOT EXISTS custom (Nom TEXT PRIMARY KEY, Description TEXT, Embed BOOL, Title TEXT, Author TEXT, Color TEXT, Footer TEXT, Image TEXT, Miniature TEXT)")
    connexion.commit()

    connexion,curseur = connectSQL(guild.id,"Giveaway","Guild",None,None)
    curseur.execute("CREATE TABLE IF NOT EXISTS liste (Nombre INT PRIMARY KEY, IDMess BIGINT, IDChan INT)")
    connexion.commit()


    connexion,curseur = connectSQL(guild.id,"Commandes","Guild",None,None)
    curseur.execute("CREATE TABLE IF NOT EXISTS commandes (MessageID BIGINT, AuthorID BIGINT, Commande TEXT, Option TEXT, Args1 TEXT, Args2 TEXT, Args3 TEXT, Args4 TEXT, Page INT, PageMax INT, Tri TEXT, Mobile BOOL)")
    curseur.execute("CREATE TABLE IF NOT EXISTS graphs (MessageID BIGINT, Graph1 TEXT, Graph2 TEXT, Graph3 TEXT, Graph4 TEXT, Graph5 TEXT, Graph6 TEXT, Graph7 TEXT, Page INT, PageMax INT)")
    connexion.commit()

    return