from time import strftime

from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.Embeds import embedAssertClassic
from Core.Fonctions.GetPeriod import getAnnee, getMois
from Core.Fonctions.SendSlash import sendSlash
from Core.Fonctions.setMaxPage import setMax
from Stats.Embeds.Central import statsEmbed
from Stats.SQL.ConnectSQL import connectSQL

tableauMois={"01":"Janvier","02":"Février","03":"Mars","04":"Avril","05":"Mai","06":"Juin","07":"Juillet","08":"Aout","09":"Septembre","10":"Octobre","11":"Novembre","12":"Décembre","TO":"Année","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","glob":"GL","to":"TO"}
dictOption={"tortues":"Tortues","tortuesduo":"TortuesDuo","trivialversus":"TrivialVersus","trivialbr":"TrivialBR","trivialparty":"TrivialParty","p4":"P4","bataillenavale":"BatailleNavale","cross":"Cross","codenames":"CodeNames","morpion":"Morpion","matrice":"Matrice"}

async def statsJeuxSlash(interaction,periode,option,bot,guild):
    try:
        connexionCMD,curseurCMD=connectSQL(interaction.guild_id,"Commandes","Guild",None,None)
        if periode==None:
            mois,annee="glob",""
        else:
            periode=periode.split(" ")
            if periode[0].lower() not in ("mois","annee"):
                try:
                    mois,annee=getMois(periode[0].lower()),getAnnee(periode[1].lower())
                except:
                    try:
                        mois,annee="to",getAnnee(periode[0].lower())
                    except:
                        mois,annee="glob",""
            elif periode[0].lower()=="mois":
                mois,annee=tableauMois[strftime("%m")].lower(),strftime("%y")
            elif periode[0].lower()=="annee":
                mois,annee="to",strftime("%y")
        
        curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'jeux','{2}','{3}','{4}','{5}','None',1,1,'countDesc',False)".format(interaction.id,interaction.user.id,option,mois,annee,guild))
        ligne=curseurCMD.execute("SELECT * FROM commandes WHERE MessageID={0}".format(interaction.id)).fetchone()
        
        connexion,curseur=connectSQL(guild,option,"Jeux",tableauMois[mois],annee)

        pagemax=setMax(curseur.execute("SELECT COUNT() as Nombre FROM {0}{1}".format(mois,annee)).fetchone()["Nombre"])
        page=1

        if mois=="glob":
            title="Classement général {0}".format(option.lower())
            evol=True
        elif mois=="to":
            title="Classement {0} 20{1}".format(option.lower(),annee)
            evol=True if annee==strftime("%y") else False
        else:
            title="Classement {0} {1} 20{2}".format(option.lower(),mois,annee)
            evol=True if tableauMois[mois]==strftime("%m") and annee==strftime("%y") else False

        embed=await statsEmbed("{0}{1}".format(mois,annee),ligne,page,pagemax,option,interaction.guild,bot,evol,False,curseur)
        embed.title=title
        embed=auteur("Olbor Track Bot",interaction.guild.get_member(990574563572187138).display_avatar,embed,"user")
        embed.colour=0x3498db
        await sendSlash(interaction,embed,curseurCMD,connexionCMD,page,pagemax)
    
    except:
        await interaction.response.send_message(embed=embedAssertClassic("Impossible de trouver ce que vous cherchez.\nLe classement cherché n'existe pas ou alors il y a un problème de mon côté."))
