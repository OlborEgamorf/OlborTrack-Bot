import discord
from Core.Fonctions.Embeds import addtoFields, createFields

def embedTrivialPerso(table:list,mobile:bool) -> discord.Embed:
    embed=discord.Embed()
    field1,field2,field3="","",""
    for ligne in table:
        categ=ligne["Categ"]
        niveau="Niveau {0}".format(ligne["Niveau"])
        exp="{0}/{1}exp".format(round(ligne["Exp"],2),ligne["Next"])

        field1,field2,field3=addtoFields(field1,field2,field3,mobile,categ,niveau,exp)

    embed=createFields(mobile,embed,field1,field2,field3,"Catégorie","Niveau","Exp") 
    return embed