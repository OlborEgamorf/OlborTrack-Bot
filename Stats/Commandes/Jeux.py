from time import strftime
from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.GetPeriod import getAnnee, getMois
from Core.Fonctions.setMaxPage import setMax, setPage
from Stats.Embeds.Central import statsEmbed
from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.Embeds import embedAssert, sendEmbed

tableauMois={"01":"Janvier","02":"Février","03":"Mars","04":"Avril","05":"Mai","06":"Juin","07":"Juillet","08":"Aout","09":"Septembre","10":"Octobre","11":"Novembre","12":"Décembre","TO":"Année","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","glob":"GL","to":"TO"}
dictOption={"tortues":"Tortues","tortuesduo":"TortuesDuo","trivialversus":"TrivialVersus","trivialbr":"TrivialBR","trivialparty":"TrivialParty","p4":"P4","bataillenavale":"BatailleNavale","cross":"Cross","codenames":"CodeNames"}

async def statsJeux(ctx,turn,react,ligne,guildOT,bot,mode):
    try:
        connexionCMD,curseurCMD=connectSQL(ctx.guild.id,"Commandes","Guild",None,None)
        if not react:
            assert ctx.args[2].lower() in ("tortues","tortuesduo","trivialversus","trivialbr","trivialparty","p4","bataillenavale","cross","codenames")
            option=ctx.args[2].lower()
            if len(ctx.args)==3 or ctx.args[3].lower() not in ("mois","annee"):
                try:
                    mois,annee=getMois(ctx.args[3].lower()),getAnnee(ctx.args[4].lower())
                except:
                    try:
                        mois,annee="to",getAnnee(ctx.args[3].lower())
                    except:
                        mois,annee="glob",""
            elif ctx.args[3].lower()=="mois":
                mois,annee=tableauMois[strftime("%m")].lower(),strftime("%y")
            elif ctx.args[3].lower()=="annee":
                mois,annee="to",strftime("%y")

            curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'jeux','{2}','{3}','{4}','{5}','None',1,1,'countDesc',False)".format(ctx.message.id,ctx.author.id,option,mois,annee,mode))
            ligne=curseurCMD.execute("SELECT * FROM commandes WHERE MessageID={0}".format(ctx.message.id)).fetchone()
        else:
            mois,annee=ligne["Args1"],ligne["Args2"]
            option=ligne["Option"]
        
        connexion,curseur=connectSQL(mode,dictOption[option],"Jeux",tableauMois[mois],annee)

        pagemax=setMax(curseur.execute("SELECT COUNT() as Nombre FROM {0}{1}".format(mois,annee)).fetchone()["Nombre"])

        page=setPage(ligne["Page"],pagemax,turn)

        if mois=="glob":
            title="Classement général {0}".format(option.lower())
            evol=True
        elif mois=="to":
            title="Classement {0} 20{1}".format(option.lower(),annee)
            evol=True if annee==strftime("%y") else False
        else:
            title="Classement {0} {1} 20{2}".format(option.lower(),mois,annee)
            evol=True if tableauMois[mois]==strftime("%m") and annee==strftime("%y") else False

        embed=await statsEmbed("{0}{1}".format(mois,annee),ligne,page,pagemax,option,ctx.guild,bot,evol,False,curseur)
        embed.title=title
        if mode=="OT":
            embed=auteur(ctx.guild.get_member(699728606493933650),None,None,embed,"olbor")
        else:
            embed=auteur(ctx.guild.id,ctx.guild.name,ctx.guild.icon,embed,"guild")
        embed.colour=0x3498db
        await sendEmbed(ctx,embed,react,True,curseurCMD,connexionCMD,page,pagemax)
    
    except:
        if react:
            await ctx.reply(embed=embedAssert("Impossible de trouver ce que vous cherchez.\nLe classement cherché n'existe plus ou alors il y a un problème de mon côté."))
        else:
            await ctx.reply(embed=embedAssert("Impossible de trouver ce que vous cherchez.\nLe classement cherché n'existe pas ou alors il y a un problème de mon côté.\nVérifiez les arguments de la commande : {0}".format(ctx.command.usage)))