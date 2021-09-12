import discord
from Core.Fonctions.Embeds import addtoFields, createFields, defEvol
from Core.Fonctions.DichoTri import dichotomieID, triID
from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.GetNom import getTitre
from Titres.Badges import getBadges

dictOption={"tortues":"Tortues","tortuesduo":"TortuesDuo","trivialversus":"TrivialVersus","trivialbr":"TrivialBR","trivialparty":"TrivialParty","p4":"P4","bataillenavale":"BatailleNavale","cross":"Cross","trivial":"trivial"}

def embedJeux(table,guild,page,mobile,id,evol,option):
    embed=discord.Embed()
    field1,field2,field3="","",""
    author=False
    stop=15*page if 15*page<len(table) else len(table)
    wl=""
    connexion,curseur=connectSQL("OT","Titres","Titres",None,None)
    for i in range(15*(page-1),stop):
        rank="{0} {1}".format(table[i]["Rank"],defEvol(table[i],evol))
        if option!="trivial":
            wl="({0}/{1})".format(table[i]["W"],table[i]["L"])
        count="{0} {1}".format(int(table[i]["Count"]),wl)

        nom="{0} {1}".format(getBadges(table[i]["ID"],dictOption[option]),getTitre(curseur,table[i]["ID"]))
        if type(guild.get_member(table[i]["ID"]))==discord.Member and nom=="Inconnu":
            nom="<@{0}>".format(table[i]["ID"])
        
        if table[i]["ID"]==id:
            rank="**__{0}__**".format(rank)
            nom="**__{0}__**".format(nom)
            count="**__{0}__**".format(count)
            author=True

        field1,field2,field3=addtoFields(field1,field2,field3,mobile,rank,nom,count)
    
    if not author:
        table.sort(key=triID)
        etat=dichotomieID(table,id,"ID")
        if etat[0]:
            rank="\n**__{0}__**".format(table[etat[1]]["Rank"])

            nom="**__{0} {1}__**".format(getBadges(id,dictOption[option]),getTitre(curseur,id))
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