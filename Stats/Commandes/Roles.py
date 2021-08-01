from time import strftime
from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.GetPeriod import getAnnee, getMois
from Core.Fonctions.GetNom import getObj, nomsOptions
from Core.Fonctions.GetTable import getTableRoles, getTableRolesMem
from Core.Fonctions.setMaxPage import setMax, setPage
from Stats.Embeds.Roles import embedRole
from Stats.Embeds.Membres import embedMembre
from Core.Fonctions.Embeds import embedAssert, newDescip, sendEmbed
from Core.Fonctions.AuteurIcon import auteur
from Stats.SQL.Verification import verifCommands

tableauMois={"01":"Janvier","02":"Février","03":"Mars","04":"Avril","05":"Mai","06":"Juin","07":"Juillet","08":"Aout","09":"Septembre","10":"Octobre","11":"Novembre","12":"Décembre","TO":"Année","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","glob":"GL","to":"TO"}
dictTriField={"countAsc":"Compteur croissant","rankAsc":"Rang croissant","countDesc":"Compteur décroissant","rankDesc":"Rang décroissant","dateAsc":"Date croissante","dateDesc":"Date décroissante","periodAsc":"Date croissante","periodDesc":"Date décroissante","moyDesc":"Moyenne décroissante","nombreDesc":"Compteur décroissant","winAsc":"Victoires croissant","winDesc":"Victoires décroissant","loseAsc":"Défaites croissant","loseDesc":"Défaites décroissant","expDesc":"Expérience décroissant","expAsc":"Expérience croissant"}

async def statsRoles(ctx,option,turn,react,ligne,guildOT,bot):
    try:
        assert verifCommands(guildOT,option)
        assert verifCommands(guildOT,"Roles")
        connexionCMD,curseurCMD=connectSQL(ctx.guild.id,"Commandes","Guild",None,None)
        if not react:
            if len(ctx.args)==2 or ctx.args[2].lower() not in ("mois","annee"):
                try:
                    mois,annee,obj,nb=getMois(ctx.args[2].lower()),getAnnee(ctx.args[3].lower()),getObj(option,ctx,4),5
                except:
                    try:
                        mois,annee,obj,nb="to",getAnnee(ctx.args[2].lower()),getObj(option,ctx,3),4
                    except:
                        mois,annee,obj,nb="glob","",getObj(option,ctx,2),3
            elif ctx.args[2].lower()=="mois":
                mois,annee,obj,nb=tableauMois[strftime("%m")].lower(),strftime("%y"),getObj(option,ctx,3),4
            elif ctx.args[2].lower()=="annee":
                mois,annee,obj,nb="to",strftime("%y"),getObj(option,ctx,3),4

            if option not in ("Messages","Voice","Mots"):
                assert obj!=None

            if obj==None:
                role=getObj("Roles",ctx,nb-1)
            else:
                role=getObj("Roles",ctx,nb)
            
            curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'roles','{2}','{3}','{4}','{5}','{6}',1,1,'countDesc',False)".format(ctx.message.id,ctx.author.id,option,mois,annee,obj,role))
            ligne=curseurCMD.execute("SELECT * FROM commandes WHERE MessageID={0}".format(ctx.message.id)).fetchone()
        else:
            mois,annee=ligne["Args1"],ligne["Args2"]

        connexion,curseur=connectSQL(ctx.guild.id,option,"Stats",tableauMois[mois],annee)
        obj="" if ligne["Args3"]=="None" else ligne["Args3"]
        role=ligne["Args4"]

        if option in ("Salons","Voicechan") and obj!="":
            assert not guildOT.chan[int(obj)]["Hide"]
        
        if role=="None":
            table=getTableRoles(curseur,ctx.guild,"{0}{1}{2}".format(mois,annee,obj),ligne["Tri"])
            pagemax=setMax(len(table))
            page=setPage(ligne["Page"],pagemax,turn)
            embed=embedRole(table,page,ligne["Mobile"],option)
            if obj!="":
                embed.description=newDescip(embed.description,option,obj,guildOT,bot)
            option="Roles"
            embed.colour=0x3498db
        else:
            table=getTableRolesMem(curseur,ctx.guild,int(role),"{0}{1}{2}".format(mois,annee,obj),ligne["Tri"])
            pagemax=setMax(len(table))
            page=setPage(ligne["Page"],pagemax,turn)
            embed=embedMembre(table,guildOT,page,ligne["Mobile"],ligne["AuthorID"],False,option)
            if obj=="":
                embed.description=newDescip(embed.description,"Roles",role,guildOT,bot)
            else:
                embed.description="{0}, {1}".format(nomsOptions("Roles",int(role),guildOT,bot),newDescip(embed.description,option,obj,guildOT,bot))
            embed.colour=ctx.guild.get_role(int(role)).color.value
        
        embed.add_field(name="Tri <:otTRI:833666016491864114>",value=dictTriField[ligne["Tri"]],inline=True)
        embed.set_footer(text="Page {0}/{1}".format(page,pagemax))

        if mois=="glob":
            title="Classement général {0}".format(option.lower())
        elif mois=="to":
            title="Classement {0} 20{1}".format(option.lower(),annee)
        else:
            title="Classement {0} {1} 20{2}".format(option.lower(),mois,annee)

        embed.title=title
        embed=auteur(ctx.guild.id,ctx.guild.name,ctx.guild.icon,embed,"guild")
        await sendEmbed(ctx,embed,react,True,curseurCMD,connexionCMD,page,pagemax)
        
    except:
        if react:
            await ctx.reply(embed=embedAssert("Impossible de trouver ce que vous cherchez.\nSoit le module de stats est désactivé, soit la table cherchée n'existe plus ou alors est masqué par un administrateur."))
        else:
            await ctx.reply(embed=embedAssert("Impossible de trouver ce que vous cherchez.\nSoit le module de stats est désactivé, soit la table cherchée cherché n'existe pas ou alors est masqué par un administrateur.\nVérifiez les arguments de la commande : {0}".format(ctx.command.usage)))