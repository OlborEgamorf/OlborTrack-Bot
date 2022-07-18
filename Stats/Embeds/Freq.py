import discord
from Core.Fonctions.Embeds import addtoFields, createFields, defEvol

def embedFreq(table,mobile,evol):
    embed=discord.Embed()
    field1,field2,field3="","",""
    for ligne in table:
        rank="{0} {1}".format(ligne["Rank"],defEvol(ligne,evol))
        count=ligne["Count"]
        nom="{0}h-{1}h".format(ligne["ID"],ligne["ID"]+1)
        field1,field2,field3=addtoFields(field1,field2,field3,mobile,rank,nom,count)
        
    embed=createFields(mobile,embed,field1,field2,field3,"Rang","Heure","Messages")
    return embed