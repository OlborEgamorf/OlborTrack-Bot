from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.Embeds import createEmbed

async def wikiNSFW(ctx,bot,guildOT):
    dictBool={False:"désactivé",True:"activé"}
    connexion,curseur=connectSQL(ctx.guild.id,"Guild","Guild",None,None)
    etat=curseur.execute("SELECT * FROM wikinsfw").fetchone()
    curseur.execute("UPDATE wikinsfw SET Active={0}".format(bool(int(etat["Active"])-1)))
    embedTable=createEmbed("Wikipedia NSFW","Paramètre {0}.".format(dictBool[bool(int(etat["Active"])-1)]),0x220cc9,ctx.invoked_with.lower(),ctx.guild)
    connexion.commit()
    guildOT.getWikiNSFW()
    await ctx.reply(embed=embedTable)