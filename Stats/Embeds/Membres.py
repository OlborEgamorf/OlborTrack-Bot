import discord
from Core.Fonctions.Embeds import addtoFields, createFields, defEvol
from Core.Fonctions.TempsVoice import formatCount, tempsVoice
from Core.Fonctions.DichoTri import dichotomieID
from Titres.Badges import getBadges

dictNameF3={"Messages":"Messages","Salons":"Messages","Freq":"Messages","Mots":"Mots","Emotes":"Utilisations","Reactions":"Utilisations","Voice":"Temps","Voicechan":"Temps","Divers":"Nombre"}

def embedMembre(table,guildOT,mobile,id,evol,option):
    embed=discord.Embed()
    field1,field2,field3="","",""
    author=False
    for ligne in table:
        rank="{0} {1}".format(ligne["Rank"],defEvol(ligne,evol))
        if option=="Divers" and ligne["IDComp"]==11:
            count=tempsVoice(ligne["Count"])
        else:
            count=formatCount(option,ligne["Count"])
        if guildOT.users[ligne["ID"]]["Hide"]:
            nom="*Membre masqué*"
            count="*?*"
        elif guildOT.users[ligne["ID"]]["Leave"]:
            nom="*Ancien membre*"
        else:
            nom="{0}<@{1}>".format(getBadges(ligne["ID"],None),ligne["ID"])
        
        if ligne["ID"]==id:
            rank="**__{0}__**".format(rank)
            nom="**__{0}__**".format(nom)
            count="**__{0}__**".format(count)
            author=True

        field1,field2,field3=addtoFields(field1,field2,field3,mobile,rank,nom,count)
    
    if not author and not guildOT.users[id]["Hide"]:
        table.sort(key=lambda x:x["ID"])
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