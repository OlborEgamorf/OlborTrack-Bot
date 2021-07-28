from time import strftime
import asyncio
import discord
from Core.Fonctions.Embeds import createEmbed, embedAssert, exeErrorExcept
from Stats.SQL.ConnectSQL import connectSQL
from Stats.Tracker.Voice import endNight
from Stats.Rapports.exeRapports import autoRapport
from Geo.PhotoNASA import embedNasaPhoto
from Savezvous.exeSavezVous import autoSV


tableauMois={"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre","TO":"to","1":"janvier","2":"février","3":"mars","4":"avril","5":"mai","6":"juin","7":"juillet","8":"aout","9":"septembre","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","to":"TO","glob":"GL"}

async def addAuto(ctx,bot,args,guildOT):
    try:
        connexion,curseur=connectSQL(ctx.guild.id,"Guild","Guild",None,None)
        if ctx.invoked_with in ("add", "edit"):
            assert len(ctx.message.channel_mentions)!=0, "Vous devez me donner un salon valide !"
            assert args[0].lower() in ("jour","mois","annee","nasaphoto","savezvous"), "Vous devez me donner un nom de commande compatible !\nCommandes automatiques disponibles : jour, mois, annee, nasaphoto, savezvous"
            curseur.execute("UPDATE auto SET Active=True, Salon={0} WHERE Commande='{1}'".format(ctx.message.channel_mentions[0].id,args[0].lower()))
            embed=createEmbed("Commande automatique activée ou modifiée","Commande : {0}\nSalon : <#{1}>".format(args[0].lower(),ctx.message.channel_mentions[0].id),0x220cc9,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)
        elif ctx.invoked_with=="del":
            assert args[0].lower() in ("jour","mois","annee","nasaphoto","savezvous"), "Vous devez me donner un nom de commande compatible !"
            curseur.execute("UPDATE auto SET Active=False, Salon=0 WHERE Commande='{0}'".format(args[0].lower()))
            embed=createEmbed("Commande automatique supprimée","Commande : {0}".format(args[0].lower()),0x220cc9,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)
        else:
            embed=embedAuto(ctx,guildOT)
        connexion.commit()
        guildOT.getAuto()
    except AssertionError as er:
        embed=embedAssert(str(er))
    except:
        embed=await exeErrorExcept(ctx,bot,args)
    await ctx.send(embed=embed)

def embedAuto(ctx,guildOT):
    descip=""
    for i in guildOT.auto:
        if i["Active"]:
            descip+="{0} : <#{1}>\n".format(i["Commande"],i["Salon"])
        else:
            descip+="{0} : *désactivé*\n".format(i["Commande"])
    embedTable=createEmbed("Liste des commandes automatiques",descip,0x220cc9,ctx.invoked_with.lower(),ctx.guild)
    return embedTable

def archivesSave(guild,jour,mois,annee):
    connexion,curseur=connectSQL(guild,"Rapports","Stats","GL","")
    for i in ("Salons","Freq","Messages","Emojis","Reactions","Voice","Voicechan"):
        try:
            for z in ("Mois","Annee","Global"):
                if z=="Mois":
                    connexionSpe,curseurSpe=connectSQL(guild,i,"Stats",mois,annee)
                    table=curseurSpe.execute("SELECT * FROM {0}{1} WHERE Rank<=10 ORDER BY Rank ASC LIMIT 10".format(tableauMois[mois],annee)).fetchall()
                elif z=="Annee":
                    connexionSpe,curseurSpe=connectSQL(guild,i,"Stats","TO",annee)
                    table=curseurSpe.execute("SELECT * FROM to{0} WHERE Rank<=10 ORDER BY Rank ASC LIMIT 10".format(annee)).fetchall()
                else:
                    connexionSpe,curseurSpe=connectSQL(guild,i,"Stats","GL","")
                    table=curseurSpe.execute("SELECT * FROM glob WHERE Rank<=10 ORDER BY Rank ASC LIMIT 10").fetchall()
                many=[]
                for j in table:
                    many.append((table[i]["Rank"],table[i]["ID"],jour,mois,annee,int(annee+mois+jour),z,table[i]["Count"],table[i]["Evol"],i))
                curseur.executemany("INSERT INTO archives VALUES (?,?,?,?,?,?,?,?,?,?)",many)
        except:
            continue
    connexion.commit()

def checkSoloEmotes(guild,mois,annee):
    connexion,curseur=connectSQL(guild,"Emotes","Stats",mois,annee)
    for i in curseur.execute("SELECT * FROM {0}{1}".format(tableauMois[mois],annee)).fetchall():
        if curseur.execute("SELECT Count() AS Total FROM {0}{1}{2}".format(tableauMois[mois],annee,i["ID"])).fetchone()["Count"]==1:
            curseur.execute("DROP TABLE {0}{1}{2}".format(tableauMois[mois],annee,i["ID"]))
    connexion.commit()

    connexion,curseur=connectSQL(guild,"Reactions","Stats",mois,annee)
    for i in curseur.execute("SELECT * FROM {0}{1}".format(tableauMois[mois],annee)).fetchall():
        if curseur.execute("SELECT Count() AS Total FROM {0}{1}{2}".format(tableauMois[mois],annee,i["ID"])).fetchone()["Count"]==1:
            curseur.execute("DROP TABLE {0}{1}{2}".format(tableauMois[mois],annee,i["ID"]))
    connexion.commit()


async def boucleAuto(bot,dictGuilds):
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

        while heure!="00":
            await asyncio.sleep(30)
            heure=strftime("%H")

        for i in bot.guilds:
            try:
                archivesSave(i.id,jour,mois,annee)
            except:
                await bot.get_channel(706175527953760277).send("Sauvegarde archive échec : {0} / {1}".format(i.id,i.name))

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
                            await autoSV(j["Salon"],i,bot)
                        elif j["Commande"]=="nasaphoto":
                            await bot.get_channel(j["Salon"]).send(embed=await embedNasaPhoto())
                    except:
                        pass     

        await asyncio.sleep(80000)