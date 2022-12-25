import discord
from Core.Fonctions.GetTable import getTablePerso
from Stats.RapportsUsers.CreateEmbed import embedRapport
from Stats.RapportsUsers.Description import descipGlobal
from Stats.RapportsUsers.Moyennes import descipMoyennes
from Stats.RapportsUsers.Paliers import paliers
from Stats.SQL.ConnectSQL import connectSQL

dictSection={"Voicechan":"vocal","Reactions":"réactions","Emotes":"emotes","Salons":"salons","Freq":"heures","Messages":"salons"}
tableauMois={"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre","TO":"TOTAL","1":"janvier","2":"février","3":"mars","4":"avril","5":"mai","6":"juin","7":"juillet","8":"aout","9":"septembre","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","to":"TO","glob":"GL"}

def homeSpe(date,guildOT,bot,guild,option,pagemax,period,user):
    embed=discord.Embed()
    connexion,curseur=connectSQL(guild.id)
    result=curseur.execute("SELECT * FROM perso{0}{1}{2} ORDER BY Count DESC".format(tableauMois[date[0]],date[1],user)).fetchall()

    if result!=[]:
        stop=5 if len(result)>5 else len(result)
        embed.add_field(name="Top {0} {1}".format(stop,dictSection[option]),value=descipGlobal(option,result,0,stop,guildOT,bot,None,period,user),inline=True)
        
        embed.add_field(name="Détails",value=descipMoyennes(option,result),inline=True)
        embed.add_field(name="Paliers",value=paliers(curseur,period,date,option,user),inline=True)

        descip=""
        if period in ("mois","annee"):
            if period=="mois":
                table=getTablePerso(guild.id,option,user,False,"M","periodAsc")
                table=list(filter(lambda x:x["Mois"]==tableauMois[date[0]], table))
            elif period=="annee":
                table=getTablePerso(guild.id,option,user,False,"A","periodAsc")
                table=list(filter(lambda x:x["Annee"]!="GL", table))
            for j in table:
                try:
                    i=curseur.execute("SELECT * FROM perso{0}{1}{2} ORDER BY Count DESC".format(j["Mois"],j["Annee"],user)).fetchone()
                    i["Rank"]=1
                    descip+="20{0} - {1}".format(i["Annee"],descipGlobal(option,[i],0,1,guildOT,bot,None,period,user))
                except:
                    pass
        if descip!="":
            embed.add_field(name="Différentes années",value=descip,inline=True)
    return embedRapport(guild,embed,date,"Section {0} : résumé".format(dictSection[option]),1,pagemax,period,user) 
