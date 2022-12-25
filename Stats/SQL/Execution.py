from time import strftime

from Titres.Outils import titresJeux

tableauMois={"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre","TO":"TOTAL"}


def executeStats(option,user,salon,count,curseur,jour=None,mois=None,annee=None):
    if jour==None:
        jour,mois,annee,dateID=strftime("%d"),strftime("%m"),strftime("%y"),strftime("%y%m%d")
    else:
        dateID="{0}{1}{2}".format(annee,mois,jour)

    curseur.execute("CREATE TABLE IF NOT EXISTS {0}_ranks (`Jour` varchar(2), `Mois` varchar(2), `Annee` varchar(2), `DateID` INT, `User` BIGINT, `Salon` BIGINT,`Count` INT, PRIMARY KEY (`DateID`, `User`, `Salon`))".format(option))
    ishere=curseur.execute("SELECT * FROM {0}_ranks WHERE User={1} AND DateID={2} AND Salon={3}".format(option,user,dateID,salon)).fetchone()
    if ishere==None:
        curseur.execute("INSERT INTO {0}_ranks VALUES ('{1}','{2}','{3}',{4},{5},{6},{7})".format(option,jour,mois,annee,dateID,user,salon,count))
    else:
        curseur.execute("UPDATE {0}_ranks SET Count=Count+{1} WHERE User={2} AND DateID={3} AND Salon={4}".format(option,count,user,dateID,salon))

def executeStatsObj(option,user,salon,obj,count,curseur,jour=None,mois=None,annee=None):
    if jour==None:
        jour,mois,annee,dateID=strftime("%d"),strftime("%m"),strftime("%y"),strftime("%y%m%d")
    else:
        dateID="{0}{1}{2}".format(annee,mois,jour)

    curseur.execute("CREATE TABLE IF NOT EXISTS {0}_ranks (`Jour` varchar(2), `Mois` varchar(2), `Annee` varchar(2), `DateID` INT, `User` BIGINT, `Salon` BIGINT, `Obj` BIGINT, `Count` INT, PRIMARY KEY(`DateID`, `User`, `Obj`, `Salon`))".format(option))
    ishere=curseur.execute("SELECT * FROM {0}_ranks WHERE User={1} AND DateID={2} AND Obj={3} AND Salon={4}".format(option,user,dateID,obj,salon)).fetchone()
    if ishere==None:
        curseur.execute("INSERT INTO {0}_ranks VALUES ('{1}','{2}','{3}',{4},{5},{6},{7},{8})".format(option,jour,mois,annee,dateID,user,salon,obj,count))
    else:
        curseur.execute("UPDATE {0}_ranks SET Count=Count+{1} WHERE User={2} AND DateID={3} AND Obj={4} AND Salon={5}".format(option,count,user,dateID,obj,salon))

def executeStatsFreq(option,user,salon,heure,count,curseur,mois=None,annee=None):
    if mois==None:
        mois,annee,dateID=strftime("%m"),strftime("%y"),strftime("%y%m")
    else:
        dateID="{0}{1}".format(annee,mois)

    curseur.execute("CREATE TABLE IF NOT EXISTS {0}_freq (`Mois` varchar(2), `Annee` varchar(2), `DateID` INT, `Heure` varchar(2), `User` BIGINT, `Salon` BIGINT,`Count` INT, PRIMARY KEY (`DateID`, `User`, `Salon`, `Heure`))".format(option))
    ishere=curseur.execute("SELECT * FROM {0}_freq WHERE User={1} AND DateID={2} AND Heure='{3}' AND Salon={4}".format(option,user,dateID,heure,salon)).fetchone()
    if ishere==None:
        curseur.execute("INSERT INTO {0}_freq VALUES ('{1}','{2}',{3},'{4}',{5},{6},{7})".format(option,mois,annee,dateID,heure,user,salon,count))
    else:
        curseur.execute("UPDATE {0}_freq SET Count=Count+{1} WHERE User={2} AND DateID={3} AND Heure='{4}' AND Salon={5}".format(option,count,user,dateID,heure,salon))

def executeJeux(option,user,guild,state,curseur,jour=None,mois=None,annee=None):
    if jour==None:
        jour,mois,annee,dateID=strftime("%d"),strftime("%m"),strftime("%y"),strftime("%y%m%d")
    else:
        dateID="{0}{1}{2}".format(annee,mois,jour)

    curseur.execute("CREATE TABLE IF NOT EXISTS {0}_ranks (`Jour` varchar(2), `Mois` varchar(2), `Annee` varchar(2), `DateID` INT, `User` BIGINT, `Guild` BIGINT,`W` INT, `L` INT, PRIMARY KEY (`DateID`, `User`, `Guild`))".format(option))
    ishere=curseur.execute("SELECT * FROM {0}_ranks WHERE User={1} AND DateID={2} AND Guild={3}".format(option,user,dateID,guild)).fetchone()
    if ishere==None:
        if state == "W":
            curseur.execute("INSERT INTO {0}_ranks VALUES ('{1}','{2}','{3}',{4},{5},{6},1,0)".format(option,jour,mois,annee,dateID,user,guild))
        else:
            curseur.execute("INSERT INTO {0}_ranks VALUES ('{1}','{2}','{3}',{4},{5},{6},0,1)".format(option,jour,mois,annee,dateID,user,guild))
    else:
        curseur.execute("UPDATE {0}_ranks SET {1}={1}+1 WHERE User={2} AND DateID={3} AND Guild={4}".format(option,state,user,dateID,guild))
    
    if state == "W":
        countW=curseur.execute("SELECT W FROM {0}_ranks WHERE User = {1}".format(option,user)).fetchone()["W"]
        if countW in (5,10):
            titresJeux(countW,option,user)
        return countW

def executeStatsTrivial(user,categ,guild,count,curseur,jour=None,mois=None,annee=None):
    if jour==None:
        jour,mois,annee,dateID=strftime("%d"),strftime("%m"),strftime("%y"),strftime("%y%m%d")
    else:
        dateID="{0}{1}{2}".format(annee,mois,jour)

    curseur.execute("CREATE TABLE IF NOT EXISTS trivial_ranks (`Jour` varchar(2), `Mois` varchar(2), `Annee` varchar(2), `DateID` INT, `User` BIGINT, `Guild` BIGINT, `Categ` INT, Count` INT, PRIMARY KEY (`DateID`, `User`, `Guild`, `Categ`))")
    ishere=curseur.execute("SELECT * FROM trivial_ranks WHERE User={0} AND DateID={1} AND Guild={2} AND Categ={3}".format(user,dateID,guild,categ)).fetchone()
    if ishere==None:
        curseur.execute("INSERT INTO trivial_ranks VALUES ('{0}','{1}','{2}',{3},{4},{5},{6},{7})".format(jour,mois,annee,dateID,user,guild,categ,count))
    else:
        curseur.execute("UPDATE trivial_ranks SET Count=Count+{0} WHERE User={1} AND DateID={2} AND Guild={3} AND Categ={4}".format(count,user,dateID,guild,categ))

def executeTrivialStreak(user,count,curseur,jour=None,mois=None,annee=None):
    if jour==None:
        jour,mois,annee,dateID=strftime("%d"),strftime("%m"),strftime("%y"),strftime("%y%m%d")
    else:
        dateID="{0}{1}{2}".format(annee,mois,jour)

    curseur.execute("CREATE TABLE IF NOT EXISTS trivialStreak_ranks (`Jour` varchar(2), `Mois` varchar(2), `Annee` varchar(2), `DateID` INT, `User` BIGINT, `Count` INT, PRIMARY KEY (`DateID`, `User`))")

    ishere=curseur.execute("SELECT * FROM trivialStreak_ranks WHERE User={0}".format(user)).fetchone()
    if ishere==None:
        curseur.execute("INSERT INTO trivialStreak_ranks VALUES ('{0}','{1}','{2}',{3},{4},{5})".format(jour,mois,annee,dateID,user,count))
    else:
        if count > ishere["Count"]:
            curseur.execute("UPDATE trivialStreak_ranks SET Count={0}, Jour={1}, Mois={2}, Annee={3}, DateID={4} WHERE User={5}".format(count,jour,mois,annee,dateID,user))
            return True, ishere["Count"]
    return False, ishere["Count"]



"""def exeClassicFocus(count,id,user,option):
    dateID=int(strftime("%y")+strftime("%m")+strftime("%d"))
    connexionUser,curseurUser=connectSQL(user,"Settings","Focus","GL","")
    connexionGL,curseurGL=connectSQL(user,option,"Focus","GL","")

    connexion,curseur=connectSQL(user,option,"Focus",strftime("%m"),strftime("%y"))
    compteurSQL(curseur,tableauMois[strftime("%m")]+strftime("%y"),id,(0,id,strftime("%m"),strftime("%y"),count,0),count,(strftime("%d"),strftime("%m"),strftime("%y")),(strftime("%m"),strftime("%y")),False,True,1,curseurGL)
    connexion.commit()

    connexion,curseur=connectSQL(user,option,"Focus","TO",strftime("%y"))
    compteurSQL(curseur,"to"+strftime("%y"),id,(0,id,"TO",strftime("%y"),count,0),count,(strftime("%d"),strftime("%m"),strftime("%y")),("TO",strftime("%y")),False,True,1,curseurGL)
    connexion.commit()

    compteurSQL(curseurGL,"glob",id,(0,id,"TO","GL",count,0),count,(strftime("%d"),strftime("%m"),strftime("%y")),("TO","GL"),False,True,1,curseurGL)
    connexionGL.commit()
    
    dailySQL(dateID,(strftime("%d"),strftime("%m"),strftime("%y")),option,curseurUser,user,"Focus")
    rapportsFocus(user,"ranks",id,None,count,(0,id,strftime("%d"),strftime("%m"),strftime("%y"),dateID,count,option),strftime("%d"),strftime("%m"),strftime("%y"),option)
    connexionUser.commit()
    connexionGL.commit()


def exeFocusFreq(start,stop,user,option,id):
    import datetime
    dateStart=datetime.datetime.fromtimestamp(start)
    dateStop=datetime.datetime.fromtimestamp(stop)
    heureStart,minStart,secStart=int(dateStart.strftime("%H")),int(dateStart.strftime("%M")),int(dateStart.strftime("%S"))
    heureStop,minStop,secStop=int(dateStop.strftime("%H")),int(dateStop.strftime("%M")),int(dateStop.strftime("%S"))

    connexionGL,curseurGL=connectSQL(user,option,"Focus","GL","")
    connexionMois,curseurMois=connectSQL(user,option,"Focus",strftime("%m"),strftime("%y"))
    connexionTO,curseurTO=connectSQL(user,option,"Focus","TO",strftime("%y"))

    for i in range(heureStart,heureStop+1):
        if heureStart==heureStop:
            count=(minStop-minStart)*60+(secStop-secStart)
        elif i==heureStart:
            count=3600-minStart*60-secStart
        elif i==heureStop:
            count=minStop*60+secStop
        else:
            count=3600

        compteurSQL(curseurMois,"freq"+id+tableauMois[strftime("%m")]+strftime("%y"),i,(0,i,strftime("%m"),strftime("%y"),count,0),count,None,None,None,False,1,curseurGL)
        compteurSQL(curseurTO,"freq"+id+"to"+strftime("%y"),i,(0,i,"TO",strftime("%y"),count,0),count,None,None,None,False,1,curseurGL)
        compteurSQL(curseurGL,"freq"+id+"glob",i,(0,i,"TO","GL",count,0),count,None,None,None,False,1,curseurGL)

    connexionGL.commit()
    connexionMois.commit()
    connexionTO.commit()"""
    