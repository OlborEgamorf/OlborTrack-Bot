import discord
from Core.Fonctions.Embeds import createEmbed
from Core.Fonctions.Phrase import createPhrase
from Core.Fonctions.WebRequest import webRequest
from Core.OS.Keys3 import ytKey
from Stats.SQL.ConnectSQL import connectSQL


async def addYT(ctx,bot,args):
    def checkValid(reaction,user):
        if type(reaction.emoji)==str:
            return False
        return reaction.emoji.id==772766033996021761 and reaction.message.id==message.id and user.id==ctx.author.id
    def checkMention(mess):
        return mess.author.id==ctx.author.id and mess.channel.id==ctx.channel.id and mess.channel_mentions!=[] and type(mess.channel_mentions[0])==discord.TextChannel
    def checkAuthor(mess):
        return mess.author.id==ctx.author.id and mess.channel.id==message.channel.id

    assert len(args)>0, "Vous devez me donner une chaîne YouTube !"
    chaine=createPhrase(args)
    infos=await webRequest("https://www.googleapis.com/youtube/v3/search?key={0}&q={1}&part=snippet,id&maxResults=1&type=channel&order=relevance".format(ytKey,chaine))
    assert infos!=False, "Il y a eu une erreur lors de la recherche de la chaîne YouTube."

    channelName=infos["items"][0]["snippet"]["channelTitle"]
    channelID=infos["items"][0]["id"]["channelId"]
    channelPicture=infos["items"][0]["snippet"]["thumbnails"]["medium"]["url"]

    embed=createEmbed("{0} - Alertes YouTube étape 1/3".format(channelName),"Est-ce bien la chaîne que vous cherchez ?\nCliquez sur <:otVALIDER:772766033996021761> pour valider.",0xFF0000,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)
    embed.set_thumbnail(url=channelPicture)
    embed.add_field(name="Description de la chaîne",value=infos["items"][0]["snippet"]["description"])
    embed.url="https://youtube.com/channel/{0}".format(channelID)

    message=await ctx.reply(embed=embed)
    await message.add_reaction("<:otVALIDER:772766033996021761>")

    reaction,user=await bot.wait_for('reaction_add', check=checkValid, timeout=60)
    await message.clear_reactions()

    embed=createEmbed("{0} - Alertes YouTube étape 2/3".format(channelName),"**Chaîne YouTube :** {0}\n**Salon :** - \n**Description :** -\n\nVeuillez mentionner le salon dans lequel les alertes devront s'envoyer.".format(channelName),0xFF0000,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)
    embed.set_thumbnail(url=channelPicture)
    await message.edit(embed=embed)
    
    mess=await bot.wait_for('message', check=checkMention, timeout=60)
    salonID=mess.channel_mentions[0].id

    embed=createEmbed("{0} - Alertes YouTube étape 3/3".format(channelName),"**Chaîne YouTube :** {0}\n**Salon :** <#{1}> \n**Description :** -\n\nVeuillez écrire la description que vous voulez mettre dans l'alerte.".format(channelName,salonID),0xFF0000,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)
    embed.set_thumbnail(url=channelPicture)
    await message.edit(embed=embed)
    
    mess=await bot.wait_for('message', check=checkAuthor, timeout=60)
    descip=createPhrase(mess.content)

    data=await webRequest("https://www.googleapis.com/youtube/v3/search?key={0}&channelId={1}&part=snippet,id&order=date&maxResults=7&type=video".format(ytKey,channelID))
    if data!=False or len(data["items"])!=0:
        last=data["items"][0]["id"]["videoId"]

    connexion,curseur=connectSQL(ctx.guild.id,"Guild","Guild",None,None)
    try:
        num=curseur.execute("SELECT COUNT() as Nombre FROM youtube").fetchone()["Nombre"]+1
        curseur.execute("INSERT INTO youtube VALUES({0},{1},'{2}','{3}','{4}','{5}')".format(num,salonID,channelID,descip,last,channelName))
    except:
        raise AssertionError("Ce couple de chaîne YouTube et de salon existe déjà.")
    connexion.commit()

    return createEmbed("Alerte YouTube créée","Numéro de l'alerte : `{0}`\nChaîne : {1}\nSalon : <#{2}>\nDescription : {3}".format(num,channelName,salonID,descip),0xFF0000,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)


async def chanYT(ctx,bot,args,curseur):
    assert ctx.message.channel_mentions!=[], "Vous devez me donner un salon valide pour modifier une alerte YouTube !" 
    assert type(ctx.message.channel_mentions[0])==discord.TextChannel, "Vous ne pouvez pas me donner de salon vocal !"
    assert ctx.message.channel_mentions[0].permissions_for(ctx.guild.get_member(bot.user.id)).view_channel==True, "Le salon mentionné n'a pas les permissions nécessaires pour que je puisse le voir."
    assert ctx.message.channel_mentions[0].permissions_for(ctx.guild.get_member(bot.user.id)).send_messages==True, "Le salon mentionné n'a pas les permissions nécessaires pour que je puisse envoyer des messages."
    assert len(args)>=2, "Il manque des éléments pour modifier le salon d'une alerte ! Donnez moi dans l'ordre : le numéro de l'alerte voulue et le nouveau salon mentionné."
    try:
        alert=curseur.execute("SELECT * FROM youtube WHERE Nombre={0}".format(args[0])).fetchone()
    except:
        raise AssertionError("Le numéro donné n'est pas valide.")
    assert alert!=None, "Le numéro donné ne correspond à aucune alerte active."
    assert alert["Salon"]!=ctx.message.channel_mentions[0].id, "Le salon actuel de cette alerte est le même que le salon mentionné."
    
    curseur.execute("UPDATE youtube SET Salon={0} WHERE Nombre={1}".format(ctx.message.channel_mentions[0].id,alert["Nombre"]))
    return createEmbed("Alerte YouTube modifiée","Numéro de l'alerte : {0}\nNouveau salon : <#{1}>".format(args[0],ctx.message.channel_mentions[0].id),0xFF0000,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)


async def delYT(ctx,bot,args,curseur,guild):
    assert len(args)>=1, "Il manque le numéro de l'alerte pour la supprimer !"
    try:
        alert=curseur.execute("SELECT * FROM youtube WHERE Nombre={0}".format(args[0])).fetchone()
    except:
        raise AssertionError("Le numéro donné n'est pas valide.")
    assert alert!=None, "Le numéro donné ne correspond à aucun tableau actif."

    curseur.execute("DELETE FROM youtube WHERE Nombre={0}".format(args[0]))

    for i in curseur.execute("SELECT * FROM youtube WHERE Nombre>{0} ORDER BY Nombre ASC".format(args[0])).fetchall():
        curseur.execute("UPDATE youtube SET Nombre={0} WHERE Nombre={1}".format(i["Nombre"]-1,i["Nombre"]))

    return createEmbed("Alerte YouTube supprimée","Numéro de l'alerte : {0}".format(args[0]),0xFF0000,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)


async def descipYT(ctx,bot,args,curseur,guild):
    assert len(args)>=1, "Il manque le numéro de l'alerte pour la modifier !"
    try:
        alert=curseur.execute("SELECT * FROM youtube WHERE Nombre={0}".format(args[0])).fetchone()
    except:
        raise AssertionError("Le numéro donné n'est pas valide.")
    assert alert!=None, "Le numéro donné ne correspond à aucun tableau actif."

    descip=createPhrase(args[1:])
    curseur.execute("UPDATE youtube SET Descip='{0}' WHERE Nombre={1}".format(descip,alert["Nombre"]))

    return createEmbed("Alerte YouTube modifiée","Numéro de l'alerte : {0}\nNouvelle description : {1}".format(args[0],descip),0xFF0000,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)
