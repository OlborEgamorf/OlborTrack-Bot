from time import strftime

from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.Embeds import embedAssertClassic, sendEmbed
from Core.Fonctions.GetPeriod import getAnnee, getMois
from Core.Fonctions.setMaxPage import setMax, setPage
from Stats.Embeds.Central import statsEmbed
from Stats.SQL.ConnectSQL import connectSQL
from Stats.SQL.Verification import verifCommands

tableauMois={"01":"Janvier","02":"Février","03":"Mars","04":"Avril","05":"Mai","06":"Juin","07":"Juillet","08":"Aout","09":"Septembre","10":"Octobre","11":"Novembre","12":"Décembre","TO":"Année","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","glob":"GL","to":"TO"}

async def statsPerso(ctx,option,turn,react,ligne,guildOT,bot):
    try:
        assert verifCommands(guildOT,option)
        connexionCMD,curseurCMD=connectSQL(ctx.guild.id,"Commandes","Guild",None,None)
        if not react:
            if len(ctx.args)==2 or ctx.args[2].lower() not in ("mois","annee"):
                try:
                    mois,annee=tableauMois[getMois(ctx.args[2].lower())],getAnnee(ctx.args[3].lower())
                except:
                    try:
                        mois,annee="TO",getAnnee(ctx.args[2].lower())
                    except:
                        mois,annee="TO","GL"
            elif ctx.args[2].lower()=="mois":
                mois,annee=strftime("%m"),strftime("%y")
            elif ctx.args[2].lower()=="annee":
                mois,annee="TO",strftime("%y")                

            curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'perso','{2}','{3}','{4}','None','None',1,1,'countDesc',False)".format(ctx.message.id,ctx.author.id,option,mois,annee))
            ligne=curseurCMD.execute("SELECT * FROM commandes WHERE MessageID={0}".format(ctx.message.id)).fetchone()
        else:
            mois,annee=ligne["Args1"],ligne["Args2"]
        
        connexion,curseur=connectSQL(ctx.guild.id,option,"Stats",mois,annee)

        author=ligne["AuthorID"]
        pagemax=setMax(curseur.execute("SELECT COUNT() as Nombre FROM perso{0}{1}{2}".format(mois,annee,author)).fetchone()["Nombre"])
        page=setPage(ligne["Page"],pagemax,turn)
        
        if annee=="GL":
            title="Perso général {0}".format(option.lower())
        elif mois=="TO":
            title="Perso {0} 20{1}".format(option.lower(),annee)
        else:
            title="Perso {0} {1} 20{2}".format(option.lower(),tableauMois[mois].lower(),annee)

        embed=await statsEmbed("perso{0}{1}{2}".format(mois,annee,author),ligne,page,pagemax,option,guildOT,bot,False,False,curseur)
        embed.title=title
        user=ctx.guild.get_member(author)
        if user!=None:
            embed=auteur(user.id,user.name,user.avatar,embed,"user")
            embed.colour=user.color.value
        else:
            embed=auteur(bot.user.id,"Ancien membre",bot.user.avatar,embed,"user")
            embed.colour=0x3498db
        await sendEmbed(ctx,embed,react,True,curseurCMD,connexionCMD,page,pagemax)
        
    except:
        if react:
            await ctx.reply(embed=embedAssertClassic("Impossible de trouver ce que vous cherchez.\nSoit le module de stats est désactivé, soit la table cherchée n'existe plus."))
        else:
            await ctx.reply(embed=embedAssertClassic("Impossible de trouver ce que vous cherchez.\nSoit le module de stats est désactivé, soit la table cherchée cherché n'existe pas.\nVérifiez les arguments de la commande : {0}".format(ctx.command.usage)))
