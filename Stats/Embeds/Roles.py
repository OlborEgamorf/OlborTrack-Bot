import discord
from Core.Fonctions.TempsVoice import formatCount
from Core.Fonctions.Embeds import addtoFields


def embedRole(table,page,mobile,option):
    embed=discord.Embed()
    field1,field2,field3="","",""
    stop=15*page if 15*page<len(table) else len(table)
    for i in range(15*(page-1),stop):
        rank=table[i]["Rank"]
        count=formatCount(option,table[i]["Count"])
        nom="<@&{0}>".format(table[i]["ID"])
        field1,field2,field3=addtoFields(field1,field2,field3,mobile,rank,nom,count)
        
    if mobile:
        embed.description=field1
    else:
        embed.add_field(name="Rang",value=field1,inline=True)
        embed.add_field(name="Rôle",value=field2,inline=True)
        embed.add_field(name="Count",value=field3,inline=True)
    return embed