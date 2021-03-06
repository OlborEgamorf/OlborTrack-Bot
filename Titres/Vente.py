import asyncio

from Core.Fonctions.Embeds import createEmbed, embedAssert
from Stats.SQL.ConnectSQL import connectSQL

from Titres.Outils import createAccount

dictSell={0:"Inestimable",1:150,2:300,3:500,4:"Inestimable",5:"Inestimable",6:"Inestimable"}

async def venteTitre(ctx,idtitre,bot):
    try:
        nom,valeur,coins=verifVente(ctx.author.id,idtitre)

        embed=createEmbed("Vente de Titre","Vous êtes sur le point de vendre **{0}** pour *{1} <:otCOINS:873226814527520809>*.\nVous possèdez {2} <:otCOINS:873226814527520809> au total, et en aurez {3} <:otCOINS:873226814527520809> après la transaction.\nAppuyez sur <:otVALIDER:772766033996021761> pour confirmer la vente.".format(nom,valeur,int(coins),int(coins+valeur)),0xf58d1d,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.author)
        message=await ctx.reply(embed=embed)
        await message.add_reaction("<:otVALIDER:772766033996021761>")

        def check(reaction,user):
            if type(reaction.emoji)==str:
                return False
            return reaction.emoji.id==772766033996021761 and reaction.message.id==message.id and user.id==ctx.author.id

        reaction,user=await bot.wait_for('reaction_add', check=check, timeout=60)
        await message.clear_reactions()
        nom,valeur,coins=verifVente(ctx.author.id,idtitre)

        connexion,curseur=connectSQL("OT","Titres","Titres",None,None)
        connexionUser,curseurUser=connectSQL("OT",ctx.author.id,"Titres",None,None)
        if curseur.execute("SELECT * FROM marketplace WHERE ID={0}".format(idtitre)).fetchone()==None:
            curseur.execute("INSERT INTO marketplace VALUES({0},0,1)".format(idtitre))
        curseur.execute("UPDATE marketplace SET Stock=Stock+1 WHERE ID={0}".format(idtitre))
        curseurUser.execute("UPDATE coins SET Coins=Coins+{0}".format(valeur))
        curseurUser.execute("DELETE FROM titresUser WHERE ID={0}".format(idtitre))

        connexion.commit()
        connexionUser.commit()

        embed=createEmbed("Vente de Titre","Titre vendu avec succès !\nVous possèdez désormais **{0} <:otCOINS:873226814527520809>**.".format(int(coins+valeur)),0xf58d1d,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.author)
        await message.reply(embed=embed)
    except asyncio.exceptions.TimeoutError:
        await embedAssert(ctx,"Une minute s'est écoulée et vous n'avez pas confirmé la vente. L'opération a été annulée",True)
        await message.clear_reactions()

def verifVente(user,idtitre):
    connexion,curseur=connectSQL("OT","Titres","Titres",None,None)
    connexionUser,curseurUser=connectSQL("OT",user,"Titres",None,None)
    createAccount(connexionUser,curseurUser)

    titre=curseurUser.execute("SELECT * FROM titresUser WHERE ID={0}".format(idtitre)).fetchone()
    assert titre!=None, "Vous ne possèdez pas ce titre."
    assert titre["Rareté"] not in (0,4,5,6), "Vous ne pouvez vendre ou échanger ce titre."
    membre=curseur.execute("SELECT * FROM active WHERE MembreID={0}".format(user)).fetchone()
    if membre!=None:
        assert membre["TitreID"]!=int(idtitre), "Le titre que vous voulez vendre est celui qui est actuellement équipé pour vous."

    coins=curseurUser.execute("SELECT * FROM coins").fetchone()["Coins"]

    connexionUser.close()
    connexion.close()
    return titre["Nom"], dictSell[titre["Rareté"]], coins
