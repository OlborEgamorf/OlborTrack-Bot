from time import strftime

import discord
from Core.Fonctions.WebRequest import getAvatar
from Outils.Bienvenue.Manipulation import formatage, fusion, fusionAdieu, squaretoround
from Stats.SQL.ConnectSQL import connectSQL


async def newMember(member,chan,bot):
    connexion,curseur=connectSQL(member.guild.id,"Guild","Guild",None,None)
    texte=curseur.execute("SELECT * FROM messagesBV ORDER BY RANDOM()").fetchone()
    if int(strftime("%H"))>8 and int(strftime("%H"))<22:
        mode="nuit"
    else:
        mode="jour"
    image=curseur.execute("SELECT * FROM imagesBV WHERE Mode<>'{0}' ORDER BY RANDOM()".format(mode)).fetchone()

    if texte==None and image==None:
        return
    elif image==None:
        content=formatage(texte["Message"],member,member.guild)
        await bot.get_channel(chan).send(content=content)
    elif texte==None:
        await getAvatar(member)
        squaretoround(member.id)
        fusion(image["Path"],member,image["Message"],image["Couleur"],image["Taille"],member.guild)
        await bot.get_channel(chan).send(file=discord.File("Temp/BV{0}.png".format(member.id)))
    else:
        content=formatage(texte["Message"],member,member.guild)
        await getAvatar(member)
        squaretoround(member.id)
        fusion(image["Path"],member,image["Message"],image["Couleur"],image["Taille"],member.guild)
        await bot.get_channel(chan).send(content=content,file=discord.File("Temp/BV{0}.png".format(member.id)))

async def oldMember(member,chan,bot):
    connexion,curseur=connectSQL(member.guild.id,"Guild","Guild",None,None)
    texte=curseur.execute("SELECT * FROM messagesAD ORDER BY RANDOM()").fetchone()
    if int(strftime("%H"))>8 and int(strftime("%H"))<22:
        mode="nuit"
    else:
        mode="jour"
    image=curseur.execute("SELECT * FROM imagesAD WHERE Mode<>'{0}' ORDER BY RANDOM()".format(mode)).fetchone()

    if texte==None and image==None:
        return
    elif image==None:
        content=formatage(texte["Message"],member,member.guild)
        await bot.get_channel(chan).send(content=content)
    elif texte==None:
        await getAvatar(member)
        squaretoround(member.id)
        fusionAdieu(image["Path"],member,image["Message"],image["Couleur"],image["Taille"],member.guild,image["Filtre"])
        await bot.get_channel(chan).send(file=discord.File("Temp/AD{0}.png".format(member.id)))
    else:
        content=formatage(texte["Message"],member,member.guild)
        await getAvatar(member)
        squaretoround(member.id)
        fusionAdieu(image["Path"],member,image["Message"],image["Couleur"],image["Taille"],member.guild,image["Filtre"])
        await bot.get_channel(chan).send(content=content,file=discord.File("Temp/AD{0}.png".format(member.id)))
