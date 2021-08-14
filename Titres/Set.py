from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.Embeds import createEmbed, embedAssert

async def setTitre(ctx,idtitre,bot):
    try:
        connexion,curseur=connectSQL("OT","Titres","Titres",None,None)
        connexionUser,curseurUser=connectSQL("OT",ctx.author.id,"Titres",None,None)
        titre=curseurUser.execute("SELECT * FROM titresUser WHERE ID={0}".format(idtitre)).fetchone()
        assert titre!=None, "Vous ne possèdez pas ce titre."
        if curseur.execute("SELECT * FROM active WHERE MembreID={0}".format(ctx.author.id)).fetchone()==None:
            curseur.execute("INSERT INTO active VALUES({0},{1})".format(idtitre,ctx.author.id))
        else:
            curseur.execute("UPDATE active SET TitreID={0} WHERE MembreID={1}".format(idtitre,ctx.author.id))
        embed=createEmbed("Titre équipé","Titre équipé avec succès !\nVotre nouveau titre est maintenant : **{0}**.".format(titre["Nom"]),0xf58d1d,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.author)
        await ctx.reply(embed=embed)
        connexion.commit()
    except AssertionError as er:
        await ctx.reply(embed=embedAssert(er))