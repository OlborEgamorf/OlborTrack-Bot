### PAS ENCORE TERMINE, ASSIGNE A AUCUNE COMMANDE

import discord
from Core.Fonctions.Help3 import *
from Core.Fonctions.AuteurIcon import auteur

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

def embedHelp30(option,guildOT,page,bot):
    dictLinks={"home":"https://media.discordapp.net/attachments/726034739550486618/768453640943042580/logoBldsqdeuddf.png","polls":"https://cdn.discordapp.com/attachments/726034739550486618/736551739473264640/helppoll.png","jeux":"https://cdn.discordapp.com/attachments/726034739550486618/736551738282213397/helpp4.png","utile":"https://cdn.discordapp.com/attachments/726034739550486618/736551744804225093/helputile.png","autre":"https://cdn.discordapp.com/attachments/726034739550486618/736551742937759914/helptrivia.png","sv":"https://cdn.discordapp.com/attachments/726034739550486618/736551741897572362/helpsv.png","outils":"https://media.discordapp.net/attachments/726034739550486618/750659474460770314/helptableaux.png","wiki":"https://media.discordapp.net/attachments/726034739550486618/757641659285635142/Wikipedia-logo-v2.png","mal":"https://media.discordapp.net/attachments/726034739550486618/756234989539950603/helpMAL.png","admin":"https://cdn.discordapp.com/attachments/726034739550486618/736551737187631144/helpadmin.png","spotify":"https://media.discordapp.net/attachments/726034739550486618/763482063319203950/Spotify_Icon_RGB_Green.png?width=676&height=676","stats":"https://media.discordapp.net/attachments/726034739550486618/736551740614246450/helpstats.png","geo":"https://media.discordapp.net/attachments/726034739550486618/769615020568608848/1f30d.png"}
    dictAuthor={"home":"Bienvenue sur la page d’aide de Olbor Track !","stats":"Aide - Statistiques","polls":"Aide - Sondages, giweaway et rappels","jeux":"Aide - Jeux","utile":"Aide - Commandes utiles","autre":"Aide - Autres commandes","sv":"Aide - Boite de connaissances","outils":"Aide - Outils","wiki":"Aide - Wikipedia","mal":"Aide - MyAnimeList","admin":"Aide - Commandes admin","spotify":"Aide - Spotify","geo":"Aide - Géographie et Espace"}
    dictLen={"home":3,"stats":len(dictStats),"polls":len(dictPoll),"jeux":len(dictJeux),"utile":len(dictUtile),"autre":len(dictAutre),"sv":len(dictSV),"tab":len(dictOutils),"wiki":len(dictWiki),"mal":len(dictMAL),"admin":len(dictAdmin),"spotify":len(dictSpotify),"geo":len(dictGeo)}

    dictDescip={"home":{},"stats":dictStats,"polls":dictPoll,"jeux":dictJeux,"utile":dictUtile,"autre":dictAutre,"sv":dictSV,"outils":dictOutils,"wiki":dictWiki,"mal":dictMAL,"admin":dictAdmin,"spotify":dictSpotify,"geo":dictGeo}
    dictDescipPlus={"home":{},"stats":dictPStats,"polls":dictPPoll,"jeux":dictPJeux,"utile":dictPUtile,"autre":dictPAutre,"sv":dictPSV,"outils":dictPOutils,"wiki":dictPWiki,"mal":dictPMAL,"admin":dictPAdmin,"spotify":dictPSpotify,"geo":dictPGeo}
    dictDescipFields={"home":{},"stats":dictFStats,"polls":dictFPoll,"jeux":dictFJeux,"utile":dictFUtile,"autre":dictFAutre,"sv":dictFSV,"outils":dictFOutils,"wiki":dictFWiki,"mal":dictFMAL,"admin":dictFAdmin,"spotify":dictFSpotify,"geo":dictFGeo}

    listeName=["<:OTHstats:859840446901649459> OT!help stats","<:OTHjeux:859840446675419167> OT!help jeux","<:OTHoutils:859840447126700083> OT!help outils","<:OTHpoll:859840447210848306> OT!help poll","<:OTHsv:859840446780145665> OT!help savezvous","<:ot30:845649462918512671> OT!help utile","<:OTHmal:859840447367348284> OT!help mal","<:OTHwiki:859840446800592937> OT!help wiki","<:OTHspotify:859840447048712201> OT!help spotify","<:OTHgeo:859840447073878036> OT!help geo","<:OTHadmin:859840446984486972> OT!help admin","<:ot30:845649462918512671> OT!help autre"]
    listeValue=["Statistiques de l'activité de votre serveur !","Gérez vos outils !","Questions de culture, Tortues et plus !","Sondages, giveaway et rappels !","Créez une boîte de connaissances commune !","Les commandes utilitaires.","Intéractions avec MyAnimeList !","Intéractions avec Wikipédia !","Intéractions avec Spotify !","Géographie et espace !","Toutes les commandes pour les administrateurs.","Autres commandes."]
    listeOptions=["stats","jeux","outils","polls","sv","utile","mal","wiki","spotify","geo","admin","autre"]

    embedHelp=discord.Embed(color=0x6EC8FA)
    embedHelp.set_author(icon_url=dictLinks[option],name=dictAuthor[option])
    if option=="home":
        embedHelp.description="Effectuez une de ces commandes pour avoir plus d'infos sur mes commandes !\n**Mon préfixe est OT!**"
        if guildOT!=None:
            dictPerms={"Stats":0,"Sondages":1,"Outils":2,"Savezvous":3,"Jeux":4,"MAL":7,"Wiki":8,"Spotify":9,"Geo":10}
            nb=0
            for i in guildOT.mcmd:
                if i["Statut"]==False:
                    del listeName[dictPerms[i["Module"]]-nb]
                    del listeValue[dictPerms[i["Module"]]-nb]
                    del listeOptions[dictPerms[i["Module"]]-nb]
                    nb+=1
        for i in range(len(listeName)):
            if page==1:
                embedHelp.add_field(name=listeName[i], value=listeValue[i], inline=True)
            else:
                descip=""
                for j in dictDescip[listeOptions[i]]:
                    for h in dictDescip[listeOptions[i]][j]:
                        descip+="{0}, ".format(h)
                embedHelp.add_field(name=listeName[i], value="`"+descip[0:-2]+"`", inline=False)
    else:
        descip=""
        for i in dictDescip[option][page]:
            com=bot.get_command(i)
            if com!=None:
                descip+="**OT!{0}** {1} : {2}\n".format(com.qualified_name,com.usage,com.help)
        try:
            embedHelp.description=dictDescipPlus[option][page]+"\n"+descip
        except:
            embedHelp.description=descip
        for i in dictDescipFields[option][page]:
            embedHelp.add_field(name=dictFields[i]["name"],value=dictFields[i]["value"],inline=True)
    embedHelp.set_footer(text=("Page {0}/{1}"))
    return embedHelp