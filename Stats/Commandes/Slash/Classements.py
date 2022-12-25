from time import strftime

import discord
from Core.Fonctions.Embeds import embedAssertClassic
from Core.Fonctions.GetTable import getTableRanks, getTableRanksJeux
from Core.Fonctions.setMaxPage import setMax
from Core.OTGuild import OTGuild
from Stats.Embeds.Central import statsEmbed
from Stats.SQL.ConnectSQL import CustomCursor


tableauMois={"01":"Janvier","02":"Février","03":"Mars","04":"Avril","05":"Mai","06":"Juin","07":"Juillet","08":"Aout","09":"Septembre","10":"Octobre","11":"Novembre","12":"Décembre","TO":"Année","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","glob":"GL","to":"TO"}

dictTables = {"Messages":"messages","Salons":"messages","Voice":"voice","Voicechan":"voice","Tortues":"tortues","TortuesDuo":"tortuesduo","TrivialVersus":"trivialversus","TrivialBR":"trivialbr","TrivialParty":"trivialparty","P4":"p4","BatailleNavale":"bataillenavale","CodeNames":"codenames","Morpion":"morpion","Matrice":"matrice","Trivial":"trivial"}
dictColumn = {"Messages":"User","Salons":"Salon","Voice":"User","Voicechan":"Salon","Tortues":"User","TortuesDuo":"User","TrivialVersus":"User","TrivialBR":"User","TrivialParty":"User","P4":"User","BatailleNavale":"User","CodeNames":"User","Morpion":"User","Matrice":"User","Trivial":"User"}

async def statsRank(interID:int,interaction:discord.Interaction,guildOT:OTGuild,bot,curseur:CustomCursor,ligne:dict) -> discord.Embed:
    try:
        mois,annee=ligne["Args1"],ligne["Args2"]
        option=ligne["Option"]
        obj=None if ligne["Args3"]=="None" else ligne["Args3"]

        if obj != None and option in ("Salons","Voicechan"):
            assert not guildOT.chan[int(obj)]["Hide"]

        if obj == None:
            embedOption = dictColumn[option]
        else:
            embedOption = "User"

        if option in ("Tortues","TortuesDuo","TrivialVersus","TrivialBR","TrivialParty","P4","BatailleNavale","CodeNames","Morpion","Matrice"):
            table = getTableRanksJeux(curseur,dictTables[option],mois,annee,obj)
        else:
            table = getTableRanks(curseur,dictTables[option],mois,annee,embedOption,obj)
        
        pagemax=setMax(len(table))
        page=ligne["Page"]
        ligne["PageMax"] = pagemax

        curseur.execute("UPDATE commandes SET PageMax={0} WHERE MessageID={1}".format(pagemax,interID))

        if pagemax == 1:
            table = table[:15]
        elif page == pagemax:
            table = table[15*(page-1):]
        else:
            table = table[15*(page-1):15*(page)]

        tableEvol=None
        evol=False

        if mois != "None":
            title="Classement {0} {1} 20{2}".format(option.lower(),tableauMois[mois],annee)
            if tableauMois[mois]==strftime("%m") and annee==strftime("%y"):
                tableEvol = getTableRanks(curseur,dictTables[option],mois,annee,embedOption,obj,dateMax=strftime("%y%m%d"))            
        elif annee != "None":
            title="Classement {0} 20{1}".format(option.lower(),annee)
            if annee == strftime("%y"):
                tableEvol = getTableRanks(curseur,dictTables[option],mois,annee,embedOption,obj,dateMax=strftime("%y%m%d"))
        else:
            title="Classement général {0}".format(option.lower())
            tableEvol = getTableRanks(curseur,dictTables[option],mois,annee,embedOption,obj,dateMax=strftime("%y%m%d"))

        if tableEvol != None:
            evol=True
            for i in table:
                inEvol=list(filter(lambda x:x["User"] == i["User"],tableEvol))
                if inEvol == []:
                    i["Evol"] = "N"
                else:
                    i["Evol"] = i["Rank"] - inEvol[0]["Rank"]

        return await statsEmbed(interaction,guildOT,bot,table,ligne,"guild",title,option,embedOption,evol=evol,obj=obj)
    
    except:
        return embedAssertClassic("Impossible de trouver ce que vous cherchez.\nSoit le module de stats est désactivé, soit le classement cherché n'existe pas ou alors est masqué par un administrateur.")
