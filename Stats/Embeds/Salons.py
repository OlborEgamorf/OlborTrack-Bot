import discord
from Core.Fonctions.Embeds import addtoFields, createFields, defEvol
from Core.Fonctions.TempsVoice import formatCount


def embedSalon(table,guildOT,page,mobile,evol,option):
    embed=discord.Embed()
    field1,field2,field3="","",""
    stop=15*page if 15*page<len(table) else len(table)
    for i in range(15*(page-1),stop):
        rank="{0} {1}".format(table[i]["Rank"],defEvol(table[i],evol))
        count=formatCount(option,table[i]["Count"])
        try:
            if guildOT.chan[table[i]["ID"]]["Hide"]:
                nom="*Salon masqué*"
                count="*?*"
            else:
                nom="<#{0}>".format(table[i]["ID"])
        except:
            nom="??"
        field1,field2,field3=addtoFields(field1,field2,field3,mobile,rank,nom,count)
        
    embed=createFields(mobile,embed,field1,field2,field3,"Rang","Salon","Messages") 
    return embed