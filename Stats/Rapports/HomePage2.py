import discord
from Stats.SQL.ConnectSQL import connectSQL
from Stats.Rapports.Moyennes import descipMoyennes
from Stats.Rapports.CreateEmbed import embedRapport


listeType=["Messages","Voice","Salons","Freq","Emotes","Reactions"]
dictFieldS={"Emotes":"Détails emotes","Salons":"Détails salons","Freq":"Détails heures","Reactions":"Détails réactions","Messages":"Détails messages","Voice":"Détails vocal"}
tableauMois={"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre","TO":"TOTAL","1":"janvier","2":"février","3":"mars","4":"avril","5":"mai","6":"juin","7":"juillet","8":"aout","9":"septembre","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","to":"TO","glob":"GL"}

def secondGlobal(date,guild,pagemax,period):
    """Deuxième page de la section principale, analyses grossières"""
    embed=discord.Embed()
    connexion,curseur=connectSQL(guild.id)
    for j in listeType:
        try:
            result=curseur.execute("SELECT * FROM {0}{1} ORDER BY Rank ASC".format(date[0],date[1])).fetchall()
            if result!=[]:
                descip=descipMoyennes(j,result)
                embed.add_field(name=dictFieldS[j],value=descip,inline=True)
        except:
            continue

    return embedRapport(guild,embed,date,"Section principale : moyennes",2,pagemax,period)