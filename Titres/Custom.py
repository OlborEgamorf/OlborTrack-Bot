import asyncio

from Core.Decorator import OTCommand
from Core.Fonctions.Embeds import createEmbed, embedAssert
from Core.Fonctions.Phrase import createPhrase
from Stats.SQL.ConnectSQL import connectSQL

from Titres.Outils import createAccount


@OTCommand
async def achatCustom(ctx,bot):
    try:
        def checkMess(reaction,user):
            if type(reaction.emoji)==str:
                return False
            return reaction.emoji.id==772766033996021761 and reaction.message.id==message.id and user.id==ctx.author.id

        def checkCustom(mess):
            try:
                assert len(mess.content)<=8
            except:
                return False
            return user.id==ctx.author.id and mess.channel.id==message.channel.id

        connexionUser,curseurUser=connectSQL("OT",ctx.author.id,"Titres",None,None)
        createAccount(connexionUser,curseurUser)
        coins=curseurUser.execute("SELECT * FROM coins").fetchone()["Coins"]
        connexionUser.close()
        assert coins>=1500, "Vous n'avez pas assez d'OT Coins pour acheter le surnom personnalisé !"

        embed=createEmbed("Surnom personnalisé","Vous êtes sur le point de personnaliser votre surnom, pour *1500 <:otCOINS:873226814527520809>*.\nVous possèdez {0} <:otCOINS:873226814527520809> au total et en aurez {1} <:otCOINS:873226814527520809> après la transaction.\nAppuyez sur <:otVALIDER:772766033996021761> pour confirmer l'achat, et passer à la configuration.".format(int(coins),int(coins-1500)),0xf58d1d,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.author)

        message=await ctx.reply(embed=embed)
        await message.add_reaction("<:otVALIDER:772766033996021761>")

        reaction,user=await bot.wait_for('reaction_add', check=checkMess, timeout=60)
        await message.clear_reactions()

        embed=createEmbed("Surnom personnalisé","Donnez moi le surnom que vous voulez avoir, et qui sera mis derrière votre titre. Il ne doit pas dépasser 8 caractères.",0xf58d1d,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.author)

        message=await ctx.reply(embed=embed)

        mess=await bot.wait_for('message', check=checkCustom, timeout=60)
        custom=createPhrase(mess.content)
        newCustom=""
        for i in custom:
            if i!="\\":
                newCustom+=i

        connexion,curseur=connectSQL("OT","Titres","Titres",None,None)
        titre=curseur.execute("SELECT titres.Nom FROM active JOIN titres ON active.TitreID=titres.ID WHERE MembreID={0}".format(ctx.author.id)).fetchone()
        connexion.close()
        if titre==None:
            embed=createEmbed("Surnom personnalisé","Votre nom affiché dans les classements mondiaux sera désormais **{0}, Inconnu**.\nValidez ce choix avec <:otVALIDER:772766033996021761>.\nVous ne pourrez plus revenir en arrière, chaque changement de surnom coûte 1500 <:otCOINS:873226814527520809>.".format(newCustom),0xf58d1d,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.author)
        else:
            embed=createEmbed("Surnom personnalisé","Votre nom affiché dans les classements mondiaux sera désormais **{0}, {1}**.\nValidez ce choix avec <:otVALIDER:772766033996021761>.\nVous ne pourrez plus revenir en arrière, chaque changement de surnom coûte 1500 <:otCOINS:873226814527520809>.".format(newCustom,titre["Nom"]),0xf58d1d,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.author)

        message=await ctx.reply(embed=embed)
        await message.add_reaction("<:otVALIDER:772766033996021761>")

        reaction,user=await bot.wait_for('reaction_add', check=checkMess, timeout=60)
        await message.clear_reactions()


        connexionUser,curseurUser=connectSQL("OT",ctx.author.id,"Titres",None,None)
        coins=curseurUser.execute("SELECT * FROM coins").fetchone()["Coins"]
        assert coins>=1500, "Vous n'avez pas assez d'OT Coins pour acheter le surnom personnalisé !"
        curseurUser.execute("UPDATE coins SET Coins=Coins-1500")
        connexionUser.commit()

        connexion,curseur=connectSQL("OT","Titres","Titres",None,None)
        assert curseur.execute("SELECT * FROM custombans WHERE ID={0}".format(ctx.author.id)).fetchone()==None, "Vous êtes banni des outils de personnalisation."
        if curseur.execute("SELECT * FROM custom WHERE ID={0}".format(ctx.author.id)).fetchone()==None:
            curseur.execute("INSERT INTO custom VALUES({0},'{1}')".format(ctx.author.id,newCustom))
        else:
            curseur.execute("UPDATE custom SET Custom='{0}' WHERE ID={1}".format(newCustom,ctx.author.id))
        connexion.commit()

        embed=createEmbed("Surnom personnalisé","Transaction effectuée avec succès.\nVotre surnom est maintenant : **{0}**".format(newCustom),0xf58d1d,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.author)
        await message.reply(embed=embed)
        await bot.get_channel(750803643820802100).send("Custom : {0} - {1}".format(ctx.author.id,newCustom))

    except asyncio.exceptions.TimeoutError:
        await embedAssert(ctx,"Une minute s'est écoulée et vous n'avez pas confirmé l'activation. L'opération a été annulée",True)
        await message.clear_reactions()
