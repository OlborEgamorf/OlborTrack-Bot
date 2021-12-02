import discord
from Core.Fonctions.Embeds import addtoFields, createFields, defEvol
from Core.Fonctions.TempsVoice import formatCount, tempsVoice
from Core.Fonctions.DichoTri import dichotomieID, triID
from Titres.Badges import getBadges

dictNameF3={"Messages":"Messages","Salons":"Messages","Freq":"Messages","Mots":"Mots","Emotes":"Utilisations","Reactions":"Utilisations","Voice":"Temps","Voicechan":"Temps","Mentions":"Mentions","Mentionne":"Mentions","Divers":"Nombre"}

def embedMembre(table,guildOT,page,mobile,id,evol,option):
    embed=discord.Embed()
    field1,field2,field3="","",""
    author=False
    stop=15*page if 15*page<len(table) else len(table)
    for i in range(15*(page-1),stop):
        rank="{0} {1}".format(table[i]["Rank"],defEvol(table[i],evol))
        if option=="Divers" and table[i]["IDComp"]==11:
            count=tempsVoice(table[i]["Count"])
        else:
            count=formatCount(option,table[i]["Count"])
        if guildOT.users[table[i]["ID"]]["Hide"]:
            nom="*Membre masqué*"
            count="*?*"
        elif guildOT.users[table[i]["ID"]]["Leave"]:
            nom="*Ancien membre*"
        else:
            nom="{0}<@{1}>".format(getBadges(table[i]["ID"],None),table[i]["ID"])
        
        if table[i]["ID"]==id:
            rank="**__{0}__**".format(rank)
            nom="**__{0}__**".format(nom)
            count="**__{0}__**".format(count)
            author=True

        field1,field2,field3=addtoFields(field1,field2,field3,mobile,rank,nom,count)
    
    if not author and not guildOT.users[id]["Hide"]:
        table.sort(key=triID)
        etat=dichotomieID(table,id,"ID")
        if etat[0]:
            rank="\n**__{0}__**".format(table[etat[1]]["Rank"])
            if mobile:
                nom="**__<@{0}>__**".format(id)
                count="**__{0}__**".format(formatCount(option,table[etat[1]]["Count"]))
            else:
                nom="\n**__<@{0}>__**".format(id)
                count="\n**__{0}__**".format(formatCount(option,table[etat[1]]["Count"]))
            field1,field2,field3=addtoFields(field1,field2,field3,mobile,rank,nom,count)

    embed=createFields(mobile,embed,field1,field2,field3,"Rang","Membre",dictNameF3[option])
    return embed