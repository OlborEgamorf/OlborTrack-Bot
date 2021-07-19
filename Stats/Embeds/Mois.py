import discord
from Core.Fonctions.TempsVoice import formatCount
from Core.Fonctions.Embeds import addtoFields

tableauMois={"01":"Janvier","02":"Février","03":"Mars","04":"Avril","05":"Mai","06":"Juin","07":"Juillet","08":"Aout","09":"Septembre","10":"Octobre","11":"Novembre","12":"Décembre","TO":"Année","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","glob":"GL","to":"TO"}
dictNameF3={"Messages":"Messages","Salons":"Messages","Freq":"Messages","Mots":"Mots","Emotes":"Utilisations","Reactions":"Utilisations","Voice":"Temps","Voicechan":"Temps","Mentions":"Mentions","Mentionne":"Mentions","Divers":"Nombre"}

def embedMois(table,page,mobile,option):
    embed=discord.Embed()
    field1,field2,field3="","",""
    stop=15*page if 15*page<len(table) else len(table)
    for i in range(15*(page-1),stop):
        rank=table[i]["Rank"]
        count=formatCount(option,table[i]["Count"])
        if table[i]["Annee"]=="GL":
            nom="Général"
        else:
            nom="{0} 20{1}".format(tableauMois[table[i]["Mois"]],table[i]["Annee"])
        field1,field2,field3=addtoFields(field1,field2,field3,mobile,rank,nom,count)
        
    if mobile:
        embed.description=field1
    else:
        embed.add_field(name="Rang",value=field1,inline=True)
        embed.add_field(name="Période",value=field2,inline=True)
        embed.add_field(name=dictNameF3[option],value=field3,inline=True)
    return embed