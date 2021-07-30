from random import choice
from Savezvous.ListModo import commandeSV
from Core.Fonctions.Embeds import createEmbed, embedAssert, exeErrorExcept
from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.Phrase import createPhrase


async def exeSavezVous(ctx,bot,args):
    try:
        args=args.split(" ")
        connexion,curseur=connectSQL(ctx.guild.id,"Guild","Guild",None,None)
        if len(args)==0 or args[0]=="" or ctx.invoked_with not in ("add", "del", "list", "modo", "edit"):
            liste=curseur.execute("SELECT * FROM savezvous").fetchall()
            assert liste!=[], "Vous devez commencer par ajouter une phrase avec `OT!savezvous add` !"
            ligne=choice(liste)
            user=ctx.guild.get_member(ligne["ID"])
            if user==None:
                embed=createEmbed("","`{0}` : {1}".format(ligne["Count"],ligne["Texte"]),ctx.guild.get_member(bot.user.id).color.value,ctx.invoked_with.lower(),bot.user)
            else:
                embed=createEmbed("","`{0}` : {1}".format(ligne["Count"],ligne["Texte"]),user.color.value,ctx.invoked_with.lower(),user)
            if ligne["Image"]!="None":
                embed.set_image(url=ligne["Image"])
        else:
            if ctx.invoked_with=="add":
                embed=addSV(ctx,args,curseur)
            elif ctx.invoked_with=="del":
                embed=deleteSV(ctx,args,curseur)
            elif ctx.invoked_with=="edit":
                embed=editSV(ctx,args,curseur)
            else:
                await commandeSV(ctx,ctx.invoked_with,None,False,None,bot)
                return
        connexion.commit()
    except AssertionError as er:
        embed=embedAssert(str(er))
    except:
        embed=await exeErrorExcept(ctx,bot,args)
    await ctx.reply(embed=embed)

async def autoSV(channel,guild,bot):
    connexion,curseur=connectSQL(guild.id,"Guild","Guild",None,None)
    liste=curseur.execute("SELECT * FROM savezvous").fetchall()
    ligne=choice(liste)
    assert liste!=[]
    user=guild.get_member(ligne["ID"])
    if user==None:
        embed=createEmbed("","`{0}` : {1}".format(ligne["Count"],ligne["Texte"]),guild.get_member(bot.user.id).color.value,"OT!savezvous",bot.user)
    else:
        embed=createEmbed("","`{0}` : {1}".format(ligne["Count"],ligne["Texte"]),user.color.value,"OT!savezvous",user)
    if ligne["Image"]!="None":
        embed.set_image(url=ligne["Image"])
    await bot.get_channel(channel).send(embed=embed)

def addSV(ctx,args,curseur):
    assert len(args)!=0, "Vous devez me donner une phrase !"
    if ctx.message.attachments!=[]:
        image=ctx.message.attachments[0].url
    else:
        image=None
    descip=createPhrase(args[0:len(args)])
    assert len(descip)<2000
    count=curseur.execute("SELECT COUNT() as Nb FROM savezvous").fetchone()["Nb"]
    curseur.execute("INSERT INTO savezvous VALUES('{0}',{1},'{2}',{3})".format(descip,ctx.author.id,image,count+1))
    embed=createEmbed("Phrase ajoutée","`{0}` : {1}".format(count+1,descip),0x00ffd0,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)
    if image!=None:
        embed.set_image(url=image)
    return embed


def deleteSV(ctx,args,curseur):
    assert len(args)!=0, "Vous devez me donner le numéro de la phrase que vous voulez supprimer !"
    try:
        descip=curseur.execute("SELECT * FROM savezvous WHERE Count={0}".format(args[0])).fetchone()
    except:
        raise AssertionError("Le numéro donné n'est pas valide.")
    assert descip!=None, "Le numéro donné ne correspond à aucune phrase."
    assert ctx.author.id==descip["ID"] or ctx.author.guild_permissions.manage_messages==True, "Cette phrase ne vous appartient pas."
    curseur.execute("DELETE FROM savezvous WHERE Count={0}".format(args[0]))
    for i in curseur.execute("SELECT * FROM savezvous WHERE Count>{0} ORDER BY Count ASC".format(args[0])).fetchall():
        curseur.execute("UPDATE savezvous SET Count={0} WHERE Count={1}".format(i["Count"]-1, i["Count"]))
    return createEmbed("Phrase supprimée","`{0}` : {1}".format(args[0],descip["Texte"]),0x00ffd0,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)


def editSV(ctx,args,curseur):
    assert len(args)>1, "Vous devez me donner le numéro de la phrase que vous voulez modifier et la nouvelle phrase !"
    try:
        phrase=curseur.execute("SELECT * FROM savezvous WHERE Count={0}".format(args[0])).fetchone()
        assert phrase!=None, "Le numéro donné ne correspond à aucune phrase."
    except:
        raise AssertionError("Le numéro donné n'est pas valide.")
    assert ctx.author.id==phrase["ID"], "Cette phrase ne vous appartient pas."
    descip=createPhrase(args[1:len(args)])
    curseur.execute("UPDATE savezvous SET Texte='{0}' WHERE Count={1}".format(descip,args[0]))
    return createEmbed("Phrase modifiée","`{0}` : {1}".format(args[0],descip),0x00ffd0,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)