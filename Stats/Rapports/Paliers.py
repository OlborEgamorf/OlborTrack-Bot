from Core.Fonctions.TempsVoice import tempsVoice

def paliers(curseur,period,date,option):
    descip=""
    if option in ("Voice","Voicechan"):
        allMile={"jour":{1800:0,3600:0,14400:0,36000:0},"mois":{7200:0,18000:0,86400:0,432000:0},"annee":{86400:0,432000:0,864000:0,2678400:0},"global":{432000:0,864000:0,2678400:0,5356800:0}}
    else:
        allMile={"jour":{50:0,250:0,500:0,1000:0},"mois":{250:0,1000:0,2500:0,5000:0},"annee":{1000:0,2500:0,5000:0,10000:0},"global":{5000:0,10000:0,25000:0,50000:0}}
    dictMile=allMile[period]
    for i in dictMile:
        if period=="jour":
            dictMile[i]=curseur.execute("SELECT COUNT() AS Total FROM ranks WHERE Jour='{0}' AND Mois='{1}' AND Annee='{2}' AND Type='{3}' AND Count>{4}".format(date[0],date[1],date[2],option,i)).fetchone()["Total"]
        else:
            dictMile[i]=curseur.execute("SELECT COUNT() AS Total FROM {0}{1} WHERE Count>{2}".format(date[0],date[1],i)).fetchone()["Total"]

    for i in dictMile:
        if dictMile[i]!=0:
            if dictMile[i]>1:
                dictPhrase={"Salons":"**{0} salons** ont vu plus de __{1} messages__ envoyés".format(dictMile[i],i),"Freq":"**{0} heures** ont vu plus de __{1} messages__ envoyés".format(dictMile[i],i),"Emotes":"**{0} emotes** ont été utilisées plus de __{1} fois__".format(dictMile[i],i),"Reactions":"**{0} réactions** ont été utilisées plus de __{1} fois__".format(dictMile[i],i),"Voicechan":"**{0} salons** ont été utilisés pendant plus de __{1} en vocal__ en cumulé.".format(dictMile[i],tempsVoice(i))}
            else:
                dictPhrase={"Salons":"**1 salon** a vu plus de __{0} messages__ envoyés".format(i),"Freq":"**1 heure** a vu plus de __{0} messages__ envoyés".format(i),"Emotes":"**1 emote** a été utilisée plus de __{0} fois__".format(i),"Reactions":"**1 réaction** a été utilisée plus de __{0} fois__".format(i),"Voicechan":"**1 salon** a été utilisé pendant plus de __{0} en vocal__ en cumulé.".format(tempsVoice(i))}
            descip+=dictPhrase[option]+"\n"
    if descip=="":
        descip="Aucun palier atteint."
    return descip