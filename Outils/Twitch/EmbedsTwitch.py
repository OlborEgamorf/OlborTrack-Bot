import discord
from Core.Fonctions.Embeds import addtoFields, createFields
from Core.Fonctions.WebRequest import webRequestHD
from Core.OS.Keys3 import headersTwitch


async def embedAlert(data,stream):
    user=await webRequestHD("https://api.twitch.tv/helix/users",headersTwitch,(("login",stream),("id",data["data"][0]["user_id"])))
    embed=discord.Embed(title=data["data"][0]["title"],url="https://www.twitch.tv/{0}".format(data["data"][0]["user_name"]),description="Live lancé !",color=0x9146FF)
    embed.set_author(name=data["data"][0]["user_login"],icon_url=user["data"][0]["profile_image_url"],url="https://www.twitch.tv/{0}".format(data["data"][0]["user_name"]))
    embed.set_thumbnail(url=user["data"][0]["profile_image_url"])
    embed.set_footer(text="OT!twitch")
    embed.add_field(name="Jeu",value=data["data"][0]["game_name"],inline=True)
    embed.add_field(name="Spectateurs",value=data["data"][0]["viewer_count"],inline=True)
    return embed

def embedTwitch(table,page,pagemax,mobile):
    embed=discord.Embed(title="Liste des alertes Twitch actives sur votre serveur",color=0xf54269)
    stop=15*page if 15*page<len(table) else len(table)
    field1,field2,field3="","",""
    for i in range(15*(page-1),stop):
        nombre="`{0}`".format(table[i]["Nombre"])
        emote="{0}".format(table[i]["Stream"])
        salon="<#{0}>".format(table[i]["Salon"])

        field1,field2,field3=addtoFields(field1,field2,field3,mobile,nombre,emote,salon)

    embed=createFields(mobile,embed,field1,field2,field3,"Numéro","Stream","Salon") 
    embed.set_footer(text="Page {0}/{1}".format(page,pagemax))
    return embed
