from Core.Fonctions.EcritureRecherche3 import rechercheCommande, rechercheCsv, rechercheHelp
from Stats.SQL.ConnectSQL import connectSQL
from Stats.SQL.NewGuild import createDirSQL
from Core.Fonctions.Phrase import createPhrase
import discord
import os
import csv
from Stats.Tracker.Jeux import exeStatsJeux
from Stats.SQL.CompteurP4 import compteurJeuxSQL
from Stats.SQL.Daily import dailySQL
from Stats.SQL.Historique import histoSQLJeux
from Stats.SQL.Compteur import compteurSQL

def convPerms(guild):
    connexion,curseur=connectSQL(guild.id,"Guild","Guild",None,None)
    table=rechercheCsv("perms",guild.id,0,0,0,0)[0]
    for i in table:
        if i["Module"]=="Autre":i["Module"]="Divers"
        if i["Module"]=="Fréquences":i["Module"]="Freq"
        if i["Module"]=="Réactions":i["Module"]="Reactions"
        if i["Module"]=="Emojis":i["Module"]="Emotes"
        curseur.execute("UPDATE modulesStats SET Statut={0} WHERE Module='{1}'".format(i["Statut"],i["Module"]))
    table=rechercheCsv("permscmd",guild.id,0,0,0,0)[0]
    for i in table:
        if i["Module"]=="Custom":i["Module"]="Outils"
        curseur.execute("UPDATE modulesStats SET Statut={0} WHERE Module='{1}'".format(i["Statut"],i["Module"]))
    table=rechercheCsv("hide",guild.id,0,0,0,0)[0]
    for i in table:
        if i["Type"]=="chan":
            curseur.execute("UPDATE chans SET Hide=True WHERE ID={0}".format(i["ID"]))
    table=rechercheCsv("blind",guild.id,0,0,0,0)[0]
    for i in table:
        if i["Type"]=="chan":
            curseur.execute("UPDATE chans SET Blind=True WHERE ID={0}".format(i["ID"]))
    table=rechercheCsv("mute",guild.id,0,0,0,0)[0]
    for i in table:
        if i["Type"]=="chan":
            curseur.execute("UPDATE chans SET Mute=True WHERE ID={0}".format(i["ID"]))
    connexion.commit()

def convSV(guild):
    connexion,curseur=connectSQL(guild.id,"Guild","Guild",None,None)
    table=rechercheCommande(guild.id,None,"quote")[0]
    for i in table:
        curseur.execute("INSERT INTO savezvous VALUES('{0}',{1},'{2}',{3})".format(createPhrase(i["Quote"].split(" ")),i["Auteur"],i["Image"],i["Numéro"]))
    connexion.commit()

async def convSB(guild):
    connexion,curseur=connectSQL(guild.id,"Guild","Guild",None,None)
    table=rechercheCsv("starboard",guild.id,0,0,0,0)[0]
    salons=[]
    for i in table:
        num=curseur.execute("SELECT COUNT() as Nombre FROM sb").fetchone()["Nombre"]+1
        if i["Salon"] not in salons:
            salons.append(i["Salon"])
        if i["ID"]=="None":
            i["ID"]=ord(i["Emote"])
        curseur.execute("INSERT INTO sb VALUES({0},{1},'{2}',{3},{4})".format(num,i["Salon"],i["Emote"],i["ID"],i["Nombre"]))
    table=rechercheCsv("starmessages",guild.id,0,0,0,0)[0]
    for j in salons:
        for i in table:
            try:
                mess=await guild.get_channel(int(j)).fetch_message(int(i["IDStar"]))
                emot=mess.content.split(" ")[0]
                etat=curseur.execute("SELECT * FROM sb WHERE Emote='{0}'".format(emot)).fetchone()
                if etat!=None:
                    curseur.execute("INSERT INTO sbmessages VALUES({0},{1},'{2}')".format(i["IDMessage"],i["IDStar"],etat["Nombre"]))
            except discord.NotFound:
                pass
    connexion.commit()

async def convCustom(guild):
    table=rechercheHelp(guild.id)[0]
    connexion,curseur=connectSQL(guild.id,"CustomCMD","Guild",None,None)
    for i in table:
        try:
            table2=rechercheCommande(guild.id,i["Commande"],"else")[0]
            if table2[0]["Embed"]=="True":
                table3=rechercheCommande(guild.id,i["Commande"],"embed")[0]
                curseur.execute("INSERT INTO custom VALUES('{0}','{1}',{2},'{3}','{4}','{5}','{6}','{7}','{8}')".format(i["Commande"],createPhrase(table3[0]["Description"].split(" ")),True,createPhrase(table3[0]["Title"].split(" ")),table3[0]["Author"],table3[0]['Color'],table3[0]["Footer"],table3[0]["Image"],table3[0]["Thumbnail"]))
            else:
                curseur.execute("INSERT INTO custom VALUES('{0}','{1}',{2},'{3}','{4}','{5}','{6}','{7}','{8}')".format(i["Commande"],createPhrase(table2[0]["Texte"].split(" ")),False,None,None,None,None,None,None))
            curseur.execute("INSERT INTO help VALUES('{0}','{1}')".format(i["Commande"],createPhrase(i["Description"].split(" "))))
        except:
            pass
    connexion.commit()

async def allConv(guild):
    createDirSQL(guild)
    convPerms(guild)
    convSV(guild)
    await convSB(guild)
    await convCustom(guild)


def convP4(guild):
    for root, dirs, files in os.walk("CSV/_"+str(guild.id)+"/zsers/_P4/"):
        for i in files:
            if i[1]=="h":
                tableStats=[]
                with open(root+"/"+i, encoding="utf-8-sig", newline="") as fichier :
                    for ligne in csv.DictReader(fichier):
                        tableStats.append(dict(ligne))
                for j in tableStats:
                    exeStatsJeuxRecup(int(j["ID"]),int(j["Versus"]),guild.id,"P4",int(j["Tours"]),j["Date"],j["Statut"])

def exeStatsJeuxRecup(idW,idL,guild,option,tours,date,state):
    connexionGuild,curseurGuild=connectSQL(guild,"Guild","Guild",None,None)
    connexionOT,curseurOT=connectSQL("OT","Guild","Guild",None,None)

    if state=="W":
        exeJeuxSQLRecup(idW,idL,"W",guild,curseurGuild,2,option,tours,date)
        exeJeuxSQLRecup(idW,idL,"W","OT",curseurOT,2,option,tours,date)
    else:
        exeJeuxSQLRecup(idW,idL,"L",guild,curseurGuild,-1,option,tours,date)
        exeJeuxSQLRecup(idW,idL,"L","OT",curseurOT,-1,option,tours,date)

    connexionGuild.commit()
    connexionOT.commit()
tableauMois={"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre","TO":"TOTAL"}
def exeJeuxSQLRecup(id,idObj,state,guild,curseurGuild,count,option,tours,date):
    dictCount={"W":2,"L":-1}
    dictW={"W":1,"L":0}
    dictL={"W":0,"L":1}
    connexionGL,curseurGL=connectSQL(guild,option,"Jeux","GL","")
    jour,mois,annee=date[3:5],date[0:2],date[6:8]
    connexion,curseur=connectSQL(guild,option,"Jeux",mois,annee)
    compteurJeuxSQL(curseur,tableauMois[mois]+annee,id,(0,id,mois,annee,dictW[state],dictL[state],dictCount[state],0),dictCount[state],(jour,mois,annee),(mois,annee),"persoM",False,state,4,curseurGL)
    if idObj!=None:
        compteurJeuxSQL(curseur,tableauMois[mois]+annee+str(idObj),id,(0,id,idObj,mois,annee,dictW[state],dictL[state],dictCount[state],0),dictCount[state],(jour,mois,annee),(mois,annee),"persoM",True,state,5,curseurGL)
    connexion.commit()

    connexion,curseur=connectSQL(guild,option,"Jeux","TO",annee)
    compteurJeuxSQL(curseur,"to"+annee,id,(0,id,"TO",annee,dictW[state],dictL[state],dictCount[state],0),dictCount[state],(jour,mois,annee),("TO",annee),"persoA",False,state,4,curseurGL)
    if idObj!=None:
        compteurJeuxSQL(curseur,"to"+annee+str(idObj),id,(0,id,idObj,"TO",annee,dictW[state],dictL[state],dictCount[state],0),dictCount[state],(jour,mois,annee),("TO",annee),"persoA",True,state,5,curseurGL)
    connexion.commit()

    compteurJeuxSQL(curseurGL,"glob",id,(0,id,"TO","GL",dictW[state],dictL[state],dictCount[state],0),dictCount[state],(jour,mois,annee),("TO","GL"),"persoA",False,state,4,curseurGL)
    if idObj!=None:
        compteurJeuxSQL(curseurGL,"glob"+str(idObj),id,(0,id,idObj,"TO","GL",dictW[state],dictL[state],dictCount[state],0),dictCount[state],(jour,mois,annee),("TO","GL"),"persoA",True,state,5,curseurGL)
        histoSQLJeux(curseurGL,id,tours,jour+"/"+mois+"/"+annee,idObj,state)
    connexionGL.commit()

def convTrivial():
    for i in range(12):
        tableStats=[]
        with open("CSV/trivial/_rank/_{0}.csv".format(i), encoding="utf-8-sig", newline="") as fichier :
            for ligne in csv.DictReader(fichier):
                tableStats.append(dict(ligne))
        for j in tableStats:
            gestionMulti(i,int(j["ID"]),int(j["Count"]))

def gestionMulti(categ,author,points):
    niveaux=[30, 60, 100, 150, 200, 400, 600, 1000, 1500, 2000, 3000, 4000, 5000, 7500, 10000, 20000, 30000, 40000, 50000, 100000, 1000000]
    listeNoms=["Culture","Divertissement","Sciences","Mythologie","Sport","Géographie","Histoire","Politique","Art","Célébrités","Animaux","Véhicules","Global"]
    connexion,curseur=connectSQL("OT",author,"Trivial",None,None)
    curseur.execute("CREATE TABLE IF NOT EXISTS trivial{0} (ID BIGINT, IDCateg INT, Categ TEXT, Exp INT, Niveau INT, Next INT, Multi INT)".format(author))
    table=curseur.execute("SELECT * FROM trivial{0}".format(author)).fetchall()
    if table==[]:
        table=[{"ID":author,"IDCateg":i,"Categ":listeNoms[i],"Exp":0,"Niveau":1,"Next":30,"Multi":0} for i in range(len(listeNoms))]
        many=[tuple(i.values()) for i in table]
        curseur.executemany("INSERT INTO trivial{0} VALUES (?,?,?,?,?,?,?)".format(author),many)

    curseur.execute("UPDATE trivial{0} SET Exp={1} WHERE IDCateg={2}".format(author,table[categ]["Exp"]+points,categ))
    curseur.execute("UPDATE trivial{0} SET Exp={1} WHERE IDCateg=12".format(author,table[12]["Exp"]+points))

    count=0
    while curseur.execute("SELECT Exp FROM trivial{0} WHERE IDCateg={1}".format(author,categ)).fetchone()["Exp"]>=curseur.execute("SELECT Next FROM trivial{0} WHERE IDCateg={1}".format(author,categ)).fetchone()["Next"]:
        count+=1
        curseur.execute("UPDATE trivial{0} SET Next={1} WHERE IDCateg={2}".format(author,niveaux[table[categ]["Niveau"]+count-1],categ))
        curseur.execute("UPDATE trivial{0} SET Niveau={1} WHERE IDCateg={2}".format(author,table[categ]["Niveau"]+count,categ))

    count=0
    while curseur.execute("SELECT Exp FROM trivial{0} WHERE IDCateg=12".format(author)).fetchone()["Exp"]>=curseur.execute("SELECT Next FROM trivial{0} WHERE IDCateg=12".format(author)).fetchone()["Next"]:
        count+=1
        curseur.execute("UPDATE trivial{0} SET Next={1} WHERE IDCateg=12".format(author,niveaux[table[categ]["Niveau"]+count-1]))
        curseur.execute("UPDATE trivial{0} SET Niveau={1} WHERE IDCateg=12".format(author,table[categ]["Niveau"]+count))
    connexion.commit()

    connexion,curseur=connectSQL("OT","ranks","Trivial",None,None)
    compteurSQL(curseur,"trivial{0}".format(categ),author,(0,author,categ,"TO","GL",points),points,None,None,None,None,None,2,None)
    compteurSQL(curseur,"trivial12",author,(0,author,12,"TO","GL",points),points,None,None,None,None,None,2,None)
    
    connexion.commit()