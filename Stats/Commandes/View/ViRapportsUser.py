from Core.Fonctions.SendView import sendView
from Core.Fonctions.setMaxPage import setPage
from Stats.RapportsUsers.AvantApres import avantapresSpe
from Stats.RapportsUsers.Classements import ranksGlobal
from Stats.RapportsUsers.ClassementsObj import ranksIntoSpes
from Stats.RapportsUsers.HomePage1 import homeGlobal
from Stats.RapportsUsers.HomePage2 import secondGlobal
from Stats.RapportsUsers.Pagemax import pagemaxHome, pagemaxSpeMois
from Stats.RapportsUsers.SectionsPage1 import homeSpe
from Stats.SQL.ConnectSQL import connectSQL

dictEmote={"ot:voicerapport":"Voicechan","ot:reactionsrapport":"Reactions","ot:emotesrapport":"Emotes","ot:salonsrapport":"Salons","ot:freqrapport":"Freq"}
tableauMois={"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre","TO":"TOTAL","1":"janvier","2":"février","3":"mars","4":"avril","5":"mai","6":"juin","7":"juillet","8":"aout","9":"septembre","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","glob":"GL","to":"TO"}

async def switchRapportUser(interaction,connexionCMD,curseurCMD,ligne,guildOT,bot):
    connexionCMD,curseurCMD=connectSQL(interaction.guild_id,"Commandes","Guild",None,None)
    mois,annee,categ,user=ligne["Args2"],ligne["Args3"],ligne["Option"],ligne["AuthorID"]
    connexion,curseur=connectSQL(interaction.guild_id,"Rapports","Stats","GL","")
    date=(mois,annee)

    if interaction.data["custom_id"]=="ot:homerapport":
        pagemax=pagemaxHome(curseur,mois,annee,categ,user)[0]
        embed=homeGlobal(date,guildOT,bot,interaction.guild,pagemax,categ,user)
        curseurCMD.execute("UPDATE commandes SET Args1='Home' WHERE MessageID={0}".format(interaction.message.interaction.id))
    else:
        option=dictEmote[interaction.data["custom_id"]]
        connexion,curseur=connectSQL(interaction.guild_id,option,"Stats",tableauMois[mois],annee)
        pagemax=pagemaxSpeMois(curseur,mois,annee,user)
        if categ=="global":
            pagemax-=1
        embed=homeSpe(date,guildOT,bot,interaction.guild,option,pagemax,categ,user)
        curseurCMD.execute("UPDATE commandes SET Args1='{0}' WHERE MessageID={1}".format(option,interaction.message.interaction.id))

    await sendView(interaction,embed,curseurCMD,connexionCMD,1,pagemax)


async def changePageUser(interaction,connexionCMD,curseurCMD,turn,ligne,guildOT,bot):
    connexionCMD,curseurCMD=connectSQL(interaction.guild_id,"Commandes","Guild",None,None)
    mois,annee,categ,user=ligne["Args2"],ligne["Args3"],ligne["Option"],ligne["AuthorID"]
    option=ligne["Args1"]
    connexion,curseur=connectSQL(interaction.guild_id,"Rapports","Stats","GL","")
    date=(mois,annee)
    if option=="Home":
        pagemax,listeOptions=pagemaxHome(curseur,mois,annee,categ,user)
    else:
        connexion,curseur=connectSQL(interaction.guild_id,option,"Stats",tableauMois[mois],annee)
        pagemax=pagemaxSpeMois(curseur,mois,annee,user)
        if categ=="global":
            pagemax-=1
            
    page=setPage(ligne["Page"],pagemax,turn)

    if option=="Home":
        if page==1:
            embed=homeGlobal(date,guildOT,bot,interaction.guild,pagemax,categ,user)
        elif page==2:
            embed=secondGlobal(date,interaction.guild,pagemax,categ,user)
        else:
            if listeOptions[page-3]=="Voicechan":
                page=setPage(page,pagemax,turn)
            embed=ranksGlobal(date,guildOT,bot,interaction.guild,listeOptions[page-3],page,pagemax,categ,"principale",user)
    else:
        if categ!="global":
            if page==1:
                embed=homeSpe(date,guildOT,bot,interaction.guild,option,pagemax,categ,user)
            elif page==2:
                embed=ranksGlobal(date,guildOT,bot,interaction.guild,option,page,pagemax,categ,option,user)
            elif page==3:
                embed=avantapresSpe(date,guildOT,bot,interaction.guild,option,page,pagemax,categ,user)
            else:
                embed=ranksIntoSpes(date,guildOT,bot,interaction.guild,option,page-3,page,pagemax,categ,user)

        else:
            if page==1:
                embed=homeSpe(date,guildOT,bot,interaction.guild,option,pagemax,categ,user)
            elif page==2:
                embed=ranksGlobal(date,guildOT,bot,interaction.guild,option,page,pagemax,categ,option,user)
            else:
                embed=ranksIntoSpes(date,guildOT,bot,interaction.guild,option,page-2,page,pagemax,categ,user)

    await sendView(interaction,embed,curseurCMD,connexionCMD,page,pagemax)
