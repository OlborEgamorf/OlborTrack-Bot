from Stats.Rapports.Pagemax import pagemaxHomeJour, pagemaxSpeJour, pagemaxSpeMois 
from Stats.Rapports.HomePage1 import homeGlobal
from Stats.Rapports.Archives import archiveRapport 
from Stats.Rapports.SectionsPage1 import homeSpe 
from Stats.Rapports.HomePage2 import secondGlobal
from Stats.Rapports.Classements import ranksGlobal
from Stats.Rapports.ClassementsObj import ranksIntoSpes
from Stats.Rapports.AvantApres import avantapresSpe
from Stats.Rapports.Anecdotes import anecdotesSpe
import discord
from time import strftime
from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.GetPeriod import getAnnee, getMois
from Core.Fonctions.Embeds import sendEmbed
from Core.Fonctions.setMaxPage import setPage

dictFieldG={"Emotes":"Meilleures emotes","Salons":"Salons les plus actifs","Freq":"Heures les plus actives","Reactions":"Meilleures réactions","Messages":"Messages envoyés","Voice":"Temps en vocal","Mots":"Mots envoyés"}
dictFieldS={"Emotes":"Détails emotes","Salons":"Détails salons","Freq":"Détails heures","Reactions":"Détails réactions","Messages":"Détails messages","Voice":"Détails vocal"}
dictSEMV={"Messages":"Membres","Voice":"Membres","Emotes":"Emotes différentes","Reactions":"Réactions différentes"}
dictTrivia={3:"Images",2:"GIFs",1:"Fichiers",4:"Liens",5:"Réponses",6:"Réactions",7:"Edits",8:"Emotes",9:"Messages",10:"Mots",11:"Vocal"}
dictFieldNom={"Emotes":"Emote","Salons":"Salon","Freq":"Heure","Reactions":"Réaction","Messages":"Membre","Voice":"Membre","Mots":"Membre"}
listeType=["Messages","Voice","Salons","Freq","Emotes","Reactions"]
dictReact={"Voice":"<:otVOICE:835928773718835260>","Reactions":"<:otREACTIONS:835928773740199936>","Emotes":"<:otEMOTES:835928773705990154>","Salons":"<:otSALONS:835928773726699520>","Freq":"<:otFREQ:835929144579326003>"}
dictEmote={835928773718835260:"Voicechan",835928773740199936:"Reactions",835928773705990154:"Emotes",835928773726699520:"Salons",835929144579326003:"Freq"}
tableauMois={"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre","TO":"TOTAL","1":"janvier","2":"février","3":"mars","4":"avril","5":"mai","6":"juin","7":"juillet","8":"aout","9":"septembre","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","glob":"GL","to":"TO"}
dictSection={"Voice":"vocal","Reactions":"réactions","Emotes":"emotes","Salons":"salons","Freq":"heures","Messages":"salons","Voicechan":"vocal"}

async def triggerRapport(ctx,guildOT,bot):
    connexionCMD,curseurCMD=connectSQL(ctx.guild.id,"Commandes","Guild",None,None)
    if len(ctx.args)==2:
        if ctx.invoked_with.lower()=="mois":
            jour,mois,annee,option=None,tableauMois[strftime("%m")],strftime("%y"),"mois"
        elif ctx.invoked_with.lower()=="jour":
            jour,mois,annee,option=strftime("%d"),strftime("%m"),strftime("%y"),"jour"
        elif ctx.invoked_with.lower()=="annee":
            jour,mois,annee,option=None,"to",strftime("%y"),"annee"
        else:
            jour,mois,annee,option=None,"glob","","global"
    else:
        try:
            jour,mois,annee,option=ctx.args[2],tableauMois[getMois(ctx.args[3])],getAnnee(ctx.args[4]),"jour"
            if len(jour)==1:
                jour="0"+jour
        except:
            try:
                jour,mois,annee,option=None,getMois(ctx.args[2]),getAnnee(ctx.args[3]),"mois"
            except:
                try:
                    jour,mois,annee,option=None,"to",getAnnee(ctx.args[2]),"annee"
                except:
                    jour,mois,annee,option=None,"glob","","global"
    
    connexion,curseur=connectSQL(ctx.guild.id,"Rapports","Stats","GL","")
    if option=="jour":
        date=(jour,mois,annee)
    else:
        date=(mois,annee)
    pagemax,listeOptions=pagemaxHomeJour(curseur,jour,mois,annee,option)
    assert listeOptions!=[]

    embed=homeGlobal(date,guildOT,bot,ctx.guild,pagemax,option)
    
    curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'rapport','{2}','Home','{3}','{4}','{5}',1,{6},'countDesc',False)".format(ctx.message.id,ctx.author.id,option,jour,mois,annee,pagemax))

    message=await sendEmbed(ctx,embed,False,False,curseurCMD,connexionCMD,1,pagemax)

    await message.add_reaction("<:otHOME:835930140571729941>")

    if "Messages" in listeOptions:
        listeOptions.remove("Messages")
    if "Voicechan" in listeOptions:
        listeOptions.remove("Voicechan")

    for i in listeOptions:
        await message.add_reaction(dictReact[i])

    if option!="global":
        await message.add_reaction("<:otARCHIVES:836947337808314389>")


async def autoRapport(guild,channel,guildOT,bot,option,date):
    connexionCMD,curseurCMD=connectSQL(guild.id,"Commandes","Guild",None,None)
    if option=="mois":
        jour,mois,annee,option=None,tableauMois[date[0]],date[1],"mois"
    elif option=="jour":
        jour,mois,annee,option=date[0],date[1],date[2],"jour"
    elif option=="annee":
        jour,mois,annee,option=None,"to",date,"annee"
    
    connexion,curseur=connectSQL(guild.id,"Rapports","Stats","GL","")
    if option=="jour":
        date=(jour,mois,annee)
    else:
        date=(mois,annee)
    pagemax,listeOptions=pagemaxHomeJour(curseur,jour,mois,annee,option)
    assert listeOptions!=[]

    embed=homeGlobal(date,guildOT,bot,guild,pagemax,option)

    message=await bot.get_channel(channel).send(embed=embed)
    await message.add_reaction("<:otGAUCHE:772766034335236127>")
    await message.add_reaction("<:otDROITE:772766034376523776>")
    
    curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'rapport','{2}','Home','{3}','{4}','{5}',1,{6},'countDesc',False)".format(message.id,699728606493933650,option,jour,mois,annee,pagemax))
    connexionCMD.commit()

    await message.add_reaction("<:otHOME:835930140571729941>")

    if "Messages" in listeOptions:
        listeOptions.remove("Messages")
    if "Voicechan" in listeOptions:
        listeOptions.remove("Voicechan")

    for i in listeOptions:
        await message.add_reaction(dictReact[i])

    if option!="global":
        await message.add_reaction("<:otARCHIVES:836947337808314389>")


async def switchRapport(ctx,emote,ligne,guildOT,bot):
    connexionCMD,curseurCMD=connectSQL(ctx.guild.id,"Commandes","Guild",None,None)
    connexion,curseur=connectSQL(ctx.guild.id,"Rapports","Stats","GL","")
    jour,mois,annee,categ=ligne["Args2"],ligne["Args3"],ligne["Args4"],ligne["Option"]
    if categ=="jour":
        date=(jour,mois,annee)
    else:
        date=(mois,annee)
    if emote==835930140571729941:
        pagemax=pagemaxHomeJour(curseur,jour,mois,annee,categ)[0]
        embed=homeGlobal(date,guildOT,bot,ctx.guild,pagemax,categ)
        curseurCMD.execute("UPDATE commandes SET Args1='Home' WHERE MessageID={0}".format(ctx.message.id))
    elif emote==836947337808314389:
        pagemax,listeOptions=pagemaxHomeJour(curseur,jour,mois,annee,categ)
        pagemax-=2
        embed=archiveRapport(date,guildOT,bot,ctx.guild,listeOptions[0],categ,1,pagemax)
        curseurCMD.execute("UPDATE commandes SET Args1='Archives' WHERE MessageID={0}".format(ctx.message.id))
    else:
        option=dictEmote[emote]
        if categ=="jour":
            pagemax=pagemaxSpeJour(curseur,jour,mois,annee,option)
        else:
            connexion,curseur=connectSQL(ctx.guild.id,option,"Stats",tableauMois[mois],annee)
            pagemax=pagemaxSpeMois(curseur,mois,annee)
            if categ=="global":
                pagemax-=1
        if option in ("Salons","Voicechan"):
            pagemax+=3
            if categ=="global":
                pagemax-=1
        embed=homeSpe(date,guildOT,bot,ctx.guild,option,pagemax,categ)
        curseurCMD.execute("UPDATE commandes SET Args1='{0}' WHERE MessageID={1}".format(option,ctx.message.id))
    await sendEmbed(ctx,embed,True,False,curseurCMD,connexionCMD,1,pagemax)


async def changePage(ctx,turn,ligne,guildOT,bot):
    connexionCMD,curseurCMD=connectSQL(ctx.guild.id,"Commandes","Guild",None,None)
    jour,mois,annee,categ=ligne["Args2"],ligne["Args3"],ligne["Args4"],ligne["Option"]
    connexion,curseur=connectSQL(ctx.guild.id,"Rapports","Stats","GL","")
    option=ligne["Args1"]
    if categ=="jour":
        date=(jour,mois,annee)
        if option=="Home":
            pagemax,listeOptions=pagemaxHomeJour(curseur,jour,mois,annee,categ)
            
        elif option=="Archives":
            pagemax,listeOptions=pagemaxHomeJour(curseur,jour,mois,annee,categ)
            pagemax-=2
        else:
            pagemax=pagemaxSpeJour(curseur,jour,mois,annee,option)
    else:
        date=(mois,annee)
        if option=="Home":
            pagemax,listeOptions=pagemaxHomeJour(curseur,jour,mois,annee,categ)
        elif option=="Archives":
            pagemax,listeOptions=pagemaxHomeJour(curseur,jour,mois,annee,categ)
            pagemax-=2
        else:
            connexion,curseur=connectSQL(ctx.guild.id,option,"Stats",tableauMois[mois],annee)
            pagemax=pagemaxSpeMois(curseur,mois,annee)
        if categ=="global":
            pagemax-=1
    if option in ("Salons","Voicechan"):
        pagemax+=3
        if categ=="global":
            pagemax-=1
            
    page=setPage(ligne["Page"],pagemax,turn)

    if option=="Home":
        if page==1:
            embed=homeGlobal(date,guildOT,bot,ctx.guild,pagemax,categ)
        elif page==2:
            embed=secondGlobal(date,ctx.guild,pagemax,categ)
        else:
            if listeOptions[page-3]=="Voice":
                page=setPage(page,pagemax,turn)
            embed=ranksGlobal(date,guildOT,bot,ctx.guild,listeOptions[page-3],page,pagemax,categ,"principale")
    elif option=="Archives":
        if "Mots" in listeOptions:
            listeOptions.remove("Mots")
        embed=archiveRapport(date,guildOT,bot,ctx.guild,listeOptions[page-1],categ,page,pagemax)
    else:
        if option not in ("Salons","Voicechan") and categ!="global":
            if page==1:
                embed=homeSpe(date,guildOT,bot,ctx.guild,option,pagemax,categ)
            elif page==2:
                embed=anecdotesSpe(date,guildOT,bot,ctx.guild,option,2,pagemax,categ)
            elif page==3:
                embed=ranksGlobal(date,guildOT,bot,ctx.guild,option,page,pagemax,categ,option)
            elif page==4:
                embed=avantapresSpe(date,guildOT,bot,ctx.guild,option,page,pagemax,categ)
            else:
                embed=ranksIntoSpes(date,guildOT,bot,ctx.guild,option,page-4,page,pagemax,categ)
        elif option=="Salons" and categ!="global":
            if page==1:
                embed=homeSpe(date,guildOT,bot,ctx.guild,option,pagemax,categ)
            elif page==2:
                embed=anecdotesSpe(date,guildOT,bot,ctx.guild,"Messages",2,pagemax,categ)
            elif page==3:
                embed=anecdotesSpe(date,guildOT,bot,ctx.guild,option,3,pagemax,categ)
            elif page==4:
                embed=ranksGlobal(date,guildOT,bot,ctx.guild,"Messages",page,pagemax,categ,option)
            elif page==5:
                embed=ranksGlobal(date,guildOT,bot,ctx.guild,option,page,pagemax,categ,option)
            elif page==6:
                embed=avantapresSpe(date,guildOT,bot,ctx.guild,"Messages",page,pagemax,categ)
            elif page==7:
                embed=avantapresSpe(date,guildOT,bot,ctx.guild,option,page,pagemax,categ)
            else:
                embed=ranksIntoSpes(date,guildOT,bot,ctx.guild,option,page-7,page,pagemax,categ)
        elif option=="Salons" and categ=="global":
            if page==1:
                embed=homeSpe(date,guildOT,bot,ctx.guild,option,pagemax,categ)
            elif page==2:
                embed=anecdotesSpe(date,guildOT,bot,ctx.guild,"Messages",2,pagemax,categ)
            elif page==3:
                embed=anecdotesSpe(date,guildOT,bot,ctx.guild,option,3,pagemax,categ)
            elif page==4:
                embed=ranksGlobal(date,guildOT,bot,ctx.guild,"Messages",page,pagemax,categ,option)
            elif page==5:
                embed=ranksGlobal(date,guildOT,bot,ctx.guild,option,page,pagemax,categ,option)
            else:
                embed=ranksIntoSpes(date,guildOT,bot,ctx.guild,option,page-5,page,pagemax,categ)
        elif option=="Voicechan" and categ!="global":
            if page==1:
                embed=homeSpe(date,guildOT,bot,ctx.guild,"Voicechan",pagemax,categ)
            elif page==2:
                embed=anecdotesSpe(date,guildOT,bot,ctx.guild,"Voice",2,pagemax,categ)
            elif page==3:
                embed=anecdotesSpe(date,guildOT,bot,ctx.guild,"Voicechan",3,pagemax,categ)
            elif page==4:
                embed=ranksGlobal(date,guildOT,bot,ctx.guild,"Voice",page,pagemax,categ,option)
            elif page==5:
                embed=ranksGlobal(date,guildOT,bot,ctx.guild,"Voicechan",page,pagemax,categ,option)
            elif page==6:
                embed=avantapresSpe(date,guildOT,bot,ctx.guild,"Voice",page,pagemax,categ)
            elif page==7:
                embed=avantapresSpe(date,guildOT,bot,ctx.guild,"Voicechan",page,pagemax,categ)
            else:
                embed=ranksIntoSpes(date,guildOT,bot,ctx.guild,"Voicechan",page-7,page,pagemax,categ)
        elif option=="Voicechan" and categ=="global":
            if page==1:
                embed=homeSpe(date,guildOT,bot,ctx.guild,"Voicechan",pagemax,categ)
            elif page==2:
                embed=anecdotesSpe(date,guildOT,bot,ctx.guild,"Voice",2,pagemax,categ)
            elif page==3:
                embed=anecdotesSpe(date,guildOT,bot,ctx.guild,"Voicechan",3,pagemax,categ)
            elif page==4:
                embed=ranksGlobal(date,guildOT,bot,ctx.guild,"Voice",page,pagemax,categ,option)
            elif page==5:
                embed=ranksGlobal(date,guildOT,bot,ctx.guild,"Voicechan",page,pagemax,categ,option)
            else:
                embed=ranksIntoSpes(date,guildOT,bot,ctx.guild,"Voicechan",page-5,page,pagemax,categ)
        elif categ=="global":
            if page==1:
                embed=homeSpe(date,guildOT,bot,ctx.guild,option,pagemax,categ)
            elif page==2:
                embed=anecdotesSpe(date,guildOT,bot,ctx.guild,option,2,pagemax,categ)
            elif page==3:
                embed=ranksGlobal(date,guildOT,bot,ctx.guild,option,page,pagemax,categ,option)
            else:
                embed=ranksIntoSpes(date,guildOT,bot,ctx.guild,option,page-3,page,pagemax,categ)
    await sendEmbed(ctx,embed,True,False,curseurCMD,connexionCMD,page,pagemax)