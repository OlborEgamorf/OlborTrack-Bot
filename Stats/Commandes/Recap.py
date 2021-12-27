from time import strftime

import discord
from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.GetNom import nomsOptions
from Core.Fonctions.GetPeriod import getAnnee, getMois
from Core.Fonctions.RankingClassic import rankingClassic
from Core.Fonctions.TempsVoice import tempsVoice
from Stats.SQL.ConnectSQL import connectSQL

tableauMois={"01":"Janvier","02":"Février","03":"Mars","04":"Avril","05":"Mai","06":"Juin","07":"Juillet","08":"Aout","09":"Septembre","10":"Octobre","11":"Novembre","12":"Décembre","TO":"TO","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","glob":"GL","to":"TO"}

async def recapStats(ctx,bot):
    if len(ctx.args)==2 or ctx.args[2].lower() not in ("mois","annee"):
        try:
            mois,annee=getMois(ctx.args[2].lower()),getAnnee(ctx.args[3].lower())
        except:
            try:
                mois,annee="to",getAnnee(ctx.args[2].lower())
            except:
                mois,annee="glob",""
    elif ctx.args[2].lower()=="mois":
        mois,annee=tableauMois[strftime("%m")].lower(),strftime("%y")
    elif ctx.args[2].lower()=="annee":
        mois,annee="to",strftime("%y")
    
    dictMessages,dictSalons,dictEmotes,dictVoc,dictFreq=[],[],[],[],[]
    guilds=ctx.author.mutual_guilds
    dictAutre={"Messages":0,"Vocal":0,"Serveurs":len(guilds)}
    for i in guilds:
        try:
            connexion,curseur=connectSQL(i.id,"Messages","Stats",tableauMois[mois],annee)
            mess=curseur.execute("SELECT Rank,Count FROM {0}{1} WHERE ID={2}".format(mois,annee,ctx.author.id)).fetchone()
            if mess!=None:
                dictMessages.append({"ID":i.id,"Count":mess["Count"],"RankIntern":mess["Rank"],"Rank":0,"Nom":i.name})
                dictAutre["Messages"]+=mess["Count"]
            curseur.close()
            connexion.close()
        except:
            pass
        
        try:
            connexion,curseur=connectSQL(i.id,"Voice","Stats",tableauMois[mois],annee)
            voc=curseur.execute("SELECT Rank,Count FROM {0}{1} WHERE ID={2}".format(mois,annee,ctx.author.id)).fetchone()
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
            connexion,curseur=connectSQL(i.id,"Salons","Stats",tableauMois[mois],annee)
            chan=curseur.execute("SELECT Rank,Count,ID FROM perso{0}{1}{2}".format(tableauMois[mois],annee,ctx.author.id)).fetchall()
            if chan!=[]:
                for j in chan:
                    dictSalons.append({"ID":j["ID"],"Count":j["Count"],"RankIntern":j["Rank"],"Rank":0})
            curseur.close()
            connexion.close()
        except:
            pass

        try:
            connexion,curseur=connectSQL(i.id,"Freq","Stats",tableauMois[mois],annee)
            freq=curseur.execute("SELECT Rank,Count,ID FROM perso{0}{1}{2}".format(tableauMois[mois],annee,ctx.author.id)).fetchall()
            if freq!=[]:
                for j in freq:
                    dictFreq.append({"ID":j["ID"],"Count":j["Count"],"RankIntern":j["Rank"],"Rank":0})
            curseur.close()
            connexion.close()
        except:
            pass

        try:
            connexion,curseur=connectSQL(i.id,"Emotes","Stats",tableauMois[mois],annee)
            emotes=curseur.execute("SELECT Rank,Count,ID FROM perso{0}{1}{2}".format(tableauMois[mois],annee,ctx.author.id)).fetchall()
            if emotes!=[]:
                for j in emotes:
                    dictEmotes.append({"ID":j["ID"],"Count":j["Count"],"RankIntern":j["Rank"],"Rank":0})
            curseur.close()
            connexion.close()
        except:
            pass

        if annee=="GL":
            mois,annee="glob",""
            
    rankingClassic(dictMessages)
    rankingClassic(dictSalons)
    rankingClassic(dictEmotes)
    rankingClassic(dictVoc)
    rankingClassic(dictFreq)

    if mois=="glob":
        title="Récapitulatif général"
    elif mois=="to":
        title="Récapitulatif 20{0}".format(annee)
    else:
        title="Récapitulatif {0} 20{1}".format(mois,annee)

    embed=discord.Embed(title=title,color=0x3498db)
    embed.set_footer(text="OT!recap")
    embed=auteur(ctx.author.id,ctx.author.name,ctx.author.avatar,embed,"user")
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
    if dictEmotes!=[]:
        descip=""
        stop=5 if len(dictEmotes)>5 else len(dictEmotes)
        for i in range(stop):
            descip+="{0}e : {1} - {2}\n".format(dictEmotes[i]["Rank"],nomsOptions("Emotes",dictEmotes[i]["ID"],None,bot),dictEmotes[i]["Count"])
        embed.add_field(name="Emotes les plus utilisées",value=descip,inline=True)
    if dictSalons!=[]:
        descip=""
        stop=5 if len(dictSalons)>5 else len(dictSalons)
        for i in range(stop):
            descip+="{0}e : <#{1}> - {2}\n".format(dictSalons[i]["Rank"],dictSalons[i]["ID"],dictSalons[i]["Count"])
        embed.add_field(name="Salons les plus utilisés",value=descip,inline=True)
    if dictFreq!=[]:
        descip=""
        stop=5 if len(dictFreq)>5 else len(dictFreq)
        for i in range(stop):
            descip+="{0}e : {1} - {2}\n".format(dictFreq[i]["Rank"],nomsOptions("Freq",dictFreq[i]["ID"],None,bot),dictFreq[i]["Count"])
        embed.add_field(name="Heures les plus actives",value=descip,inline=True)

    embed.add_field(name="Stats diverses",value="Messages envoyés : {0}\nTemps passé en vocal : {1}\nNombre de serveurs en commun : {2}\n[Invitez moi sur votre serveur](https://discord.com/oauth2/authorize?client_id=699728606493933650&permissions=120259472576&scope=bot)".format(dictAutre["Messages"],tempsVoice(dictAutre["Vocal"]),dictAutre["Serveurs"]))

    await ctx.send(embed=embed)