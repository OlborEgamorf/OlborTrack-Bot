from time import strftime
from Stats.SQL.Compteur import compteurSQL
from Stats.SQL.Rapports import rapportsSQL
from Stats.SQL.Daily import dailySQL
from Stats.SQL.CompteurP4 import compteurJeuxSQL
from Stats.SQL.Historique import histoSQL, histoSQLJeux
from Stats.SQL.ConnectSQL import connectSQL
from Titres.Outils import titresJeux

tableauMois={"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre","TO":"TOTAL"}

def exeClassic(count,id,nom,curseurGuild,guild):
    dateID=int(strftime("%y")+strftime("%m")+strftime("%d"))
    connexionGL,curseurGL=connectSQL(guild.id,nom,"Stats","GL","")

    connexion,curseur=connectSQL(guild.id,nom,"Stats",strftime("%m"),strftime("%y"))
    compteurSQL(curseur,tableauMois[strftime("%m")]+strftime("%y"),id,(0,id,strftime("%m"),strftime("%y"),count,0),count,(strftime("%d"),strftime("%m"),strftime("%y")),(strftime("%m"),strftime("%y")),"persoM",False,True,1,curseurGL)
    connexion.commit()

    connexion,curseur=connectSQL(guild.id,nom,"Stats","TO",strftime("%y"))
    compteurSQL(curseur,"to"+strftime("%y"),id,(0,id,"TO",strftime("%y"),count,0),count,(strftime("%d"),strftime("%m"),strftime("%y")),("TO",strftime("%y")),"persoA",False,True,1,curseurGL)
    connexion.commit()

    liste=compteurSQL(curseurGL,"glob",id,(0,id,"TO","GL",count,0),count,(strftime("%d"),strftime("%m"),strftime("%y")),("TO","GL"),"persoA",False,True,1,curseurGL)
    if nom in ("Messages","Voice"):
        compteurSQL(curseurGL,"dayRank",int(strftime("%y")+strftime("%m")+strftime("%d")),(0,int(strftime("%y")+strftime("%m")+strftime("%d")),strftime("%d"),strftime("%m"),strftime("%y"),count),count,None,None,None,None,False,3,curseurGL)
    
    if nom in ("Emotes","Reactions"):
        countGL=curseurGL.execute("SELECT Count FROM glob WHERE ID={0}".format(id)).fetchone()["Count"]
        for i in liste:
            if i["Rank"]>400:
                curseurGL.execute("DROP TABLE IF EXISTS persoM{0}".format(i["ID"]))
                curseurGL.execute("DROP TABLE IF EXISTS persoA{0}".format(i["ID"]))
    connexionGL.commit()

    dailySQL(dateID,(strftime("%d"),strftime("%m"),strftime("%y")),nom,curseurGuild,guild.id,"Stats")
    if nom not in ("Mentions","Mentionne"):
        rapportsSQL(guild,"ranks",id,None,count,(0,id,strftime("%d"),strftime("%m"),strftime("%y"),dateID,count,nom),strftime("%d"),strftime("%m"),strftime("%y"),nom)

def exeObj(count,idObj,id,obj,guild,nom):
    dateID=int(strftime("%y")+strftime("%m")+strftime("%d"))
    connexionGL,curseurGL=connectSQL(guild.id,nom,"Stats","GL","")

    connexion,curseur=connectSQL(guild.id,nom,"Stats",strftime("%m"),strftime("%y"))
    compteurSQL(curseur,tableauMois[strftime("%m")]+strftime("%y")+str(idObj),id,(0,id,idObj,strftime("%m"),strftime("%y"),count),count,(strftime("%d"),strftime("%m"),strftime("%y")),(strftime("%m"),strftime("%y")),"persoM",obj,False,2,curseurGL)
    if nom in ("Emotes","Reactions") and curseur.execute("SELECT Count FROM {0}{1} WHERE ID={2}".format(tableauMois[strftime("%m")],strftime("%y"),idObj)).fetchone()["Count"]<10:
        curseur.execute("DROP TABLE {0}{1}{2}".format(tableauMois[strftime("%m")],strftime("%y"),idObj))
    connexion.commit()

    connexion,curseur=connectSQL(guild.id,nom,"Stats","TO",strftime("%y"))
    compteurSQL(curseur,"to"+strftime("%y")+str(idObj),id,(0,id,idObj,"TO",strftime("%y"),count),count,(strftime("%d"),strftime("%m"),strftime("%y")),("TO",strftime("%y")),"persoA",obj,False,2,curseurGL)
    if nom in ("Emotes","Reactions") and curseur.execute("SELECT Count FROM to{0} WHERE ID={1}".format(strftime("%y"),idObj)).fetchone()["Count"]<25:
        curseur.execute("DROP TABLE to{0}{1}".format(strftime("%y"),idObj))
    connexion.commit()

    liste=compteurSQL(curseurGL,"glob"+str(idObj),id,(0,id,idObj,"TO","GL",count),count,(strftime("%d"),strftime("%m"),strftime("%y")),("TO","GL"),"persoA",obj,False,2,curseurGL)
    if nom in ("Emotes","Reactions"):
        if curseurGL.execute("SELECT Count FROM glob WHERE ID={0}".format(idObj)).fetchone()["Count"]<50:
            curseurGL.execute("DROP TABLE glob{0}".format(idObj))
        if curseurGL.execute("SELECT Rank FROM glob WHERE ID={0}".format(idObj)).fetchone()["Rank"]>400:
            for i in liste:
                curseurGL.execute("DROP TABLE IF EXISTS persoM{0}{1}".format(i["ID"],idObj))
                curseurGL.execute("DROP TABLE IF EXISTS persoA{0}{1}".format(i["ID"],idObj))
    connexionGL.commit()

    if nom not in ("Mentions","Mentionne"):
        rapportsSQL(guild,"objs",idObj,id,count,(0,id,idObj,strftime("%d"),strftime("%m"),strftime("%y"),dateID,count,nom),strftime("%d"),strftime("%m"),strftime("%y"),nom)

def exeJeuxSQL(id,idObj,state,guild,curseurGuild,count,option,tours):
    dictCount={"W":2,"L":-1}
    dictW={"W":1,"L":0}
    dictL={"W":0,"L":1}
    connexionGL,curseurGL=connectSQL(guild,option,"Jeux","GL","")

    connexion,curseur=connectSQL(guild,option,"Jeux",strftime("%m"),strftime("%y"))
    compteurJeuxSQL(curseur,tableauMois[strftime("%m")]+strftime("%y"),id,(0,id,strftime("%m"),strftime("%y"),dictW[state],dictL[state],dictCount[state],0),dictCount[state],(strftime("%d"),strftime("%m"),strftime("%y")),(strftime("%m"),strftime("%y")),"persoM",False,state,4,curseurGL)
    if idObj!=None:
        compteurJeuxSQL(curseur,tableauMois[strftime("%m")]+strftime("%y")+str(idObj),id,(0,id,idObj,strftime("%m"),strftime("%y"),dictW[state],dictL[state],dictCount[state],0),dictCount[state],(strftime("%d"),strftime("%m"),strftime("%y")),(strftime("%m"),strftime("%y")),"persoM",True,state,5,curseurGL)
    connexion.commit()

    connexion,curseur=connectSQL(guild,option,"Jeux","TO",strftime("%y"))
    compteurJeuxSQL(curseur,"to"+strftime("%y"),id,(0,id,"TO",strftime("%y"),dictW[state],dictL[state],dictCount[state],0),dictCount[state],(strftime("%d"),strftime("%m"),strftime("%y")),("TO",strftime("%y")),"persoA",False,state,4,curseurGL)
    if idObj!=None:
        compteurJeuxSQL(curseur,"to"+strftime("%y")+str(idObj),id,(0,id,idObj,"TO",strftime("%y"),dictW[state],dictL[state],dictCount[state],0),dictCount[state],(strftime("%d"),strftime("%m"),strftime("%y")),("TO",strftime("%y")),"persoA",True,state,5,curseurGL)
    connexion.commit()

    compteurJeuxSQL(curseurGL,"glob",id,(0,id,"TO","GL",dictW[state],dictL[state],dictCount[state],0),dictCount[state],(strftime("%d"),strftime("%m"),strftime("%y")),("TO","GL"),"persoA",False,state,4,curseurGL)
    if idObj!=None:
        compteurJeuxSQL(curseurGL,"glob"+str(idObj),id,(0,id,idObj,"TO","GL",dictW[state],dictL[state],dictCount[state],0),dictCount[state],(strftime("%d"),strftime("%m"),strftime("%y")),("TO","GL"),"persoA",True,state,5,curseurGL)
        histoSQLJeux(curseurGL,id,tours,strftime("%d")+"/"+strftime("%m")+"/"+strftime("%y"),idObj,state)
    if guild=="OT" and state=="W":
        count=curseurGL.execute("SELECT Count FROM glob WHERE ID= {0}".format(id)).fetchone()["Count"]
        if count in (5,10):
            titresJeux(count,option,id)
    connexionGL.commit()

    dailySQL(int(strftime("%y")+strftime("%m")+strftime("%d")),(strftime("%d"),strftime("%m"),strftime("%y")),option,curseurGuild,guild,"Jeux")