from Core.Fonctions.Embeds import embedAssert, exeErrorExcept
from Titres.Achat import achatTitre
from Titres.Vente import venteTitre
from Titres.Set import setTitre
from Titres.Trade import tradeTitre
from Titres.Info import infosTitre

async def exeTitres(ctx,bot,args):
    try:
        assert len(args)>0, "Vous devez me donner l'ID d'un titre !"
        if ctx.invoked_with=="achat":
            await achatTitre(ctx,args[0],bot,False)
        elif ctx.invoked_with=="gift":
            await achatTitre(ctx,args[0],bot,True)
        elif ctx.invoked_with=="vente":
            await venteTitre(ctx,args[0],bot)
        elif ctx.invoked_with=="set":
            await setTitre(ctx,args[0],bot)
        elif ctx.invoked_with=="trade":
            await tradeTitre(ctx,args[0],bot)
        elif ctx.invoked_with=="infos":
            await infosTitre(ctx,args[0],bot)
    except AssertionError as er:
        embed=embedAssert(str(er))
    except:
        embed=await exeErrorExcept(ctx,bot,args)
    await ctx.send(embed=embed)