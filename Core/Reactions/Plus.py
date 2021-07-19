from Geo.MoreInfo import embedMoreGeo
import discord

async def reactPlus(message,user):
    lat=message.content.split(" ")[1]
    lon=message.content.split(" ")[2]
    embedP=await embedMoreGeo([lat,lon])
    await message.reply(embed=embedP)