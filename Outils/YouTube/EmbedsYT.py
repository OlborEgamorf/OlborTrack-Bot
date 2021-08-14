from Core.Fonctions.WebRequest import webRequest
from Core.OS.Keys3 import ytKey
import discord
from Core.Fonctions.Embeds import addtoFields, createFields, sendEmbed
from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.AuteurIcon import auteur

async def embedAlertYT(data,j):
    user=await webRequest("https://www.googleapis.com/youtube/v3/channels?key={0}&id={1}&part=snippet&maxResults=1".format(ytKey,j.chaine))
    embed=discord.Embed(title=data["items"][0]["snippet"]["title"],url="https://www.youtube.com/watch?v={0}".format(data["items"][0]["id"]["videoId"]),description="Nouvelle vidéo !",color=0xFF0000)
    embed.set_author(name=user["items"][0]["snippet"]["title"],icon_url=user["items"][0]["snippet"]["thumbnails"]["medium"]["url"],url="https://youtube.com/channel/{0}".format(j.chaine))
    embed.set_thumbnail(url=user["items"][0]["snippet"]["thumbnails"]["medium"]["url"])
    embed.set_footer(text="OT!youtube")
    embed.add_field(name="Description",value=data["items"][0]["snippet"]["description"],inline=True)
    embed.set_image(url=data["items"][0]["snippet"]["thumbnails"]["medium"]["url"])
    embed.add_field(name="Lien",value="[Lien de la vidéo](https://www.youtube.com/watch?v={0})".format(data["items"][0]["id"]["videoId"]),inline=True)
    return embed

def embedYT(table,page,pagemax,mobile):
    embed=discord.Embed(title="Liste des alertes YouTube actives sur votre serveur",color=0xf54269)
    stop=15*page if 15*page<len(table) else len(table)
    field1,field2,field3="","",""
    for i in range(15*(page-1),stop):
        nombre="`{0}`".format(table[i]["Nombre"])
        emote="{0}".format(table[i]["Nom"])
        salon="<#{0}>".format(table[i]["Salon"])

        field1,field2,field3=addtoFields(field1,field2,field3,mobile,nombre,emote,salon)

    embed=createFields(mobile,embed,field1,field2,field3,"Numéro","Chaîne","Salon") 
    embed.set_footer(text="Page {0}/{1}".format(page,pagemax))
    return embed