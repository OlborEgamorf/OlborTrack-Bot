from random import randint
import discord
from Core.Fonctions.WebRequest import webRequest
from Core.Fonctions.AuteurIcon import auteur
tableauMois={"01":"Janvier","02":"Février","03":"Mars","04":"Avril","05":"Mai","06":"Juin","07":"Juillet","08":"Aout","09":"Septembre","10":"Octobre","11":"Novembre","12":"Décembre","TO":"Année","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","glob":"GL","to":"TO"}

async def embedWikiEvents(option,jour,mois):
    descip,hyper="",""
    table=await webRequest("https://byabbe.se/on-this-day/"+str(int(mois))+"/"+str(int(jour))+"/"+option+".json")
    assert table!=False, "Il y a eu une erreur lors de la recherche de la page."
    date1, date2=randint(0,len(table[option])-1),randint(0,len(table[option])-1)
    while date2==date1:
        date2=randint(0,len(table[option])-1)
    listeDates=[date1,date2]
    listeDates.sort()
    for i in range(2):
        descip+="**"+table[option][listeDates[i]]["year"]+": **"+table[option][listeDates[i]]["description"]+"\n"
        for k in range(len(table[option][listeDates[i]]["wikipedia"])):
            hyper+="["+table[option][listeDates[i]]["wikipedia"][k]["title"]+"]("+table[option][listeDates[i]]["wikipedia"][k]["wikipedia"]+"), "
    embedW=discord.Embed(title=jour+" "+tableauMois[mois],description=descip+"\nRéférences : "+hyper[0:len(hyper)-2],color=0xfcfcfc)
    embedW.set_footer(text="OT!events - "+option)
    embedW=auteur(table["wikipedia"],0,0,embedW,"wp")
    return embedW