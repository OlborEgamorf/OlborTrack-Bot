from Core.Decorator import OTCommand
from Core.Fonctions.Embeds import createEmbed
from Stats.SQL.ConnectSQL import connectSQL


@OTCommand
async def showAnniversaire(ctx,bot):
    connexion,curseur=connectSQL("OT","Guild","Guild",None,None)
    if ctx.message.mentions!=[]:
        user=curseur.execute("SELECT * FROM anniversaires WHERE ID={0}".format(ctx.message.mentions[0].id)).fetchone()
        assert user!=None, "Cette personne n'a pas ajouté son anniversaire."
        embed=createEmbed("Anniversaire","L'anniversaire de <@{0}> est le **{1} {2}** !".format(ctx.message.mentions[0].id,user["Jour"],user["Mois"]),ctx.message.mentions[0].color.value,ctx.invoked_with.lower(),ctx.message.mentions[0])
    else:
        user=curseur.execute("SELECT * FROM anniversaires WHERE ID={0}".format(ctx.author.id)).fetchone()
        assert user!=None, "Vous n'avez pas ajouté votre anniversaire. Vous pouvez le faire avec la commande `OT!anniversaire set [jour] [mois]`"
        embed=createEmbed("Anniversaire","Vous avez affirmé que votre anniversaire est le **{0} {1}** !".format(user["Jour"],user["Mois"]),ctx.author.color.value,ctx.invoked_with.lower(),ctx.author)
    await ctx.reply(embed=embed)
