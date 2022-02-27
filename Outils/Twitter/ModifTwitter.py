from Core.Fonctions.Embeds import createEmbed
from Core.Fonctions.Phrase import createPhrase
from Core.Fonctions.WebRequest import webRequestHD
from Stats.SQL.ConnectSQL import connectSQL
from Core.OS.Keys3 import headerTwit

async def addTwitter(ctx,bot,args):
    def checkValid(reaction,user):
        if type(reaction.emoji)==str:
            return False
        return reaction.emoji.id==772766033996021761 and reaction.message.id==message.id and user.id==ctx.author.id
    def checkMentions(mess):
        return mess.author.id==ctx.author.id and mess.channel.id==message.channel.id and mess.channel_mentions!=[]
    def checkAuthor(mess):
        return mess.author.id==ctx.author.id and mess.channel.id==message.channel.id

    assert len(args)>0, "Vous devez me donner un compte Twitter !"
    chaine=createPhrase(args)[:-1]
    infos=await webRequestHD("https://api.twitter.com/2/users/by/username/{0}".format(chaine),headerTwit,(("user.fields","id,name,profile_image_url,description"),("tweet.fields","id,created_at")))
    assert infos!=False, "Il y a eu une erreur lors de la recherche du compte Twitter."
    if infos==None:
        await bot.get_channel(752150155276451993).send("PROBLEME AUTHENTIFICATION TWITTER. AGIR VITE.")
        raise AssertionError("Il y a eu une erreur lors de l'authentification du bot envers Twitter. Réessayez plus tard.")

    accountName=infos["data"]["name"]
    accountUser=infos["data"]["username"]
    accountID=infos["data"]["id"]
    accountPicture=infos["data"]["profile_image_url"]

    embed=createEmbed("{0} - Alertes Twitter étape 1/3".format(accountName),"{0} - @{1}\n\nEst-ce bien le compte que vous cherchez ?\nCliquez sur <:otVALIDER:772766033996021761> pour valider.".format(accountName,accountUser),0x00ACEE,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)
    embed.set_thumbnail(url=accountPicture)
    embed.add_field(name="Biographie du compte",value=infos["data"]["description"])
    embed.url="https://twitter.com/{0}".format(accountUser)

    message=await ctx.reply(embed=embed)
    await message.add_reaction("<:otVALIDER:772766033996021761>")

    reaction,user=await bot.wait_for('reaction_add', check=checkValid, timeout=60)
    await message.clear_reactions()

    embed=createEmbed("{0} - Alertes Twitter étape 2/3".format(accountName),"**Compte Twitter :** @{0}\n**Salon :** - \n**Description :** -\n\nVeuillez mentionner le salon dans lequel les alertes devront s'envoyer.".format(accountUser),0x00ACEE,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)
    embed.set_thumbnail(url=accountPicture)
    await message.edit(embed=embed)

    mess=await bot.wait_for('message', check=checkMentions, timeout=60)
    salonID=mess.channel_mentions[0].id

    embed=createEmbed("{0} - Alertes Twitter étape 3/3".format(accountName),"**Compte Twitter :** {0}\n**Salon :** <#{1}> \n**Description :** -\n\nVeuillez écrire la description que vous voulez mettre dans l'alerte.".format(accountUser,salonID),0x00ACEE,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)
    embed.set_thumbnail(url=accountPicture)
    await message.edit(embed=embed)

    mess=await bot.wait_for('message', check=checkAuthor, timeout=60)
    descip=createPhrase(mess.content.split(" "))

    data=await webRequestHD("https://api.twitter.com/2/tweets/search/recent",headerTwit,(("query","from:{0}".format(accountID)),("tweet.fields","id")))
    if data["meta"]["result_count"]!=0:
        last=data["data"][0]["id"]
    else:
        last=0

    connexion,curseur=connectSQL(ctx.guild.id,"Guild","Guild",None,None)
    try:
        num=curseur.execute("SELECT COUNT() as Nombre FROM twitter").fetchone()["Nombre"]+1
        curseur.execute("INSERT INTO twitter VALUES({0},{1},'{2}','{3}',{4},'{5}')".format(num,salonID,accountID,descip,last,accountName))
    except:
        raise AssertionError("Ce couple de compte Twitter et de salon existe déjà.")
    if num==4:
        connexion.close()
        raise AssertionError("Désolé, mais vous êtes limité à 3 alertes Twitter par serveur. Cela est dû à un problème de rate limit de la part de Twitter. Si trop d'alertes sont configurées, alors le bot ne sera pas en mesure de toutes les faire fonctionner. Une solution sera trouvée un jour...")
    connexion.commit()

    return createEmbed("Alerte Twitter créée","Numéro de l'alerte : `{0}`\nChaîne : {1}\nSalon : <#{2}>\nDescription : {3}".format(num,accountName,salonID,descip),0x00ACEE,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)


async def chanTwitter(ctx,bot,args,curseur):
    assert ctx.message.channel_mentions!=[], "Vous devez me donner un salon valide pour modifier une alerte Twitter !" 
    assert ctx.message.channel_mentions[0].permissions_for(ctx.guild.get_member(bot.user.id)).view_channel==True, "Le salon mentionné n'a pas les permissions nécessaires pour que je puisse le voir."
    assert ctx.message.channel_mentions[0].permissions_for(ctx.guild.get_member(bot.user.id)).send_messages==True, "Le salon mentionné n'a pas les permissions nécessaires pour que je puisse envoyer des messages."
    assert len(args)>=2, "Il manque des éléments pour modifier le salon d'une alerte ! Donnez moi dans l'ordre : le numéro de l'alerte voulue et le nouveau salon mentionné."
    try:
        alert=curseur.execute("SELECT * FROM twitter WHERE Nombre={0}".format(args[0])).fetchone()
    except:
        raise AssertionError("Le numéro donné n'est pas valide.")
    assert alert!=None, "Le numéro donné ne correspond à aucune alerte active."
    assert alert["Salon"]!=ctx.message.channel_mentions[0].id, "Le salon actuel de cette alerte est le même que le salon mentionné."
    
    curseur.execute("UPDATE twitter SET Salon={0} WHERE Nombre={1}".format(ctx.message.channel_mentions[0].id,alert["Nombre"]))
    return createEmbed("Alerte Twitter modifiée","Numéro de l'alerte : {0}\nNouveau salon : <#{1}>".format(args[0],ctx.message.channel_mentions[0].id),0x00ACEE,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)


async def delTwitter(ctx,bot,args,curseur):
    assert len(args)>=1, "Il manque le numéro de l'alerte pour la supprimer !"
    try:
        alert=curseur.execute("SELECT * FROM twitter WHERE Nombre={0}".format(args[0])).fetchone()
    except:
        raise AssertionError("Le numéro donné n'est pas valide.")
    assert alert!=None, "Le numéro donné ne correspond à aucun tableau actif."

    curseur.execute("DELETE FROM twitter WHERE Nombre={0}".format(args[0]))

    for i in curseur.execute("SELECT * FROM twitter WHERE Nombre>{0} ORDER BY Nombre ASC".format(args[0])).fetchall():
        curseur.execute("UPDATE twitter SET Nombre={0} WHERE Nombre={1}".format(i["Nombre"]-1,i["Nombre"]))

    return createEmbed("Alerte Twitter supprimée","Numéro de l'alerte : {0}".format(args[0]),0x00ACEE,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)


async def descipTwitter(ctx,bot,args,curseur):
    assert len(args)>=1, "Il manque le numéro de l'alerte pour la modifier !"
    try:
        alert=curseur.execute("SELECT * FROM twitter WHERE Nombre={0}".format(args[0])).fetchone()
    except:
        raise AssertionError("Le numéro donné n'est pas valide.")
    assert alert!=None, "Le numéro donné ne correspond à aucun tableau actif."

    descip=createPhrase(args[1:len(args)])
    curseur.execute("UPDATE twitter SET Descip='{0}' WHERE Nombre={1}".format(descip,alert["Nombre"]))

    return createEmbed("Alerte Twitter modifiée","Numéro de l'alerte : {0}\nNouvelle description : {1}".format(args[0],descip),0x00ACEE,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)
