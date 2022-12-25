import asyncio
from time import strftime

from Autre.Events import autoEvents
from Autre.PhotoNASA import embedNasaPhoto
from Core.Fonctions.Embeds import createEmbed
from Savezvous.exeSavezVous import showSV
from Stats.Rapports.exeRapports import autoRapport
from Stats.SQL.ConnectSQL import connectSQL
from Stats.Tracker.Voice import endNight
from Titres.Auto import (annualyBadges, annualyTitles,
                         monthlyBadges, monthlyTitles)
from Titres.Outils import setMarketPlace

from Outils.Anniversaires.Auto import autoAnniv
from Outils.DynamicPP.Rotation import rotation

tableauMois={"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre","TO":"to","1":"janvier","2":"février","3":"mars","4":"avril","5":"mai","6":"juin","7":"juillet","8":"aout","9":"septembre","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","to":"TO","glob":"GL"}

def embedAuto(ctx,guildOT):
    descip=""
    for i in guildOT.auto:
        if i["Active"]:
            descip+="{0} : <#{1}>\n".format(i["Commande"],i["Salon"])
        else:
            descip+="{0} : *désactivé*\n".format(i["Commande"])
    embedTable=createEmbed("Liste des commandes automatiques",descip,0x220cc9,ctx.invoked_with.lower(),ctx.guild)
    return embedTable

def checkSoloEmotes(guild,mois,annee):
    connexion,curseur=connectSQL(guild)
    for i in curseur.execute("SELECT * FROM {0}{1}".format(tableauMois[mois],annee)).fetchall():
        if curseur.execute("SELECT Count() AS Total FROM {0}{1}{2}".format(tableauMois[mois],annee,i["ID"])).fetchone()["Count"]==1:
            curseur.execute("DROP TABLE {0}{1}{2}".format(tableauMois[mois],annee,i["ID"]))
    connexion.commit()

    connexion,curseur=connectSQL(guild)
    for i in curseur.execute("SELECT * FROM {0}{1}".format(tableauMois[mois],annee)).fetchall():
        if curseur.execute("SELECT Count() AS Total FROM {0}{1}{2}".format(tableauMois[mois],annee,i["ID"])).fetchone()["Count"]==1:
            curseur.execute("DROP TABLE {0}{1}{2}".format(tableauMois[mois],annee,i["ID"]))
    connexion.commit()

async def boucleAutoCMD(bot,dictGuilds):
    while True:
        minute,heure=strftime("%M"),strftime("%H")
        jour,mois,annee=strftime("%d"),strftime("%m"),strftime("%y")
        while minute!="00":
            await asyncio.sleep(60)
            minute=strftime("%M")

        heure=strftime("%H")
        while heure!="00":
            await asyncio.sleep(3600)
            heure=strftime("%H")
        
        if mois!=strftime("%m"):
            await monthlyTitles(mois,annee,bot)
            await monthlyBadges(mois,annee)
        if annee!=strftime("%y"):
            await annualyTitles(annee,bot)
            await annualyBadges(annee)
        
        setMarketPlace()

        for i in bot.guilds:
            
            if dictGuilds[i.id].dynicon!=None:
                await rotation(i,dictGuilds[i.id].dynicon)
            if dictGuilds[i.id].auto==None:
                continue

            for j in dictGuilds[i.id].auto:
                if j["Active"]==True:
                    try:
                        if j["Commande"]=="jour":
                            if strftime("%d")!=jour:
                                await autoRapport(i,j["Salon"],dictGuilds[i.id],bot,"jour",(jour,mois,annee))
                        elif j["Commande"]=="mois":
                            if strftime("%m")!=mois:
                                await autoRapport(i,j["Salon"],dictGuilds[i.id],bot,"mois",(mois,annee))
                        elif j["Commande"]=="annee":
                            if strftime("%y")!=annee:
                                await autoRapport(i,j["Salon"],dictGuilds[i.id],bot,"annee",(annee))
                        elif j["Commande"]=="savezvous":
                            await bot.get_channel(j["Salon"]).send(embed=showSV(i,bot))
                        elif j["Commande"]=="nasaphoto":
                            await bot.get_channel(j["Salon"]).send(embed=await embedNasaPhoto())
                        elif j["Commande"]=="events":
                            await autoEvents(bot,j["Salon"],dictGuilds[i.id].id)
                    except:
                        pass     
        await autoAnniv(bot,dictGuilds,int(strftime("%d")),strftime("%m"))
        await asyncio.sleep(80000)

async def boucleAutoStats(bot,dictGuilds):
    while True:
        minute,heure=strftime("%M"),strftime("%H")
        jour,mois,annee=strftime("%d"),strftime("%m"),strftime("%y")
        while minute!="59":
            await asyncio.sleep(60)
            minute=strftime("%M")

        heure=strftime("%H")
        while heure!="23":
            await asyncio.sleep(3600)
            heure=strftime("%H")

        await endNight(bot,dictGuilds)
            
        await asyncio.sleep(80000)
