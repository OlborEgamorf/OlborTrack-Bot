import discord
from Core.Fonctions.Help3 import *
from Core.Fonctions.AuteurIcon import auteur
from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.setMaxPage import setPage
from Core.Fonctions.Embeds import embedAssert, exeErrorExcept, sendEmbed
from Outils.CustomCMD.ListeCMD import commandeCMD

dictDescip={"home":{},"stats":dictStats,"polls":dictPoll,"jeux":dictJeux,"utile":dictUtile,"autre":dictAutre,"sv":dictSV,"outils":dictOutils,"wiki":dictWiki,"mal":dictMAL,"admin":dictAdmin,"spotify":dictSpotify,"geo":dictGeo,"titres":dictTitres}

async def commandeHelp(ctx,turn,react,ligne,bot,guildOT):
    connexionCMD,curseurCMD=connectSQL(guildOT.id,"Commandes","Guild",None,None)
    if not react:
        page=1
        if len(ctx.args)==2:
            option="home"
        else:
            if ctx.args[2].lower()=="serv":
                await commandeCMD(ctx,None,False,None)
                return
            elif ctx.args[2].lower() in ("polls","stats","jeux","autre","sv","outils","admin","titres","interact"):
                option=ctx.args[2].lower()
            else:
                option="home"
                if ctx.args[2].lower() in ("messganim","saloganim","emotganim","reacganim","motsganim","freqganim","voicganim","vchaganim"):
                    option,page="stats",13
                elif ctx.args[2].lower()=="getdata":
                    option,page="admin",4
                else:
                    for i in dictDescip:
                        for j in dictDescip[i]:
                            for h in dictDescip[i][j]:
                                if h==ctx.args[2].lower():
                                    option,page=i,j
                                    break
        curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'help','{2}','None','None','None','None',{3},99,'countDesc',False)".format(ctx.message.id,ctx.author.id,option,page))
        ligne=curseurCMD.execute("SELECT * FROM commandes WHERE MessageID={0}".format(ctx.message.id)).fetchone()
    else:
        option=ligne["Option"]

    page=setPage(ligne["Page"],ligne["PageMax"],turn)
    embed,pagemax=embedHelp30(option,guildOT,page,bot)
    message=await sendEmbed(ctx,embed,react,False,curseurCMD,connexionCMD,page,pagemax)

def embedHelp30(option,guildOT,page,bot):
    dictColor={"home":0x6EC8FA,"stats":0x3498db,"polls":0xfc03d7,"jeux":0xad917b,"outils":0xf54269,"autre":0x6EC8FA,"sv":0x00ffd0,"admin":0x220cc9,"titres":0xf58d1d,"interact":0xfcfc03}

    dictLinks={"home":"https://cdn.discordapp.com/attachments/726034739550486618/870604901334536192/NEW.png","polls":"https://cdn.discordapp.com/attachments/726034739550486618/870604052315136050/poll.png","jeux":"https://cdn.discordapp.com/attachments/726034739550486618/870604061739732992/jeux.png","utile":"https://cdn.discordapp.com/attachments/726034739550486618/870604901334536192/NEW.png","autre":"https://cdn.discordapp.com/attachments/726034739550486618/870604901334536192/NEW.png","sv":"https://cdn.discordapp.com/attachments/726034739550486618/870604056203231252/sv.png","outils":"https://cdn.discordapp.com/attachments/726034739550486618/870604051069407272/outils.png","admin":"https://cdn.discordapp.com/attachments/726034739550486618/870604058883420170/admin.png","titres":"https://cdn.discordapp.com/attachments/726034739550486618/870604901334536192/NEW.png","interact":"https://cdn.discordapp.com/attachments/726034739550486618/885879620157730886/globe.png"}

    dictAuthor={"home":"Bienvenue sur la page d’aide de Olbor Track !","stats":"Aide - Statistiques","polls":"Aide - Sondages, giweaway et rappels","jeux":"Aide - Jeux","autre":"Aide - Autres commandes","sv":"Aide - Boite de connaissances","outils":"Aide - Outils","admin":"Aide - Commandes admin","titres":"Aide - Système de titres","interact":"Aide - Interactions"}
    dictLen={"home":3,"stats":len(dictStats),"polls":len(dictPoll),"jeux":len(dictJeux),"autre":len(dictAutre),"sv":len(dictSV),"outils":len(dictOutils),"admin":len(dictAdmin),"titres":len(dictTitres),"interact":len(dictInteract)}

    dictDescipPlus={"home":{},"stats":dictPStats,"polls":dictPPoll,"jeux":dictPJeux,"autre":dictPAutre,"sv":dictPSV,"outils":dictPOutils,"admin":dictPAdmin,"titres":dictPTitres,"interact":dictPInteract}
    dictDescipFields={"home":{},"stats":dictFStats,"polls":dictFPoll,"jeux":dictFJeux,"autre":dictFAutre,"sv":dictFSV,"outils":dictFOutils,"admin":dictFAdmin,"titres":dictFTitres}
    dictDescipTitres={"home":{},"stats":dictTStats,"polls":dictTPoll,"jeux":dictTJeux,"autre":dictTAutre,"sv":dictTSV,"outils":dictTOutils,"admin":dictTAdmin,"titres":dictTTitres}

    listeName=["<:OTHstats:859840446901649459> OT!help stats","<:OTHoutils:859840447126700083> OT!help outils","<:OTHjeux:859840446675419167> OT!help jeux","<:OTHpoll:859840447210848306> OT!help polls","<:OTHsv:859840446780145665> OT!help savezvous","<:OTHadmin:859840446984486972> OT!help admin","<:ot30:845649462918512671> OT!help autre","<:OTHinteract:885883292593827842> OT!help interact","<:ot30:845649462918512671> OT!help serv","<:ot30:845649462918512671> OT!help titres"]
    listeValue=["Statistiques de l'activité de votre serveur !","Gérez vos outils !","Questions de culture, Tortues et plus !","Sondages, giveaway et rappels !","Créez une boîte de connaissances commune !","Les intéreactions avec d'autres sites","Toutes les commandes pour les administrateurs.","Autres commandes.","Les commandes personnalisées de votre serveur (s'il y en a)","Gestion des titres !"]
    listeOptions=["stats","jeux","outils","polls","sv","interact","admin","autre","serv","titres"]

    embedHelp=discord.Embed(color=dictColor[option])
    embedHelp.set_author(icon_url=dictLinks[option],name=dictAuthor[option])
    if option=="home":
        embedHelp.description="Effectuez une de ces commandes pour avoir plus d'infos sur mes commandes !\n**Mon préfixe est OT!**\nVous pouvez aussi faire **OT!help [nom d'une commande]** pour avoir directement les infos d'une commande.\n[Invitez moi !](https://discord.com/oauth2/authorize?client_id=699728606493933650&permissions=120259472576&scope=bot) - [Faites une donation !](https://paypal.me/OlborTrack) - [Serveur de test](https://discord.com/invite/kMQz7nF) - [Twitter](https://twitter.com/olbortrack) - [Instagram](https://www.instagram.com/OlborTrack/)"
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
                                descip+="{0}, ".format(h)
                        embedHelp.add_field(name=listeName[i], value="`"+descip[0:-2]+"`", inline=False)
        else:
            embedHelp.set_image(url="https://cdn.discordapp.com/attachments/726034739550486618/870617284920619058/unknown.png")
            #embedHelp.description="**Commandes actuellement en bêta :**\n\n**Jeux Cross-Serveurs** :\nVous pouvez désormais jouer avec des personnes hors de votre serveur !\n- OT!tortuescross\n- OT!tortuesduocross\n- OT!p4cross\n- OT!trivialversuscross\n- OT!trivialbrcross\n- OT!trivialpartycross\n\n**Titres** :\nRetour du système de titres !\nVoir OT!help titres\n\n**Alertes YouTube** :\nRecevez un message quand votre créateur favori poste une vidéo !\nVoir OT!help youtube\n\n**Salons vocaux éphémères**\nCréez des hubs de salons éphémères, qui disparaissent quand plus personne n'est connecté !\nVoir OT!help voiceephem"
    else:
        descip=""
        for i in dictDescip[option][page]:
            com=bot.get_command(i)
            if com!=None:
                if com.usage!=None:
                    descip+="**OT!{0}** *{1}* : {2}\n".format(com.qualified_name,com.usage,com.help)
                else:
                    descip+="**OT!{0}** : {1}\n".format(com.qualified_name,com.help)
        try:
            embedHelp.description=dictDescipPlus[option][page]+"\n"+descip
        except:
            embedHelp.description=descip
        for i in dictDescipFields[option][page]:
            embedHelp.add_field(name=dictFields[i]["name"],value=dictFields[i]["value"],inline=True)
        embedHelp.title=dictDescipTitres[option][page]
    embedHelp.set_footer(text=("Page {0}/{1}".format(page,dictLen[option])))
    
    if option=="outils":
        if page==2:
            embedHelp.set_image(url="https://media.discordapp.net/attachments/726034739550486618/872435056533184512/sb.gif")
        elif page==3:
            embedHelp.set_image(url="https://media.discordapp.net/attachments/726034739550486618/872776089678778399/cmd.gif")

    return embedHelp, dictLen[option]