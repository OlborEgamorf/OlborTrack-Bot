from Core.Fonctions.Phrase import createPhrase
from Core.Fonctions.Embeds import createEmbed

async def addTwitch(ctx,bot,args,curseur):
    assert ctx.message.channel_mentions!=[], "Vous devez me donner un salon valide pour créer une alerte Twitch !"
    assert ctx.message.channel_mentions[0].permissions_for(ctx.guild.get_member(bot.user.id)).view_channel==True, "Le salon mentionné n'a pas les permissions nécessaires pour que je puisse le voir."
    assert ctx.message.channel_mentions[0].permissions_for(ctx.guild.get_member(bot.user.id)).send_messages==True, "Le salon mentionné n'a pas les permissions nécessaires pour que je puisse envoyer des messages."
    assert len(args)>=3, "Il manque des éléments pour créer l'alerte ! Donnez moi dans l'ordre : un streamer, un salon mentionné et une description."
    
    if True:
        num=curseur.execute("SELECT COUNT() as Nombre FROM twitch").fetchone()["Nombre"]+1
        stream=createPhrase([args[0]]).lower()[0:-1]
        descip=createPhrase(args[2:len(args)])
        curseur.execute("INSERT INTO twitch VALUES({0},{1},'{2}','{3}',False)".format(num,ctx.message.channel_mentions[0].id,stream,descip))
    else:
        raise AssertionError("Ce couple de streamer et de salon existe déjà.")

    return createEmbed("Alerte Twitch créée","Numéro de l'alerte : {0}\nStreamer : {1}\nSalon : <#{2}>\nDescription : {3}".format(num,stream,ctx.message.channel_mentions[0].id,descip),0x220cc9,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)



async def chanTwitch(ctx,bot,args,curseur):
    assert ctx.message.channel_mentions!=[], "Vous devez me donner un salon valide pour modifier une alerte Twitch !" 
    assert ctx.message.channel_mentions[0].permissions_for(ctx.guild.get_member(bot.user.id)).view_channel==True, "Le salon mentionné n'a pas les permissions nécessaires pour que je puisse le voir."
    assert ctx.message.channel_mentions[0].permissions_for(ctx.guild.get_member(bot.user.id)).send_messages==True, "Le salon mentionné n'a pas les permissions nécessaires pour que je puisse envoyer des messages."
    assert len(args)>=2, "Il manque des éléments pour modifier le salon d'une alerte ! Donnez moi dans l'ordre : le numéro de l'alerte voulue et le nouveau salon mentionné."
    try:
        alert=curseur.execute("SELECT * FROM twitch WHERE Nombre={0}".format(args[0])).fetchone()
    except:
        raise AssertionError("Le numéro donné n'est pas valide.")
    assert alert!=None, "Le numéro donné ne correspond à aucune alerte active."
    assert alert["Salon"]!=ctx.message.channel_mentions[0].id, "Le salon actuel de cette alerte est le même que le salon mentionné."
    
    curseur.execute("UPDATE twitch SET Salon={0} WHERE Nombre={1}".format(ctx.message.channel_mentions[0].id,alert["Nombre"]))
    return createEmbed("Alerte Twitch modifiée","Numéro de l'alerte : {0}\nNouveau salon : <#{1}>".format(args[0],ctx.message.channel_mentions[0].id),0x220cc9,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)



async def delTwitch(ctx,bot,args,curseur,guild):
    assert len(args)>=1, "Il manque le numéro de l'alerte pour la supprimer !"
    try:
        alert=curseur.execute("SELECT * FROM twitch WHERE Nombre={0}".format(args[0])).fetchone()
    except:
        raise AssertionError("Le numéro donné n'est pas valide.")
    assert alert!=None, "Le numéro donné ne correspond à aucun tableau actif."

    curseur.execute("DELETE FROM twitch WHERE Nombre={0}".format(args[0]))

    for i in curseur.execute("SELECT * FROM twitch WHERE Nombre>{0} ORDER BY Nombre ASC".format(args[0])).fetchall():
        curseur.execute("UPDATE twitch SET Nombre={0} WHERE Nombre={1}".format(i["Nombre"]-1,i["Nombre"]))

    return createEmbed("Alerte Twitch supprimée","Numéro de l'alerte : {0}".format(args[0]),0x220cc9,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)


async def descipTwitch(ctx,bot,args,curseur,guild):
    assert len(args)>=1, "Il manque le numéro de l'alerte pour la modifier !"
    try:
        alert=curseur.execute("SELECT * FROM twitch WHERE Nombre={0}".format(args[0])).fetchone()
    except:
        raise AssertionError("Le numéro donné n'est pas valide.")
    assert alert!=None, "Le numéro donné ne correspond à aucun tableau actif."

    descip=createPhrase(args[1:len(args)])
    curseur.execute("UPDATE twitch SET Descip='{0}' WHERE Nombre={1}".format(descip,alert["Nombre"]))

    return createEmbed("Alerte Twitch modifiée","Numéro de l'alerte : {0}\nNouvelle description : {1}".format(args[0],descip),0x220cc9,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)