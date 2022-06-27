from Core.Fonctions.TempsVoice import tempsVoice

tableauMois={"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre","TO":"TOTAL","1":"janvier","2":"février","3":"mars","4":"avril","5":"mai","6":"juin","7":"juillet","8":"aout","9":"septembre","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","to":"TO","glob":"GL"}

def paliers(curseur,period,date,option,user):
    descip=""
    if option=="Voicechan":
        allMile={"mois":{7200:0,18000:0,86400:0,432000:0},"annee":{86400:0,432000:0,864000:0,2678400:0},"global":{432000:0,864000:0,2678400:0,5356800:0}}
    else:
        allMile={"mois":{250:0,1000:0,2500:0,5000:0},"annee":{1000:0,2500:0,5000:0,10000:0},"global":{5000:0,10000:0,25000:0,50000:0}}
    dictMile=allMile[period]
    for i in dictMile:
        dictMile[i]=curseur.execute("SELECT COUNT() AS Total FROM perso{0}{1}{2} WHERE Count>{3}".format(tableauMois[date[0]],date[1],user,i)).fetchone()["Total"]

    for i in dictMile:
        if dictMile[i]!=0:
            if dictMile[i]>1:
                dictPhrase={"Salons":"Vous avez envoyé plus de __{1} messages__ envoyés dans **{0} salons**".format(dictMile[i],i),"Freq":"**{0} heures** ont vu plus de __{1} messages__ envoyés".format(dictMile[i],i),"Emotes":"Vous avez utilisé plus de __{1} fois__ **{0} emotes**".format(dictMile[i],i),"Reactions":"Vous avez utilisé plus de __{1} fois__ **{0} réactions**".format(dictMile[i],i),"Voicechan":"Vous avez passé plus de __{1}__ en vocal dans **{0} salons**".format(dictMile[i],tempsVoice(i))}
            else:
                dictPhrase={"Salons":"**1 salon** a vu plus de __{0} messages__ envoyés".format(i),"Freq":"**1 heure** a vu plus de __{0} messages__ envoyés".format(i),"Emotes":"**1 emote** a été utilisée plus de __{0} fois__".format(i),"Reactions":"**1 réaction** a été utilisée plus de __{0} fois__".format(i),"Voicechan":"Vous avez passé plus de __{0}__ en vocal dans **1 salon**".format(tempsVoice(i))}
            descip+=dictPhrase[option]+"\n"
    if descip=="":
        descip="Aucun palier atteint."
    return descip