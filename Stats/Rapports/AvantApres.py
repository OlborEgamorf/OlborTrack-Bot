import discord
from Stats.SQL.ConnectSQL import connectSQL
from Stats.Rapports.OlderEarlier import getEarlierAnnee, getEarlierJour, getEarlierMois, getOlderJour, hierMAG
from Stats.Rapports.Description import descipGlobal
from Stats.Rapports.CreateEmbed import embedRapport

tableauMois={"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre","TO":"TOTAL","1":"janvier","2":"février","3":"mars","4":"avril","5":"mai","6":"juin","7":"juillet","8":"aout","9":"septembre","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","to":"TO","glob":"GL"}
dictSection={"Voice":"vocal","Reactions":"réactions","Emotes":"emotes","Salons":"salons","Freq":"heures","Messages":"salons","Voicechan":"vocal"}

def avantapresSpe(date,guildOT,bot,guild,option,page,pagemax,period):
    embed=discord.Embed()
    if period=="jour":
        connexion,curseur=connectSQL(guild.id,"Rapports","Stats","GL","")
        result=curseur.execute("SELECT * FROM ranks WHERE Jour='{0}' AND Mois='{1}' AND Annee='{2}' AND Type='{3}' ORDER BY Rank ASC".format(date[0],date[1],date[2],option)).fetchall()
        hier=getOlderJour(date[0],date[1],date[2],curseur,"ranks",option)
        demain=getEarlierJour(date[0],date[1],date[2],curseur,"ranks",option)
    elif period in ("mois","annee","global"):
        connexion,curseur=connectSQL(guild.id,option,"Stats",tableauMois[date[0]],date[1])
        result=curseur.execute("SELECT * FROM {0}{1} ORDER BY Rank ASC".format(date[0],date[1])).fetchall()
        hier=hierMAG(date,period,guild,option)
        if period=="mois":
            demain=getEarlierMois(tableauMois[date[0]],date[1],guild,option)
        elif period=="annee":
            demain=getEarlierAnnee(date[1],guild,option)
        elif period=="global":
            demain=None

    if hier!=None:
        if period=="jour":
            resultH=curseur.execute("SELECT * FROM ranks WHERE Jour='{0}' AND Mois='{1}' AND Annee='{2}' AND Type='{3}' ORDER BY Rank ASC".format(hier[0],hier[1],hier[2],option)).fetchall()
            title="{0}/{1}/{2}".format(hier[0],hier[1],hier[2])
        elif period in ("mois","annee"):
            connexion,curseur=connectSQL(guild.id,option,"Stats",tableauMois[hier[0]],hier[1])
            resultH=curseur.execute("SELECT * FROM {0}{1} ORDER BY Rank ASC".format(hier[0],hier[1])).fetchall()
            if period=="mois":
                title="{0}/{1}".format(tableauMois[hier[0]],hier[1])
            else:
                title="20{0}".format(hier[1])

        stop=15 if len(resultH)>15 else len(resultH)
        embed.add_field(name=title,value=descipGlobal(option,resultH,0,stop,guildOT,bot,None,period),inline=True)

    stop=15 if len(result)>15 else len(result)
    if period=="jour":
        embed.add_field(name="{0}/{1}/{2}".format(date[0],date[1],date[2]),value=descipGlobal(option,result,0,stop,guildOT,bot,hier,period),inline=True)
    elif period=="mois":
        embed.add_field(name="{0}/{1}".format(tableauMois[date[0]],date[1]),value=descipGlobal(option,result,0,stop,guildOT,bot,hier,period),inline=True)
    elif period=="annee":
        embed.add_field(name="20{0}".format(date[1]),value=descipGlobal(option,result,0,stop,guildOT,bot,hier,period),inline=True)
    elif period=="global":
        embed.add_field(name="Global",value=descipGlobal(option,result,0,stop,guildOT,bot,hier,period),inline=True)

    if demain!=None:
        if period=="jour":
            resultD=curseur.execute("SELECT * FROM ranks WHERE Jour='{0}' AND Mois='{1}' AND Annee='{2}' AND Type='{3}' ORDER BY Rank ASC".format(demain[0],demain[1],demain[2],option)).fetchall()
            title="{0}/{1}/{2}".format(demain[0],demain[1],demain[2])
        elif period in ("mois","annee"):
            connexion,curseur=connectSQL(guild.id,option,"Stats",tableauMois[demain[0]],demain[1])
            resultD=curseur.execute("SELECT * FROM {0}{1} ORDER BY Rank ASC".format(demain[0],demain[1])).fetchall()
            if period=="mois":
                title="{0}/{1}".format(tableauMois[demain[0]],demain[1])
            else:
                title="20{0}".format(demain[1])
        stop=15 if len(resultD)>15 else len(resultD)
        embed.add_field(name=title,value=descipGlobal(option,resultD,0,stop,guildOT,bot,date,period),inline=True)
    return embedRapport(guild,embed,date,"Section {0} : évolution".format(dictSection[option]),page,pagemax,period) 