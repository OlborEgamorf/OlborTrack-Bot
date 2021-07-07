### PAS ENCORE TERMINE, ASSIGNE A AUCUNE COMMANDE

import discord
from Core.Fonctions.Embeds3 import embedHelp2VI
from Core.Fonctions.Help3 import *
from Code.Fonctions.Embeds import tablesEmbed
from Core.Fonctions.EcritureRecherche3 import rechercheHelp
from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.Embeds import addReact

async def exeHelp(ctx,bot,args):
    if ctx.message.channel.type==discord.ChannelType.private:
        guild=None
    else:
        guild=ctx.guild.id
    if len(args)==0:
        embedH=embedHelp2VI(0,"HE",guild)
    elif args[0]=="serv" and ctx.guild!=None:
        embedH=tablesEmbed(ctx.guild.id,rechercheHelp(ctx.guild.id)[0],0,ctx.guild.id,"VC",0,0xfcfc03,True)
        embedH=auteur(ctx.guild.id,ctx.guild.name,ctx.guild.icon,embedH,"guild")
    else:
        dictArgs={"stats":"HS","statistiques":"HS","ranks":"HS","poll":"HP","polls":"HP","sondage":"HP","sondages":"HP","p4":"H4","puissance4":"H4","puissance":"H4","servcommand":"HC","custom":"HC","utile":"HU","utiles":"HU","autre":"HO","autres":"HO","sv":"HV","savezvous":"HV","tab":"HT","tableau":"HT","tableaux":"HT","starboard":"HT","outils":"HT","rapports":"HT","wiki":"HW","wikipedia":"HW","mal":"HM","myanimelist":"HM","anime":"HM","admin":"HA","special":"HA","spotify":"HY","spo":"HY","music":"HY","geo":"HG","nasa":"HG","fun":"H4","jeu":"H4","jeux":"H4","trivial":"H4"}
        try:
            embedH=embedHelp2VI(0,dictArgs[args[0].lower()],guild)
        except:
            embedH=embedHelp2VI(0,"HE",guild)
    message=await ctx.send(embed=embedH)
    await addReact(message,False)
    return

def embedHelp30(mode):
    dictOption={"HE":"home","HS":"stats","HP":"polls","H4":"p4","HC":"custom","HU":"utile","HO":"autre","HV":"sv","HT":"tab","HW":"wiki","HM":"mal","HA":"admin","HY":"spotify","HG":"geo"}
    option=dictOption[mode]
    dictLinks={"home":"https://media.discordapp.net/attachments/726034739550486618/768453640943042580/logoBldsqdeuddf.png","polls":"https://cdn.discordapp.com/attachments/726034739550486618/736551739473264640/helppoll.png","p4":"https://cdn.discordapp.com/attachments/726034739550486618/736551738282213397/helpp4.png","custom":"https://cdn.discordapp.com/attachments/726034739550486618/736551744804225093/helputile.png","utile":"https://cdn.discordapp.com/attachments/726034739550486618/736551744804225093/helputile.png","autre":"https://cdn.discordapp.com/attachments/726034739550486618/736551742937759914/helptrivia.png","sv":"https://cdn.discordapp.com/attachments/726034739550486618/736551741897572362/helpsv.png","tab":"https://media.discordapp.net/attachments/726034739550486618/750659474460770314/helptableaux.png","wiki":"https://media.discordapp.net/attachments/726034739550486618/757641659285635142/Wikipedia-logo-v2.png","mal":"https://media.discordapp.net/attachments/726034739550486618/756234989539950603/helpMAL.png","admin":"https://cdn.discordapp.com/attachments/726034739550486618/736551737187631144/helpadmin.png","spotify":"https://media.discordapp.net/attachments/726034739550486618/763482063319203950/Spotify_Icon_RGB_Green.png?width=676&height=676","stats":"https://media.discordapp.net/attachments/726034739550486618/736551740614246450/helpstats.png","geo":"https://media.discordapp.net/attachments/726034739550486618/769615020568608848/1f30d.png"}
    dictAuthor={"home":"Bienvenue sur la page d’aide de Olbor Track !","stats":"Aide - Statistiques","polls":"Aide - Sondages, giweaway et rappels","p4":"Aide - Jeux","custom":"Aide - Commandes personnalisées","utile":"Aide - Commandes utiles","autre":"Aide - Autres commandes","sv":"Aide - Boite de connaissances","tab":"Aide - Outils","wiki":"Aide - Wikipedia","mal":"Aide - MyAnimeList","admin":"Aide - Commandes admin","spotify":"Aide - Spotify","geo":"Aide - Géographie et Espace"}
    dictLen={"home":len(dictHome),"stats":len(dictStats),"polls":len(dictPoll),"p4":len(dictP4),"custom":len(dictCustom),"utile":len(dictUtile),"autre":len(dictAutre),"sv":len(dictSV),"tab":len(dictTab),"wiki":len(dictWiki),"mal":len(dictMAL),"admin":len(dictAdmin),"spotify":len(dictSpotify),"geo":len(dictGeo)}
    dictDescip={"home":dictHome,"stats":dictStats,"polls":dictPoll,"p4":dictP4,"custom":dictCustom,"utile":dictUtile,"autre":dictAutre,"sv":dictSV,"tab":dictTab,"wiki":dictWiki,"mal":dictMAL,"admin":dictAdmin,"spotify":dictSpotify,"geo":dictGeo}
    listeName=["<:OTHstats:859840446901649459> OT!help stats","<:OTHpoll:859840447210848306> OT!help poll","<:OTHcustom:859840446900207646> OT!help custom","<:OTHsv:859840446780145665> OT!help savezvous","<:OTHjeux:859840446675419167> OT!help jeux","<:ot30:845649462918512671> OT!help utile","<:OTHoutils:859840447126700083> OT!help outils","<:OTHmal:859840447367348284> OT!help mal","<:OTHwiki:859840446800592937> OT!help wiki","<:OTHspotify:859840447048712201> OT!help spotify","<:OTHgeo:859840447073878036> OT!help geo","<:OTHadmin:859840446984486972> OT!help admin","<:ot30:845649462918512671> OT!help autre"]
    listeValue=["Statistiques de l'activité de votre serveur !","Sondages, giveaway et rappels !","Créez vos commandes personnalisées !","Créez une boîte de connaissances commune !","Questions de culture, Bataille Navale et plus !","Les commandes utilitaires.","Gérez vos outils !","Intéractions avec MyAnimeList !","Intéractions avec Wikipédia !","Intéractions avec Spotify !","Géographie et espace !","Toutes les commandes pour les administrateurs.","Autres commandes."]
    listeCMDs=["jour, mois, annee, global, random, count, perso, compare, messages, messperiods, messevol, messjours, messroles, voice, voicperiods, voicevol, voicjours, voicroles, mots, motsperiods, motsevol, motsroles, salons, saloserv, saloperiods, saloevol, saloperso, saloroles, voicechans, vchaserv, vchaperiods, vchaevol, vchaperso, vcharoles, freq, freqserv, freqperiods, freqevol, freqperso, freqroles, emotes, emotserv, emotperiods, emotevol, emotperso, emotroles, reactions, reacserv, reacperiods, reacevol, reacperso, reacroles, divers, diveserv, diveperiods, diveperso, diveroles, mentions, mentperiods, mentperso, moyheure, moyjour, moymois, moyannee", "poll, polltime, giveaway, gareroll, reminder", "help serv, servcommand","savezvous, savezvous add, savezvous delete, savezvous list, savezvous modo", "trivial, trivialbr, trivialversus, trivialparty, trivialstreak, trivialperso, trivialrank, p4, p4 rank, p4 histo, p4 mondial, ", "help, support, feedback about, invite, servcount, test, hideme, blindme", "tableau, auto", "malsearch, maluser, mallist, malcompare", "wikipedia, events, wikiqotd, wikiquote", "spoartiste, spoalbum, spotitre, spoplaylist, spopodcast", "iss, geosearch, issmembers, meteomars, nasaphoto", "getdata, modulestat, modulecmd, hide, blind, mute, zip, wikinsfw", "dice, roulette, snipe, avatar, say", "zeynah"]
    embedHelp=discord.Embed(color=0x6EC8FA)
    embedHelp.set_author(icon_url=dictLinks[option],name=dictAuthor[option])
    if option=="home":
        if page==1 or page==2:
            embedHelp.description="Effectuez une de ces commandes pour avoir plus d'infos sur mes commandes !"
            if guild!=None:
                dictPerms={"Stats":0,"Sondages":1,"Custom":2,"Savezvous":3,"Jeux":4,"MAL":7,"Wiki":8,"Spotify":9,"Geo":10}
                tablePerms=rechercheCsv("permscmd",guild,0,0,0,0)[0]
                nb=0
                for i in tablePerms:
                    if i["Statut"]=="False":
                        del listeName[dictPerms[i["Module"]]-nb]
                        del listeValue[dictPerms[i["Module"]]-nb]
                        del listeCMDs[dictPerms[i["Module"]]-nb]
                        nb+=1
            for i in range(len(listeName)):
                if page==1:
                    embedHelp.add_field(name=listeName[i], value=listeValue[i], inline=True)
                else:
                    embedHelp.add_field(name=listeName[i], value="`"+listeCMDs[i]+"`", inline=False)
        else:
            embedHelp.description=dictHome[page]
    else:
        embedHelp.description=dictDescip[option][page]
    embedHelp.set_footer(text=("Page "+str(page+1)+" / "+str(dictLen[option])+" - "+mode+" | OT!help"))
    return embedHelp