from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.Embeds import createEmbed, embedAssert, exeErrorExcept

async def addAlertOT(ctx,bot,args,guildOT):
    dictSalons={"github":bot.get_channel(709764487733051454),"updates":bot.get_channel(702208752035692654),"cross":bot.get_channel(878254347459366952)}
    try:
        connexion,curseur=connectSQL(ctx.guild.id,"Guild","Guild",None,None)
        if ctx.invoked_with=="add":
            assert len(ctx.message.channel_mentions)!=0, "Vous devez me donner un salon valide !"
            assert args[0].lower() in ("github","updates","cross"), "Vous devez me donner un nom d'une alerte existante !\nAlertes disponibles : updates, github, cross"
            alert=curseur.execute("SELECT * FROM alertesot WHERE Type='{0}'".format(args[0].lower())).fetchone()
            assert alert["Active"]==False, "Cette alerte existe déjà !"
            hook=await dictSalons[args[0].lower()].follow(destination=ctx.message.channel_mentions[0])
            curseur.execute("UPDATE alertesot SET Active=True, Salon={0}, Webhook={1} WHERE Type='{2}'".format(ctx.message.channel_mentions[0].id,hook.id,args[0].lower()))
            embed=createEmbed("Alerte OT activée","Alerte : {0}\nSalon : <#{1}>".format(args[0].lower(),ctx.message.channel_mentions[0].id),0x220cc9,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)

        elif ctx.invoked_with=="del":
            assert args[0].lower() in ("github","updates","cross"), "Vous devez me donner un nom d'une alerte existante !\nAlertes disponibles : updates, github, cross"
            alert=curseur.execute("SELECT * FROM alertesot WHERE Type='{0}'".format(args[0].lower())).fetchone()
            assert alert["Active"]==True, "Vous ne pouvez pas supprimer une alerte qui n'existe pas !"
            for i in await bot.get_channel(alert["Salon"]).webhooks():
                assert i.id==alert["Webhook"], "Malheureusement, je ne peux pas supprimer moi-même les alertes. Pour le faire, allez dans les paramètres du salon où est configuré l'alerte, puis dans la sections 'Intégrations', puis dans les salons suivis. Supprimez l'alerte que vous souhaitez avec le bouton 'ne plus suivre', et refaites cette commande pour actualiser le bot et pouvoir la remettre dans un autre salon.\nCe n'est pas dû à moi ou à vous mais à Discord qui m'empêche de faire cette action, pour n'importe quel serveur."
            curseur.execute("UPDATE alertesot SET Active=False, Salon=0 WHERE Type='{0}'".format(args[0].lower()))
            embed=createEmbed("Alerte OT supprimée","Alerte : {0}".format(args[0].lower()),0x220cc9,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)
        else:
            embed=embedAlertesOT(ctx)
        connexion.commit()
    except AssertionError as er:
        embed=embedAssert(str(er))
    except:
        embed=await exeErrorExcept(ctx,bot,args)
    await ctx.send(embed=embed)

def embedAlertesOT(ctx):
    connexion,curseur=connectSQL(ctx.guild.id,"Guild","Guild",None,None)
    descip=""
    for i in curseur.execute("SELECT * FROM alertesot").fetchall():
        if i["Active"]:
            descip+="{0} : <#{1}>\n".format(i["Type"],i["Salon"])
        else:
            descip+="{0} : *désactivé*\n".format(i["Type"])
    embedTable=createEmbed("Liste des alertes Olbor Track",descip,0x220cc9,ctx.invoked_with.lower(),ctx.guild)
    return embedTable
