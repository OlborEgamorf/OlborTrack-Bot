from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.setMaxPage import setMax, setPage
from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.Embeds import embedAssert, exeErrorExcept, sendEmbed
from Outils.Twitch.ModifTwitch import addTwitch, chanTwitch, delTwitch, descipTwitch
from Outils.Twitch.EmbedsTwitch import embedTwitch
from Core.OTGuild import OTGuild

async def exeTwitch(ctx,bot,args,guildOT):
    try:
        connexion,curseur=connectSQL(ctx.guild.id,"Guild","Guild",None,None)
        if len(args)==0:
            await commandeTwitch(ctx,None,False,None,bot,guildOT,curseur)
            return
        elif args[0].lower()=="add":
            embed=await addTwitch(ctx,bot,args,curseur)
        elif args[0].lower()=="chan":
            embed=await chanTwitch(ctx,bot,args,curseur)
        elif args[0].lower()=="del":
            embed=await delTwitch(ctx,bot,args,curseur,guildOT)
        elif args[0].lower()=="edit":
            embed=await descipTwitch(ctx,bot,args,curseur,guildOT)
        connexion.commit()
        guildOT.getTwitch()
    except AssertionError as er:
        embed=embedAssert(str(er))
    except:
        embed=await exeErrorExcept(ctx,bot,args)
    await ctx.send(embed=embed)


async def commandeTwitch(ctx,turn,react,ligne,bot,guildOT:OTGuild,curseur):
    connexionCMD,curseurCMD=connectSQL(ctx.guild.id,"Commandes","Guild",None,None)
    if not react:
        assert guildOT.stardict!={}, "Aucun tableau n'est configuré pour votre serveur."
        pagemax=setMax(len(guildOT.stardict))
        curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'twitch','None','None','None','None','None',1,{2},'countDesc',False)".format(ctx.message.id,ctx.author.id,pagemax))
        ligne=curseurCMD.execute("SELECT * FROM commandes WHERE MessageID={0}".format(ctx.message.id)).fetchone()
    else:
        connexion,curseur=connectSQL(ctx.guild.id,"Guild","Guild",None,None)
        pagemax=setMax(len(guildOT.stardict))

    mobile=ligne["Mobile"]
    table=curseur.execute("SELECT * FROM twitch ORDER BY Nombre ASC").fetchall()
    page=setPage(ligne["Page"],pagemax,turn)

    embed=embedTwitch(table,page,pagemax,mobile)
    embed=auteur(ctx.guild.id,ctx.guild.name,ctx.guild.icon,embed,"guild")
    message=await sendEmbed(ctx,embed,react,False,curseurCMD,connexionCMD,page,pagemax)
    if not react:
        await message.add_reaction("<:otMOBILE:833736320919797780>")