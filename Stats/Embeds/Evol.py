import discord
from Core.Fonctions.GetTable import collapseEvol
from Core.Fonctions.Embeds import addtoFields, defEvol
from Core.Fonctions.TempsVoice import formatCount

dictNameF3={"Messages":"Messages","Salons":"Messages","Freq":"Messages","Mots":"Mots","Emotes":"Utilisations","Reactions":"Utilisations","Voice":"Temps","Voicechan":"Temps"}

def embedEvol(table,page,mobile,collapse,evol,option):
    embed=discord.Embed()
    field1,field2,field3="","",""
    if collapse:
        table=collapseEvol(table)
    stop=15*page if 15*page<len(table) else len(table)
    for i in range(15*(page-1),stop):
        rank="{0} {1}".format(table[i]["Rank"],defEvol(table[i],evol))
        count=formatCount(option,table[i]["Count"])
        nom="{0}/{1}/{2}".format(table[i]["Jour"],table[i]["Mois"],table[i]["Annee"])
        field1,field2,field3=addtoFields(field1,field2,field3,mobile,rank,nom,count)
        
    if mobile:
        embed.description=field1
    else:
        embed.add_field(name="Rang",value=field1,inline=True)
        embed.add_field(name="Date",value=field2,inline=True)
        embed.add_field(name=dictNameF3[option],value=field3,inline=True)
    return embed