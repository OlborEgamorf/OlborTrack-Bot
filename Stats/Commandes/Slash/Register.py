from Stats.SQL.Verification import verifCommands
from Core.Fonctions.GetPeriod import getAnnee, getMois
from time import strftime

def registerCMD(interaction,curseur,cmd,option,guildOT,periode=None,obj=None):
    #assert verifCommands(guildOT,option)
    if periode==None:
        mois,annee=None,None
    else:
        periode=periode.split(" ")
        if periode[0].lower() not in ("mois","annee"):
            try:
                mois,annee=getMois(periode[0].lower()),getAnnee(periode[1].lower())
            except:
                try:
                    mois,annee=None,getAnnee(periode[0].lower())
                except:
                    mois,annee=None,None
        elif periode[0].lower()=="mois":
            mois,annee=strftime("%m"),strftime("%y")
        elif periode[0].lower()=="annee":
            mois,annee=None,strftime("%y")

    obj=None if obj==None else obj.id

    curseur.execute("CREATE TABLE IF NOT EXISTS commandes (`MessageID` BIGINT, `AuthorID` BIGINT, `Commande` varchar(50), `Option` varchar(50), `Args1` varchar(50), `Args2` varchar(50), `Args3` varchar(50), `Args4` varchar(50), `Page` INT, `PageMax` INT, `Tri` varchar(50), `Mobile` BOOLEAN)")

    curseur.execute("INSERT INTO commandes VALUES({0},{1},'{2}','{3}','{4}','{5}','{6}','None',1,1,'countDesc',0);".format(interaction.id,interaction.user.id,cmd,option,mois,annee,obj))
    ligne=curseur.execute("SELECT * FROM commandes WHERE MessageID={0}".format(interaction.id)).fetchone()
    return ligne