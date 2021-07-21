import discord
from Core.Fonctions.Embeds import addtoFields, createFields, defEvol

def embedFreq(table,page,mobile,evol):
    embed=discord.Embed()
    field1,field2,field3="","",""
    stop=15*page if 15*page<len(table) else len(table)
    for i in range(15*(page-1),stop):
        rank="{0} {1}".format(table[i]["Rank"],defEvol(table[i],evol))
        count=table[i]["Count"]
        nom="{0}h-{1}h".format(table[i]["ID"],table[i]["ID"]+1)
        field1,field2,field3=addtoFields(field1,field2,field3,mobile,rank,nom,count)
        
    embed=createFields(mobile,embed,field1,field2,field3,"Rang","Heure","Messages")
    return embed