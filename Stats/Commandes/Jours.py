from time import strftime

from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.Embeds import embedAssertClassic, sendEmbed
from Core.Fonctions.GetPeriod import getAnnee, getMois
from Core.Fonctions.GetTable import getTableDay
from Core.Fonctions.setMaxPage import setMax, setPage
from Stats.Embeds.Evol import embedEvol
from Stats.SQL.ConnectSQL import connectSQL
from Stats.SQL.Verification import verifCommands

tableauMois={"01":"Janvier","02":"Février","03":"Mars","04":"Avril","05":"Mai","06":"Juin","07":"Juillet","08":"Aout","09":"Septembre","10":"Octobre","11":"Novembre","12":"Décembre","TO":"Année","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","glob":"GL","to":"TO"}
dictTriField={"countAsc":"Compteur croissant","rankAsc":"Rang croissant","countDesc":"Compteur décroissant","rankDesc":"Rang décroissant","dateAsc":"Date croissante","dateDesc":"Date décroissante","periodAsc":"Date croissante","periodDesc":"Date décroissante","moyDesc":"Moyenne décroissante","nombreDesc":"Compteur décroissant","winAsc":"Victoires croissant","winDesc":"Victoires décroissant","loseAsc":"Défaites croissant","loseDesc":"Défaites décroissant","expDesc":"Expérience décroissant","expAsc":"Expérience croissant"}

async def statsJours(ctx,option,turn,react,ligne,guildOT,bot):
    try:
        assert verifCommands(guildOT,option)
        connexionCMD,curseurCMD=connectSQL(ctx.guild.id,"Commandes","Guild",None,None)
        if not react:
            if len(ctx.args)==2 or ctx.args[2].lower() not in ("mois","annee"):
                try:
                    mois,annee=tableauMois[getMois(ctx.args[2].lower())],getAnnee(ctx.args[3].lower())
                except:
                    try:
                        mois,annee="to",getAnnee(ctx.args[2].lower())
                    except:
                        mois,annee="glob",""
            elif ctx.args[2].lower()=="mois":
                mois,annee=strftime("%m"),strftime("%y")
            elif ctx.args[2].lower()=="annee":
                mois,annee="to",strftime("%y")

            curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'day','{2}','{3}','{4}','None','None',1,1,'countDesc',False)".format(ctx.message.id,ctx.author.id,option,mois,annee))
            ligne=curseurCMD.execute("SELECT * FROM commandes WHERE MessageID={0}".format(ctx.message.id)).fetchone()
        else:
            mois,annee=ligne["Args1"],ligne["Args2"]

        connexion,curseur=connectSQL(ctx.guild.id,option,"Stats","GL","")

        table=getTableDay(curseur,mois,annee,ligne["Tri"])
        print(table,mois,annee)
        pagemax=setMax(len(table))
        page=setPage(ligne["Page"],pagemax,turn)
        author=ligne["AuthorID"]

        if mois=="glob":
            title="Classement jours {0}".format(option.lower())
        elif mois=="to":
            title="Classement jours {0} 20{1}".format(option.lower(),annee)
        else:
            title="Classement jours {0} {1} 20{2}".format(option.lower(),tableauMois[mois],annee)

        embed=embedEvol(table,page,ligne["Mobile"],False,False,option)
        embed.title=title
        user=ctx.guild.get_member(author)
        embed=auteur(user.id,user.name,user.avatar,embed,"user")
        embed.colour=user.color.value
        embed.add_field(name="Tri <:otTRI:833666016491864114>",value=dictTriField[ligne["Tri"]],inline=True)
        embed.set_footer(text="Page {0}/{1}".format(page,pagemax))
        await sendEmbed(ctx,embed,react,True,curseurCMD,connexionCMD,page,pagemax)
        
    except:
        if react:
            await ctx.reply(embed=embedAssertClassic("Impossible de trouver ce que vous cherchez.\nSoit le module de stats est désactivé, soit le classement cherché n'existe plus."))
        else:
            await ctx.reply(embed=embedAssertClassic("Impossible de trouver ce que vous cherchez.\nSoit le module de stats est désactivé, soit le classement cherché n'existe pas.\nVérifiez les arguments de la commande : {0}".format(ctx.command.usage)))
