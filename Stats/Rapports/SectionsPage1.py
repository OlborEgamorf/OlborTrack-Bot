import discord
from Core.Fonctions.DichoTri import dichotomieID
from Core.Fonctions.RankingClassic import rankingClassic
from Stats.Rapports.CreateEmbed import embedRapport
from Stats.Rapports.Description import descipGlobal
from Stats.Rapports.Moyennes import descipMoyennes
from Stats.Rapports.Paliers import paliers
from Stats.SQL.ConnectSQL import connectSQL

dictSection={"Voice":"vocal","Reactions":"réactions","Emotes":"emotes","Salons":"salons","Freq":"heures","Messages":"salons","Voicechan":"vocal"}
tableauMois={"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre","TO":"TOTAL","1":"janvier","2":"février","3":"mars","4":"avril","5":"mai","6":"juin","7":"juillet","8":"aout","9":"septembre","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","to":"TO","glob":"GL"}

def homeSpe(date,guildOT,bot,guild,option,pagemax,period):
    embed=discord.Embed()
    connexion,curseur=connectSQL(guild.id,option,"Stats",tableauMois[date[0]],date[1])
    result=curseur.execute("SELECT * FROM {0}{1} ORDER BY Rank ASC".format(date[0],date[1])).fetchall()

    if result!=[]:
        stop=5 if len(result)>5 else len(result)
        embed.add_field(name="Top {0} {1}".format(stop,dictSection[option]),value=descipGlobal(option,result,0,stop,guildOT,bot,None,period),inline=True)

        classement=[]
        for i in result:
            try:
                for j in curseur.execute("SELECT * FROM {0}{1}{2} ORDER BY Rank ASC".format(date[0],date[1],i["ID"])).fetchall():
                    exe=dichotomieID(classement,j["ID"],"ID")
                    if exe[0]:
                        classement[exe[1]]["Count"]+=j["Count"]
                    else:
                        classement.append({"Rank":0,"ID":j["ID"],"Count":j["Count"]})
                        classement.sort(key=lambda x:x["ID"])
            except:
                pass
            
        if classement!=[]:
            rankingClassic(classement)
            stop=5 if len(classement)>5 else len(classement)
            embed.add_field(name="Top {0} membres".format(stop),value=descipGlobal("Messages",classement,0,stop,guildOT,bot,None,period),inline=True)
        
        embed.add_field(name="Détails",value=descipMoyennes(option,result),inline=True)
        embed.add_field(name="Paliers",value=paliers(curseur,period,date,option),inline=True)

        descip=""
        if period in ("mois","annee"):
            connexion,curseur=connectSQL(guild.id,option,"Stats","GL","")
            if period=="mois":
                table=curseur.execute("SELECT DISTINCT * FROM firstM WHERE Mois='{0}' ORDER BY Annee ASC".format(tableauMois[date[0]])).fetchall()
            elif period=="annee":
                table=curseur.execute("SELECT DISTINCT * FROM firstA WHERE Annee<>'{0}' ORDER BY Annee ASC".format(date[1])).fetchall()
            for i in table:
                i["Rank"]=1
                descip+="20{0} - {1}".format(i["Annee"],descipGlobal(option,[i],0,1,guildOT,bot,None,period))
        if descip!="":
            embed.add_field(name="Différentes années",value=descip,inline=True)
    return embedRapport(guild,embed,date,"Section {0} : résumé".format(dictSection[option]),1,pagemax,period) 
