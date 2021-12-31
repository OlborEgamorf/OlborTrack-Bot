import discord
from Core.Fonctions.GetNom import nomsOptions
from Core.Fonctions.TempsVoice import formatCount
from Core.Fonctions.Embeds import addtoFields, createFields




tableauMois={"01":"Janvier","02":"Février","03":"Mars","04":"Avril","05":"Mai","06":"Juin","07":"Juillet","08":"Aout","09":"Septembre","10":"Octobre","11":"Novembre","12":"Décembre","TO":"Année","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","glob":"GL","to":"TO"}
dictNameF2={"Messages":"Membre","Salons":"Salon","Freq":"Heure","Mots":"Membre","Emotes":"Emote","Reactions":"Emote","Voice":"Membre","Voicechan":"Salon","Mentions":"Membre","Mentionne":"Membre"}
dictNameF3={"Messages":"Messages","Salons":"Messages","Freq":"Messages","Mots":"Mots","Emotes":"Utilisations","Reactions":"Utilisations","Voice":"Temps","Voicechan":"Temps","Mentions":"Mentions","Mentionne":"Mentions"}

def embedFirst(table,page,option,guildOT,bot,mobile):
    embed=discord.Embed()
    field1,field2,field3="","",""
    stop=15*page if 15*page<len(table) else len(table)
    for i in range(15*(page-1),stop):
        nom=nomsOptions(option,table[i]["ID"],guildOT,bot)
        count=formatCount(option,table[i]["Count"])
        if table[i]["Annee"]=="GL":
            period="Général"
        else:
            period="{0} 20{1}".format(tableauMois[table[i]["Mois"]],table[i]["Annee"])
        field1,field2,field3=addtoFields(field1,field2,field3,mobile,period,nom,count)
    
    embed=createFields(mobile,embed,field1,field2,field3,"Période",dictNameF2[option],dictNameF3[option]) 
    return embed
        