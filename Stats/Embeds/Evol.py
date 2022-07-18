import discord
from Core.Fonctions.GetTable import collapseEvol
from Core.Fonctions.Embeds import addtoFields, createFields, defEvol
from Core.Fonctions.TempsVoice import formatCount

dictNameF3={"Messages":"Messages","Salons":"Messages","Freq":"Messages","Mots":"Mots","Emotes":"Utilisations","Reactions":"Utilisations","Voice":"Temps","Voicechan":"Temps"}

def embedEvol(table,mobile,collapse,evol,option):
    embed=discord.Embed()
    field1,field2,field3="","",""
    if collapse:
        table=collapseEvol(table)
    for ligne in table:
        rank="{0} {1}".format(ligne["Rank"],defEvol(ligne,evol))
        count=formatCount(option,ligne["Count"])
        nom="{0}/{1}/{2}".format(ligne["Jour"],ligne["Mois"],ligne["Annee"])
        field1,field2,field3=addtoFields(field1,field2,field3,mobile,rank,nom,count)
        
    embed=createFields(mobile,embed,field1,field2,field3,"Rang","Date",dictNameF3[option])
    return embed