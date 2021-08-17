from Stats.SQL.EmoteDetector import emoteDetector
from Core.Fonctions.Embeds import createEmbed

async def addTableau(ctx,bot,args,curseur):
    assert curseur.execute("SELECT * FROM sb WHERE ID=0").fetchone()==None, "Vous avez déjà paramétré un tableau général !"
    assert ctx.message.channel_mentions!=[], "Vous devez me donner un salon valide pour créer un tableau !"
    assert ctx.message.channel_mentions[0].permissions_for(ctx.guild.get_member(bot.user.id)).view_channel==True, "Le salon mentionné n'a pas les permissions nécessaires pour que je puisse le voir."
    assert ctx.message.channel_mentions[0].permissions_for(ctx.guild.get_member(bot.user.id)).send_messages==True, "Le salon mentionné n'a pas les permissions nécessaires pour que je puisse envoyer des messages."
    assert len(args)>=0, "Il manque des éléments pour créer le tableau ! Donnez moi dans l'ordre : un emoji, le nombre de réactions nécessaire pour faire apparaître un message et un salon mentionné."
    try:
        if args[0].lower()!="all":
            id=emoteDetector(args[0])[0]
        else:
            id=0
            curseur.execute("DELETE FROM sb WHERE ID<>0")
            curseur.execute("UPDATE sb SET Nombre=1")
    except:
        raise AssertionError("L'emoji donné n'est pas valide.")

    try:
        nb=args[1]
        assert int(nb)>0, "Le nombre de réactions doit être strictement supérieur à 0."
    except:
        raise AssertionError("Le nombre de réactions n'est pas valide.")
    
    try:
        num=curseur.execute("SELECT COUNT() as Nombre FROM sb").fetchone()["Nombre"]+1
        curseur.execute("INSERT INTO sb VALUES({0},{1},'{2}',{3},{4})".format(num,ctx.message.channel_mentions[0].id,args[0],id,nb))
    except:
        raise AssertionError("Ce couple d'emoji et de salon existe déjà.")

    return createEmbed("Tableau créé","Numéro du tableau : {0}\nEmoji : {1}\nNombre d'utilisations : {2}\nSalon : <#{3}>".format(num,args[0],nb,ctx.message.channel_mentions[0].id),0xf54269,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)



async def chanTableau(ctx,bot,args,curseur):
    assert ctx.message.channel_mentions!=[], "Vous devez me donner un salon valide pour modifier un tableau !" 
    assert ctx.message.channel_mentions[0].permissions_for(ctx.guild.get_member(bot.user.id)).view_channel==True, "Le salon mentionné n'a pas les permissions nécessaires pour que je puisse le voir."
    assert ctx.message.channel_mentions[0].permissions_for(ctx.guild.get_member(bot.user.id)).send_messages==True, "Le salon mentionné n'a pas les permissions nécessaires pour que je puisse envoyer des messages."
    assert len(args)>=2, "Il manque des éléments pour modifier le salon d'un tableau ! Donnez moi dans l'ordre : le numéro du tableau voulu et le nouveau salon mentionné."
    try:
        star=curseur.execute("SELECT * FROM sb WHERE Nombre={0}".format(args[0])).fetchone()
    except:
        raise AssertionError("Le numéro donné n'est pas valide.")
    assert star!=None, "Le numéro donné ne correspond à aucun tableau actif."
    assert star["Salon"]!=ctx.message.channel_mentions[0].id, "Le salon actuel de ce tableau est le même que le salon mentionné."

    count=0
    for i in curseur.execute("SELECT * FROM sbmessages WHERE Nombre={0}".format(star["Nombre"])).fetchall():
        message=await bot.get_channel(star["Salon"]).fetch_message(i["IDStar"])
        newMessage=await ctx.message.channel_mentions[0].send(content=message.content, embed=message.embeds[0])
        curseur.execute("UPDATE sbmessages SET IDStar={0} WHERE IDStar={1}".format(newMessage.id,i["IDStar"]))
        await message.delete()
        count+=1
    
    curseur.execute("UPDATE sb SET Salon={0} WHERE Nombre={1}".format(ctx.message.channel_mentions[0].id,star["Nombre"]))
    return createEmbed("Tableau modifié","Numéro du tableau : {0}\nNouveau salon : <#{1}>\nMessages transférés : {2}".format(args[0],ctx.message.channel_mentions[0].id,count),0xf54269,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)



async def nbTableau(ctx,args,curseur):
    assert len(args)>=2, "Il manque des éléments pour modifier le nombre d'utilisations nécessaire ! Donnez moi dans l'ordre : le numéro du tableau voulu et le nouveau nombre d'utilisations."
    try:
        star=curseur.execute("SELECT * FROM sb WHERE Nombre={0}".format(args[0])).fetchone()
    except:
        raise AssertionError("Le numéro donné n'est pas valide.")
    assert star!=None, "Le numéro donné ne correspond à aucun tableau actif."
    assert star["Count"]!=args[1], "Le nombre d'utilisations donné est le même que celui actuel."

    curseur.execute("UPDATE sb SET Count={0} WHERE Nombre={1}".format(args[1],star["Nombre"]))
    return createEmbed("Tableau modifié","Numéro du tableau : {0}\nNouveau nombre d'utilisations : {1}".format(args[0],args[1]),0xf54269,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)



async def delTableau(ctx,bot,args,curseur,guild):
    assert len(args)>=1, "Il manque le numéro de tableau pour le supprimer !"
    try:
        star=curseur.execute("SELECT * FROM sb WHERE Nombre={0}".format(args[0])).fetchone()
    except:
        raise AssertionError("Le numéro donné n'est pas valide.")
    assert star!=None, "Le numéro donné ne correspond à aucun tableau actif."

    curseur.execute("DELETE FROM sb WHERE Nombre={0}".format(args[0]))

    if star["ID"]!=0:
        for i in curseur.execute("SELECT * FROM sbmessages WHERE Nombre={0}".format(args[0])).fetchall():
            idchan=guild.stardict[i["Nombre"]].salon
            messageDel=await bot.get_channel(idchan).fetch_message(i["IDStar"])
            await messageDel.delete()
        curseur.execute("DELETE FROM sbmessages WHERE Nombre={0}".format(args[0]))
    else:
        curseur.execute("UPDATE sbmessages SET Nombre=0")

    for i in curseur.execute("SELECT * FROM sb WHERE Nombre>{0} ORDER BY Nombre ASC".format(args[0])).fetchall():
        curseur.execute("UPDATE sb SET Nombre={0} WHERE Nombre={1}".format(i["Nombre"]-1,i["Nombre"]))
        curseur.execute("UPDATE sbmessages SET Nombre={0} WHERE Nombre={1}".format(i["Nombre"]-1,i["Nombre"]))

    return createEmbed("Tableau supprimé","Numéro du tableau : {0}".format(args[0]),0xf54269,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)