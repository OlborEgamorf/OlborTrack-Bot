import discord
from Core.Fonctions.TempsVoice import formatCount, tempsVoice
from Core.Fonctions.Embeds import addtoFields, createFields

tableauMois={"01":"Janvier","02":"Février","03":"Mars","04":"Avril","05":"Mai","06":"Juin","07":"Juillet","08":"Aout","09":"Septembre","10":"Octobre","11":"Novembre","12":"Décembre","TO":"Année","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","glob":"GL","to":"TO"}
dictNameF3={"Messages":"Messages","Salons":"Messages","Freq":"Messages","Mots":"Mots","Emotes":"Utilisations","Reactions":"Utilisations","Voice":"Temps","Voicechan":"Temps","Mentions":"Mentions","Mentionne":"Mentions","Divers":"Nombre"}

def embedMois(table,mobile,option):
    embed=discord.Embed()
    field1,field2,field3="","",""
    for ligne in table:
        rank=ligne["Rank"]
        if option=="Divers" and ligne["ID"]==11:
            count=tempsVoice(ligne["Count"])
        else:
            count=formatCount(option,ligne["Count"])
        if ligne["Annee"]=="GL":
            nom="Général"
        else:
            nom="{0} 20{1}".format(tableauMois[ligne["Mois"]],ligne["Annee"])
        field1,field2,field3=addtoFields(field1,field2,field3,mobile,rank,nom,count)
    
    embed=createFields(mobile,embed,field1,field2,field3,"Rang","Période",dictNameF3[option]) 
    return embed