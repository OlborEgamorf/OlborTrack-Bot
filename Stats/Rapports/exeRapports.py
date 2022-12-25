from time import strftime

from Core.Fonctions.GetPeriod import getAnnee, getMois
from Core.Fonctions.SendSlash import sendSlash
from Core.Reactions.exeReactions import ViewRapports
from Stats.Rapports.HomePage1 import homeGlobal
from Stats.Rapports.Pagemax import pagemaxHome
from Stats.SQL.ConnectSQL import connectSQL

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


async def rapportGlobal(interaction,guildOT,bot):
    connexion,curseur=connectSQL(interaction.guild_id)

    date=("glob","")
    pagemax,listeOptions=pagemaxHome(curseur,"glob","","global")
    assert listeOptions!=[]

    embed=homeGlobal(date,guildOT,bot,interaction.guild,pagemax,"global")
    
    curseur.execute("INSERT INTO commandes VALUES({0},{1},'rapport','{2}','Home','{3}','{4}','None',1,{5},'countDesc',False)".format(interaction.id,interaction.user.id,"global","glob","",pagemax))

    if "Messages" in listeOptions:
        listeOptions.remove("Messages")
    if "Voicechan" in listeOptions:
        listeOptions.remove("Voicechan")

    view=ViewRapports(listeOptions,archives=False)
    await sendSlash(interaction,embed,curseur,connexion,1,pagemax,customView=view)

async def rapportMois(interaction,periode,guildOT,bot):
    connexion,curseur=connectSQL(interaction.guild_id)
    if periode==None:
        mois,annee=tableauMois[strftime("%m")].lower(),strftime("%y")
    else:
        periode=periode.split(" ")
        mois,annee=getMois(periode[0].lower()),getAnnee(periode[1].lower())

    date=(mois,annee)
    pagemax,listeOptions=pagemaxHome(curseur,mois,annee,"mois")
    assert listeOptions!=[]

    embed=homeGlobal(date,guildOT,bot,interaction.guild,pagemax,"mois")
    
    curseur.execute("INSERT INTO commandes VALUES({0},{1},'rapport','{2}','Home','{3}','{4}','None',1,{5},'countDesc',False)".format(interaction.id,interaction.user.id,"mois",mois,annee,pagemax))

    if "Messages" in listeOptions:
        listeOptions.remove("Messages")
    if "Voicechan" in listeOptions:
        listeOptions.remove("Voicechan")

    view=ViewRapports(listeOptions)
    await sendSlash(interaction,embed,curseur,connexion,1,pagemax,customView=view)

async def rapportAnnee(interaction,periode,guildOT,bot):
    connexion,curseur=connectSQL(interaction.guild_id)
    if periode==None:
        annee=strftime("%y")
    else:
        annee=getAnnee(periode)

    date=("to",annee)
    pagemax,listeOptions=pagemaxHome(curseur,"to",annee,"annee")
    assert listeOptions!=[]

    embed=homeGlobal(date,guildOT,bot,interaction.guild,pagemax,"annee")
    
    curseur.execute("INSERT INTO commandes VALUES({0},{1},'rapport','{2}','Home','{3}','{4}','None',1,{5},'countDesc',False)".format(interaction.id,interaction.user.id,"annee","to",annee,pagemax))

    if "Messages" in listeOptions:
        listeOptions.remove("Messages")
    if "Voicechan" in listeOptions:
        listeOptions.remove("Voicechan")

    view=ViewRapports(listeOptions)
    await sendSlash(interaction,embed,curseur,connexion,1,pagemax,customView=view)


async def autoRapport(guild,channel,guildOT,bot,option,date):
    connexion,curseur=connectSQL(guild.id,"Rapports","Stats","GL","")
    if option=="mois":
        mois,annee,option=tableauMois[date[0]],date[1],"mois"
    elif option=="annee":
        mois,annee,option="to",date,"annee"
    
    date=(mois,annee)
    pagemax,listeOptions=pagemaxHome(curseur,mois,annee,option)
    assert listeOptions!=[]

    embed=homeGlobal(date,guildOT,bot,guild,pagemax,option)
    view=ViewRapports(listeOptions)
    message=await bot.get_channel(channel).send(embed=embed,view=view)
    
    curseur.execute("INSERT INTO commandes VALUES({0},{1},'rapport','{2}','Home','{3}','{4}','None',1,{5},'countDesc',False)".format(message.id,699728606493933650,option,mois,annee,pagemax))
    connexion.commit()
