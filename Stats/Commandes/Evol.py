from time import strftime
from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.GetPeriod import getAnnee, getMois
from Core.Fonctions.GetNom import getAuthor
from Core.Fonctions.setMaxPage import setMax, setPage
from Core.Fonctions.GetTable import collapseEvol
from Stats.Embeds.Central import statsEmbed
from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.Embeds import embedAssert, newDescip, sendEmbed
from Stats.SQL.Verification import verifCommands


tableauMois={"01":"Janvier","02":"Février","03":"Mars","04":"Avril","05":"Mai","06":"Juin","07":"Juillet","08":"Aout","09":"Septembre","10":"Octobre","11":"Novembre","12":"Décembre","TO":"Année","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","glob":"GL","to":"TO"}

async def statsEvol(ctx,option,turn,react,ligne,guildOT,bot):
    try:
        assert verifCommands(guildOT,option)
        connexionCMD,curseurCMD=connectSQL(ctx.guild.id,"Commandes","Guild",None,None)
        if not react:
            if len(ctx.args)==2 or ctx.args[2].lower() not in ("mois","annee"):
                try:
                    mois,annee,obj=getMois(ctx.args[2].lower()),getAnnee(ctx.args[3].lower()),getAuthor(option,ctx,4)
                except:
                    try:
                        mois,annee,obj="to",getAnnee(ctx.args[2].lower()),getAuthor(option,ctx,3)
                    except:
                        mois,annee,obj="glob","",getAuthor(option,ctx,2)
            elif ctx.args[2].lower()=="mois":
                mois,annee,obj=tableauMois[strftime("%m")].lower(),strftime("%y"),getAuthor(option,ctx,3)
            elif ctx.args[2].lower()=="annee":
                mois,annee,obj="to",strftime("%y"),getAuthor(option,ctx,3)
                
            assert obj!=None
            curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'evol','{2}','{3}','{4}','{5}','True',1,1,'dateAsc',False)".format(ctx.message.id,ctx.author.id,option,mois,annee,obj))
            ligne=curseurCMD.execute("SELECT * FROM commandes WHERE MessageID={0}".format(ctx.message.id)).fetchone()
        else:
            mois,annee,obj=ligne["Args1"],ligne["Args2"],ligne["Args3"]
        
        connexion,curseur=connectSQL(ctx.guild.id,option,"Stats",tableauMois[mois],annee)

        if ligne["Args4"]=="False":
            pagemax=setMax(curseur.execute("SELECT COUNT() as Nombre FROM evol{0}{1}{2}".format(mois,annee,obj)).fetchone()["Nombre"])
        else:
            pagemax=setMax(len(collapseEvol(curseur.execute("SELECT * FROM evol{0}{1}{2}".format(mois,annee,obj)).fetchall())))
        
        page=setPage(ligne["Page"],pagemax,turn)
        collapse=bool(ligne["Args4"])

        if mois=="glob":
            title="Évolution classement général {0}".format(option.lower())
        elif mois=="to":
            title="Évolution classement {0} 20{1}".format(option.lower(),annee)
        else:
            title="Évolution classement {0} {1} 20{2}".format(option.lower(),mois,annee)

        embed=await statsEmbed("evol{0}{1}{2}".format(mois,annee,obj),ligne,page,pagemax,"Evol",guildOT,bot,True,collapse,curseur)
        embed.title=title
        
        if option in ("Voice","Messages","Mots","Mentions","Mentionne"):
            user=ctx.guild.get_member(int(obj))
            if user!=None:
                embed=auteur(user.id,user.name,user.avatar,embed,"user")
                embed.colour=user.color.value
            else:
                embed=auteur(bot.user.id,"Ancien membre",bot.user.avatar,embed,"user")
                embed.colour=0x3498db
        else:
            embed.description=newDescip(embed.description,option,obj,guildOT,bot)
            embed=auteur(ctx.guild.id,ctx.guild.name,ctx.guild.icon,embed,"guild")
            embed.colour=0x3498db
        await sendEmbed(ctx,embed,react,True,curseurCMD,connexionCMD,page,pagemax)
        
    except:
        if react:
            await ctx.reply(embed=embedAssert("Impossible de trouver ce que vous cherchez.\nSoit le module de stats est désactivé, soit la table cherchée n'existe plus."))
        else:
            await ctx.reply(embed=embedAssert("Impossible de trouver ce que vous cherchez.\nSoit le module de stats est désactivé, soit la table cherchée cherché n'existe pas.\nVérifiez les arguments de la commande : {0}".format(ctx.command.usage)))