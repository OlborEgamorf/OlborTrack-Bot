from random import randint
from Core.Fonctions.Embeds import createEmbed
from Core.Decorator import OTCommand

@OTCommand
async def exeDice(ctx,bot,args):
    """Cette fonction simule le lancer de 1 à 75 dés, et renvoie le résultat."""
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
    while numb!=0:
        lancer=randint(1,6)
        somme+=lancer
        descip+=dictDe[lancer]+" "
        numb-=1
    await ctx.reply(embed=createEmbed("Lancer de dé(s)","{0}\nCela fait un total de **{1}** !".format(descip,somme),0x2ba195,ctx.invoked_with.lower(),ctx.author))
