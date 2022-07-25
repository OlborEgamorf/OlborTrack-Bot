from Core.Fonctions.Help3 import *
import discord

dictDescip={"home":{},"stats":dictStats,"polls":dictPoll,"jeux":dictJeux,"autre":dictAutre,"sv":dictSV,"outils":dictOutils,"admin":dictAdmin,"titres":dictTitres,"alertes":dictAlertes,"anniv":dictAnniv}

def embedHelp(option,guildOT,page,bot):
    dictColor={"home":0x6EC8FA,"stats":0x3498db,"polls":0xfc03d7,"jeux":0xad917b,"outils":0xf54269,"autre":0x6EC8FA,"sv":0x00ffd0,"admin":0x220cc9,"titres":0xf58d1d,"alertes":0xf54269,"anniv":0x11f738}

    dictLinks={"home":"https://cdn.discordapp.com/attachments/726034739550486618/870604901334536192/NEW.png","polls":"https://cdn.discordapp.com/attachments/726034739550486618/870604052315136050/poll.png","jeux":"https://cdn.discordapp.com/attachments/726034739550486618/870604061739732992/jeux.png","utile":"https://cdn.discordapp.com/attachments/726034739550486618/870604901334536192/NEW.png","autre":"https://cdn.discordapp.com/attachments/726034739550486618/870604901334536192/NEW.png","sv":"https://cdn.discordapp.com/attachments/726034739550486618/870604056203231252/sv.png","outils":"https://cdn.discordapp.com/attachments/726034739550486618/870604051069407272/outils.png","admin":"https://cdn.discordapp.com/attachments/726034739550486618/870604058883420170/admin.png","titres":"https://cdn.discordapp.com/attachments/726034739550486618/870604901334536192/NEW.png","alertes":"https://cdn.discordapp.com/attachments/726034739550486618/888141463421071420/alertes.png","anniv":"https://cdn.discordapp.com/attachments/726034739550486618/888141462066303056/anniv.png","stats":"https://media.discordapp.net/attachments/726034739550486618/870604054831714344/stats.png"}

    dictAuthor={"home":"Bienvenue sur la page d’aide de Olbor Track !","stats":"Aide - Statistiques","polls":"Aide - Sondages, giweaway et rappels","jeux":"Aide - Jeux","autre":"Aide - Autres commandes","sv":"Aide - Boite de connaissances","outils":"Aide - Outils","admin":"Aide - Commandes admin","titres":"Aide - Système de titres","alertes":"Aide - Alertes","anniv":"Aide - Anniversaires"}
    dictLen={"home":3,"stats":len(dictStats),"polls":len(dictPoll),"jeux":len(dictJeux),"autre":len(dictAutre),"sv":len(dictSV),"outils":len(dictOutils),"admin":len(dictAdmin),"titres":len(dictTitres),"alertes":len(dictAlertes),"anniv":len(dictAnniv)}

    dictDescipPlus={"home":{},"stats":dictPStats,"polls":dictPPoll,"jeux":dictPJeux,"autre":dictPAutre,"sv":dictPSV,"outils":dictPOutils,"admin":dictPAdmin,"titres":dictPTitres,"alertes":dictPAlertes,"anniv":dictPAnniv}
    dictDescipFields={"home":{},"stats":dictFStats,"polls":dictFPoll,"jeux":dictFJeux,"autre":dictFAutre,"sv":dictFSV,"outils":dictFOutils,"admin":dictFAdmin,"titres":dictFTitres,"alertes":dictFAlertes,"anniv":dictFAnniv}
    dictDescipTitres={"home":{},"stats":dictTStats,"polls":dictTPoll,"jeux":dictTJeux,"autre":dictTAutre,"sv":dictTSV,"outils":dictTOutils,"admin":dictTAdmin,"titres":dictTTitres,"alertes":dictTAlertes,"anniv":dictTAnniv}

    listeName=["<:OTHstats:859840446901649459> OT!help stats","<:OTHoutils:859840447126700083> OT!help outils","<:OTHjeux:859840446675419167> OT!help jeux","<:OTHpoll:859840447210848306> OT!help polls","<:OTHsv:859840446780145665> OT!help savezvous","<:OTHalertes:888140611469844510> OT!help alertes","<:OTHanniv:888140611750854697> OT!help anniv","<:OTHadmin:859840446984486972> OT!help admin","<:ot30:845649462918512671> OT!help autre","<:ot30:845649462918512671> OT!help serv","<:ot30:845649462918512671> OT!help titres"]
    listeValue=["Statistiques de l'activité de votre serveur ! Messages, temps en vocal, emotes, ...","Gérez vos outils : messages de bienvenue, commandes personnalisée, tableaux, ...","Questions de culture, Tortues et plus !","Sondages, giveaway et rappels !","Créez une boîte de connaissances commune !","Gérez vos alertes YouTube, Twitch et Twitter !","Activez les anniversaires sur votre serveur !","Toutes les commandes pour les administrateurs.","Autres commandes.","Les commandes personnalisées de votre serveur (s'il y en a)","Gestion des titres, badges et personnalisation !"]
    listeOptions=["stats","outils","jeux","polls","sv","alertes","anniv","admin","autre","serv","titres"]

    embedHelp=discord.Embed(color=dictColor[option])
    embedHelp.set_author(icon_url=dictLinks[option],name=dictAuthor[option])
    if option=="home":
        embedHelp.description="**Olbor Track Companion bientôt disponible :** plus d'info avec OT!companion !\n\nEffectuez une de ces commandes pour avoir plus d'infos sur mes commandes !\n**Mon préfixe est OT!**\nVous pouvez aussi faire **OT!help [nom d'une commande]** pour avoir directement les infos d'une commande.\n[Invitez moi !](https://discord.com/oauth2/authorize?client_id=699728606493933650&permissions=120259472576&scope=bot) - [Faites une donation !](https://paypal.me/OlborTrack) - [Serveur de test](https://discord.com/invite/kMQz7nF) - [Twitter](https://twitter.com/olbortrack) - [Instagram](https://www.instagram.com/OlborTrack/)"
        if page==1 or page==2:
            if guildOT.mcmd!=None:
                dictPerms={"Stats":0,"Sondages":3,"Outils":1,"Savezvous":4,"Jeux":2}
                nb=0
                for i in guildOT.mcmd:
                    if i["Statut"]==False and i["Module"] in dictPerms:
                        del listeName[dictPerms[i["Module"]]-nb]
                        del listeValue[dictPerms[i["Module"]]-nb]
                        del listeOptions[dictPerms[i["Module"]]-nb]
                        nb+=1
            for i in range(len(listeName)):
                if page==1:
                    embedHelp.add_field(name=listeName[i], value=listeValue[i], inline=True)
                else:
                    descip=""
                    if listeOptions[i]!="serv":
                        for j in dictDescip[listeOptions[i]]:
                            for h in dictDescip[listeOptions[i]][j]:
                                descip+="/{0}, ".format(h)
                        embedHelp.add_field(name=listeName[i], value="`"+descip[0:-2]+"`", inline=False)
        else:
            embedHelp.set_image(url="https://cdn.discordapp.com/attachments/702208752035692654/975873681525993522/OTC.png")
            embedHelp.description="Merci d'avoir ajouté Olbor Track sur votre serveur ! Voici une petite liste de gens qui ont aidé à ce que le projet perdure :\nDonateurs : Alfashield, NatG34, Zey\nContributeurs : Tonton Mathias, Zey, ZAGUE, Lexadi, Souaip\nRéalisation badges : Shimi\n\n***Vous savez pas quoi faire ?***\nVous avez déjà joué à la courses de tortues ? Commencez dès maintenant avec **OT!tortues** !\nEnvie de vous battre sur une partie de Puissance 4 ? Lancez un **OT!p4** !\nVous voulez savoir qui passe le plus de temps en vocal ? Faites **OT!vocal** !\nA votre avis, qui est le plus gros spammeur de votre serveur ? Découvrez le avec **OT!messages** !\nApprenez des choses aux autres avec **OT!savezvous add** !\n\n***Découvrez toutes les informations sur la Bêta de Olbor Track Companion : OT!companion***"
    else:
        descip=""
        for i in dictDescip[option][page]:
            try:
                com=bot.tree._global_commands[i]
                if type(com)==discord.app_commands.commands.Command:
                    descip+="**/{0}** : {1}\n".format(com.name,com.description)
                else:
                    for j in com.commands:
                        descip+="**/{0} {1}** : {2}\n".format(com.name,j.name,j.description)
            except:
                pass
        try:
            embedHelp.description=dictDescipPlus[option][page]+"\n"+descip
        except:
            embedHelp.description=descip
        for i in dictDescipFields[option][page]:
            embedHelp.add_field(name=dictFields[i]["name"],value=dictFields[i]["value"],inline=True)
        if dictDescip[option][page]==[]:
            descip=""
            for i in range(1,len(dictDescipTitres[option])+1):
                descip+="*Page {0} :* {1}\n".format(i,dictDescipTitres[option][i])
            if descip!="":
                embedHelp.add_field(name="Sommaire",value=descip)
        embedHelp.title=dictDescipTitres[option][page]

    embedHelp.set_footer(text=("Page {0}/{1}".format(page,dictLen[option])))
    
    if option=="outils":
        if page==4:
            embedHelp.set_image(url="https://media.discordapp.net/attachments/726034739550486618/872435056533184512/sb.gif")
        elif page==7:
            embedHelp.set_image(url="https://media.discordapp.net/attachments/726034739550486618/872776089678778399/cmd.gif")

    return embedHelp, dictLen[option]
