import discord
from Core.Fonctions.Embeds import addtoFields, createFields, defEvol

def embedEmote(table,bot,page,mobile,evol):
    embed=discord.Embed()
    field1,field2,field3="","",""
    stop=15*page if 15*page<len(table) else len(table)
    for i in range(15*(page-1),stop):
        rank="{0} {1}".format(table[i]["Rank"],defEvol(table[i],evol))
        count=table[i]["Count"]
        try:
            nom=chr(table[i]["ID"])
        except:
            emote=bot.get_emoji(table[i]["ID"])
            if type(emote)!=discord.emoji.Emoji:
                nom="*Emote inconnue*"
            else:
                nom=str(emote)
        field1,field2,field3=addtoFields(field1,field2,field3,mobile,rank,nom,count)
        
    embed=createFields(mobile,embed,field1,field2,field3,"Rang","Emote","Utilisations")
    return embed