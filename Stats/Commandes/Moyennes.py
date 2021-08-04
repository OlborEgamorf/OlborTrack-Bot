from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.setMaxPage import setMax, setPage
from Stats.Embeds.Central import statsEmbed 
from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.Embeds import embedAssert, sendEmbed
from Stats.SQL.Verification import verifCommands

async def statsMoy(ctx,option,turn,react,ligne,guildOT,bot):
    try:
        assert verifCommands(guildOT,"Moyennes")
        connexionCMD,curseurCMD=connectSQL(ctx.guild.id,"Commandes","Guild",None,None)
        connexion,curseur=connectSQL(ctx.guild.id,"Moyennes","Stats","GL","")
        if not react:     
            curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'moy','{2}','None','None','None','None',1,1,'moyDesc',False)".format(ctx.message.id,ctx.author.id,option))
            ligne=curseurCMD.execute("SELECT * FROM commandes WHERE MessageID={0}".format(ctx.message.id)).fetchone()
            
        author=ligne["AuthorID"]
        pagemax=setMax(curseur.execute("SELECT COUNT() as Nombre FROM moy{0}{1}".format(option,ligne["AuthorID"])).fetchone()["Nombre"])
        page=setPage(ligne["Page"],pagemax,turn)
        

        embed=await statsEmbed("moy{0}{1}".format(option,author),ligne,page,pagemax,"Moy",guildOT,bot,False,False,curseur)
        embed.title="Moyennes messages envoyés - {0}".format(option.lower())
        user=ctx.guild.get_member(author)
        if user!=None:
            embed=auteur(user.id,user.name,user.avatar,embed,"user")
            embed.colour=user.color.value
        else:
            embed=auteur(bot.user.id,"Ancien membre",bot.user.avatar,embed,"user")
            embed.colour=0x3498db
        embed.colour=user.color.value
        await sendEmbed(ctx,embed,react,True,curseurCMD,connexionCMD,page,pagemax)
        
    except:
        if react:
            await ctx.reply(embed=embedAssert("Impossible de trouver ce que vous cherchez.\nSoit le module de stats est désactivé, soit la table cherchée n'existe plus."))
        else:
            await ctx.reply(embed=embedAssert("Impossible de trouver ce que vous cherchez.\nSoit le module de stats est désactivé, soit la table cherchée cherché n'existe pas.\nVérifiez les arguments de la commande : {0}".format(ctx.command.usage)))