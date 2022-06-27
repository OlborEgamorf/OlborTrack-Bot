from Stats.SQL.ConnectSQL import connectSQL
import discord
from Stats.Rapports.OlderEarlier import getEarlierAnnee, getEarlierMois, getOlderMois
from Stats.Rapports.Description import descipGlobal
from Stats.Rapports.CreateEmbed import embedRapport
tableauMois={"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre","TO":"TOTAL","1":"janvier","2":"février","3":"mars","4":"avril","5":"mai","6":"juin","7":"juillet","8":"aout","9":"septembre","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12"}

def archiveRapport(date,guildOT,bot,guild,option,period,page,pagemax):
    
    embed=discord.Embed()
    if period=="mois":
        connexion,curseur=connectSQL(guild.id,"Rapports","Stats","GL","GL")
        demain=getEarlierMois(tableauMois[date[0]],date[1],guild,option)
        if demain==None:
            dateArch=curseur.execute("SELECT Jour,Mois,Annee FROM archives WHERE Type='{0}' AND Periode='Annee' ORDER BY DateID DESC".format(option)).fetchone()
        else:
            dateArch=curseur.execute("SELECT Jour,Mois,Annee FROM archives WHERE DateID<{0}{1}00 AND Type='{2}' AND Periode='Annee' ORDER BY DateID DESC".format(demain[1],tableauMois[demain[0]],option)).fetchone()
        if dateArch!=None:
            annee=curseur.execute("SELECT * FROM archives WHERE DateID={0}{1}{2} AND Type='{3}' AND Periode='Annee'".format(dateArch["Annee"],dateArch["Mois"],dateArch["Jour"],option)).fetchall()
            if annee!=[]:
                embed.add_field(name="Classement année 20{0}".format(date[1]),value=descipGlobal(option,annee,0,len(annee),guildOT,bot,None,period),inline=True)

            glob=curseur.execute("SELECT * FROM archives WHERE DateID={0}{1}{2} AND Type='{3}' AND Periode='Global'".format(dateArch["Annee"],dateArch["Mois"],dateArch["Jour"],option)).fetchall()
            if glob!=[]:
                embed.add_field(name="Classement global",value=descipGlobal(option,glob,0,len(glob),guildOT,bot,None,period),inline=True)
    elif period=="annee":
        connexion,curseur=connectSQL(guild.id,"Rapports","Stats","GL","")
        demain=getEarlierAnnee(date[1],guild,option)
        
        if demain==None:
            dateArch=curseur.execute("SELECT Jour,Mois,Annee FROM archives WHERE Type='{0}' AND Periode='Global' ORDER BY DateID DESC".format(option)).fetchone()
        else:
            dateArch=curseur.execute("SELECT Jour,Mois,Annee FROM archives WHERE DateID<{0}0000 AND Type='{1}' AND Periode='Annee' ORDER BY DateID DESC".format(demain[1],option)).fetchone()
        if dateArch!=None:
            glob=curseur.execute("SELECT * FROM archives WHERE DateID={0}{1}{2} AND Type='{3}' AND Periode='Global'".format(dateArch["Annee"],dateArch["Mois"],dateArch["Jour"],option)).fetchall()
            if glob!=[]:
                embed.add_field(name="Classement global",value=descipGlobal(option,glob,0,len(glob),guildOT,bot,None,period),inline=True)
    return embedRapport(guild,embed,date,"Archives à cette date : classements {0}".format(option.lower()),page,pagemax,period)