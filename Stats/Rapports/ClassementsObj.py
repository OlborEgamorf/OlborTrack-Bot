from Stats.SQL.ConnectSQL import connectSQL
import discord
from Stats.Rapports.Description import descipGlobal
from Stats.Rapports.CreateEmbed import embedRapport
from Core.Fonctions.GetNom import nomsOptions

dictSection={"Voice":"vocal","Reactions":"réactions","Emotes":"emotes","Salons":"salons","Freq":"heures","Messages":"salons","Voicechan":"vocal"}
tableauMois={"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre","TO":"TOTAL","1":"janvier","2":"février","3":"mars","4":"avril","5":"mai","6":"juin","7":"juillet","8":"aout","9":"septembre","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","to":"TO","glob":"GL"}

def ranksIntoSpes(date,guildOT,bot,guild,option,page,pagenorm,pagemax,period):
    embed=discord.Embed()

    connexion,curseur=connectSQL(guild.id,option,"Stats",tableauMois[date[0]],date[1])
    result=curseur.execute("SELECT * FROM {0}{1} ORDER BY Rank ASC".format(date[0],date[1])).fetchall()

    if result!=[]:
        start=5*(page-1)
        stop=5*page if len(result)>5*page else len(result)
        for i in range(start,stop):
            try:
                obj=curseur.execute("SELECT * FROM {0}{1}{2} ORDER BY Rank ASC".format(date[0],date[1],result[i]["ID"])).fetchall()
            except:
                embed.add_field(name="Introuvable",value="Le classement de cet objet est introuvable.",inline=True)
                continue
            stop2=6 if len(obj)>6 else len(obj)
            if option in ("Salons","Voicechan"):
                nom=guild.get_channel(result[i]["ID"]).name
            else:
                nom=nomsOptions(option,result[i]["ID"],guildOT,bot)
            embed.add_field(name=nom,value=descipGlobal("Messages",obj,0,stop2,guildOT,bot,None,period),inline=True)
    return embedRapport(guild,embed,date,"Section {0} : classements internes".format(dictSection[option]),pagenorm,pagemax,period)