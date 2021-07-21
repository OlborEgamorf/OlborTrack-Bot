import discord
from Core.Fonctions.TempsVoice import formatCount
from Core.Fonctions.Embeds import addtoFields, createFields

dictNameF3={"Messages":"Messages","Salons":"Messages","Freq":"Messages","Mots":"Mots","Emotes":"Utilisations","Reactions":"Utilisations","Voice":"Temps","Voicechan":"Temps","Mentions":"Mentions","Mentionne":"Mentions","Divers":"Nombre"}

def embedRole(table,page,mobile,option):
    embed=discord.Embed()
    field1,field2,field3="","",""
    stop=15*page if 15*page<len(table) else len(table)
    for i in range(15*(page-1),stop):
        rank=table[i]["Rank"]
        count=formatCount(option,table[i]["Count"])
        nom="<@&{0}>".format(table[i]["ID"])
        field1,field2,field3=addtoFields(field1,field2,field3,mobile,rank,nom,count)
        
    embed=createFields(mobile,embed,field1,field2,field3,"Rang","Rôle",dictNameF3[option]) 
    return embed