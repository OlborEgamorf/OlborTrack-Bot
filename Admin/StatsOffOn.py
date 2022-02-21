from Core.Decorator import OTCommand
from Core.Fonctions.Embeds import createEmbed
from Stats.SQL.ConnectSQL import connectSQL


@OTCommand
async def statsOffOn(ctx,guild,state):
    connexion,curseur=connectSQL(guild.id,"Guild","Guild",None,None)
    if curseur.execute("SELECT * FROM stats").fetchone()["Active"]==state:
        if state:
            raise AssertionError("Les statistiques de votre serveur sont déjà activées.")
        else:
            raise AssertionError("Les statistiques de votre serveur sont déjà désactivées.")
    curseur.execute("UPDATE stats SET Active={0}".format(state))
    curseur.execute("UPDATE modulesCMD SET Statut={0} WHERE Module='Stats'".format(state))
    if state:
        await ctx.reply(embed=createEmbed("Statistiques activées","Vous avez réactivé les statistiques pour votre serveur. Les commandes associées sont réactivées aussi.",0x220cc9,ctx.invoked_with.lower(),ctx.guild))
    else:
        await ctx.reply(embed=createEmbed("Statistiques désactivées","Vous avez désactivé les statistiques pour votre serveur. Les commandes associées le sont aussi.",0x220cc9,ctx.invoked_with.lower(),ctx.guild))
    connexion.commit()
    guild.getPerms(curseur)
    guild.getStats(curseur)
