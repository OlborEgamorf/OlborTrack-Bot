import discord
from Stats.RapportsUsers.OlderEarlier import getEarlierAnnee, getEarlierMois, hierMAG
from Stats.RapportsUsers.Description import descipGlobal
from Stats.RapportsUsers.CreateEmbed import embedRapport
from Stats.SQL.ConnectSQL import connectSQL

tableauMois={"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre","TO":"TOTAL","1":"janvier","2":"février","3":"mars","4":"avril","5":"mai","6":"juin","7":"juillet","8":"aout","9":"septembre","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","to":"TO","glob":"GL"}
dictSection={"Voice":"vocal","Reactions":"réactions","Emotes":"emotes","Salons":"salons","Freq":"heures","Messages":"salons","Voicechan":"vocal"}

def avantapresSpe(date,guildOT,bot,guild,option,page,pagemax,period,user):
    embed=discord.Embed()
    connexion,curseur=connectSQL(guild.id)
    result=curseur.execute("SELECT * FROM perso{0}{1}{2} ORDER BY Count DESC".format(tableauMois[date[0]],date[1],user)).fetchall()
    hier=hierMAG(date,period,guild,option,user)
    if period=="mois":
        demain=getEarlierMois(tableauMois[date[0]],date[1],curseur,user)
    elif period=="annee":
        demain=getEarlierAnnee(date[1],guild,user)
    elif period=="global":
        demain=None

    if hier!=None:
        resultH=curseur.execute("SELECT * FROM perso{0}{1}{2} ORDER BY Count DESC".format(tableauMois[hier[0]],hier[1],user)).fetchall()
        if period=="mois":
            title="{0}/{1}".format(tableauMois[hier[0]],hier[1])
        else:
            title="20{0}".format(hier[1])
        stop=15 if len(resultH)>15 else len(resultH)
        embed.add_field(name=title,value=descipGlobal(option,resultH,0,stop,guildOT,bot,None,period,user),inline=True)

    stop=15 if len(result)>15 else len(result)
    if period=="mois":
        embed.add_field(name="{0}/{1}".format(tableauMois[date[0]],date[1]),value=descipGlobal(option,result,0,stop,guildOT,bot,hier,period,user),inline=True)
    elif period=="annee":
        embed.add_field(name="20{0}".format(date[1]),value=descipGlobal(option,result,0,stop,guildOT,bot,hier,period,user),inline=True)
    elif period=="global":
        embed.add_field(name="Global",value=descipGlobal(option,result,0,stop,guildOT,bot,hier,period,user),inline=True)

    if demain!=None:
        resultD=curseur.execute("SELECT * FROM perso{0}{1}{2} ORDER BY Count DESC".format(tableauMois[demain[0]],demain[1],user)).fetchall()
        if period=="mois":
            title="{0}/{1}".format(tableauMois[demain[0]],demain[1])
        else:
            title="20{0}".format(demain[1])
        stop=15 if len(resultD)>15 else len(resultD)
        embed.add_field(name=title,value=descipGlobal(option,resultD,0,stop,guildOT,bot,date,period,user),inline=True)
    return embedRapport(guild,embed,date,"Section {0} : évolution".format(dictSection[option]),page,pagemax,period,user) 