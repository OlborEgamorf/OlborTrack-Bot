from Core.Fonctions.SendView import sendView
from Core.Fonctions.setMaxPage import setPage
from Stats.Rapports.Anecdotes import anecdotesSpe
from Stats.Rapports.Archives import archiveRapport
from Stats.Rapports.AvantApres import avantapresSpe
from Stats.Rapports.Classements import ranksGlobal
from Stats.Rapports.ClassementsObj import ranksIntoSpes
from Stats.Rapports.HomePage1 import homeGlobal
from Stats.Rapports.HomePage2 import secondGlobal
from Stats.Rapports.Pagemax import pagemaxHome, pagemaxSpeMois
from Stats.Rapports.SectionsPage1 import homeSpe
from Stats.SQL.ConnectSQL import connectSQL

dictEmote={"ot:voicerapport":"Voicechan","ot:reactionsrapport":"Reactions","ot:emotesrapport":"Emotes","ot:salonsrapport":"Salons","ot:freqrapport":"Freq"}
tableauMois={"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre","TO":"TOTAL","1":"janvier","2":"février","3":"mars","4":"avril","5":"mai","6":"juin","7":"juillet","8":"aout","9":"septembre","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","glob":"GL","to":"TO"}

async def switchRapport(interaction,connexion,curseur,ligne,guildOT,bot):
    mois,annee,categ=ligne["Args2"],ligne["Args3"],ligne["Option"]
    date=(mois,annee)

    if interaction.data["custom_id"]=="ot:homerapport":
        pagemax=pagemaxHome(curseur,mois,annee,categ)[0]
        embed=homeGlobal(date,guildOT,bot,interaction.guild,pagemax,categ)
        curseur.execute("UPDATE commandes SET Args1='Home' WHERE MessageID={0}".format(interaction.message.interaction.id))
    elif interaction.data["custom_id"]=="ot:archiverapport":
        pagemax,listeOptions=pagemaxHome(curseur,mois,annee,categ)
        pagemax-=2
        embed=archiveRapport(date,guildOT,bot,interaction.guild,listeOptions[0],categ,1,pagemax)
        curseur.execute("UPDATE commandes SET Args1='Archives' WHERE MessageID={0}".format(interaction.message.interaction.id))
    else:
        option=dictEmote[interaction.data["custom_id"]]
        pagemax=pagemaxSpeMois(curseur,mois,annee)
        if categ=="global":
            pagemax-=1
        if option in ("Salons","Voicechan"):
            pagemax+=3
            if categ=="global":
                pagemax-=1
        embed=homeSpe(date,guildOT,bot,interaction.guild,option,pagemax,categ)
        curseur.execute("UPDATE commandes SET Args1='{0}' WHERE MessageID={1}".format(option,interaction.message.interaction.id))
        
    await sendView(interaction,embed,curseur,connexion,1,pagemax)
    
async def changePage(interaction,connexion,curseur,turn,ligne,guildOT,bot):
    mois,annee,categ=ligne["Args2"],ligne["Args3"],ligne["Option"]
    option=ligne["Args1"]
    date=(mois,annee)

    if option=="Home":
        pagemax,listeOptions=pagemaxHome(curseur,mois,annee,categ)
    elif option=="Archives":
        pagemax,listeOptions=pagemaxHome(curseur,mois,annee,categ)
        pagemax-=2
    else:
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
            embed=homeGlobal(date,guildOT,bot,interaction.guild,pagemax,categ)
        elif page==2:
            embed=secondGlobal(date,interaction.guild,pagemax,categ)
        else:
            if listeOptions[page-3]=="Voice":
                page=setPage(page,pagemax,turn)
            embed=ranksGlobal(date,guildOT,bot,interaction.guild,listeOptions[page-3],page,pagemax,categ,"principale")
    elif option=="Archives":
        if "Mots" in listeOptions:
            listeOptions.remove("Mots")
        embed=archiveRapport(date,guildOT,bot,interaction.guild,listeOptions[page-1],categ,page,pagemax)
    else:
        if option not in ("Salons","Voicechan") and categ!="global":
            if page==1:
                embed=homeSpe(date,guildOT,bot,interaction.guild,option,pagemax,categ)
            elif page==2:
                embed=anecdotesSpe(date,guildOT,bot,interaction.guild,option,2,pagemax,categ)
            elif page==3:
                embed=ranksGlobal(date,guildOT,bot,interaction.guild,option,page,pagemax,categ,option)
            elif page==4:
                embed=avantapresSpe(date,guildOT,bot,interaction.guild,option,page,pagemax,categ)
            else:
                embed=ranksIntoSpes(date,guildOT,bot,interaction.guild,option,page-4,page,pagemax,categ)
        elif option=="Salons" and categ!="global":
            if page==1:
                embed=homeSpe(date,guildOT,bot,interaction.guild,option,pagemax,categ)
            elif page==2:
                embed=anecdotesSpe(date,guildOT,bot,interaction.guild,"Messages",2,pagemax,categ)
            elif page==3:
                embed=anecdotesSpe(date,guildOT,bot,interaction.guild,option,3,pagemax,categ)
            elif page==4:
                embed=ranksGlobal(date,guildOT,bot,interaction.guild,"Messages",page,pagemax,categ,option)
            elif page==5:
                embed=ranksGlobal(date,guildOT,bot,interaction.guild,option,page,pagemax,categ,option)
            elif page==6:
                embed=avantapresSpe(date,guildOT,bot,interaction.guild,"Messages",page,pagemax,categ)
            elif page==7:
                embed=avantapresSpe(date,guildOT,bot,interaction.guild,option,page,pagemax,categ)
            else:
                embed=ranksIntoSpes(date,guildOT,bot,interaction.guild,option,page-7,page,pagemax,categ)
        elif option=="Salons" and categ=="global":
            if page==1:
                embed=homeSpe(date,guildOT,bot,interaction.guild,option,pagemax,categ)
            elif page==2:
                embed=anecdotesSpe(date,guildOT,bot,interaction.guild,"Messages",2,pagemax,categ)
            elif page==3:
                embed=anecdotesSpe(date,guildOT,bot,interaction.guild,option,3,pagemax,categ)
            elif page==4:
                embed=ranksGlobal(date,guildOT,bot,interaction.guild,"Messages",page,pagemax,categ,option)
            elif page==5:
                embed=ranksGlobal(date,guildOT,bot,interaction.guild,option,page,pagemax,categ,option)
            else:
                embed=ranksIntoSpes(date,guildOT,bot,interaction.guild,option,page-5,page,pagemax,categ)
        elif option=="Voicechan" and categ!="global":
            if page==1:
                embed=homeSpe(date,guildOT,bot,interaction.guild,"Voicechan",pagemax,categ)
            elif page==2:
                embed=anecdotesSpe(date,guildOT,bot,interaction.guild,"Voice",2,pagemax,categ)
            elif page==3:
                embed=anecdotesSpe(date,guildOT,bot,interaction.guild,"Voicechan",3,pagemax,categ)
            elif page==4:
                embed=ranksGlobal(date,guildOT,bot,interaction.guild,"Voice",page,pagemax,categ,option)
            elif page==5:
                embed=ranksGlobal(date,guildOT,bot,interaction.guild,"Voicechan",page,pagemax,categ,option)
            elif page==6:
                embed=avantapresSpe(date,guildOT,bot,interaction.guild,"Voice",page,pagemax,categ)
            elif page==7:
                embed=avantapresSpe(date,guildOT,bot,interaction.guild,"Voicechan",page,pagemax,categ)
            else:
                embed=ranksIntoSpes(date,guildOT,bot,interaction.guild,"Voicechan",page-7,page,pagemax,categ)
        elif option=="Voicechan" and categ=="global":
            if page==1:
                embed=homeSpe(date,guildOT,bot,interaction.guild,"Voicechan",pagemax,categ)
            elif page==2:
                embed=anecdotesSpe(date,guildOT,bot,interaction.guild,"Voice",2,pagemax,categ)
            elif page==3:
                embed=anecdotesSpe(date,guildOT,bot,interaction.guild,"Voicechan",3,pagemax,categ)
            elif page==4:
                embed=ranksGlobal(date,guildOT,bot,interaction.guild,"Voice",page,pagemax,categ,option)
            elif page==5:
                embed=ranksGlobal(date,guildOT,bot,interaction.guild,"Voicechan",page,pagemax,categ,option)
            else:
                embed=ranksIntoSpes(date,guildOT,bot,interaction.guild,"Voicechan",page-5,page,pagemax,categ)
        elif categ=="global":
            if page==1:
                embed=homeSpe(date,guildOT,bot,interaction.guild,option,pagemax,categ)
            elif page==2:
                embed=anecdotesSpe(date,guildOT,bot,interaction.guild,option,2,pagemax,categ)
            elif page==3:
                embed=ranksGlobal(date,guildOT,bot,interaction.guild,option,page,pagemax,categ,option)
            else:
                embed=ranksIntoSpes(date,guildOT,bot,interaction.guild,option,page-3,page,pagemax,categ)

    await sendView(interaction,embed,curseur,connexion,page,pagemax)
