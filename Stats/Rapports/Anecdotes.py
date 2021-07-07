from Stats.SQL.ConnectSQL import connectSQL
import discord
from random import choice
from Stats.Rapports.OlderEarlier import getOlderJour, hierMAG
from Stats.Rapports.CreateEmbed import embedRapport
from Stats.Rapports.Description import descipGlobal
from Core.Fonctions.GetNom import nomsOptions
from Core.Fonctions.TempsVoice import formatCount
dictSection={"Voice":"vocal","Reactions":"réactions","Emotes":"emotes","Salons":"salons","Freq":"heures","Messages":"salons","Voicechan":"vocal"}
dictTrivia={3:"Images",2:"GIFs",1:"Fichiers",4:"Liens",5:"Réponses",6:"Réactions",7:"Edits",8:"Emotes",9:"Messages",10:"Mots",11:"Vocal"}
tableauMois={"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre","TO":"TOTAL","1":"janvier","2":"février","3":"mars","4":"avril","5":"mai","6":"juin","7":"juillet","8":"aout","9":"septembre","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","to":"TO","glob":"GL"}

def anecdotesSpe(date,guildOT,bot,guild,option,page,pagemax,period):
    if period=="jour":
        connexion,curseur=connectSQL(guild.id,"Rapports","Stats","GL","")
    else:
        connexion,curseur=connectSQL(guild.id,option,"Stats",tableauMois[date[0]],date[1])
        conGL,curGL=connectSQL(guild.id,option,"Stats","GL","")
    embed=discord.Embed()

    if period=="jour":
        result=curseur.execute("SELECT * FROM ranks WHERE Jour='{0}' AND Mois='{1}' AND Annee='{2}' AND Type='{3}' ORDER BY Rank ASC".format(date[0],date[1],date[2],option)).fetchall()
        premiers=curseur.execute("SELECT * FROM ranks WHERE DateID={0} AND Type='{1}' AND Rank=1 ORDER BY Rank ASC".format(int(date[2]+date[1]+date[0]),option)).fetchall()
        alea=choice(premiers)
        first=curseur.execute("SELECT COUNT() AS Premier FROM ranks WHERE DateID<{0} AND Type='{1}' AND ID={2} AND Rank=1".format(int(date[2]+date[1]+date[0]),option,alea["ID"])).fetchone()
    elif period in ("mois","annee"):
        result=curseur.execute("SELECT * FROM {0}{1} ORDER BY Rank ASC".format(date[0],date[1])).fetchall()
        premiers=curseur.execute("SELECT * FROM {0}{1} WHERE Rank=1 ORDER BY Rank ASC".format(date[0],date[1])).fetchall()
        alea=choice(premiers)
        if period=="mois":
            first=curGL.execute("SELECT COUNT() AS Premier FROM firstM WHERE DateID<{0} AND ID={1}".format(date[1]+tableauMois[date[0]],alea["ID"])).fetchone()
        else:
            first=curGL.execute("SELECT COUNT() AS Premier FROM firstA WHERE DateID<{0} AND ID={1}".format(date[1],alea["ID"])).fetchone()
    elif period=="global":
        result=curseur.execute("SELECT * FROM glob ORDER BY Rank ASC").fetchall()
        premiers=curseur.execute("SELECT * FROM glob WHERE Rank=1 ORDER BY Rank ASC".format()).fetchall()
        alea=choice(premiers)
    nom=nomsOptions(option,alea["ID"],guildOT,bot)
    if period=="global":
        count=""
    elif first["Premier"]==0:
        count=", c'est la **première** fois !"
    else:
        count=" pour la **{0}e** fois.".format(first["Premier"]+1)
    if len(premiers)==1:
        ex=""
    else:
        ex="\nIl est accompagné par {0} autre(s)".format(len(premiers)-1)
    dictPremier={"Salons":"Le salon le plus actif est {0}{1}{2}","Freq":"L'heure la plus active est {0}{1}{2}","Emotes":"L'emote la plus utilisée est {0}{1}{2}","Reactions":"La réaction la plus utilisée est {0}{1}{2}","Messages":"Le membre le plus actif est {0}{1}{2}","Voice":"Le membre le plus actif est {0}{1}{2}","Voicechan":"Le salon le plus actif est {0}{1}{2}"}
    embed.add_field(name="Premier",value=dictPremier[option].format(nom,count,ex),inline=False)

    if period=="jour":
        hier=getOlderJour(date[0],date[1],date[2],curseur,"ranks",option)
    else:
        hier=hierMAG(date,period,guild,option)
    if period!="global":
        if hier!=None:
            if True:
                if period=="jour":
                    premierH=curseur.execute("SELECT Rank FROM ranks WHERE DateID={0} AND Type='{1}' AND ID={2}".format(hier[2]+hier[1]+hier[0],option,alea["ID"])).fetchone()
                    if premierH==None or premierH["Rank"]!=1:
                        serie=curseur.execute("SELECT ID FROM ranks WHERE DateID={0} AND Type='{1}' AND Rank=1".format(hier[2]+hier[1]+hier[0],option)).fetchone()
                        if serie!=None:
                            consec=curseur.execute("SELECT ID FROM ranks WHERE DateID<={0} AND Type='{1}' AND Rank=1 ORDER BY DateID DESC".format(hier[2]+hier[1]+hier[0],option)).fetchall()
                            try:
                                i=0
                                while consec[i]["ID"]==serie["ID"]:
                                    i+=1
                            except:
                                i=len(consec)
                            embed.add_field(name="Série première place",value="Il arrête la série de {0}, premier **{1} fois** d'affilée jusque là".format(nomsOptions(option,serie["ID"],guildOT,bot),i),inline=False)
                    else:
                        serie=curseur.execute("SELECT ID FROM ranks WHERE DateID<={0} AND Type='{1}' AND Rank=1 ORDER BY DateID DESC".format(hier[2]+hier[1]+hier[0],option)).fetchall()
                        try:
                            i=1
                            while serie[i]["ID"]==alea["ID"]:
                                i+=1
                            embed.add_field(name="Série première place",value="Il est sur une série de **{0}** premières places d'affilée.".format(i),inline=False)
                        except:
                            embed.add_field(name="Série première place",value="Il n'a **jamais arrêté** d'être premier.",inline=False)
                        
                elif period=="mois":
                    premierH=curGL.execute("SELECT ID FROM firstM WHERE Mois='{0}' AND Annee='{1}'".format(tableauMois[hier[0]],hier[1])).fetchone()["ID"]
                    if premierH!=alea["ID"]:
                        consec=curGL.execute("SELECT ID FROM firstM WHERE DateID<={0} ORDER BY DateID DESC".format(hier[1]+tableauMois[hier[0]])).fetchall()
                        try:
                            i=0
                            while consec[i]["ID"]==premierH:
                                i+=1
                        except:
                            i=len(consec)
                        embed.add_field(name="Série première place",value="Il arrête la série de {0}, premier **{1} fois** d'affilée jusque là".format(nomsOptions(option,premierH,guildOT,bot),i),inline=False)
                    else:
                        consec=curGL.execute("SELECT ID FROM firstM WHERE DateID<={0} ORDER BY DateID DESC".format(hier[1]+tableauMois[hier[0]])).fetchall()
                        try:
                            i=1
                            while consec[i]["ID"]==alea["ID"]:
                                i+=1
                            embed.add_field(name="Série première place",value="Il est sur une série de **{0}** premières places d'affilée.".format(i),inline=False)
                        except:
                            embed.add_field(name="Série première place",value="Il n'a **jamais arrêté** d'être premier.",inline=False)

                elif period=="annee":
                    premierH=curGL.execute("SELECT ID FROM firstA WHERE Annee='{0}'".format(hier[1])).fetchone()["ID"]
                    if premierH!=alea["ID"]:
                        consec=curGL.execute("SELECT ID FROM firstA WHERE DateID<={0} ORDER BY DateID DESC".format(hier[1])).fetchall()
                        try:
                            i=0
                            while consec[i]["ID"]==premierH:
                                i+=1
                        except:
                            i=len(consec)
                        embed.add_field(name="Série première place",value="Il arrête la série de {0}, premier **{1} fois** d'affilée jusque là".format(nomsOptions(option,premierH,guildOT,bot),i),inline=False)
                    else:
                        consec=curGL.execute("SELECT ID FROM firstA WHERE DateID<={0} ORDER BY DateID DESC".format(hier[1])).fetchall()
                        try:
                            i=1
                            while consec[i]["ID"]==alea["ID"]:
                                i+=1
                            embed.add_field(name="Série première place",value="Il est sur une série de **{0}** premières places d'affilée.".format(i),inline=False)
                        except:
                            embed.add_field(name="Série première place",value="Il n'a **jamais arrêté** d'être premier.",inline=False)
                

    if period!="jour":
        evol=curseur.execute("SELECT Count() AS Count FROM evol{0}{1}{2} WHERE Rank=1".format(date[0],date[1],alea["ID"])).fetchone()["Count"]
        count=curseur.execute("SELECT Count() AS Count FROM evol{0}{1}{2}".format(date[0],date[1],alea["ID"])).fetchone()["Count"]
        embed.add_field(name="Longévité",value="Sur la période, il a été premier **{0}** jours sur **{1}**".format(evol,count),inline=False)
    
    if period!="global":
        records=[]
        if period=="jour":
            for i in curseur.execute("SELECT * FROM ranks WHERE DateID={0} AND Type='{1}'".format(date[2]+date[1]+date[0],option)).fetchall():
                best=curseur.execute("SELECT MAX(Count),DateID,Count FROM ranks WHERE DateID<={0} AND Type='{1}' AND ID={2} ORDER BY DateID DESC".format(date[2]+date[1]+date[0],option,i["ID"])).fetchone()
                if best["DateID"]==int(date[2]+date[1]+date[0]):
                    records.append({"ID":i["ID"],"Count":formatCount(option,best["Count"])})
        elif period=="mois":
            for i in result:
                tablePerso=curGL.execute("SELECT Mois, Annee, Annee || '' || Mois AS DateID, Count FROM persoM{0} WHERE DateID<='{1}{2}' ORDER BY Count DESC".format(i["ID"],date[1],tableauMois[date[0]])).fetchone()
                if tablePerso["Mois"]==tableauMois[date[0]] and tablePerso["Annee"]==date[1]:
                    records.append({"ID":i["ID"],"Count":formatCount(option,tablePerso["Count"])})
        elif period=="annee":
            for i in result:
                tablePerso=curGL.execute("SELECT Mois, Annee, Count FROM persoA{0} WHERE Annee<='{1}' ORDER BY Count DESC".format(i["ID"],date[1])).fetchone()
                if tablePerso["Annee"]==date[1]:
                    records.append({"ID":i["ID"],"Count":formatCount(option,tablePerso["Count"])})
        if records==[]:
            embed.add_field(name="Records",value="Rien ou personne n'a battu son record d'activité à cette date.".format(i),inline=False)
        else:
            descip=""
            stop=4 if len(records)>4 else len(records)
            for i in range(stop):
                choix=choice(records)
                descip+=", {0} ({1})".format(nomsOptions(option,choix["ID"],guildOT,bot),choix["Count"])
                records.remove(choix)
            descip=descip[1:len(descip)]
            if len(records)==0:
                reste=""
            else:
                reste=", ainsi que {0} autre(s)".format(len(records))
            dictPremier={"Salons":"Des salons ont vu leur plus grande activité à cette date : {0}{1}","Freq":"Certaines heures ont vu leur pic d'activité à cette date : {0}{1}","Emotes":"Certaines emotes n'ont jamais été autant utilisées à cette date : {0}{1}","Reactions":"Certaines réactions n'ont jamais été autant utilisées à cette date : {0}{1}","Messages":"Certaines personnes n'ont jamais été autant actifs à cette date : {0}{1}","Voicechan":"Des salons ont vu leur plus grande activité à cette date : {0}{1}","Voice":"Certaines personnes n'ont jamais été autant actifs à cette date : {0}{1}"}
            embed.add_field(name="Records",value=dictPremier[option].format(descip,reste),inline=False)
        
    if option in ("Freq","Messages","Salons","Voice","Voicechan"):
        dictSilent={"Messages":"Sur les **{0}** humains de ce serveur, **{1}** ont été actifs à cette date, soit {2}%.","Salons":"Sur les **{0}** salons existants de ce serveur, **{1}** ont été actifs à cette date, soit {2}%.","Freq":"Sur les 24 heures qui composent une journée, **{1}** ont vu des messages, soit {2}%.","Voice":"Sur les **{0}** humains de ce serveur, **{1}** ont été actifs à cette date, soit {2}%.","Voicechan":"Sur les **{0}** salons vocaux existants de ce serveur, **{1}** ont été actifs à cette date, soit {2}%."}
        count=0
        if option in ("Messages","Voice"):
            for i in guild.members:
                if not i.bot:
                    count+=1
        elif option=="Salons":
            count=len(guild.text_channels)
        elif option=="Voicechan":
            count=len(guild.voice_channels)
        elif option=="Freq":
            count=24
        
        if period=="jour":
            countR=curseur.execute("SELECT COUNT() As Count FROM ranks WHERE DateID={0} AND Type='{1}'".format(date[2]+date[1]+date[0],option)).fetchone()["Count"]
        else:
            countR=curseur.execute("SELECT COUNT() As Count FROM {0}{1}".format(date[0],date[1])).fetchone()["Count"]
        embed.add_field(name="Proportions",value=dictSilent[option].format(count,countR,round(countR*100/count,2)),inline=False)
    
    if period=="jour":
        dictDivers={"Messages":9,"Salons":9,"Freq":9,"Emotes":8,"Reactions":6,"Voice":11,"Voicechan":11}
        somme=curseur.execute("SELECT Count FROM ranks WHERE DateID={0} AND Type='Divers' AND ID={1}".format(date[2]+date[1]+date[0],dictDivers[option])).fetchone()
        record=curseur.execute("SELECT Count,Jour,Mois,Annee FROM ranks WHERE Type='Divers' AND ID={0} ORDER BY Count DESC".format(dictDivers[option])).fetchone()
        if somme!=None and record!=None:
            if record["Count"]==somme["Count"]:
                dictRecord={"Messages":"Il n'y a jamais eu autant de messages envoyés qu'aujourd'hui, avec un total de **{0}**","Freq":"Il n'y a jamais eu autant de messages envoyés qu'aujourd'hui, avec un total de **{0}**","Salons":"Il n'y a jamais eu autant de messages envoyés qu'aujourd'hui, avec un total de **{0}**","Emotes":"Il n'y a jamais eu autant d'emotes utilisées qu'aujourd'hui, avec un total de **{0}**","Reactions":"Il n'y a jamais eu autant de réactions utilisées qu'aujourd'hui, avec un total de **{0}**","Voice":"Il n'y a jamais eu autant de temps passé en vocal cumulé qu'aujourd'hui, avec un total de **{0}**","Voicechan":"Il n'y a jamais eu autant de temps passé en vocal cumulé qu'aujourd'hui, avec un total de **{0}**"}
            else:
                dictRecord={"Messages":"Aujourd'hui **{0}** messages ont été envoyés. La date record est le **{1}/{2}/{3}** avec **{4}** messages.","Freq":"Aujourd'hui **{0}** messages ont été envoyés. La date record est le **{1}/{2}/{3}** avec **{4}** messages.","Salons":"Aujourd'hui **{0}** messages ont été envoyés. La date record est le **{1}/{2}/{3}** avec **{4}** messages.","Emotes":"Aujourd'hui **{0}** emotes ont été utilisées. La date record est le **{1}/{2}/{3}** avec **{4}** emotes.","Reactions":"Aujourd'hui **{0}** réactions ont été utilisées. La date record est le **{1}/{2}/{3}** avec **{4}** réactions.","Voice":"Aujourd'hui **{0}** ont été passées en vocal en cumulé. La date record est le **{1}/{2}/{3}** avec **{4}**.","Voicechan":"Aujourd'hui **{0}** ont été passées en vocal en cumulé. La date record est le **{1}/{2}/{3}** avec **{4}**."}
            embed.add_field(name="Total",value=dictRecord[option].format(formatCount(option,somme["Count"]),record["Jour"],record["Mois"],record["Annee"],formatCount(option,record["Count"])),inline=False)
    
    if hier!=None and period!="global":
        plus,moins,new=0,0,0
        if period in ("mois","annee"):
            connexion,curseur=connectSQL(guild.id,option,"Stats",tableauMois[hier[0]],hier[1])
            if period=="mois":
                title="Par rapport au {0}/{1}".format(tableauMois[hier[0]],hier[1])
            else:
                title="Par rapport au 20{0}".format(hier[1])
        else:
            title="Par rapport au {0}/{1}/{2}".format(hier[0],hier[1],hier[2])
        for i in result:
            if period=="jour":
                count=curseur.execute("SELECT Count FROM ranks WHERE Jour='{0}' AND Mois='{1}' AND Annee='{2}' AND Type='{3}' AND ID={4}".format(hier[0],hier[1],hier[2],option,i["ID"])).fetchone()
            else:
                count=curseur.execute("SELECT Count FROM {0}{1} WHERE ID={2}".format(hier[0],hier[1],i["ID"])).fetchone()
            if count==None:
                new+=1
            elif count["Count"]>i["Count"]:
                moins+=1
            elif count["Count"]<i["Count"]:
                plus+=1
        dictPlusMoins={"Messages":"Parmi les membres actifs à cette date, **{0}** l'ont été **moins** que la période précédente, **{1} plus** et **{2} ne l'avaient pas été**.","Salons":"Parmi les salons actifs à cette date, {0} l'ont été moins que la période précédente, {1} plus et {2} ne l'avaient pas été.","Freq":"Parmi les heures actives à cette date, {0} l'ont été moins que la période précédente, {1} plus et {2} ne l'avaient pas été.","Emotes":"Parmi les emotes utilisées à cette date, {0} l'ont été moins que la période précédente, {1} plus et {2} ne l'avaient pas été.","Reactions":"Parmi les réactions utilisées à cette date, {0} l'ont été moins que la période précédente, {1} plus et {2} ne l'avaient pas été.","Voice":"Parmi les membres actifs à cette date, **{0}** l'ont été **moins** que la période précédente, **{1} plus** et **{2} ne l'avaient pas été**.","Voicechan":"Parmi les salons actifs à cette date, {0} l'ont été moins que la période précédente, {1} plus et {2} ne l'avaient pas été."}
        embed.add_field(name=title,value=dictPlusMoins[option].format(moins,plus,new),inline=False)

    return embedRapport(guild,embed,date,"Section {0} : anecdotes".format(dictSection[option]),page,pagemax,period) 