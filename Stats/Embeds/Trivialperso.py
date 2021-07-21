import discord
from Core.Fonctions.Embeds import addtoFields, createFields

def embedTrivialPerso(table:list,page:int,mobile:bool) -> discord.Embed:
    embed=discord.Embed()
    field1,field2,field3="","",""
    stop=15*page if 15*page<len(table) else len(table)
    for i in range(15*(page-1),stop):
        categ=table[i]["Categ"]
        niveau="Niveau {0}".format(table[i]["Niveau"])
        exp="{0}/{1}exp".format(round(table[i]["Exp"],2),table[i]["Next"])

        field1,field2,field3=addtoFields(field1,field2,field3,mobile,categ,niveau,exp)

    embed=createFields(mobile,embed,field1,field2,field3,"Catégorie","Niveau","Exp") 
    return embed