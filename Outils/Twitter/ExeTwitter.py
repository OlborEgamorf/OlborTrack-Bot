async def exeTwitterAlerts(ctx,bot,args,guildOT):
    try:
        connexion,curseur=connectSQL(ctx.guild.id,"Guild","Guild",None,None)
        if ctx.invoked_with=="twitter":
            await commandeTwitter(ctx,None,False,None,bot,guildOT,curseur)
            return
        elif ctx.invoked_with=="add":
            embed=await addTwitter(ctx,bot,args)
        elif ctx.invoked_with=="chan":
            embed=await chanTwitter(ctx,bot,args,curseur)
        elif ctx.invoked_with=="del":
            embed=await delTwitter(ctx,bot,args,curseur,guildOT)
        elif ctx.invoked_with=="edit":
            embed=await descipTwitter(ctx,bot,args,curseur,guildOT)
        connexion.commit()
        guildOT.getTwitter()
    except AssertionError as er:
        embed=embedAssert(str(er))
    except:
        embed=await exeErrorExcept(ctx,bot,args)
    await ctx.send(embed=embed)


async def commandeTwitter(ctx,turn,react,ligne,bot,guildOT,curseur):
    connexionCMD,curseurCMD=connectSQL(ctx.guild.id,"Commandes","Guild",None,None)
    if not react:
        assert guildOT.twitter!=[], "Aucune alerte n'est configurée pour votre serveur."
        pagemax=setMax(len(guildOT.twitter))
        curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'twitter','None','None','None','None','None',1,{2},'countDesc',False)".format(ctx.message.id,ctx.author.id,pagemax))
        ligne=curseurCMD.execute("SELECT * FROM commandes WHERE MessageID={0}".format(ctx.message.id)).fetchone()
    else:
        connexion,curseur=connectSQL(ctx.guild.id,"Guild","Guild",None,None)
        pagemax=setMax(len(guildOT.twitter))

    mobile=ligne["Mobile"]
    table=curseur.execute("SELECT * FROM twitter ORDER BY Nombre ASC").fetchall()
    page=setPage(ligne["Page"],pagemax,turn)

    embed=embedTwitter(table,page,pagemax,mobile)
    embed=auteur(ctx.guild.id,ctx.guild.name,ctx.guild.icon,embed,"guild")
    message=await sendEmbed(ctx,embed,react,False,curseurCMD,connexionCMD,page,pagemax)
    if not react:
        await message.add_reaction("<:otMOBILE:833736320919797780>")


def embedTwitter(table,page,pagemax,mobile):
    embed=discord.Embed(title="Liste des alertes Twitter actives sur votre serveur",color=0xf54269)
    stop=15*page if 15*page<len(table) else len(table)
    field1,field2,field3="","",""
    for i in range(15*(page-1),stop):
        nombre="`{0}`".format(table[i]["Nombre"])
        emote="[{0}]".format(table[i]["Nom"])
        salon="<#{0}>".format(table[i]["Salon"])

        field1,field2,field3=addtoFields(field1,field2,field3,mobile,nombre,emote,salon)

    embed=createFields(mobile,embed,field1,field2,field3,"Numéro","Compte","Salon") 
    embed.set_footer(text="Page {0}/{1}".format(page,pagemax))
    return embed