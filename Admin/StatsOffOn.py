from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.Embeds import createEmbed, embedAssert

async def statsOffOn(ctx,bot,guild,state):
    connexion,curseur=connectSQL(guild.id,"Guild","Guild",None,None)
    if curseur.execute("SELECT * FROM stats").fetchone()["Active"]==state:
        if state:
            await ctx.send(embed=embedAssert("Les statistiques de votre serveur sont déjà activées."))
        else:
            await ctx.send(embed=embedAssert("Les statistiques de votre serveur sont déjà désactivées."))
        return
    curseur.execute("UPDATE stats SET Active={0}".format(state))
    curseur.execute("UPDATE modulesCMD SET Statut={0} WHERE Module='Stats'".format(state))
    if state:
        await ctx.send(embed=createEmbed("Statistiques activées","Vous avez réactivé les statistiques pour votre serveur. Les commandes associées sont réactivées aussi.",0x220cc9,ctx.invoked_with.lower(),ctx.guild))
    else:
        await ctx.send(embed=createEmbed("Statistiques désactivées","Vous avez désactivé les statistiques pour votre serveur. Les commandes associées le sont aussi.",0x220cc9,ctx.invoked_with.lower(),ctx.guild))
    connexion.commit()
    guild.getPerms(curseur)
    guild.getStats(curseur)