from time import strftime

from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.Embeds import embedAssertClassic
from Core.Fonctions.GetPeriod import getAnnee, getMois
from Core.Fonctions.SendSlash import sendSlash
from Core.Fonctions.setMaxPage import setMax
from Stats.Embeds.Central import statsEmbed
from Stats.SQL.ConnectSQL import connectSQL
from Stats.SQL.Verification import verifCommands

tableauMois={"01":"Janvier","02":"Février","03":"Mars","04":"Avril","05":"Mai","06":"Juin","07":"Juillet","08":"Aout","09":"Septembre","10":"Octobre","11":"Novembre","12":"Décembre","TO":"Année","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","glob":"GL","to":"TO"}

async def statsPerso(interaction,periode,option,guildOT,bot):
    if True:
        assert verifCommands(guildOT,option)
        connexionCMD,curseurCMD=connectSQL(interaction.guild_id,"Commandes","Guild",None,None)
        if periode==None:
            mois,annee="TO","GL"
        else:
            periode=periode.split(" ")
            if periode[0].lower() not in ("mois","annee"):
                try:
                    mois,annee=tableauMois[getMois(periode[0].lower())],getAnnee(periode[1].lower())
                except:
                    try:
                        mois,annee="TO",getAnnee(periode[0].lower())
                    except:
                        mois,annee="TO","GL"
            elif periode[0].lower()=="mois":
                mois,annee=strftime("%m"),strftime("%y")
            elif periode[0].lower()=="annee":
                mois,annee="TO",strftime("%y")

        curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'perso','{2}','{3}','{4}','None','None',1,1,'countDesc',False)".format(interaction.id,interaction.user.id,option,mois,annee))
        ligne=curseurCMD.execute("SELECT * FROM commandes WHERE MessageID={0}".format(interaction.id)).fetchone()
        
        connexion,curseur=connectSQL(interaction.guild_id,option,"Stats",mois,annee)

        author=ligne["AuthorID"]
        pagemax=setMax(curseur.execute("SELECT COUNT() as Nombre FROM perso{0}{1}{2}".format(mois,annee,author)).fetchone()["Nombre"])
        page=1
        
        if annee=="GL":
            title="Perso général {0}".format(option.lower())
        elif mois=="TO":
            title="Perso {0} 20{1}".format(option.lower(),annee)
        else:
            title="Perso {0} {1} 20{2}".format(option.lower(),tableauMois[mois].lower(),annee)

        embed=await statsEmbed("perso{0}{1}{2}".format(mois,annee,author),ligne,page,pagemax,option,guildOT,bot,False,False,curseur)
        embed.title=title
        user=interaction.guild.get_member(author)
        if user!=None:
            embed=auteur(user.id,user.name,user.avatar,embed,"user")
            embed.colour=user.color.value
        else:
            embed=auteur(bot.user.id,"Ancien membre",bot.user.avatar,embed,"user")
            embed.colour=0x3498db
        await sendSlash(interaction,embed,curseurCMD,connexionCMD,page,pagemax)
        
    else:
        await interaction.response.send_message(embed=embedAssertClassic("Impossible de trouver ce que vous cherchez.\nSoit le module de stats est désactivé, soit la table cherchée cherché n'existe pas."))
