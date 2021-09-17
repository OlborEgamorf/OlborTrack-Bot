async def addAlertOT(ctx,bot,args,guildOT):
    dictSalons={"github":,"updates":,"cross":}
    try:
        connexion,curseur=connectSQL(ctx.guild.id,"Guild","Guild",None,None)
        if ctx.invoked_with in ("add"):
            assert len(ctx.message.channel_mentions)!=0, "Vous devez me donner un salon valide !"
            assert args[0].lower() in ("github","updates","cross"), "Vous devez me donner un nom d'une alerte existante !\nAlertes disponibles : updates, github, cross"
            hook=await ctx.mess.channel_mentions[0].follow(dictSalons[args[0].lower())
            curseur.execute("UPDATE alertsot SET Active=True, Salon={0}, Webhook={1} WHERE Type='{2}'".format(ctx.message.channel_mentions[0].id,hook.id,args[0].lower()))
            embed=createEmbed("Commande automatique activée ou modifiée","Commande : {0}\nSalon : <#{1}>".format(args[0].lower(),ctx.message.channel_mentions[0].id),0x220cc9,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)
        elif ctx.invoked_with=="edit":
            assert len(ctx.message.channel_mentions)!=0, "Vous devez me donner un salon valide !"
            assert args[0].lower() in ("github","updates","cross"), "Vous devez me donner un nom d'une alerte existante !\nAlertes disponibles : updates, github, cross"
            curseur.execute("SELECT * alertesot WHERE Type='{0}'.format(args[0].lower())).fetchone()
            assert curseur["Active"]==True, "Vous ne pouvez pas éditer une alerte qui n'existe pas !"
            assert curseur["Salon"]!=ctx.message.channel_mentions[0].id, "Cette alerte est déjà dans ce salon !"
            for i in await bot.get_channel(curseur["Salon"]).webhooks:
                if i.id==curseur["Webhook"]:
                    await i.delete()
                    break
            hook=await ctx.mess.channel_mentions[0].follow(dictSalons[args[0].lower())
            curseur.execute("UPDATE alertsot SET Active=True, Salon={0}, Webhook={1} WHERE Type='{2}'".format(ctx.message.channel_mentions[0].id,hook.id,args[0].lower()))
        elif ctx.invoked_with=="del":
            assert args[0].lower() in ("jour","mois","annee","nasaphoto","savezvous"), "Vous devez me donner un nom de commande compatible !"
            curseur.execute("UPDATE auto SET Active=False, Salon=0 WHERE Commande='{0}'".format(args[0].lower()))
            embed=createEmbed("Commande automatique supprimée","Commande : {0}".format(args[0].lower()),0x220cc9,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)
        else:
            embed=embedAuto(ctx,guildOT)
        connexion.commit()
        guildOT.getAuto()
    except AssertionError as er:
        embed=embedAssert(str(er))
    except:
        embed=await exeErrorExcept(ctx,bot,args)
    await ctx.send(embed=embed)

def embedAuto(ctx,guildOT):
    descip=""
    for i in guildOT.auto:
        if i["Active"]:
            descip+="{0} : <#{1}>\n".format(i["Commande"],i["Salon"])
        else:
            descip+="{0} : *désactivé*\n".format(i["Commande"])
    embedTable=createEmbed("Liste des commandes automatiques",descip,0x220cc9,ctx.invoked_with.lower(),ctx.guild)
    return embedTable
