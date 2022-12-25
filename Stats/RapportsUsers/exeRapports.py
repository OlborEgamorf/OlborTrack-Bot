from time import strftime

from Core.Fonctions.GetPeriod import getAnnee, getMois
from Core.Fonctions.SendSlash import sendSlash
from Core.Reactions.exeReactions import ViewRapports
from Stats.RapportsUsers.HomePage1 import homeGlobal
from Stats.RapportsUsers.Pagemax import pagemaxHome
from Stats.SQL.ConnectSQL import connectSQL

tableauMois={"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre","TO":"TOTAL","1":"janvier","2":"février","3":"mars","4":"avril","5":"mai","6":"juin","7":"juillet","8":"aout","9":"septembre","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","glob":"GL","to":"TO"}

async def rapportUser(interaction,periode,guildOT,bot):
    connexion,curseur=connectSQL(interaction.guild_id)
    if periode==None:
        mois,annee,option="to","GL","global"
    else:
        periode=periode.split(" ")
        if periode[0].lower() not in ("mois","annee"):
            try:
                mois,annee,option=getMois(periode[0].lower()),getAnnee(periode[1].lower()),"mois"
            except:
                try:
                    mois,annee,option="to",getAnnee(periode[0].lower()),"annee"
                except:
                    mois,annee,option="to","GL","global"
        elif periode[0].lower()=="mois":
            mois,annee,option=tableauMois[strftime("%m")],strftime("%y"),"mois"
        elif periode[0].lower()=="annee":
            mois,annee,option="to",strftime("%y"),"annee"

    date=(mois,annee)

    pagemax,listeOptions=pagemaxHome(curseur,mois,annee,option,interaction.user.id)
    embed=homeGlobal(date,guildOT,bot,interaction.guild,pagemax,option,interaction.user.id)
    curseur.execute("INSERT INTO commandes VALUES({0},{1},'rapportUser','{2}','Home','{3}','{4}','None',1,{5},'countDesc',False)".format(interaction.id,interaction.user.id,option,mois,annee,pagemax))

    if "Mentionnes" in listeOptions:
        listeOptions.remove("Mentionnes")

    view=ViewRapports(listeOptions,archives=False)
    await sendSlash(interaction,embed,curseur,connexion,1,pagemax,customView=view)
