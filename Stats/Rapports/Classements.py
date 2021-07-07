from Stats.SQL.ConnectSQL import connectSQL
import discord
from Stats.Rapports.OlderEarlier import getOlderJour, hierMAG
from Stats.Rapports.Description import descipGlobal
from Stats.Rapports.CreateEmbed import embedRapport

tableauMois={"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre","TO":"TOTAL","1":"janvier","2":"février","3":"mars","4":"avril","5":"mai","6":"juin","7":"juillet","8":"aout","9":"septembre","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","to":"TO","glob":"GL"}

def ranksGlobal(date,guildOT,bot,guild,option,page,pagemax,period,section):
    embed=discord.Embed()
    if period=="jour":
        connexion,curseur=connectSQL(guild.id,"Rapports","Stats","GL","")
        hier=getOlderJour(date[0],date[1],date[2],curseur,"ranks",option)
        result=curseur.execute("SELECT * FROM ranks WHERE Jour='{0}' AND Mois='{1}' AND Annee='{2}' AND Type='{3}' ORDER BY Rank ASC".format(date[0],date[1],date[2],option)).fetchall()
    elif period in ("mois","annee","global"):
        connexion,curseur=connectSQL(guild.id,option,"Stats",tableauMois[date[0]],date[1])
        hier=hierMAG(date,period,guild,option)
        result=curseur.execute("SELECT * FROM {0}{1} ORDER BY Rank ASC".format(date[0],date[1])).fetchall()
    if result==[]:
        return embed
    stop=20 if len(result)>20 else len(result)
    stop2=40 if len(result)>40 else len(result)
    embed.add_field(name="Top 1-{0}".format(stop),value=descipGlobal(option,result,0,stop,guildOT,bot,hier,period),inline=True)
    if stop2>20:
        embed.add_field(name="Top 20-{0}".format(stop2),value=descipGlobal(option,result,20,stop2,guildOT,bot,hier,period),inline=True)
    if hier!=None:
        if period=="jour":
            embed.description="*Comparaison avec le {0}/{1}/{2}*".format(hier[0],hier[1],hier[2])
        elif period=="mois":
            embed.description="*Comparaison avec le {0}/{1}*".format(tableauMois[hier[0]],hier[1])
    return embedRapport(guild,embed,date,"Section {0} : classement {1}".format(section.lower(),option.lower()),page,pagemax,period)