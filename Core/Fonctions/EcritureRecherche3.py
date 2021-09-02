### ANCIENS FICHIERS QUAND LES STATS ETAIENT STOCKEES EN CSV, NE SERT PLUS A GRAND CHOSE MAIS ENCORE LA POUR QUELQUES TEMPS AU CAS OU

############################################################################

 #######  #########     #########       #######
#       #     #                 #            #     Olbor Track Bot    
#       #     #                 #           #      Créé par OlborEgamorf  
#       #     #         #########          #       Ecriture et recherche de fichiers
#       #     #         #                 #                  
 #######      #         ############# #  #                         

############################################################################

### Importations
import os
import csv
import sys
sys.path.append('Code/Modules')
tableauMois={"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre"}
from time import strftime
#####


### Fonction qui cherche la bonne table
def rechercheCsv(option,guild,arg1,arg2,arg3,arg4):
    """mois, userMois, userAnnee, jour, total, global, trivia, request, data, freq, freqserv, param, ww, svtitle, ustitle, gltitle, indics, wwservers, chanMois, chanGlobal, chanAnnee, userChan, totalMois, userMoyenne"""
    tableStats=[]
    mois=tableauMois[strftime("%m")]
    annee=strftime("%y")
    if option=="mois":
        ouverture="CSV/_"+str(guild)+"/mois/_"+annee+"/_"+mois+".csv"                    # Table de ce mois
    elif option=="userMois":
        ouverture="CSV/_"+str(guild)+"/zsers/_moisM/_"+str(arg1)+".csv"                        # Table de l'utilisateur
    elif option=="userAnnee":
        ouverture="CSV/_"+str(guild)+"/zsers/_anneesM/_"+str(arg1)+".csv"                      # Table de l'utilisateur pour les totaux
    elif option=="jour":
        ouverture="CSV/_"+str(guild)+"/mois/LogJour.csv"                                    # Table du jour
    elif option=="jourVoice":
        ouverture="CSV/_"+str(guild)+"/voice/LogJour.csv" 
    elif option=="total":
        ouverture="CSV/_"+str(guild)+"/mois/_"+annee+"/_TOTAL.csv"                       # Table du total de l'année
    elif option=="global":
        ouverture="CSV/_"+str(guild)+"/mois/_General.csv"                                    # Table du classement général
    elif option=="trivia":
        if os.path.exists("CSV/_"+str(guild)+"/zsers/_trivia/_"+str(arg1)+"/_"+arg2)==False:
            os.makedirs("CSV/_"+str(guild)+"/zsers/_trivia/_"+str(arg1)+"/_"+arg2)
        ouverture="CSV/_"+str(guild)+"/zsers/_trivia/_"+str(arg1)+"/_"+arg2+"/_"+arg3+".csv"  
    elif option=="triviaType":
        ouverture="CSV/_"+str(guild)+"/zsers/_trivia/_"+str(arg1)+"/_"+arg2+".csv"  
    elif option=="request":
        ouverture="CSV/_"+str(guild)+"/_Requests.csv"
    elif option=="data":
        ouverture="CSV/_"+str(guild)+"/_Data.csv"
    elif option=="freq":
        ouverture="CSV/_"+str(guild)+"/zsers/_freq/_"+str(arg1)+".csv"  
    elif option=="freqserv":
        ouverture="CSV/_"+str(guild)+"/mois/_freq.csv"  
    elif option=="param":
        ouverture="CSV/_"+str(guild)+"/_Param.csv"
    elif option=="ww":
        ouverture="CSV/_ww.csv"
    elif option=="svtitle":
        ouverture="CSV/_"+str(guild)+"/_servtitle.csv"
    elif option=="ustitle":
        ouverture="CSV/zsers/_titles/_"+str(arg1)+".csv"
    elif option=="gltitle":
        ouverture="CSV/_titles.csv"
    elif option=="titlesAll":
        ouverture="CSV/_usTitle.csv"
    elif option=="indics":
        ouverture="CSV/_indics.csv"
    elif option=="wwservers":
        ouverture="CSV/_servers.csv"
    if option=="chanMois":
        ouverture="CSV/_"+str(guild)+"/channels/_"+annee+"/_"+mois+".csv" 
    elif option=="chanGlobal":    
        ouverture="CSV/_"+str(guild)+"/channels/_General.csv"   
    elif option=="chanAnnee":
        ouverture="CSV/_"+str(guild)+"/channels/_"+annee+"/_TOTAL.csv"  
    elif option=="userChan":
        ouverture="CSV/_"+str(guild)+"/zsers/_channels/_"+str(arg1)+".csv"  
    elif option=="rankChanM" or option=="rankChanT" or option=="rankChanG": 
        if os.path.exists("CSV/_"+str(guild)+"/channels/_"+str(arg1)+"/_"+str(arg2))==False:
            os.makedirs("CSV/_"+str(guild)+"/channels/_"+str(arg1)+"/_"+str(arg2))
        if option=="rankChanG":
            ouverture="CSV/_"+str(guild)+"/channels/_"+str(arg1)+"/_General.csv" 
        elif option=="rankChanT":
            ouverture="CSV/_"+str(guild)+"/channels/_"+str(arg1)+"/_"+str(arg2)+"/_TOTAL.csv"  
        elif option=="rankChanM":
            ouverture="CSV/_"+str(guild)+"/channels/_"+str(arg1)+"/_"+str(arg2)+"/_"+str(arg3)+".csv" 
    elif option=="userChanPlus":
        if os.path.exists("CSV/_"+str(guild)+"/zsers/_channels/_"+str(arg1)+"/_"+str(arg2))==False:
            os.makedirs("CSV/_"+str(guild)+"/zsers/_channels/_"+str(arg1)+"/_"+str(arg2))
        ouverture="CSV/_"+str(guild)+"/zsers/_channels/_"+str(arg1)+"/_"+str(arg2)+"/_"+str(arg3)+".csv"  
    elif option=="totalMois":
        ouverture="CSV/_"+str(guild)+"/mois/_TOTAL.csv"  
    elif option=="heure":
        ouverture="CSV/_"+str(guild)+"/mois/LogHeure.csv"  
    elif option=="rankMoy":
        ouverture="CSV/_"+str(guild)+"/mois/_moy"+arg1+".csv"
    elif option=="get":
        ouverture="CSV/_"+str(guild)+"/GETING/_chan.csv"
    elif option=="spaceTitle":
        ouverture="CSV/zsers/_space/_"+str(arg1)+".csv"
    elif option=="evol":
        if os.path.exists("CSV/_"+str(guild)+"/zsers/_evol"+arg4+"/_"+str(arg1))==False:
            os.makedirs("CSV/_"+str(guild)+"/zsers/_evol"+arg4+"/_"+str(arg1))
        ouverture="CSV/_"+str(guild)+"/zsers/_evol"+arg4+"/_"+str(arg1)+"/_"+str(arg2)+str(arg3)+".csv"
    elif option=="quote":
        ouverture="CSV/_"+str(guild)+"/_Quotes.csv"
    elif option=="blind":
        ouverture="CSV/_"+str(guild)+"/_Blind.csv"
    elif option=="hide":
        ouverture="CSV/_"+str(guild)+"/_Hide.csv"
    elif option=="mute":
        ouverture="CSV/_"+str(guild)+"/_Mute.csv"
    elif option=="rankP4":
        ouverture="CSV/_"+str(guild)+"/_P4.csv"
    elif option=="histoP4":
        ouverture="CSV/_"+str(guild)+"/zsers/_P4/_h"+str(arg1)+".csv"  
    elif option=="pingenv":
        ouverture="CSV/_"+str(guild)+"/zsers/_pingenv/_"+str(arg1)+".csv" 
    elif option=="pingrec":
        ouverture="CSV/_"+str(guild)+"/zsers/_pingrec/_"+str(arg1)+".csv" 
    elif option=="pres":
        ouverture="CSV/_statuts.csv"
    elif option=="perms":
        ouverture="CSV/_"+str(guild)+"/_Perms.csv"
    elif option=="permscmd":
        ouverture="CSV/_"+str(guild)+"/_PermsCMD.csv"
    elif option=="moisWord":
        ouverture="CSV/_"+str(guild)+"/words/_"+annee+"/_"+mois+".csv"          
    elif option=="userMoisWord":
        ouverture="CSV/_"+str(guild)+"/zsers/_moisW/_"+str(arg1)+".csv"          
    elif option=="userAnneeWord":
        ouverture="CSV/_"+str(guild)+"/zsers/_anneesW/_"+str(arg1)+".csv"        
    elif option=="totalWord":
        ouverture="CSV/_"+str(guild)+"/words/_"+annee+"/_TOTAL.csv"                 
    elif option=="globalWord":
        ouverture="CSV/_"+str(guild)+"/words/_General.csv"  
    elif option=="totalMoisWord":
        ouverture="CSV/_"+str(guild)+"/words/_TOTAL.csv"       
    elif option=="commandes":
        ouverture="CSV/_"+str(guild)+"/commandes/_"+str(arg1)+".csv" 
    elif option=="cmdOT":
        ouverture="CSV/_commandesOT.csv"
    elif option=="globalRole" or option=="totalRole" or option=="moisRole": 
        if os.path.exists("CSV/_"+str(guild)+"/roles/_"+str(arg1)+"/_"+str(arg2))==False:
            os.makedirs("CSV/_"+str(guild)+"/roles/_"+str(arg1)+"/_"+str(arg2))
        if option=="globalRole":
            ouverture="CSV/_"+str(guild)+"/roles/_"+str(arg1)+"/_General.csv" 
        elif option=="totalRole":
            ouverture="CSV/_"+str(guild)+"/roles/_"+str(arg1)+"/_"+str(arg2)+"/_TOTAL.csv"  
        elif option=="moisRole":
            ouverture="CSV/_"+str(guild)+"/roles/_"+str(arg1)+"/_"+str(arg2)+"/_"+str(arg3)+".csv"  
    elif option=="voiceMois":
        ouverture="CSV/_"+str(guild)+"/voice/_"+arg1+"/_"+annee+"/_"+mois+".csv" 
    elif option=="voiceTotal":
        ouverture="CSV/_"+str(guild)+"/voice/_"+arg1+"/_"+annee+"/_TOTAL.csv"                     
    elif option=="voiceGlobal":
        ouverture="CSV/_"+str(guild)+"/voice/_"+arg1+"/_General.csv"
    elif option=="voicePerso":
        ouverture="CSV/_"+str(guild)+"/voice/_perso/_"+str(arg1)+".csv"
    elif option=="voiceHisto":
        ouverture="CSV/_"+str(guild)+"/voice/_histo/_"+str(arg1)+".csv"
    elif option=="voiceChan":
        ouverture="CSV/_"+str(guild)+"/voice/_persoChan/_"+str(arg1)+".csv"
    elif option=="dayRank":
        ouverture="CSV/_"+str(guild)+"/mois/_dayRank.csv" 
    elif option=="freqMois":
        if os.path.exists("CSV/_"+str(guild)+"/zsers/_freq/_"+str(arg1)+"/_"+str(arg2))==False:
            os.makedirs("CSV/_"+str(guild)+"/zsers/_freq/_"+str(arg1)+"/_"+str(arg2))
        ouverture="CSV/_"+str(guild)+"/zsers/_freq/_"+str(arg1)+"/_"+str(arg2)+"/_"+str(arg3)+".csv"  
    elif option=="freqHeure":
        if os.path.exists("CSV/_"+str(guild)+"/zsers/_freq/_"+str(arg1))==False:
            os.makedirs("CSV/_"+str(guild)+"/zsers/_freq/_"+str(arg1))
        ouverture="CSV/_"+str(guild)+"/zsers/_freq/_"+str(arg1)+"/_"+str(arg2)+".csv" 
    elif option=="starboard":
        ouverture="CSV/_"+str(guild)+"/_SB.csv"
    elif option=="starmessages":
        ouverture="CSV/_"+str(guild)+"/_SBmessages.csv"
    elif option=="subs":
        ouverture="CSV/_subs.csv"
    elif option=="P4WW":
        ouverture="CSV/_P4WW.csv"
    elif option=="owners":
        ouverture="CSV/_owners.csv"
    elif option=="reports":
        ouverture="CSV/_reports"+str(arg1)+".csv"
    elif option=="reportJ":
        if os.path.exists("CSV/_"+str(guild)+"/reports/_jours/_"+str(arg1)+str(arg2)+str(arg3))==False:
            os.makedirs("CSV/_"+str(guild)+"/reports/_jours/_"+str(arg1)+str(arg2)+str(arg3))
        ouverture="CSV/_"+str(guild)+"/reports/_jours/_"+str(arg1)+str(arg2)+str(arg3)+"/_"+str(arg4)+".csv"
    elif option=="reportS":
        if os.path.exists("CSV/_"+str(guild)+"/reports/_semaines/_"+str(arg1)+str(arg2))==False:
            os.makedirs("CSV/_"+str(guild)+"/reports/_semaines/_"+str(arg1)+str(arg2))
        ouverture="CSV/_"+str(guild)+"/reports/_semaines/_"+str(arg1)+str(arg2)+"/_"+str(arg3)+".csv"
    elif option=="reportM":
        if os.path.exists("CSV/_"+str(guild)+"/reports/_mois/_"+str(arg1)+str(arg2))==False:
            os.makedirs("CSV/_"+str(guild)+"/reports/_mois/_"+str(arg1)+str(arg2))
        ouverture="CSV/_"+str(guild)+"/reports/_mois/_"+str(arg1)+str(arg2)+"/_"+str(arg3)+".csv"
    elif option=="snipe":
        ouverture="CSV/_"+str(guild)+"/_snipe.csv"
    elif option=="emoteMois":
        ouverture="CSV/_"+str(guild)+"/emotes/_rank"+annee+"/_"+mois+".csv" 
    elif option=="emoteTotal":
        ouverture="CSV/_"+str(guild)+"/emotes/_rank"+annee+"/_TOTAL.csv"                     
    elif option=="emoteGlobal":
        ouverture="CSV/_"+str(guild)+"/emotes/_rank/_General.csv"
    elif option=="emotePerso":
        ouverture="CSV/_"+str(guild)+"/emotes/_perso/_"+str(arg1)+".csv"
    elif option=="archive":
        ouverture="CSV/_"+str(guild)+"/"+arg1+"/_"+arg2+"/_"+arg3+".csv"
    elif option=="trivial":
        ouverture="CSV/trivial/_zsers/_"+str(arg1)+".csv"
    elif option=="trivialRank":
        ouverture="CSV/trivial/_rank/_"+str(arg1)+".csv"
    elif option=="trivialInvent":
        ouverture="CSV/trivial/_invent/_"+str(arg1)+".csv"
    elif option=="trivialHisto":
        ouverture="CSV/trivial/_histo/_"+str(arg1)+".csv"
    elif option=="emotesG" or option=="emotesT" or option=="emotesM": 
        if os.path.exists("CSV/_"+str(guild)+"/emotes/_"+arg4+"/_"+str(arg1)+"/_"+str(arg2))==False:
            os.makedirs("CSV/_"+str(guild)+"/emotes/_"+arg4+"/_"+str(arg1)+"/_"+str(arg2))
        if option=="emotesG":
            ouverture="CSV/_"+str(guild)+"/emotes/_"+arg4+"/_"+str(arg1)+"/_General.csv" 
        elif option=="emotesT":
            ouverture="CSV/_"+str(guild)+"/emotes/_"+arg4+"/_"+str(arg1)+"/_"+str(arg2)+"/_TOTAL.csv"  
        elif option=="emotesM":
            ouverture="CSV/_"+str(guild)+"/emotes/_"+arg4+"/_"+str(arg1)+"/_"+str(arg2)+"/_"+str(arg3)+".csv" 
    elif option=="emotesP":
        ouverture="CSV/_"+str(guild)+"/emotes/_"+arg4+"/_emotes/_"+str(arg1)+".csv" 
    elif option=="emotesU":
        if os.path.exists("CSV/_"+str(guild)+"/emotes/_"+arg4+"/_emoteszsers/_"+str(arg1))==False:
            os.makedirs("CSV/_"+str(guild)+"/emotes/_"+arg4+"/_emoteszsers/_"+str(arg1))
        ouverture="CSV/_"+str(guild)+"/emotes/_"+arg4+"/_emoteszsers/_"+str(arg1)+"/_"+str(arg2)+".csv" 
    elif option=="emotesPG" or option=="emotesPT" or option=="emotesPM": 
        if os.path.exists("CSV/_"+str(guild)+"/emotes/_"+arg4+"/_perso/_"+str(arg1)+"/_"+str(arg2))==False:
            os.makedirs("CSV/_"+str(guild)+"/emotes/_"+arg4+"/_perso/_"+str(arg1)+"/_"+str(arg2))
        if option=="emotesPG":
            ouverture="CSV/_"+str(guild)+"/emotes/_"+arg4+"/_perso/_"+str(arg1)+"/_General.csv" 
        elif option=="emotesPT":
            ouverture="CSV/_"+str(guild)+"/emotes/_"+arg4+"/_perso/_"+str(arg1)+"/_"+str(arg2)+"/_TOTAL.csv"  
        elif option=="emotesPM":
            ouverture="CSV/_"+str(guild)+"/emotes/_"+arg4+"/_perso/_"+str(arg1)+"/_"+str(arg2)+"/_"+str(arg3)+".csv" 
    elif option=="gareroll":
        ouverture="CSV/_"+str(guild)+"/giveaways/_"+str(arg1)+".csv"
    elif option=="tesdqsd":
        ouverture="CSV/_qqq.csv"
    elif option=="2048r":
        ouverture="CSV/2048/_General.csv"
    elif option=="2048u":
        ouverture="CSV/2048/_"+str(arg1)+".csv"
    try:
        open(ouverture, "a",encoding="utf-8-sig")
        with open(ouverture, encoding="utf-8-sig", newline="") as fichier :
            for ligne in csv.DictReader(fichier):
                tableStats.append(dict(ligne))
    except csv.Error:
        if option=="mois" or option=="rankmoy":
            tableStats=recup(option,guild,arg1)
        elif option=="rankMoy":
            tableStats=recup(option+arg1,guild,arg2)
        elif option=="voiceMois":
            tableStats=recup(option,guild,arg2)
        else:
            tableStats=recup(option,guild,0)
        print("RECUP "+option+" "+str(guild))
    return [tableStats, ouverture]
#####


### Fonction pour chercher un ancien classement
def rechercheArchives(mois,annee,guild,classe):
    try:
        add=False
        tableStats=[]
        ouverture="CSV/_"+str(guild)+"/"+classe+"/_"+annee+"/_"+mois+".csv"
        open(ouverture, "a",encoding="utf-8-sig")
        with open(ouverture, encoding="utf-8-sig", newline="") as fichier :
            for ligne in csv.DictReader(fichier):
                tableStats.append(dict(ligne))
    except:
        assert add==True, "Dossier d'année introuvable."
        return
    return tableStats, ouverture
#####


### Fonction pour chercher un fichier de moyennes
def rechercheMoyennes(id,guild,annee,option):
    tableStats=[]
    ouverture="CSV/_"+str(guild)+"/zsers/_moyennes/_"+str(annee)+"/_"+option+"/_"+str(id)+".csv"
    open(ouverture, "a",encoding="utf-8-sig")
    with open(ouverture, encoding="utf-8-sig", newline="") as fichier :
        for ligne in csv.DictReader(fichier):
            tableStats.append(dict(ligne))
    return tableStats, ouverture
#####


### Fonction pour chercher une page d'aide
def rechercheHelp(page):
    tableStats=[]
    ouverture="CSV/help/_"+str(page)+".csv"
    open(ouverture, "a",encoding="utf-8-sig")
    with open(ouverture, encoding="utf-8-sig", newline="") as fichier :
        for ligne in csv.DictReader(fichier, delimiter=";"):
            tableStats.append(dict(ligne))
    return tableStats, ouverture
#####


### Fonction pour chercher une commande custom
def rechercheCommande(guild,command,option):
    tableStats=[]
    if option=="embed":
        ouverture="CSV/_"+str(guild)+"/commandes/_embeds/_"+str(command)+".csv" 
    elif option=="quote":
        ouverture="CSV/_"+str(guild)+"/_Quotes.csv"
    elif option=="snipe":
        ouverture="CSV/_"+str(guild)+"/_snipe.csv"
    elif option=="trivial":
        ouverture="CSV/trivial/_questions/"+str(guild)+".csv"
    else:
        ouverture="CSV/_"+str(guild)+"/commandes/_"+str(command)+".csv" 
    open(ouverture, "a",encoding="utf-8-sig")
    with open(ouverture, encoding="utf-8-sig", newline="") as fichier :
        for ligne in csv.DictReader(fichier, delimiter="§"):
            tableStats.append(dict(ligne))
    return [tableStats, ouverture]
#####


### Fonction d'écriture dans le CSV
def ecritureCsvCMD(table,fichier,delim):
    if table==[] or table==None:
        ecrire=open(fichier, "w", encoding="utf-8-sig")
        return
    ecrire=open(fichier, "w", encoding="utf-8-sig")
    ajout_key=""
    for key in table[0].keys():
        if ajout_key=="":
            ajout_key=key
        else:
            ajout_key=ajout_key+delim+key
    ecrire.write(ajout_key)

    for i in range(len(table)):
        ajout_value=""
        for valeur in table[i].values():
            if ajout_value=="":
                ajout_value=str(valeur)
            else:
                ajout_value=ajout_value+delim+str(valeur)
        ecrire.write("\n"+ajout_value)
    return
#####


### Fonction d'écriture dans le CSV
def ecritureCsv(table,fichier):
    if table==[] or table==None:
        ecrire=open(fichier, "w", encoding="utf-8-sig")
        return
    ecrire=open(fichier, "w", encoding="utf-8-sig")
    ajout_key=""
    for key in table[0].keys():
        if ajout_key=="" or ajout_key==None:
            ajout_key=str(key)
        else:
            ajout_key=str(ajout_key)+","+str(key)
    ecrire.write(ajout_key)

    for i in range(len(table)):
        ajout_value=""
        for valeur in table[i].values():
            if ajout_value=="":
                ajout_value=str(valeur)
            else:
                ajout_value=ajout_value+","+str(valeur)
        ecrire.write("\n"+ajout_value)
    return
#####

def ecritureCsvGD(table,fichier):
    fichPath=fichier.split("/")
    path=""
    for i in range(len(fichPath)-1):
        path+=fichPath[i]+"/"
    if os.path.exists(path)==False:
        os.makedirs(path)
    if table==[] or table==None:
        ecrire=open(fichier, "w", encoding="utf-8-sig")
        return
    ecrire=open(fichier, "w", encoding="utf-8-sig")
    ajout_key=""
    for key in table[0].keys():
        if ajout_key=="" or ajout_key==None:
            ajout_key=str(key)
        else:
            ajout_key=str(ajout_key)+","+str(key)
    ecrire.write(ajout_key)

    for i in range(len(table)):
        ajout_value=""
        for valeur in table[i].values():
            if ajout_value=="":
                ajout_value=str(valeur)
            else:
                ajout_value=ajout_value+","+str(valeur)
        ecrire.write("\n"+ajout_value)
    return