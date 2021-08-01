from random import randint
import discord
from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.Embeds import exeErrorExcept, embedAssert


async def exeDice(ctx,bot,args):
    """Cette fonction simule le lancer de 1 à 75 dés, et renvoie le résultat."""
    try:
        dictDe={1:"<:ot1:705766186909958185>",2:"<:ot2:705766186989912154>",3:"<:ot3:705766186930929685>",4:"<:ot4:705766186947706934>",5:"<:ot5:705766186713088042>",6:"<:ot6:705766187182850148>"}
        if len(args)==0:
            numb=1
        else:
            try:
                numb=int(args[0])
            except:
                numb=-666
        assert numb<=75 and numb>0,"Le nombre donné n'est pas valide ! Le minimum est 1 et le maximum 75."
        somme,descip=0,""
        for i in range(numb):
            lancer=randint(1,6)
            somme+=lancer
            descip+=dictDe[lancer]+" "
        embedTable=discord.Embed(title="Lancer de dé(s)", description=descip+"\nCela fait un total de **"+str(somme)+"** !", color=0x2ba195)
        embedTable=auteur(ctx.author.id,ctx.author.name,ctx.author.avatar,embedTable,"user")
        embedTable.set_footer(text="OT!dice")
    except AssertionError as er:
        embedTable=embedAssert(str(er))
    except:
        embedTable=await exeErrorExcept(ctx,bot,args)
    await ctx.send(embed=embedTable)
    return