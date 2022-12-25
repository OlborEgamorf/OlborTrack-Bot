from Core.Fonctions.Phrase import createPhrase
from Stats.SQL.ConnectSQL import connectSQL

def createDirSQL(guild):
    connexion,curseur = connectSQL(guild.id)
    
    curseur.execute("CREATE TABLE IF NOT EXISTS etatStats (`Module` varchar(50) PRIMARY KEY, `Active` BOOLEAN)")
    listeN=["Messages","Voice","Emotes","Reactions","Divers"]
    for i in listeN:
        try:
            curseur.execute("INSERT INTO etatStats VALUES('{0}',True)".format(i))
        except:
            pass

    curseur.execute("CREATE TABLE IF NOT EXISTS etatModules (`Module` varchar(50) PRIMARY KEY, `Active` BOOLEAN, `Count` INT, `Count2` INT, `Salon` BIGINT)")
    listeC=["BV","AD","DynIcon","Stats","Polls","Twitch","Twitter","YouTube","Tableaux","VoiceEphem","CMDAuto","SavezVous","Jeux","Anniv","Timeline","RoleSelector","CMDCustom"]
    listeC.sort()
    for i in listeC:
        try:
            curseur.execute("INSERT INTO etatModules VALUES('{0}',True,0,0,NULL)".format(i))
        except:
            pass
    
    curseur.execute("CREATE TABLE IF NOT EXISTS polls_petitions (`ID` BIGINT, `Petition` INT, `Nb` INT, Final INT, Active INT, Debut INT, Fin INT, Auteur BIGINT, Channel BIGINT, Description varchar(300))")
    curseur.execute("CREATE TABLE IF NOT EXISTS polls_giveaways (`ID` BIGINT, `Lot` INT, `Gagnants` INT, `Winner` varchar(500), `Participants` varchar(15000), `Active` INT, `Debut` INT, `Fin` INT, `Auteur` BIGINT, `Channel` BIGINT, `Description` varchar(300))")
    curseur.execute("CREATE TABLE IF NOT EXISTS polls_polls (`ID` BIGINT, `Question` varchar(300), `Propositions` varchar(1000), `Results` varchar(200), `Active` BOOLEAN, `Multiple` BOOLEAN, `Total` INT, `Start` BIGINT, `End` BIGINT, `Auteur` BIGINT, `Channel` BIGINT)")

    curseur.execute("CREATE TABLE IF NOT EXISTS tab_messages (`Nombre` INT, `IDMess` BIGINT, `IDStar` BIGINT, PRIMARY KEY(IDMess,IDStar))")
    curseur.execute("CREATE TABLE IF NOT EXISTS tab_tableaux (`Nombre` INT, `Salon` BIGINT, `Emote` varchar(100), `ID` BIGINT, `Count` INT, `Active` BOOLEAN, PRIMARY KEY(Salon, Emote))")
    
    curseur.execute("CREATE TABLE IF NOT EXISTS sv_savezvous (`Nombre` INT, `Texte` varchar(2000), `ID` BIGINT, `Image` varchar(300), Source varchar(2000))")
    curseur.execute("CREATE TABLE IF NOT EXISTS sv_comment (`Nombre` INT, `ID` BIGINT, `Texte` varchar(300), `Date` varchar(10))")
    
    curseur.execute("CREATE TABLE IF NOT EXISTS al_twitch (`Nombre` INT, `Salon` BIGINT, `Stream` varchar(50), `Descip` varchar(300), `Sent` BOOLEAN, `Active` BOOLEAN, PRIMARY KEY(Salon, Stream))")
    curseur.execute("CREATE TABLE IF NOT EXISTS al_youtube (`Nombre` INT, `Salon` BIGINT, `Chaine` varchar(50), `Descip` varchar(300), `LastID` varchar(50), `Nom` varchar(50), `Active` BOOLEAN, PRIMARY KEY(Salon, Chaine))")
    curseur.execute("CREATE TABLE IF NOT EXISTS al_twitter (`Nombre` INT, `Salon` BIGINT, `Compte` BIGINT, `Descip` varchar(300), `LastID` BIGINT, `Nom` varchar(50), `Active` BOOLEAN, PRIMARY KEY(Salon, Compte))")

    curseur.execute("CREATE TABLE IF NOT EXISTS bv_images (`Nombre` INT, `Path` varchar(300), `Message` varchar(500), `Couleur` varchar(7), `Taille` INT, `Mode` varchar(4), `Active` BOOLEAN)")
    curseur.execute("CREATE TABLE IF NOT EXISTS bv_messages (`Nombre` INT, `Message` varchar(500), `Active` BOOLEAN)")

    curseur.execute("CREATE TABLE IF NOT EXISTS ad_images (`Nombre` INT, `Path` varchar(300), `Message` varchar(500), `Couleur` varchar(7), `Taille` INT, `Mode` varchar(4), `Filtre` BOOLEAN, `Active` BOOLEAN)")
    curseur.execute("CREATE TABLE IF NOT EXISTS ad_messages (`Nombre` INT, `Message` varchar(500), `Active` BOOLEAN)")

    curseur.execute("CREATE TABLE IF NOT EXISTS dyn_icons (`Nombre` INT PRIMARY KEY, `Path` varchar(300), `Description` varchar(500), `Membres` varchar(1800), `Auteur` BIGINT, `Rotation` BOOLEAN, `Active` BOOLEAN)")

    curseur.execute("CREATE TABLE IF NOT EXISTS anniv (`Message` varchar(500))")

    curseur.execute("CREATE TABLE IF NOT EXISTS chans (`ID` BIGINT PRIMARY KEY, `Hide` BOOLEAN, `Blind` BOOLEAN, `Mute` BOOLEAN, `Tab` BOOLEAN)")
    for i in guild.text_channels:
        if curseur.execute("SELECT * FROM chans WHERE ID={0}".format(i.id)).fetchone()==None:
            curseur.execute("INSERT INTO chans VALUES({0},{1},{2},{3},{4})".format(i.id,False,False,False,False))
    for i in guild.voice_channels:
        if curseur.execute("SELECT * FROM chans WHERE ID={0}".format(i.id)).fetchone()==None:
            curseur.execute("INSERT INTO chans VALUES({0},{1},{2},{3},{4})".format(i.id,False,False,False,False))
    
    curseur.execute("CREATE TABLE IF NOT EXISTS users (`ID` BIGINT PRIMARY KEY, `Hide` BOOLEAN, `Blind` BOOLEAN, `Leave` BOOLEAN)")
    for i in guild.members:
        if not i.bot:
            if curseur.execute("SELECT * FROM users WHERE ID={0}".format(i.id)).fetchone()==None:
                curseur.execute("INSERT INTO users VALUES({0},{1},{2},{3})".format(i.id,False,False,False))
    
    curseur.execute("CREATE TABLE IF NOT EXISTS cmd_auto (`Commande` varchar(50) PRIMARY KEY, `Salon` BIGINT, `Active` BOOLEAN)")
    listeA=["savezvous","nasaphoto","jour","mois","annee","events"]
    for i in listeA:
        try:
            curseur.execute("INSERT INTO cmd_auto VALUES('{0}',False,0)".format(i))
        except:
            pass

    curseur.execute("CREATE TABLE IF NOT EXISTS cmd_custom (`Nom` varchar(50) PRIMARY KEY, `Description` varchar(1000), `Embed` BOOLEAN, `Title` varchar(200), `Author` varchar(25), `Color` varchar(7), `Footer` varchar(100), `Image` varchar(100), `Miniature` varchar(100))")

    curseur.execute("CREATE TABLE IF NOT EXISTS commandes (`MessageID` BIGINT, `AuthorID` BIGINT, `Commande` varchar(50), `Option` varchar(50), `Args1` varchar(50), `Args2` varchar(50), `Args3` varchar(50), `Args4` varchar(50), `Page` INT, `PageMax` INT, `Tri` varchar(50), `Mobile` BOOLEAN)")
    curseur.execute("CREATE TABLE IF NOT EXISTS graphs (`MessageID` BIGINT, `Graph1` varchar(50), `Graph2` varchar(50), `Graph3` varchar(50), `Graph4` varchar(50), `Graph5` varchar(50), `Graph6` varchar(50), `Graph7` varchar(50), `Page` INT, `PageMax` INT)")

    curseur.execute("CREATE TABLE IF NOT EXISTS vep_hub (`Nombre` INT PRIMARY KEY, `ID` BIGINT, `Limite` INT, `Pattern` varchar(200), `Active` BOOLEAN)")
    curseur.execute("CREATE TABLE IF NOT EXISTS vep_salons (`IDHub` BIGINT, `IDChannel` BIGINT, `IDOwner` BIGINT, `Lock` BOOLEAN)")
    
    connexion.commit()


def backGuild(bot):
    for i in bot.guilds:
        print(i.id)
        createDirSQL(i)
        connexion,curseur=connectSQL(i.id,"Guild","Guild",None,None)
        connexionMY,curseurMY=connectSQL(i.id)

        for i in curseur.execute("SELECT * FROM auto").fetchall():
            if i["Active"]==True:
                curseurMY.execute("UPDATE cmd_auto SET Salon={0}, Active=True WHERE Commande='{1}'".format(i["Salon"],i["Commande"]))

        for i in curseur.execute("SELECT * FROM chans").fetchall():
            curseurMY.execute("UPDATE chans SET Hide={0}, Blind={1}, Mute={2}, Tab={3} WHERE ID={4}".format(i["Hide"],i["Blind"],i["Mute"],i["Tab"],i["ID"])) 

        anniv=curseur.execute("SELECT * FROM etatAnniv").fetchone()
        if anniv["Statut"]==True:
            curseurMY.execute("UPDATE etatModules Set Active=True, Salon={0} WHERE Module='Anniv'".format(anniv["Salon"]))
            curseurMY.execute("INSERT INTO anniv VALUES ('{0}')".format(anniv["Message"]))

        bv=curseur.execute("SELECT * FROM etatBVAD WHERE Type='BV'").fetchone()
        if bv["Statut"]==True:
            curseurMY.execute("UPDATE etatModules Set Active=True, Salon={0} WHERE Module='BV'".format(bv["Salon"]))
        
        ad=curseur.execute("SELECT * FROM etatBVAD WHERE Type='AD'").fetchone()
        if ad["Statut"]==True:
            curseurMY.execute("UPDATE etatModules Set Active=True, Salon={0} WHERE Module='AD'".format(ad["Salon"]))

        dyn=curseur.execute("SELECT * FROM etatPP").fetchone()
        if dyn["Statut"]==True:
            curseurMY.execute("UPDATE etatModules Set Active=True, Salon={0} WHERE Module='DynIcon'".format(dyn["Salon"]))

        for i in curseur.execute("SELECT * FROM icons").fetchall():
            curseurMY.execute("INSERT INTO dyn_icons VALUES ({0},'{1}','{2}','{3}',{4},{5},True)".format(i["Nombre"],i["Path"],createPhrase(i["Description"]),i["Membres"],i["Auteur"],i["Rotation"]))
            curseurMY.execute("UPDATE etatModules SET Count=Count+1 WHERE Module='DynIcon'")

        for i in curseur.execute("SELECT * FROM imagesAD").fetchall():
            curseurMY.execute("INSERT INTO ad_images VALUES ({0},'{1}','{2}','{3}',{4},'{5}',{6},True)".format(i["Nombre"],i["Path"],i["Message"],i["Couleur"],i["Taille"],i["Mode"],i["Filtre"]))
            curseurMY.execute("UPDATE etatModules SET Count2=Count2+1 WHERE Module='AD'")

        for i in curseur.execute("SELECT * FROM imagesBV").fetchall():
            curseurMY.execute("INSERT INTO bv_images VALUES ({0},'{1}','{2}','{3}',{4},'{5}',True)".format(i["Nombre"],i["Path"],i["Message"],i["Couleur"],i["Taille"],i["Mode"]))
            curseurMY.execute("UPDATE etatModules SET Count2=Count2+1 WHERE Module='BV'")
        
        for i in curseur.execute("SELECT * FROM messagesAD").fetchall():
            curseurMY.execute("INSERT INTO ad_messages VALUES ({0},'{1}',True)".format(i["Nombre"],i["Message"]))
            curseurMY.execute("UPDATE etatModules SET Count=Count+1 WHERE Module='AD'")
        
        for i in curseur.execute("SELECT * FROM messagesBV").fetchall():
            curseurMY.execute("INSERT INTO bv_messages VALUES ({0},'{1}',True)".format(i["Nombre"],i["Message"]))
            curseurMY.execute("UPDATE etatModules SET Count=Count+1 WHERE Module='BV'")

        for i in curseur.execute("SELECT * FROM savezvous").fetchall():
            curseurMY.execute("INSERT INTO sv_savezvous VALUES ({0},'{1}',{2},'{3}','{4}')".format(i["Count"],i["Texte"],i["ID"],i["Image"],i["Source"]))
            curseurMY.execute("UPDATE etatModules SET Count=Count+1 WHERE Module='Savezvous'")

        for i in curseur.execute("SELECT * FROM sb").fetchall():
            curseurMY.execute("INSERT INTO tab_tableaux VALUES ({0},{1},'{2}',{3},{4},True)".format(i["Nombre"],i["Salon"],i["Emote"],i["ID"],i["Count"]))
            curseurMY.execute("UPDATE etatModules SET Count=Count+1 WHERE Module='Tableaux'")

        for i in curseur.execute("SELECT * FROM sbmessages").fetchall():
            curseurMY.execute("INSERT INTO tab_messages VALUES ({0},{1},{2})".format(i["Nombre"],i["IDMess"],i["IDStar"]))

        for i in curseur.execute("SELECT * FROM svcomment").fetchall():
            curseurMY.execute("INSERT INTO sv_comment VALUES ({0},{1},'{2}','{3}')".format(i["Count"],i["ID"],i["Texte"],i["Date"]))

        for i in curseur.execute("SELECT * FROM twitch").fetchall():
            curseurMY.execute("INSERT INTO al_twitch VALUES ({0},{1},'{2}','{3}',{4},True)".format(i["Nombre"],i["Salon"],i["Stream"],i["Descip"],i["Sent"]))
            curseurMY.execute("UPDATE etatModules SET Count=Count+1 WHERE Module='Twitch'")

        for i in curseur.execute("SELECT * FROM twitter").fetchall():
            curseurMY.execute("INSERT INTO al_twitter VALUES ({0},{1},{2},'{3}',{4},'{5}',True)".format(i["Nombre"],i["Salon"],i["Compte"],i["Descip"],i["LastID"],i["Nom"]))
            curseurMY.execute("UPDATE etatModules SET Count=Count+1 WHERE Module='Twitter'")

        for i in curseur.execute("SELECT * FROM youtube").fetchall():
            curseurMY.execute("INSERT INTO al_youtube VALUES ({0},{1},'{2}','{3}','{4}','{5}',True)".format(i["Nombre"],i["Salon"],i["Chaine"],i["Descip"],i["LastID"],i["Nom"]))
            curseurMY.execute("UPDATE etatModules SET Count=Count+1 WHERE Module='Youtube'")

        connexionMY.commit()