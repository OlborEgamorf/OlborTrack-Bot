

from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.GetNom import getAuthor
from Core.Fonctions.setMaxPage import setMax, setPage
from Stats.Embeds.Central import statsEmbed
from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.Embeds import embedAssert, newDescip, sendEmbed

async def statsPeriods(ctx,option,turn,react,ligne,guildOT,bot):
    if True:
        connexionCMD,curseurCMD=connectSQL(ctx.guild.id,"Commandes","Guild",None,None)
        connexion,curseur=connectSQL(ctx.guild.id,option,"Stats","GL","")
        if not react:
            author=getAuthor(option,ctx,2)
            curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'periods','{2}','None','None','None','None',1,1,'countDesc',False)".format(ctx.message.id,author,option))
            ligne=curseurCMD.execute("SELECT * FROM commandes WHERE MessageID={0}".format(ctx.message.id)).fetchone()
        else:
            author=ligne["AuthorID"]

        pagemax=setMax(curseur.execute("SELECT COUNT() as Nombre FROM persoM{0}".format(author)).fetchone()["Nombre"])+1
        page=setPage(ligne["Page"],pagemax,turn)

        if page==pagemax:
            ligne["Tri"]="countDesc"
            embed=await statsEmbed("persoA{0}".format(author),ligne,1,pagemax,"Mois",guildOT,bot,False,False,curseur)
            embed.set_footer(text="Page {0}/{1}".format(page,pagemax))
        else:
            embed=await statsEmbed("persoM{0}".format(author),ligne,page,pagemax,"Mois",guildOT,bot,False,False,curseur)
            
        embed.title="Périodes {0}".format(option.lower())
        if option in ("Voice","Messages","Mots","Mentions","Mentionne"):
            user=ctx.guild.get_member(author)
            embed=auteur(user.id,user.name,user.avatar,embed,"user")
            embed.colour=user.color.value
        else:
            embed.description=newDescip(embed.description,option,author,guildOT,bot)
            embed=auteur(ctx.guild.id,ctx.guild.name,ctx.guild.icon,embed,"guild")
            embed.colour=0x3498db
        await sendEmbed(ctx,embed,react,True,curseurCMD,connexionCMD,page,pagemax)
        
    else:
        await ctx.reply(embed=embedAssert("Impossible de trouver ce que vous cherchez."))