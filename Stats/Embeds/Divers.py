import discord
from Core.Fonctions.Embeds import addtoFields, createFields, defEvol
from Core.Fonctions.TempsVoice import tempsVoice

dictTrivia={3:"Images",2:"GIFs",1:"Fichiers",4:"Liens",5:"Réponse",6:"Réactions",7:"Edits",8:"Emotes",9:"Messages",10:"Mots",11:"Vocal","images":3,"gifs":2,"fichiers":1,"liens":4,"réponse":5,"réactions":6,"edits":7,"emotes":8,"messages":9,"mots":10,"vocal":11}

def embedDivers(table,mobile,evol):
    embed=discord.Embed()
    field1,field2,field3="","",""
    for ligne in table:
        rank="{0} {1}".format(ligne["Rank"],defEvol(ligne,evol))
        if ligne["ID"]==11:
            count=tempsVoice(ligne["Count"])
        else:
            count=ligne["Count"]
        nom=dictTrivia[ligne["ID"]]
        field1,field2,field3=addtoFields(field1,field2,field3,mobile,rank,nom,count)
        
    embed=createFields(mobile,embed,field1,field2,field3,"Rang","Objet","Nombre")
    return embed