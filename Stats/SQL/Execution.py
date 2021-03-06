from time import strftime
from Stats.SQL.Compteur import compteurSQL
from Stats.SQL.Rapports import rapportsSQL
from Stats.SQL.Daily import dailySQL
from Stats.SQL.CompteurJeux import compteurJeuxSQL
from Stats.SQL.Historique import histoSQL, histoSQLJeux
from Stats.SQL.ConnectSQL import connectSQL
from Titres.Outils import titresJeux

tableauMois={"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre","TO":"TOTAL"}

def exeClassic(count,id,nom,curseurGuild,guild):
    option="Stats"
    if nom=="Cross":
        option=="Jeux"
    dateID=int(strftime("%y")+strftime("%m")+strftime("%d"))
    connexionGL,curseurGL=connectSQL(guild.id,nom,option,"GL","")

    connexion,curseur=connectSQL(guild.id,nom,option,strftime("%m"),strftime("%y"))
    compteurSQL(curseur,tableauMois[strftime("%m")]+strftime("%y"),id,(0,id,strftime("%m"),strftime("%y"),count,0),count,(strftime("%d"),strftime("%m"),strftime("%y")),(strftime("%m"),strftime("%y")),False,True,1,curseurGL)
    connexion.commit()

    connexion,curseur=connectSQL(guild.id,nom,option,"TO",strftime("%y"))
    compteurSQL(curseur,"to"+strftime("%y"),id,(0,id,"TO",strftime("%y"),count,0),count,(strftime("%d"),strftime("%m"),strftime("%y")),("TO",strftime("%y")),False,True,1,curseurGL)
    connexion.commit()

    compteurSQL(curseurGL,"glob",id,(0,id,"TO","GL",count,0),count,(strftime("%d"),strftime("%m"),strftime("%y")),("TO","GL"),False,True,1,curseurGL)
    if nom in ("Messages","Voice"):
        compteurSQL(curseurGL,"dayRank",int(strftime("%y")+strftime("%m")+strftime("%d")),(0,int(strftime("%y")+strftime("%m")+strftime("%d")),strftime("%d"),strftime("%m"),strftime("%y"),count),count,None,None,None,False,3,curseurGL)
    
    connexionGL.commit()

    dailySQL(dateID,(strftime("%d"),strftime("%m"),strftime("%y")),nom,curseurGuild,guild.id,option)
    rapportsSQL(guild,"ranks",id,None,count,(0,id,strftime("%d"),strftime("%m"),strftime("%y"),dateID,count,nom),strftime("%d"),strftime("%m"),strftime("%y"),nom)

def exeObj(count,idObj,id,obj,guild,nom):
    option="Stats"
    if nom=="Cross":
        option=="Jeux"
    dateID=int(strftime("%y")+strftime("%m")+strftime("%d"))
    connexionGL,curseurGL=connectSQL(guild.id,nom,option,"GL","")

    connexion,curseur=connectSQL(guild.id,nom,option,strftime("%m"),strftime("%y"))
    compteurSQL(curseur,tableauMois[strftime("%m")]+strftime("%y")+str(idObj),id,(0,id,idObj,strftime("%m"),strftime("%y"),count),count,(strftime("%d"),strftime("%m"),strftime("%y")),(strftime("%m"),strftime("%y")),obj,False,2,curseurGL)
    if nom in ("Emotes","Reactions") and curseur.execute("SELECT Count FROM {0}{1} WHERE ID={2}".format(tableauMois[strftime("%m")],strftime("%y"),idObj)).fetchone()["Count"]<10:
        curseur.execute("DROP TABLE {0}{1}{2}".format(tableauMois[strftime("%m")],strftime("%y"),idObj))
    connexion.commit()

    connexion,curseur=connectSQL(guild.id,nom,option,"TO",strftime("%y"))
    compteurSQL(curseur,"to"+strftime("%y")+str(idObj),id,(0,id,idObj,"TO",strftime("%y"),count),count,(strftime("%d"),strftime("%m"),strftime("%y")),("TO",strftime("%y")),obj,False,2,curseurGL)
    if nom in ("Emotes","Reactions") and curseur.execute("SELECT Count FROM to{0} WHERE ID={1}".format(strftime("%y"),idObj)).fetchone()["Count"]<25:
        curseur.execute("DROP TABLE to{0}{1}".format(strftime("%y"),idObj))
    connexion.commit()

    compteurSQL(curseurGL,"glob"+str(idObj),id,(0,id,idObj,"TO","GL",count),count,(strftime("%d"),strftime("%m"),strftime("%y")),("TO","GL"),obj,False,2,curseurGL)
    if nom in ("Emotes","Reactions"):
        if curseurGL.execute("SELECT Count FROM glob WHERE ID={0}".format(idObj)).fetchone()["Count"]<50:
            curseurGL.execute("DROP TABLE glob{0}".format(idObj))
    connexionGL.commit()

    rapportsSQL(guild,"objs",idObj,id,count,(0,id,idObj,strftime("%d"),strftime("%m"),strftime("%y"),dateID,count,nom),strftime("%d"),strftime("%m"),strftime("%y"),nom)

def exeJeuxSQL(id,idObj,state,guild,curseurGuild,option,tours):
    dictCount={"W":2,"L":-1}
    dictW={"W":1,"L":0}
    dictL={"W":0,"L":1}
    connexionGL,curseurGL=connectSQL(guild,option,"Jeux","GL","")

    connexion,curseur=connectSQL(guild,option,"Jeux",strftime("%m"),strftime("%y"))
    compteurJeuxSQL(curseur,tableauMois[strftime("%m")]+strftime("%y"),id,(0,id,strftime("%m"),strftime("%y"),dictW[state],dictL[state],dictCount[state],0),dictCount[state],(strftime("%d"),strftime("%m"),strftime("%y")),(strftime("%m"),strftime("%y")),False,state,4,curseurGL)
    if idObj!=None:
        compteurJeuxSQL(curseur,tableauMois[strftime("%m")]+strftime("%y")+str(idObj),id,(0,id,idObj,strftime("%m"),strftime("%y"),dictW[state],dictL[state],dictCount[state],0),dictCount[state],(strftime("%d"),strftime("%m"),strftime("%y")),(strftime("%m"),strftime("%y")),True,state,5,curseurGL)
    connexion.commit()

    connexion,curseur=connectSQL(guild,option,"Jeux","TO",strftime("%y"))
    compteurJeuxSQL(curseur,"to"+strftime("%y"),id,(0,id,"TO",strftime("%y"),dictW[state],dictL[state],dictCount[state],0),dictCount[state],(strftime("%d"),strftime("%m"),strftime("%y")),("TO",strftime("%y")),False,state,4,curseurGL)
    if idObj!=None:
        compteurJeuxSQL(curseur,"to"+strftime("%y")+str(idObj),id,(0,id,idObj,"TO",strftime("%y"),dictW[state],dictL[state],dictCount[state],0),dictCount[state],(strftime("%d"),strftime("%m"),strftime("%y")),("TO",strftime("%y")),True,state,5,curseurGL)
    connexion.commit()

    compteurJeuxSQL(curseurGL,"glob",id,(0,id,"TO","GL",dictW[state],dictL[state],dictCount[state],0),dictCount[state],(strftime("%d"),strftime("%m"),strftime("%y")),("TO","GL"),False,state,4,curseurGL)
    if idObj!=None:
        compteurJeuxSQL(curseurGL,"glob"+str(idObj),id,(0,id,idObj,"TO","GL",dictW[state],dictL[state],dictCount[state],0),dictCount[state],(strftime("%d"),strftime("%m"),strftime("%y")),("TO","GL"),True,state,5,curseurGL)
        histoSQLJeux(curseurGL,id,tours,strftime("%d")+"/"+strftime("%m")+"/"+strftime("%y"),idObj,state)
    if guild=="OT" and state=="W":
        countW=curseurGL.execute("SELECT W FROM glob WHERE ID= {0}".format(id)).fetchone()["W"]
        if countW in (5,10):
            titresJeux(countW,option,id)
    connexionGL.commit()

    dailySQL(int(strftime("%y")+strftime("%m")+strftime("%d")),(strftime("%d"),strftime("%m"),strftime("%y")),option,curseurGuild,guild,"Jeux")

    if "countW" in locals():
        return countW