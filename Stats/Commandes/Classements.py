from time import strftime
from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.GetPeriod import getAnnee, getMois
from Core.Fonctions.GetNom import getObj
from Stats.Commandes.FirstAnnee import statsFirst
from Core.Fonctions.setMaxPage import setMax, setPage
from Stats.Embeds.Central import statsEmbed
from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.Embeds import embedAssert, newDescip, sendEmbed


tableauMois={"01":"Janvier","02":"Février","03":"Mars","04":"Avril","05":"Mai","06":"Juin","07":"Juillet","08":"Aout","09":"Septembre","10":"Octobre","11":"Novembre","12":"Décembre","TO":"Année","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","glob":"GL","to":"TO"}

async def statsRank(ctx,option,turn,react,ligne,guildOT,bot):
    try:
        connexionCMD,curseurCMD=connectSQL(ctx.guild.id,"Commandes","Guild",None,None)
        if not react:
            if len(ctx.args)==2 or ctx.args[2].lower() not in ("mois","annee"):
                try:
                    mois,annee,obj=getMois(ctx.args[2].lower()),getAnnee(ctx.args[3].lower()),getObj(option,ctx,4)
                except:
                    try:
                        await statsFirst(ctx,option,guildOT,bot)
                        return
                    except:
                        try:
                            mois,annee,obj="to",getAnnee(ctx.args[2].lower()),getObj(option,ctx,3)
                        except:
                            mois,annee,obj="glob","",getObj(option,ctx,2)
            elif ctx.args[2].lower()=="mois":
                mois,annee,obj=tableauMois[strftime("%m")].lower(),strftime("%y"),getObj(option,ctx,3)
            elif ctx.args[2].lower()=="annee":
                mois,annee,obj="to",strftime("%y"),getObj(option,ctx,3)

            curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'rank','{2}','{3}','{4}','{5}','None',1,1,'countDesc',False)".format(ctx.message.id,ctx.author.id,option,mois,annee,obj))
            ligne=curseurCMD.execute("SELECT * FROM commandes WHERE MessageID={0}".format(ctx.message.id)).fetchone()
        else:
            mois,annee=ligne["Args1"],ligne["Args2"]
        
        connexion,curseur=connectSQL(ctx.guild.id,option,"Stats",tableauMois[mois],annee)

        if ligne["Args3"]=="None":
            pagemax=setMax(curseur.execute("SELECT COUNT() as Nombre FROM {0}{1}".format(mois,annee)).fetchone()["Nombre"])
        else:
            pagemax=setMax(curseur.execute("SELECT COUNT() as Nombre FROM {0}{1}{2}".format(mois,annee,ligne["Args3"])).fetchone()["Nombre"])

        page=setPage(ligne["Page"],pagemax,turn)
        obj="" if ligne["Args3"]=="None" else ligne["Args3"]
        if obj!="":
            tempOption=option
            if option=="Voicechan":
                option="Voice"
            else:
                option="Messages"

        if mois=="glob":
            title="Classement général {0}".format(option.lower())
            evol=True if obj=="" else False
        elif mois=="to":
            title="Classement {0} 20{1}".format(option.lower(),annee)
            evol=True if annee==strftime("%y") and obj=="" else False
        else:
            title="Classement {0} {1} 20{2}".format(option.lower(),mois,annee)
            evol=True if tableauMois[mois]==strftime("%m") and annee==strftime("%y") and obj=="" else False

        embed=await statsEmbed("{0}{1}{2}".format(mois,annee,obj),ligne,page,pagemax,option,guildOT,bot,evol,False,curseur)
        embed.title=title
        embed=auteur(ctx.guild.id,ctx.guild.name,ctx.guild.icon,embed,"guild")
        embed.colour=0x3498db
        if obj!="":
            embed.description=newDescip(embed.description,tempOption,obj,guildOT,bot)
        await sendEmbed(ctx,embed,react,True,curseurCMD,connexionCMD,page,pagemax)
    
    except:
        await ctx.reply(embed=embedAssert("Impossible de trouver ce que vous cherchez."))