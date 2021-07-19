import discord
from Core.Fonctions.Embeds import addtoFields, defEvol
from Core.Fonctions.TempsVoice import formatCount


def embedSalon(table,guildOT,page,mobile,evol,option):
    embed=discord.Embed()
    field1,field2,field3="","",""
    stop=15*page if 15*page<len(table) else len(table)
    for i in range(15*(page-1),stop):
        rank="{0} {1}".format(table[i]["Rank"],defEvol(table[i],evol))
        count=formatCount(option,table[i]["Count"])
        if guildOT.chan[table[i]["ID"]]["Hide"]:
            nom="*Salon masqué*"
            count="*?*"
        else:
            nom="<#{0}>".format(table[i]["ID"])
        field1,field2,field3=addtoFields(field1,field2,field3,mobile,rank,nom,count)
        
    if mobile:
        embed.description=field1
    else:
        embed.add_field(name="Rang",value=field1,inline=True)
        embed.add_field(name="Salon",value=field2,inline=True)
        embed.add_field(name="Messages",value=field3,inline=True)
    return embed