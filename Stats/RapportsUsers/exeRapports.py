from Stats.RapportsUsers.Pagemax import pagemaxHomeJour, pagemaxSpeJour, pagemaxSpeMois 
from Stats.RapportsUsers.HomePage1 import homeGlobal
from Stats.RapportsUsers.SectionsPage1 import homeSpe 
from Stats.RapportsUsers.HomePage2 import secondGlobal
from Stats.RapportsUsers.Classements import ranksGlobal
from Stats.RapportsUsers.ClassementsObj import ranksIntoSpes
from Stats.RapportsUsers.AvantApres import avantapresSpe
import discord
from time import strftime
from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.GetPeriod import getAnnee, getMois
from Core.Fonctions.Embeds import sendEmbed
from Core.Fonctions.setMaxPage import setPage

listeType=["Messages","Voicechan","Salons","Freq","Emotes","Reactions"]
dictReact={"Voicechan":"<:otVOICE:835928773718835260>","Reactions":"<:otREACTIONS:835928773740199936>","Emotes":"<:otEMOTES:835928773705990154>","Salons":"<:otSALONS:835928773726699520>","Freq":"<:otFREQ:835929144579326003>"}
dictEmote={835928773718835260:"Voicechan",835928773740199936:"Reactions",835928773705990154:"Emotes",835928773726699520:"Salons",835929144579326003:"Freq"}
tableauMois={"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre","TO":"TOTAL","1":"janvier","2":"février","3":"mars","4":"avril","5":"mai","6":"juin","7":"juillet","8":"aout","9":"septembre","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","glob":"GL","to":"TO"}
dictSection={"Voice":"vocal","Reactions":"réactions","Emotes":"emotes","Salons":"salons","Freq":"heures","Messages":"salons","Voicechan":"vocal"}

async def triggerRapportUser(ctx,guildOT,bot):
    connexionCMD,curseurCMD=connectSQL(ctx.guild.id,"Commandes","Guild",None,None)
    if len(ctx.args)==2 or ctx.args[2].lower() not in ("mois","annee","jour"):
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
                    jour,mois,annee,option=None,"to","GL","global"
    elif ctx.args[2].lower()=="mois":
        jour,mois,annee,option=None,tableauMois[strftime("%m")],strftime("%y"),"mois"
    elif ctx.args[2].lower()=="jour":
        jour,mois,annee,option=strftime("%d"),strftime("%m"),strftime("%y"),"jour"
    elif ctx.args[2].lower()=="annee":
        jour,mois,annee,option=None,"to",strftime("%y"),"annee"

    
    connexion,curseur=connectSQL(ctx.guild.id,"Rapports","Stats","GL","")
    if option=="jour":
        date=(jour,mois,annee)
    else:
        date=(mois,annee)

    pagemax,listeOptions=pagemaxHomeJour(curseur,jour,mois,annee,option,ctx.author.id)
    embed=homeGlobal(date,guildOT,bot,ctx.guild,pagemax,option,ctx.author.id)
    curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'rapportUser','{2}','Home','{3}','{4}','{5}',1,{6},'countDesc',False)".format(ctx.message.id,ctx.author.id,option,jour,mois,annee,pagemax))

    message=await sendEmbed(ctx,embed,False,False,curseurCMD,connexionCMD,1,pagemax)

    await message.add_reaction("<:otHOME:835930140571729941>")

    if "Mentionnes" in listeOptions:
        listeOptions.remove("Mentionnes")
    for i in listeOptions:
        await message.add_reaction(dictReact[i])


async def switchRapportUser(ctx,emote,ligne,guildOT,bot):
    connexionCMD,curseurCMD=connectSQL(ctx.guild.id,"Commandes","Guild",None,None)
    jour,mois,annee,categ,user=ligne["Args2"],ligne["Args3"],ligne["Args4"],ligne["Option"],ligne["AuthorID"]
    connexion,curseur=connectSQL(ctx.guild.id,"Rapports","Stats","GL","")
    if categ=="jour":
        date=(jour,mois,annee)
    else:
        date=(mois,annee)
    if emote==835930140571729941:
        pagemax=pagemaxHomeJour(curseur,jour,mois,annee,categ,user)[0]
        embed=homeGlobal(date,guildOT,bot,ctx.guild,pagemax,categ,user)
        curseurCMD.execute("UPDATE commandes SET Args1='Home' WHERE MessageID={0}".format(ctx.message.id))
    else:
        option=dictEmote[emote]
        if categ=="jour":
            pagemax=pagemaxSpeJour(curseur,jour,mois,annee,option,user)
        else:
            connexion,curseur=connectSQL(ctx.guild.id,option,"Stats",tableauMois[mois],annee)
            pagemax=pagemaxSpeMois(curseur,mois,annee,user)
            if categ=="global":
                pagemax-=1
        embed=homeSpe(date,guildOT,bot,ctx.guild,option,pagemax,categ,user)
        curseurCMD.execute("UPDATE commandes SET Args1='{0}' WHERE MessageID={1}".format(option,ctx.message.id))
    await sendEmbed(ctx,embed,True,False,curseurCMD,connexionCMD,1,pagemax)


async def changePageUser(ctx,turn,ligne,guildOT,bot):
    connexionCMD,curseurCMD=connectSQL(ctx.guild.id,"Commandes","Guild",None,None)
    jour,mois,annee,categ,user=ligne["Args2"],ligne["Args3"],ligne["Args4"],ligne["Option"],ligne["AuthorID"]
    option=ligne["Args1"]
    connexion,curseur=connectSQL(ctx.guild.id,"Rapports","Stats","GL","")
    if categ=="jour":
        date=(jour,mois,annee)
        if option=="Home":
            pagemax,listeOptions=pagemaxHomeJour(curseur,jour,mois,annee,categ,user)
        else:
            pagemax=pagemaxSpeJour(curseur,jour,mois,annee,option,user)
    else:
        date=(mois,annee)
        if option=="Home":
            pagemax,listeOptions=pagemaxHomeJour(curseur,jour,mois,annee,categ,user)
        else:
            connexion,curseur=connectSQL(ctx.guild.id,option,"Stats",tableauMois[mois],annee)
            pagemax=pagemaxSpeMois(curseur,mois,annee,user)
            if categ=="global":
                pagemax-=1
            
    page=setPage(ligne["Page"],pagemax,turn)

    if option=="Home":
        if page==1:
            embed=homeGlobal(date,guildOT,bot,ctx.guild,pagemax,categ,user)
        elif page==2:
            embed=secondGlobal(date,ctx.guild,pagemax,categ,user)
        else:
            if listeOptions[page-3]=="Voicechan":
                page=setPage(page,pagemax,turn)
            embed=ranksGlobal(date,guildOT,bot,ctx.guild,listeOptions[page-3],page,pagemax,categ,"principale",user)
    else:
        if categ!="global":
            if page==1:
                embed=homeSpe(date,guildOT,bot,ctx.guild,option,pagemax,categ,user)
            elif page==2:
                embed=ranksGlobal(date,guildOT,bot,ctx.guild,option,page,pagemax,categ,option,user)
            elif page==3:
                embed=avantapresSpe(date,guildOT,bot,ctx.guild,option,page,pagemax,categ,user)
            else:
                embed=ranksIntoSpes(date,guildOT,bot,ctx.guild,option,page-3,page,pagemax,categ,user)

        else:
            if page==1:
                embed=homeSpe(date,guildOT,bot,ctx.guild,option,pagemax,categ,user)
            elif page==2:
                embed=ranksGlobal(date,guildOT,bot,ctx.guild,option,page,pagemax,categ,option,user)
            else:
                embed=ranksIntoSpes(date,guildOT,bot,ctx.guild,option,page-2,page,pagemax,categ,user)
    await sendEmbed(ctx,embed,True,False,curseurCMD,connexionCMD,page,pagemax)