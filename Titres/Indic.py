import asyncio

from Core.Fonctions.Embeds import createEmbed, embedAssert
from Core.Fonctions.Phrase import createPhrase
from Stats.SQL.ConnectSQL import connectSQL
from Core.Decorator import OTCommand

@OTCommand
async def setServer(ctx,bot):
    try:
        def checkMess(reaction,user):
            if type(reaction.emoji)==str:
                return False
            return reaction.emoji.id==772766033996021761 and reaction.message.id==message.id and user.id==ctx.author.id

        def checkCustom(mess):
            try:
                assert len(mess.content)<=4
            except:
                return False
            return mess.author.id==ctx.author.id and mess.channel.id==message.channel.id

        embed=createEmbed("Indicatif de serveur","Donnez moi l'indicatif que vous voulez donner à votre serveur. Il ne doit pas dépasser 4 caractères et être unique. Il sera affiché dans le classement des jeux Cross-Serveurs.",0xf58d1d,ctx.invoked_with.lower(),ctx.guild)

        message=await ctx.reply(embed=embed)

        mess=await bot.wait_for('message', check=checkCustom, timeout=60)
        custom=createPhrase(mess.content)
        newCustom=""
        for i in custom:
            if i!="\\":
                newCustom+=i

        connexion,curseur=connectSQL("OT","Titres","Titres",None,None)
        titre=curseur.execute("SELECT * FROM servers WHERE Nom='{0}'".format(newCustom)).fetchone()
        assert titre==None, "Cet indicatif existe déjà !"
        connexion.close()

        embed=createEmbed("Indicatif de serveur","L'indicatif affiché pour votre serveur dans le classement Cross-Serveurs sera désormais **{0}**.\nValidez ce choix avec <:otVALIDER:772766033996021761>.\nVous pourrez toujours le modifier en refaisant cette commande.".format(newCustom),0xf58d1d,ctx.invoked_with.lower(),ctx.guild)

        message=await ctx.reply(embed=embed)
        await message.add_reaction("<:otVALIDER:772766033996021761>")

        reaction,user=await bot.wait_for('reaction_add', check=checkMess, timeout=60)
        await message.clear_reactions()

        connexion,curseur=connectSQL("OT","Titres","Titres",None,None)
        titre=curseur.execute("SELECT * FROM servers WHERE Nom='{0}'".format(newCustom)).fetchone()
        assert titre==None, "Cet indicatif existe déjà !"
        if curseur.execute("SELECT * FROM servers WHERE ID={0}".format(ctx.guild.id)).fetchone()==None:
            curseur.execute("INSERT INTO servers VALUES({0},'{1}')".format(ctx.guild.id,newCustom))
        else:
            curseur.execute("UPDATE servers SET Nom='{0}' WHERE ID={1}".format(newCustom,ctx.guild.id))
        connexion.commit()

        embed=createEmbed("Indicatif de serveur","Opération effectuée avec succès.\L'indicatif de votre serveur est maintenant : **{0}**".format(newCustom),0xf58d1d,ctx.invoked_with.lower(),ctx.guild)
        await message.reply(embed=embed)
        await bot.get_channel(750803643820802100).send("Serveur : {0} - {1}".format(ctx.guild.id,newCustom))

    except asyncio.exceptions.TimeoutError:
        await embedAssert(ctx,"Une minute s'est écoulée et vous n'avez pas confirmé la configuration. L'opération a été annulée",True)
        await message.clear_reactions()
