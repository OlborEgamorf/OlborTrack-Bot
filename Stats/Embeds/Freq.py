import discord
from Core.Fonctions.Embeds import addtoFields, defEvol

def embedFreq(table,page,mobile,evol):
    embed=discord.Embed()
    field1,field2,field3="","",""
    stop=15*page if 15*page<len(table) else len(table)
    for i in range(15*(page-1),stop):
        rank="{0} {1}".format(table[i]["Rank"],defEvol(table[i],evol))
        count=table[i]["Count"]
        nom="{0}h-{1}h".format(table[i]["ID"],table[i]["ID"]+1)
        field1,field2,field3=addtoFields(field1,field2,field3,mobile,rank,nom,count)
        
    if mobile:
        embed.description=field1
    else:
        embed.add_field(name="Rang",value=field1,inline=True)
        embed.add_field(name="Heure",value=field2,inline=True)
        embed.add_field(name="Count",value=field3,inline=True)
    return embed