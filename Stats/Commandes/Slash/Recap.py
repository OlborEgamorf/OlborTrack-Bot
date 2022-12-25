from time import strftime

import discord
from Core.Decorator import OTCommand
from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.GetNom import nomsOptions
from Core.Fonctions.GetPeriod import getAnnee, getMois
from Core.Fonctions.RankingClassic import rankingClassic
from Core.Fonctions.TempsVoice import tempsVoice
from Stats.SQL.ConnectSQL import connectSQL

tableauMois={"01":"Janvier","02":"Février","03":"Mars","04":"Avril","05":"Mai","06":"Juin","07":"Juillet","08":"Aout","09":"Septembre","10":"Octobre","11":"Novembre","12":"Décembre","TO":"TO","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","glob":"GL","to":"TO"}

@OTCommand
async def recapStats(interaction,bot,periode):
    if periode==None:
        mois,annee="glob",""
    else:
        periode=periode.split(" ")
        if periode[0].lower() not in ("mois","annee"):
            try:
                mois,annee=getMois(periode[0].lower()),getAnnee(periode[1].lower())
            except:
                try:
                    mois,annee="to",getAnnee(periode[0].lower())
                except:
                    mois,annee="glob",""
        elif periode[0].lower()=="mois":
            mois,annee=tableauMois[strftime("%m")].lower(),strftime("%y")
        elif periode[0].lower()=="annee":
            mois,annee="to",strftime("%y")
    
    dictMessages,dictSalons,dictEmotes,dictVoc,dictFreq=[],[],{},[],{}
    guilds=interaction.user.mutual_guilds
    dictAutre={"Messages":0,"Vocal":0,"Serveurs":len(guilds)}
    for i in guilds:
        connexion,curseur=connectSQL(i.id)
        try:
            mess=curseur.execute("SELECT Rank,Count FROM {0}{1} WHERE ID={2}".format(mois,annee,interaction.user.id)).fetchone()
            if mess!=None:
                dictMessages.append({"ID":i.id,"Count":mess["Count"],"RankIntern":mess["Rank"],"Rank":0,"Nom":i.name})
                dictAutre["Messages"]+=mess["Count"]
            curseur.close()
            connexion.close()
        except:
            pass
        
        try:
            voc=curseur.execute("SELECT Rank,Count FROM {0}{1} WHERE ID={2}".format(mois,annee,interaction.user.id)).fetchone()
            if mess!=None:
                dictVoc.append({"ID":i.id,"Count":voc["Count"],"RankIntern":voc["Rank"],"Rank":0,"Nom":i.name})
                dictAutre["Vocal"]+=voc["Count"]
            curseur.close()
            connexion.close()
        except:
            pass
        
        if mois=="glob":
            mois,annee="TO","GL"

        try:
            chan=curseur.execute("SELECT Rank,Count,ID FROM perso{0}{1}{2}".format(tableauMois[mois],annee,interaction.user.id)).fetchall()
            if chan!=[]:
                for j in chan:
                    dictSalons.append({"ID":j["ID"],"Count":j["Count"],"RankIntern":j["Rank"],"Rank":0})
            curseur.close()
            connexion.close()
        except:
            pass

        try:
            freq=curseur.execute("SELECT Rank,Count,ID FROM perso{0}{1}{2}".format(tableauMois[mois],annee,interaction.user.id)).fetchall()
            if freq!=[]:
                for j in freq:
                    if j["ID"] not in dictFreq:
                        dictFreq[j["ID"]]=j["Count"]
                    else:
                        dictFreq[j["ID"]]+=j["Count"]
            curseur.close()
            connexion.close()
        except:
            pass

        try:
            emotes=curseur.execute("SELECT Rank,Count,ID FROM perso{0}{1}{2}".format(tableauMois[mois],annee,interaction.user.id)).fetchall()
            if emotes!=[]:
                for j in emotes:
                    if j["ID"] not in dictEmotes:
                        dictEmotes[j["ID"]]=j["Count"]
                    else:
                        dictEmotes[j["ID"]]+=j["Count"]
            curseur.close()
            connexion.close()
        except:
            pass

        if annee=="GL":
            mois,annee="glob",""
    
    listeFreq=list(map(lambda x:{"ID":x,"Count":dictFreq[x],"Rank":0},dictFreq))
    listeEmotes=list(map(lambda x:{"ID":x,"Count":dictEmotes[x],"Rank":0},dictEmotes))

    rankingClassic(dictMessages)
    rankingClassic(dictSalons)
    rankingClassic(listeEmotes)
    rankingClassic(dictVoc)
    rankingClassic(listeFreq)

    if mois=="glob":
        title="Récapitulatif général"
    elif mois=="to":
        title="Récapitulatif 20{0}".format(annee)
    else:
        title="Récapitulatif {0} 20{1}".format(mois,annee)

    embed=discord.Embed(title=title,color=0x3498db)
    embed.set_footer(text="OT!recap")
    embed=auteur(interaction.user.name,interaction.user.avatar,embed,"user")
    if dictMessages!=[]:
        descip=""
        stop=5 if len(dictMessages)>5 else len(dictMessages)
        for i in range(stop):
            descip+="{0}e : {1} - {2}\n".format(dictMessages[i]["Rank"],dictMessages[i]["Nom"],dictMessages[i]["Count"])
        embed.add_field(name="Serveurs les plus actifs - messages",value=descip,inline=True)
    if dictVoc!=[]:
        descip=""
        stop=5 if len(dictVoc)>5 else len(dictVoc)
        for i in range(stop):
            descip+="{0}e : {1} - {2}\n".format(dictVoc[i]["Rank"],dictVoc[i]["Nom"],tempsVoice(dictVoc[i]["Count"]))
        embed.add_field(name="Serveurs les plus actifs - vocal",value=descip,inline=True)
    if listeEmotes!=[]:
        descip=""
        stop=5 if len(listeEmotes)>5 else len(listeEmotes)
        for i in range(stop):
            descip+="{0}e : {1} - {2}\n".format(listeEmotes[i]["Rank"],nomsOptions("Emotes",listeEmotes[i]["ID"],None,bot),listeEmotes[i]["Count"])
        embed.add_field(name="Emotes les plus utilisées",value=descip,inline=True)
    if dictSalons!=[]:
        descip=""
        stop=5 if len(dictSalons)>5 else len(dictSalons)
        for i in range(stop):
            descip+="{0}e : <#{1}> - {2}\n".format(dictSalons[i]["Rank"],dictSalons[i]["ID"],dictSalons[i]["Count"])
        embed.add_field(name="Salons les plus utilisés",value=descip,inline=True)
    if listeFreq!=[]:
        descip=""
        stop=5 if len(listeFreq)>5 else len(listeFreq)
        for i in range(stop):
            descip+="{0}e : {1} - {2}\n".format(listeFreq[i]["Rank"],nomsOptions("Freq",listeFreq[i]["ID"],None,bot),listeFreq[i]["Count"])
        embed.add_field(name="Heures les plus actives",value=descip,inline=True)

    embed.add_field(name="Stats diverses",value="Messages envoyés : {0}\nTemps passé en vocal : {1}\nNombre de serveurs en commun : {2}\n[Invitez moi sur votre serveur](https://discord.com/oauth2/authorize?client_id=699728606493933650&permissions=120259472576&scope=bot)".format(dictAutre["Messages"],tempsVoice(dictAutre["Vocal"]),dictAutre["Serveurs"]))

    await interaction.response.send_message(embed=embed)
