from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.Embeds import embedAssertClassic, sendEmbed
from Core.Fonctions.setMaxPage import setMax, setPage
from Stats.Embeds.Central import statsEmbed
from Stats.SQL.ConnectSQL import connectSQL
from Stats.SQL.Verification import verifCommands


async def statsFirstPeriods(ctx,option,turn,react,ligne,guildOT,bot):
    try:
        assert verifCommands(guildOT,option)
        connexionCMD,curseurCMD=connectSQL(ctx.guild.id,"Commandes","Guild",None,None)
        connexion,curseur=connectSQL(ctx.guild.id,option,"Stats","GL","")
        if not react:
            curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'first','{2}','None','None','None','None',1,1,'countDesc',False)".format(ctx.message.id,ctx.author.id,option))
            ligne=curseurCMD.execute("SELECT * FROM commandes WHERE MessageID={0}".format(ctx.message.id)).fetchone()
        else:
            author=ligne["AuthorID"]

        pagemax=setMax(curseur.execute("SELECT COUNT() as Nombre FROM firstM").fetchone()["Nombre"])+1
        page=setPage(ligne["Page"],pagemax,turn)

        if page==pagemax:
            ligne["Tri"]="countDesc"
            embed=await statsEmbed("firstA",ligne,1,pagemax,"First",guildOT,bot,False,False,curseur)
            embed.set_footer(text="Page {0}/{1}".format(page,pagemax))
        else:
            embed=await statsEmbed("firstM",ligne,page,pagemax,"First",guildOT,bot,False,False,curseur)
            
        embed.title="Premiers {0}".format(option.lower())
        embed=auteur(ctx.guild.id,ctx.guild.name,ctx.guild.icon,embed,"guild")
        embed.colour=0x3498db
        await sendEmbed(ctx,embed,react,True,curseurCMD,connexionCMD,page,pagemax)
        
    except:
        if react:
            await ctx.reply(embed=embedAssertClassic("Impossible de trouver ce que vous cherchez.\nSoit le module de stats est désactivé, soit la table cherchée n'existe plus ou alors est masqué par un administrateur."))
        else:
            await ctx.reply(embed=embedAssertClassic("Impossible de trouver ce que vous cherchez.\nSoit le module de stats est désactivé, soit la table cherchée cherché n'existe pas ou alors est masqué par un administrateur.\nVérifiez les arguments de la commande : {0}".format(ctx.command.usage)))
