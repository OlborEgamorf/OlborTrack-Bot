from Fonctions.ConnectSQL import connectSQL
from Fonctions.Divers3 import addtoFields, getAnnee, getMois, getObj, nomsOptions
from time import strftime

tableauMois={"01":"Janvier","02":"Février","03":"Mars","04":"Avril","05":"Mai","06":"Juin","07":"Juillet","08":"Aout","09":"Septembre","10":"Octobre","11":"Novembre","12":"Décembre","TO":"Année","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","glob":"GL","to":"TO"}
dictTriArg={"countAsc":"Count","rankAsc":"Rank","countDesc":"Count","rankDesc":"Rank","dateAsc":"DateID","dateDesc":"DateID","periodAsc":"None","periodDesc":"None","moyDesc":"Moyenne","nombreDesc":"Nombre"}
dictTriSens={"countAsc":"ASC","rankAsc":"ASC","countDesc":"DESC","rankDesc":"DESC","dateAsc":"ASC","dateDesc":"DESC","periodAsc":"None","periodDesc":"None","moyDesc":"DESC","nombreDesc":"DESC"}

async def compareUser(ctx,option,turn,react,ligne,guildOT,bot):
    if True:
        connexionCMD,curseurCMD=connectSQL(ctx.guild.id,"Guild")
        connexion,curseur=connectSQL(ctx.guild.id,option) 
        if not react:
            assert ctx.message.mentions!=[]
            mention=ctx.message.mentions[0].id
            assert not guildOT.users[mention]["Hide"]
            if getObj(option,ctx,2)==None:
                if option in ("Messages","Mots","Voice"):
                    curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'compareUser','{2}','periods','None','None','{3}',1,1,'countDesc',False)".format(ctx.message.id,ctx.author.id,option,mention))
                elif len(ctx.args)==2 or ctx.args[2].lower() not in ("mois","annee"):
                    try:
                        mois,annee=tableauMois[getMois(ctx.args[2].lower())],getAnnee(ctx.args[3].lower())
                    except:
                        try:
                            mois,annee="TO",getAnnee(ctx.args[2].lower())
                        except:
                            mois,annee="TO","GL"
                elif ctx.args[2].lower()=="mois":
                    mois,annee=strftime("%m").lower(),strftime("%y")
                elif ctx.args[2].lower()=="annee":
                    mois,annee="TO",strftime("%y")
                curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'compareUser','{2}','perso','{3}','{4}','{5}',1,1,'countDesc',False)".format(ctx.message.id,ctx.author.id,option,mois,annee,mention))
            else:
                obj=getObj(option,ctx,2)
                curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'compareUser','{2}','obj','{3}','None','{4}',1,1,'countDesc',False)".format(ctx.message.id,ctx.author.id,option,mois,annee,mention))
            ligne=curseurCMD.execute("SELECT * FROM commandes WHERE MessageID={0}".format(ctx.message.id)).fetchone()
    
    if ligne["Args1"]=="periods":
        pass

async def comparePeriods(ctx,option,turn,react,ligne,guildOT,bot):
    if True:
        connexionCMD,curseurCMD=connectSQL("OT","Commandes")
        connexion,curseur=connectSQL(ctx.guild.id,option) 
        if not react:
            liste=[]
            args=ctx.args[2:len(ctx.args)]
            while len(args)!=0 and len(liste)<2:
                detectPeriod(args,liste,curseur)
            assert len(liste)==2
            obj=getObj(option,ctx,len(args)+2)
            curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'comparePeriods','{2}','{3}','{4}','{5}','None',1,1,'countDesc',False)".format(ctx.message.id,ctx.author.id,option,liste[0],liste[1],obj))

            ligne=curseurCMD.execute("SELECT * FROM commandes WHERE MessageID={0}".format(ctx.message.id)).fetchone()


def detectPeriod(args,liste,curseur):
    if args[0].lower()=="mois":
        liste.append("{0}{1}".format(tableauMois[strftime("%m")].lower(),strftime("%y"))) 
    elif args[0].lower()=="annee":
        liste.append("to{0}".format(strftime("%y"))) 
    elif args[0].lower()=="global":
        liste.append("glob") 
    else:
        try:
            curseur.execute("SELECT * FROM to{0}".format(getAnnee(args[0])))
        except:
            try:
                curseur.execute("SELECT * FROM {0}{1}".format(getMois(args[0].lower()),getAnnee(args[1])))
                del args[1]
            except:
                pass
    del args[0]


def embedCompare(nom,id1,id2,option,curseur,ligne,page,guildOT,bot):
    field1,field2,field3="","",""
    tri=ligne["Tri"]
    mobile=ligne["Mobile"]
    if option in ("periods","obj"):
        table=curseur.execute("SELECT * FROM {0}{1} ORDER BY {2} {3}".format(nom,id1,dictTriArg[tri],dictTriSens[tri])).fetchall()
        stop=15*page if 15*page<len(table) else len(table)
        for i in range(15*(page-1),stop):
            if table[i]["Annee"]=="GL":
                period="Général"
            else:
                period="{0} 20{1}".format(tableauMois[table[i]["Mois"]],table[i]["Annee"])
            cr1="{0}e - {1}".format(table[i]["Rank"],table[i]["Count"])
            table2=curseur.execute("SELECT * FROM {0}{1} WHERE Mois='{2}' AND Annee='{3}'".format(nom,id2,table[i]["Mois"],table[i]["Annee"])).fetchone()
            if table2==None:
                cr2="//"
            else:
                cr2="{0}e - {1}".format(table2["Rank"],table2["Count"])
            field1,field2,field3=addtoFields(field1,field2,field3,mobile,period,cr1,cr2)
    elif option=="perso":
        table=curseur.execute("SELECT * FROM perso{0}{1} ORDER BY {2} {3}".format(nom,id1,dictTriArg[tri],dictTriSens[tri])).fetchall()
        stop=15*page if 15*page<len(table) else len(table)
        for i in range(15*(page-1),stop):
            nom=nomsOptions(option,table[i]["ID"],guildOT,bot)
            cr1="{0}e - {1}".format(table[i]["Rank"],table[i]["Count"])
            table2=curseur.execute("SELECT * FROM persoM{0} WHERE Mois='{1}' AND Annee='{2}'".format(id2,table[i]["Mois"],table[i]["Annee"])).fetchone()
            if table2==None:
                cr2="//"
            else:
                cr2="{0}e - {1}".format(table2["Rank"],table2["Count"])
            field1,field2,field3=addtoFields(field1,field2,field3,mobile,period,cr1,cr2)