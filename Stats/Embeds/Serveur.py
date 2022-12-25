import discord
from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.Embeds import addtoFields, createFields, defEvol
from Core.Fonctions.GetNom import getIndic
from Core.Fonctions.DichoTri import dichotomieID

def embedServeurs(table,guild,mobile,evol):
    embed=discord.Embed()
    field1,field2,field3="","",""
    author=False
    connexion,curseur=connectSQL("OT")
    for ligne in table:
        rank="{0} {1}".format(ligne["Rank"],defEvol(ligne,evol))
        count=str(ligne["Count"])
        nom=getIndic(curseur,ligne["ID"])
        
        if ligne["ID"]==guild.id:
            rank="**__{0}__**".format(rank)
            nom="**__{0}__**".format(nom)
            count="**__{0}__**".format(count)
            author=True

        field1,field2,field3=addtoFields(field1,field2,field3,mobile,rank,nom,count)
    
    if not author:
        table.sort(key=lambda x:x["ID"])
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