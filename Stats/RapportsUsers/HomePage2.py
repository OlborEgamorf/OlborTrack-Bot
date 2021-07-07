import discord
from Stats.RapportsUsers.CreateEmbed import embedRapport
from Stats.RapportsUsers.Moyennes import descipMoyennes
from Stats.SQL.ConnectSQL import connectSQL

listeType=["Messages","Voice","Salons","Freq","Emotes","Reactions"]
dictFieldS={"Emotes":"Détails emotes","Salons":"Détails salons","Freq":"Détails heures","Reactions":"Détails réactions","Messages":"Détails messages","Voice":"Détails vocal"}
tableauMois={"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre","TO":"TOTAL","1":"janvier","2":"février","3":"mars","4":"avril","5":"mai","6":"juin","7":"juillet","8":"aout","9":"septembre","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","to":"TO","glob":"GL"}

def secondGlobal(date,guild,pagemax,period,user):
    """Deuxième page de la section principale, analyses grossières"""
    embed=discord.Embed()
    if period=="jour":
        connexion,curseur=connectSQL(guild.id,"Rapports","Stats","GL","")
        for j in listeType:
            result=curseur.execute("SELECT *,IDComp AS ID FROM objs WHERE Jour='{0}' AND Mois='{1}' AND Annee='{2}' AND Type='{3}' AND ID={4} ORDER BY Count DESC".format(date[0],date[1],date[2],j,user)).fetchall()
            if result!=[]:
                descip=descipMoyennes(j,result)
                embed.add_field(name=dictFieldS[j],value=descip,inline=True)
    elif period in ("mois","annee","global"):
        for j in listeType:
            try:
                connexion,curseur=connectSQL(guild.id,j,"Stats",tableauMois[date[0]],date[1])
                result=curseur.execute("SELECT * FROM perso{0}{1}{2} ORDER BY Rank ASC".format(tableauMois[date[0]].upper(),date[1].upper(),user)).fetchall()
                if result!=[]:
                    descip=descipMoyennes(j,result)
                    embed.add_field(name=dictFieldS[j],value=descip,inline=True)
            except:
                continue

    return embedRapport(guild,embed,date,"Section principale : moyennes",2,pagemax,period,user)