############################################################################

 #######  #########     #########       #######
#       #     #                 #            #     Olbor Track Bot    
#       #     #                 #           #      Créé par OlborEgamorf  
#       #     #         #########          #       Fonctions diverses
#       #     #         #                 #                  
 #######      #         ############# #  #                         

############################################################################

### Importations
import aiohttp
import aiofiles
import discord
from Core.Fonctions.EcritureRecherche3 import rechercheCsv
from time import sleep, strftime
import sys
from math import inf
tableauSiom={"janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","TOTAL":"TO"}
tableauMoisInt={1:"janvier",2:"février",3:"mars",4:"avril",5:"mai",6:"juin",7:"juillet",8:"aout",9:"septembre",10:"octobre",11:"novembre",12:"décembre"}
dictTrivia={3:"Images",2:"GIFs",1:"Fichiers",4:"Liens",5:"Réponses",6:"Réactions",7:"Edits",8:"Emotes",9:"Messages",10:"Mots",11:"Vocal"}
dictPage={"+":1,"-":-1,None:0}
dictTriArg={"countAsc":"Count","rankAsc":"Rank","countDesc":"Count","rankDesc":"Rank","dateAsc":"DateID","dateDesc":"DateID","periodAsc":"None","periodDesc":"None","moyDesc":"Moyenne","nombreDesc":"Nombre"}
dictTriSens={"countAsc":"ASC","rankAsc":"ASC","countDesc":"DESC","rankDesc":"DESC","dateAsc":"ASC","dateDesc":"DESC","periodAsc":"None","periodDesc":"None","moyDesc":"DESC","nombreDesc":"DESC"}
#####


def lignesEmbed(nb,table,page):
    surplus=len(table)-nb
    if surplus%nb!=0:
        pageT=len(table)//nb+1
    else:
        pageT=len(table)//nb

    debut=nb*page
    borne=nb+(page*nb)
    if borne>len(table):
        borne=len(table)
    return debut,borne,pageT

def salonHideEmbed(option,table,arg):
    for i in option:
        h=0
        for j in table:
            if i[arg]==j[arg]:
                del table[h]
            h=h+1
    return table

def joursEmbed(table,option):
    i,longueur=0,len(table)
    while i<longueur:
        if option[1]=="TO":
            if len(table[i]["ID"])==5:
                if table[i]["ID"][3:5]!=option[0]:
                    del table[i]
                    i,longueur=i-1,longueur-1
            elif len(table[i]["ID"])==6:
                if table[i]["ID"][4:6]!=option[0]:
                    del table[i]
                    i,longueur=i-1,longueur-1
        else:
            if len(table[i]["ID"])==5:
                if table[i]["ID"][3:5]!=option[0] or table[i]["ID"][1:3]!=option[1]:
                    del table[i]
                    i,longueur=i-1,longueur-1
            elif len(table[i]["ID"])==6:
                if table[i]["ID"][4:6]!=option[0] or table[i]["ID"][2:4]!=option[1]:
                    del table[i]
                    i,longueur=i-1,longueur-1
        i+=1
    return table