from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.Embeds import embedAssert, newDescip, sendEmbed
from Core.Fonctions.GetNom import getAuthor
from Core.Fonctions.GetTable import getTablePerso
from Core.Fonctions.setMaxPage import setMax, setPage
from Stats.Embeds.Mois import embedMois
from Stats.SQL.ConnectSQL import connectSQL
from Stats.SQL.Verification import verifCommands

dictTriField={"countAsc":"Compteur croissant","rankAsc":"Rang croissant","countDesc":"Compteur décroissant","rankDesc":"Rang décroissant","dateAsc":"Date croissante","dateDesc":"Date décroissante","periodAsc":"Date croissante","periodDesc":"Date décroissante","moyDesc":"Moyenne décroissante","nombreDesc":"Compteur décroissant","winAsc":"Victoires croissant","winDesc":"Victoires décroissant","loseAsc":"Défaites croissant","loseDesc":"Défaites décroissant","expDesc":"Expérience décroissant","expAsc":"Expérience croissant"}

async def statsPeriodsInter(ctx,option,turn,react,ligne,guildOT,bot):
    if True:
        assert verifCommands(guildOT,option)
        connexionCMD,curseurCMD=connectSQL(ctx.guild.id,"Commandes","Guild",None,None)
        connexion,curseur=connectSQL(ctx.guild.id,option,"Stats","GL","")
        if not react:
            author=ctx.author.id
            obj=getAuthor(option,ctx,2)
            assert obj!=None
            curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'periodsInter','{2}','{3}','None','None','None',1,1,'countDesc',False)".format(ctx.message.id,author,option,obj))
            ligne=curseurCMD.execute("SELECT * FROM commandes WHERE MessageID={0}".format(ctx.message.id)).fetchone()
        else:
            author=ligne["AuthorID"]
            obj=ligne["Args1"]

        if option in ("Salons","Voicechan"):
            assert not guildOT.chan[int(obj)]["Hide"]
        table=getTablePerso(ctx.guild.id,option,author,obj,"M",ligne["Tri"])
        pagemax=setMax(len(table))+1
        page=setPage(ligne["Page"],pagemax,turn)

        if page==pagemax:
            table=getTablePerso(ctx.guild.id,option,author,obj,"A","countDesc")
            embed=embedMois(table,1,ligne["Mobile"],ligne["Option"])
            embed.add_field(name="Tri <:otTRI:833666016491864114>",value=dictTriField["countDesc"],inline=True)
            embed.set_footer(text="Page {0}/{1}".format(page,pagemax))
        else:
            embed=embedMois(table,page,ligne["Mobile"],ligne["Option"])
            embed.add_field(name="Tri <:otTRI:833666016491864114>",value=dictTriField[ligne["Tri"]],inline=True)
            embed.set_footer(text="Page {0}/{1}".format(page,pagemax))
            
        embed.title="Périodes {0}".format(option.lower())
        embed.description=newDescip(embed.description,option,obj,guildOT,bot)
        user=ctx.guild.get_member(author)
        if user!=None:
            embed=auteur(user.id,user.name,user.avatar,embed,"user")
            embed.colour=user.color.value
        else:
            embed=auteur(bot.user.id,"Ancien membre",bot.user.avatar,embed,"user")
            embed.colour=0x3498db
        embed.colour=user.color.value

        await sendEmbed(ctx,embed,react,True,curseurCMD,connexionCMD,page,pagemax)
        
    else:
        if react:
            await ctx.reply(embed=embedAssert("Impossible de trouver ce que vous cherchez.\nSoit le module de stats est désactivé, soit la table cherchée n'existe plus ou alors est masqué par un administrateur."))
        else:
            await ctx.reply(embed=embedAssert("Impossible de trouver ce que vous cherchez.\nSoit le module de stats est désactivé, soit la table cherchée cherché n'existe pas ou alors est masqué par un administrateur.\nVérifiez les arguments de la commande : {0}".format(ctx.command.usage)))
