import discord
from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.Embeds import addtoFields, createFields, defEvol
from Core.Fonctions.GetNom import getIndic
from Core.Fonctions.DichoTri import dichotomieID, triID

def embedServeurs(table,guild,page,mobile,evol):
    embed=discord.Embed()
    field1,field2,field3="","",""
    author=False
    stop=15*page if 15*page<len(table) else len(table)
    wl=""
    connexion,curseur=connectSQL("OT","Titres","Titres",None,None)
    for i in range(15*(page-1),stop):
        rank="{0} {1}".format(table[i]["Rank"],defEvol(table[i],evol))
        count=str(table[i]["Count"])
        nom=getIndic(curseur,table[i]["ID"])
        
        if table[i]["ID"]==guild.id:
            rank="**__{0}__**".format(rank)
            nom="**__{0}__**".format(nom)
            count="**__{0}__**".format(count)
            author=True

        field1,field2,field3=addtoFields(field1,field2,field3,mobile,rank,nom,count)
    
    if not author:
        table.sort(key=triID)
        etat=dichotomieID(table,guild.id,"ID")
        if etat[0]:
            rank="\n**__{0}__**".format(table[etat[1]]["Rank"])
            nom="**__{0}__**".format(getIndic(curseur,guild.id))

            if mobile:
                count="**__{0}__**".format(int(table[etat[1]]["Count"]))
            else:
                nom="\n{0}".format(nom)
                count="\n**__{0}__**".format(int(table[etat[1]]["Count"]))
            field1,field2,field3=addtoFields(field1,field2,field3,mobile,rank,nom,count)
    
    embed=createFields(mobile,embed,field1,field2,field3,"Rang","Serveur","Points")
    return embed