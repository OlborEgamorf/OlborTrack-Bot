import discord
from Core.Fonctions.Embeds import addtoFields, defEvol
from Core.Fonctions.DichoTri import dichotomieID, triID

def embedJeux(table,guild,page,mobile,id,evol,option):
    embed=discord.Embed()
    field1,field2,field3="","",""
    author=False
    stop=15*page if 15*page<len(table) else len(table)
    for i in range(15*(page-1),stop):
        rank="{0} {1}".format(table[i]["Rank"],defEvol(table[i],evol))
        count="{0} ({1}/{2})".format(table[i]["Count"],table[i]["W"],table[i]["L"])
        if type(guild.get_member(table[i]["ID"]))==discord.Member:
            nom="<@{0}>".format(table[i]["ID"])
        else:
            nom="*???*"
        
        if table[i]["ID"]==id:
            rank="**__{0}__**".format(rank)
            nom="**__{0}__**".format(nom)
            count="**__{0}__**".format(count)
            author=True

        field1,field2,field3=addtoFields(field1,field2,field3,mobile,rank,nom,count)
    
    if not author:
        table.sort(key=triID)
        etat=dichotomieID(table,id,"ID")
        if etat[0]:
            rank="\n**__{0}__**".format(table[etat[1]]["Rank"])
            if mobile:
                nom="**__<@{0}>__**".format(id)
                count="**__{0} ({1}/{2})__**".format(table[etat[1]]["Count"],table[etat[1]]["W"],table[etat[1]]["L"])
            else:
                nom="\n**__<@{0}>__**".format(id)
                count="\n**__{0} ({1}/{2})__**".format(table[etat[1]]["Count"],table[etat[1]]["W"],table[etat[1]]["L"])
            field1,field2,field3=addtoFields(field1,field2,field3,mobile,rank,nom,count)

    if mobile:
        embed.description=field1
    else:
        embed.add_field(name="Rang",value=field1,inline=True)
        embed.add_field(name="Membre",value=field2,inline=True)
        embed.add_field(name="Points (W/L)",value=field3,inline=True)
    return embed