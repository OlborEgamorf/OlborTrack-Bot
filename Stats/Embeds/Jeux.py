import discord
from Core.Fonctions.DichoTri import dichotomieID
from Core.Fonctions.Embeds import addtoFields, createFields, defEvol
from Core.Fonctions.GetNom import getTitre
from Stats.SQL.ConnectSQL import connectSQL
from Titres.Badges import getBadges

def embedJeux(table,guild,mobile,id,evol,option):
    embed=discord.Embed()
    field1,field2,field3="","",""
    author=False
    wl=""
    connexion,curseur=connectSQL("OT")
    for ligne in table:
        rank="{0} {1}".format(ligne["Rank"],defEvol(ligne,evol))
        if option!="trivial":
            wl="({0}/{1})".format(ligne["W"],ligne["L"])
        count="{0} {1}".format(int(ligne["Count"]),wl)

        nom="{0} {1}".format(getBadges(ligne["ID"],option),getTitre(curseur,ligne["ID"]))
        if type(guild.get_member(ligne["ID"]))==discord.Member and nom=="Inconnu":
            nom="<@{0}>".format(ligne["ID"])
        
        if ligne["ID"]==id:
            rank="**__{0}__**".format(rank)
            nom="**__{0}__**".format(nom)
            count="**__{0}__**".format(count)
            author=True

        field1,field2,field3=addtoFields(field1,field2,field3,mobile,rank,nom,count)
    
    if not author:
        table.sort(key=lambda x:x["ID"])
        etat=dichotomieID(table,id,"ID")
        if etat[0]:
            rank="\n**__{0}__**".format(table[etat[1]]["Rank"])

            nom="**__{0} {1}__**".format(getBadges(id,option),getTitre(curseur,id))
            if nom=="**__Inconnu__**":
                nom="**__<@{0}>__**".format(id)

            if option!="trivial":
                wl="({0}/{1})".format(table[etat[1]]["W"],table[etat[1]]["L"])
            if mobile:
                count="**__{0} {1}__**".format(int(table[etat[1]]["Count"]),wl)
            else:
                nom="\n{0}".format(nom)
                count="\n**__{0} {1}__**".format(int(table[etat[1]]["Count"]),wl)
            field1,field2,field3=addtoFields(field1,field2,field3,mobile,rank,nom,count)

    if option!="trivial":
        nomF3="Points (W/L)"
    else:
        nomF3="Exp"
    
    embed=createFields(mobile,embed,field1,field2,field3,"Rang","Membre",nomF3)
    return embed
