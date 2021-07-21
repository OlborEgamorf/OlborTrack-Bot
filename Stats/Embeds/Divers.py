import discord
from Core.Fonctions.Embeds import addtoFields, createFields, defEvol
from Core.Fonctions.TempsVoice import tempsVoice

dictTrivia={3:"Images",2:"GIFs",1:"Fichiers",4:"Liens",5:"Réponse",6:"Réactions",7:"Edits",8:"Emotes",9:"Messages",10:"Mots",11:"Vocal","images":3,"gifs":2,"fichiers":1,"liens":4,"réponse":5,"réactions":6,"edits":7,"emotes":8,"messages":9,"mots":10,"vocal":11}

def embedDivers(table,page,mobile,evol):
    embed=discord.Embed()
    field1,field2,field3="","",""
    stop=15*page if 15*page<len(table) else len(table)
    for i in range(15*(page-1),stop):
        rank="{0} {1}".format(table[i]["Rank"],defEvol(table[i],evol))
        if table[i]["ID"]==11:
            count=tempsVoice(table[i]["Count"])
        else:
            count=table[i]["Count"]
        nom=dictTrivia[table[i]["ID"]]
        field1,field2,field3=addtoFields(field1,field2,field3,mobile,rank,nom,count)
        
    embed=createFields(mobile,embed,field1,field2,field3,"Rang","Objet","Nombre")
    return embed