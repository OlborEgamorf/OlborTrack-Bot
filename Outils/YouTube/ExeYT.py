from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.Embeds import embedAssert, exeErrorExcept, sendEmbed
from Core.Fonctions.setMaxPage import setMax, setPage
from Outils.YouTube.EmbedsYT import embedYT
from Outils.YouTube.ModifYT import addYT, chanYT, delYT, descipYT
from Stats.SQL.ConnectSQL import connectSQL


async def exeYTAlerts(ctx,bot,args,guildOT):
    try:
        connexion,curseur=connectSQL(ctx.guild.id,"Guild","Guild",None,None)
        if ctx.invoked_with=="youtube":
            await commandeYT(ctx,None,False,None,bot,guildOT,curseur)
            return
        elif ctx.invoked_with=="add":
            embed=await addYT(ctx,bot,args)
        elif ctx.invoked_with=="chan":
            embed=await chanYT(ctx,bot,args,curseur)
        elif ctx.invoked_with=="del":
            embed=await delYT(ctx,bot,args,curseur,guildOT)
        elif ctx.invoked_with=="edit":
            embed=await descipYT(ctx,bot,args,curseur,guildOT)
        connexion.commit()
        guildOT.getYouTube()
    except AssertionError as er:
        embed=embedAssert(str(er))
    except:
        embed=await exeErrorExcept(ctx,bot,args)
    await ctx.send(embed=embed)


async def commandeYT(ctx,turn,react,ligne,bot,guildOT,curseur):
    connexionCMD,curseurCMD=connectSQL(ctx.guild.id,"Commandes","Guild",None,None)
    if not react:
        assert guildOT.yt!=[], "Aucune alerte n'est configurée pour votre serveur."
        pagemax=setMax(len(guildOT.stardict))
        curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'youtube','None','None','None','None','None',1,{2},'countDesc',False)".format(ctx.message.id,ctx.author.id,pagemax))
        ligne=curseurCMD.execute("SELECT * FROM commandes WHERE MessageID={0}".format(ctx.message.id)).fetchone()
    else:
        connexion,curseur=connectSQL(ctx.guild.id,"Guild","Guild",None,None)
        pagemax=setMax(len(guildOT.stardict))

    mobile=ligne["Mobile"]
    table=curseur.execute("SELECT * FROM youtube ORDER BY Nombre ASC").fetchall()
    page=setPage(ligne["Page"],pagemax,turn)

    embed=embedYT(table,page,pagemax,mobile)
    embed=auteur(ctx.guild.id,ctx.guild.name,ctx.guild.icon,embed,"guild")
    message=await sendEmbed(ctx,embed,react,False,curseurCMD,connexionCMD,page,pagemax)
    if not react:
        await message.add_reaction("<:otMOBILE:833736320919797780>")
