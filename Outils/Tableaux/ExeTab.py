from Stats.SQL.ConnectSQL import connectSQL
from Outils.Tableaux.ModifTab import addTableau, chanTableau, delTableau, nbTableau 
from Core.Fonctions.Embeds import embedAssert, exeErrorExcept
from Outils.Tableaux.EmbedsTab import commandeSB

async def exeTableau(ctx,bot,args,guildOT):
    try:
        connexion,curseur=connectSQL(ctx.guild.id,"Guild","Guild",None,None)
        if len(args)==0:
            await commandeSB(ctx,None,False,None,bot,guildOT,curseur)
            return
        elif args[0].lower()=="add":
            embed=await addTableau(ctx,bot,args,curseur)
        elif args[0].lower()=="chan":
            embed=await chanTableau(ctx,bot,args,curseur)
        elif args[0].lower()=="del":
            embed=await delTableau(ctx,bot,args,curseur,guildOT)
        elif args[0].lower()=="nb":
            embed=await nbTableau(ctx,args,curseur)
        else:
            await commandeSB(ctx,None,False,None,bot,guildOT,curseur)
            return 
        connexion.commit()
        guildOT.getStar()
    except AssertionError as er:
        embed=embedAssert(str(er))
    except:
        embed=await exeErrorExcept(ctx,bot,args)
    await ctx.send(embed=embed)