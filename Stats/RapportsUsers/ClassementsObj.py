import discord
from Stats.RapportsUsers.Description import descipGlobal
from Stats.RapportsUsers.CreateEmbed import embedRapport
from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.GetNom import nomsOptions
from Core.Fonctions.TempsVoice import formatCount

dictSection={"Voice":"vocal","Reactions":"réactions","Emotes":"emotes","Salons":"salons","Freq":"heures","Messages":"salons","Voicechan":"vocal"}
tableauMois={"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre","TO":"TOTAL","1":"janvier","2":"février","3":"mars","4":"avril","5":"mai","6":"juin","7":"juillet","8":"aout","9":"septembre","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","to":"TO","glob":"GL","TO":""}

def ranksIntoSpes(date,guildOT,bot,guild,option,page,pagenorm,pagemax,period,user):
    embed=discord.Embed()

    if period=="jour":
        connexion,curseur=connectSQL(guild.id,"Rapports","Stats","GL","")
        result=curseur.execute("SELECT *,IDComp AS ID FROM objs WHERE Jour='{0}' AND Mois='{1}' AND Annee='{2}' AND Type='{3}' AND ID={4} ORDER BY Rank ASC".format(date[0],date[1],date[2],option,user)).fetchall()
    elif period in ("mois","annee","global"):
        connexion,curseur=connectSQL(guild.id,option,"Stats",tableauMois[date[0]],date[1])
        result=curseur.execute("SELECT * FROM perso{0}{1}{2} ORDER BY Count DESC".format(tableauMois[date[0]],date[1],user)).fetchall()
        connexion,curseur=connectSQL(guild.id,option,"Stats","GL","")
    if result!=[]:
        start=5*(page-1)
        stop=5*page if len(result)>5*page else len(result)
        for i in range(start,stop):
            try:
                if period=="jour":
                    obj=curseur.execute("SELECT *,IDComp AS ID FROM objs WHERE Type='{0}' AND IDComp={1} AND ID={2} AND DateID<={3} ORDER BY DateID DESC".format(option,result[i]["ID"],user,date[2]+date[1]+date[0])).fetchall()
                elif period=="mois":
                    obj=curseur.execute("SELECT Count,Rank,ID,Mois,Annee, Annee || '' || Mois AS DateID FROM persoM{0}{1} WHERE DateID<='{2}' ORDER BY DateID DESC".format(user,result[i]["ID"],date[1]+tableauMois[date[0]])).fetchall()
                else:
                    obj=curseur.execute("SELECT * FROM persoA{0}{1} ORDER BY Count DESC".format(user,result[i]["ID"])).fetchall()
            except:
                embed.add_field(name="Introuvable",value="La table de cet objet est introuvable.",inline=True)
                continue
            if option in ("Salons","Voicechan"):
                nom=guild.get_channel(result[i]["ID"]).name
            else:
                nom=nomsOptions(option,result[i]["ID"],guildOT,bot)
            descip=""
            for j in range(6 if len(obj)>6 else len(obj)):
                if period=="jour":
                    descip+="**{0} {1} 20{2}** : {3} - {4}e\n".format(obj[j]["Jour"],tableauMois[obj[j]["Mois"]],obj[j]["Annee"],formatCount(option,obj[j]["Count"]),obj[j]["Rank"])
                elif obj[j]["Annee"]=="GL":
                    descip+="**Global** : {0} - {1}e\n".format(formatCount(option,obj[j]["Count"]),obj[j]["Rank"])
                else:
                    descip+="**{0} 20{1}** : {2} - {3}e\n".format(tableauMois[obj[j]["Mois"]],obj[j]["Annee"],formatCount(option,obj[j]["Count"]),obj[j]["Rank"])
            embed.add_field(name=nom,value=descip,inline=True)
    return embedRapport(guild,embed,date,"Section {0} : classements internes".format(dictSection[option]),pagenorm,pagemax,period,user)