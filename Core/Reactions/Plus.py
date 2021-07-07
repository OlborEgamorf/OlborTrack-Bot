### PEUT ETRE OBSOLETE

from Core.Reactions.Outils import removeReact, embedE
from Core.Fonctions.EcritureRecherche3 import rechercheCsv
from Stats.Graphiques.Spider import graphSpider
from Geo.MoreInfo import embedMoreGeo
import discord

async def reactPlus(message,user):
    global embedE
    for i in message.mentions:
        if i.id==user.id:
            await removeReact(message,772766034163400715,user)
            return
    if len(message.mentions)>0:
        table,color,ids,names=[],[],[],[]
        descip=""
        for i in message.mentions:
            table.append(rechercheCsv("trivial",0,i.id,0,0,0)[0])
            color.append(i.color)
            ids.append(i.id)
            names.append(i.name)
        table.append(rechercheCsv("trivial",0,user.id,0,0,0)[0])
        color.append(user.color)
        ids.append(user.id)
        names.append(user.name)
        for i in ids:
            descip+="<@"+str(i)+"> "
        link=graphSpider(table,user.id,color,names)
        messageTU=await message.channel.send(content=":spider_web: "+descip, file=discord.File(link))
        await messageTU.add_reaction("<:otPLUS:772766034163400715>")
    else:
        lat=message.content.split(" ")[1]
        lon=message.content.split(" ")[2]
        embedP=await embedMoreGeo([lat,lon])
        await message.channel.send(embed=embedP)
    try:
        for i in message.reactions:
            if i.emoji.id==772766034163400715:
                await i.clear()
    except discord.errors.Forbidden:
        await message.channel.send(embed=embedE,delete_after=8)
    except:
        pass
    return