from Stats.SQL.ConnectSQL import connectSQL
from Outils.Tableaux.ModifTab import addTableau, chanTableau, delTableau, nbTableau 
from Core.Fonctions.Embeds import embedAssert, exeErrorExcept

async def exeTableau(ctx,bot,args,guild):
    try:
        connexion,curseur=connectSQL(ctx.guild.id,"Guild","Guild",None,None)
        if len(args)==0:
            pass
        elif args[0].lower()=="add":
            embed=await addTableau(ctx,bot,args,curseur)
        elif args[0].lower()=="chan":
            embed=await chanTableau(ctx,bot,args,curseur)
        elif args[0].lower()=="del":
            embed=await delTableau(ctx,bot,args,curseur,guild)
        elif args[0].lower()=="nb":
            embed=await nbTableau(ctx,args,curseur)
        connexion.commit()
        guild.getStar()
    except AssertionError as er:
        embed=embedAssert(str(er))
    except:
        embed=await exeErrorExcept(ctx,bot,args)
    await ctx.send(embed=embed)