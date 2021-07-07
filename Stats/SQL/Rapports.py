from Stats.SQL.ConnectSQL import connectSQL

def rapportsSQL(guild,table,id,idcomp,count,insert,jour,mois,annee,option):
    connexion,base=connectSQL(guild.id,"Rapports","Stats","GL","")
    if option in ("Mentions","Mentionne"):
        return
    typeRapport={"ranks":"(Rank INT, ID BIGINT, Jour TEXT, Mois TEXT, Annee TEXT, DateID INT, Count INT, Type TEXT, PRIMARY KEY(Jour,Mois,Annee,ID,Type))","objs":"(Rank INT, ID BIGINT, IDComp BIGINT, Jour TEXT, Mois TEXT, Annee TEXT, DateID INT, Count INT, Type TEXT, PRIMARY KEY(Jour,Mois,Annee,ID,Type,IDComp))"}
    base.execute("CREATE TABLE IF NOT EXISTS {0} {1}".format(table,typeRapport[table]))

    if table=="ranks":
        etat=base.execute("SELECT * FROM {0} WHERE ID={1} AND Jour='{2}' AND Mois='{3}' AND Annee='{4}' AND Type='{5}'".format(table,id,jour,mois,annee,option)).fetchone()
    else:
        etat=base.execute("SELECT * FROM {0} WHERE IDComp={1} AND Jour='{2}' AND Mois='{3}' AND Annee='{4}' AND Type='{5}' AND ID={6}".format(table,id,jour,mois,annee,option,idcomp)).fetchone()

    if etat==None:
        base.execute("INSERT INTO {0} VALUES {1}".format(table,insert))
        countB,countN,baseRank=0,count,0
    else:
        countB,baseRank=etat["Count"],etat["Rank"]
        countN=countB+count
        if table=="ranks":
            base.execute("UPDATE ranks SET Count= {0} WHERE ID={1} AND Jour='{2}' AND Mois='{3}' AND Annee='{4}' AND Type='{5}'".format(countN,id,jour,mois,annee,option))
        else:
            base.execute("UPDATE objs SET Count= {0} WHERE ID={1} AND IDComp={2} AND Jour='{3}' AND Mois='{4}' AND Annee='{5}' AND Type='{6}'".format(countN,idcomp,id,jour,mois,annee,option))

    if table=="ranks":
        rank=base.execute("SELECT COUNT() AS nombre FROM ranks WHERE Count> {0} AND Jour='{1}' AND Mois='{2}' AND Annee='{3}' AND Type='{4}'".format(countN,jour,mois,annee,option)).fetchone()["nombre"]
        equal=base.execute("SELECT COUNT() AS nombre FROM ranks WHERE Rank= {0} AND Jour='{1}' AND Mois='{2}' AND Annee='{3}' AND Type='{4}'".format(baseRank,jour,mois,annee,option)).fetchone()["nombre"]
    else:
        rank=base.execute("SELECT COUNT() AS nombre FROM objs WHERE Count> {0} AND Jour='{1}' AND Mois='{2}' AND Annee='{3}' AND Type='{4}' AND IDComp={5}".format(countN,jour,mois,annee,option,id)).fetchone()["nombre"]
        equal=base.execute("SELECT COUNT() AS nombre FROM objs WHERE Rank= {0} AND Jour='{1}' AND Mois='{2}' AND Annee='{3}' AND Type='{4}' AND IDComp={5}".format(baseRank,jour,mois,annee,option,id)).fetchone()["nombre"]
    newRank=rank+1

    if newRank!=baseRank or equal!=0:
        if table=="ranks":
            base.execute("UPDATE ranks SET Rank= {0} WHERE ID = {1} AND Jour='{2}' AND Mois='{3}' AND Annee='{4}' AND Type='{5}'".format(newRank,id,jour,mois,annee,option))
        else:
            base.execute("UPDATE objs SET Rank= {0} WHERE ID = {1} AND Jour='{2}' AND Mois='{3}' AND Annee='{4}' AND Type='{5}' AND IDComp={6}".format(newRank,idcomp,jour,mois,annee,option,id))
        countE=countN

        if baseRank==0:
            if table=="ranks":
                exe="SELECT * FROM ranks WHERE Count<= {0} AND Jour='{1}' AND Mois='{2}' AND Annee='{3}' AND Type='{4}' ORDER BY Count DESC".format(countN,jour,mois,annee,option)
            else:
                exe="SELECT * FROM objs WHERE Count<= {0} AND Jour='{1}' AND Mois='{2}' AND Annee='{3}' AND Type='{4}' AND IDComp={5} ORDER BY Count DESC".format(countN,jour,mois,annee,option,id)
        elif countN>=countB:
            if table=="ranks":
                exe="SELECT * FROM ranks WHERE Count<= {0} AND Count>= {1} AND Jour='{2}' AND Mois='{3}' AND Annee='{4}' AND Type='{5}' ORDER BY Count DESC".format(countN,countB,jour,mois,annee,option)
            else:
                exe="SELECT * FROM objs WHERE Count<= {0} AND Count>= {1} AND Jour='{2}' AND Mois='{3}' AND Annee='{4}' AND Type='{5}' AND IDComp={6} ORDER BY Count DESC".format(countN,countB,jour,mois,annee,option,id)

        else:
            newRank=baseRank
            if table=="ranks":
                exe="SELECT * FROM ranks WHERE Count>= {0} AND Count<= {1} AND Jour='{2}' AND Mois='{3}' AND Annee='{4}' AND Type='{5}' ORDER BY Count DESC".format(countN,countB,jour,mois,annee,option)
            else:
                exe="SELECT * FROM objs WHERE Count>= {0} AND Count<= {1} AND Jour='{2}' AND Mois='{3}' AND Annee='{4}' AND Type='{5}' AND IDComp={6} ORDER BY Count DESC".format(countN,countB,jour,mois,annee,option,id)
                
        etat=base.execute(exe).fetchall()
        for i in range(len(etat)):
            if etat[i]["ID"]!=id:
                if etat[i]["Count"]==countN:
                    newRank=rank+1
                elif etat[i]["Count"]!=countE:
                    if countN>=countB:
                        newRank=rank+i+1
                    else:
                        newRank=baseRank+i
                    countE=etat[i]["Count"]
                if table=="ranks":
                    base.execute("UPDATE ranks SET Rank= {0} WHERE ID = {1} AND Jour='{2}' AND Mois='{3}' AND Annee='{4}' AND Type='{5}'".format(newRank,etat[i]["ID"],jour,mois,annee,option)) 
                else:
                    base.execute("UPDATE objs SET Rank= {0} WHERE ID = {1} AND IDComp={2} AND Jour='{3}' AND Mois='{4}' AND Annee='{5}' AND Type='{6}'".format(newRank,etat[i]["ID"],id,jour,mois,annee,option)) 
    connexion.commit()