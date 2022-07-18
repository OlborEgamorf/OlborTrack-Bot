import discord
from Core.Fonctions.Embeds import addtoFields, createFields, defEvol
from Core.Fonctions.TempsVoice import formatCount


def embedSalon(table,guildOT,page,mobile,evol,option):
    embed=discord.Embed()
    field1,field2,field3="","",""
    for ligne in table:
        rank="{0} {1}".format(ligne["Rank"],defEvol(ligne,evol))
        count=formatCount(option,ligne["Count"])
        try:
            if ligne["ID"]==0:
                nom="Salons éphémères"
            elif guildOT.chan[ligne["ID"]]["Hide"]:
                nom="*Salon masqué*"
                count="*?*"
            else:
                nom="<#{0}>".format(ligne["ID"])
        except:
            nom="??"
        field1,field2,field3=addtoFields(field1,field2,field3,mobile,rank,nom,count)
        
    embed=createFields(mobile,embed,field1,field2,field3,"Rang","Salon","Messages") 
    return embed