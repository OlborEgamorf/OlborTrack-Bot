import discord
from Core.Fonctions.WebRequest import webRequestHD
from Core.Fonctions.AuteurIcon import auteur

async def embedSpotifyAlbum(table,code):
    headers = {'Authorization': code, 'Content-Type': 'application/json', 'Accept': 'application/json'}
    params = (('market', 'FR'),('limit',10))
    id=table["albums"]["items"][0]["id"]
    tableAlbum=await webRequestHD('https://api.spotify.com/v1/albums/'+id,headers,params)
    titre=tableAlbum["artists"][0]["name"]
    if len(tableAlbum["artists"])!=1:
        for i in range(1,len(tableAlbum["artists"])):
            titre=titre+" / "+tableAlbum["artists"][i]["name"]
    embedS=discord.Embed(title=titre+" - "+tableAlbum["name"],color=0x1DB954)
    embedS=auteur(tableAlbum["external_urls"]["spotify"],0,0,embedS,"spo")
    embedS.set_footer(text="OT!spoalbum")
    embedS.add_field(name="Morceaux",value=tableAlbum["total_tracks"],inline=True)
    embedS.add_field(name="Date",value=tableAlbum["release_date"],inline=True)
    embedS.add_field(name="Liens",value="[Artiste]("+tableAlbum["artists"][0]["external_urls"]["spotify"]+")\n[Album]("+tableAlbum["external_urls"]["spotify"]+")",inline=True)
    if tableAlbum["images"]!=[]:
        embedS.set_thumbnail(url=tableAlbum["images"][0]["url"])
    if len(tableAlbum["tracks"]["items"])>10:
        descip=""
        for i in range(0,10):
            descip+=str(tableAlbum["tracks"]["items"][i]["track_number"])+". ["+tableAlbum["tracks"]["items"][i]["name"]+"]("+tableAlbum["tracks"]["items"][i]["external_urls"]["spotify"]+")\n"
        embedS.add_field(name="Titres",value=descip,inline=True)
        descip=""
        if len(tableAlbum["tracks"]["items"])>20:
            borne=20
        else:
            borne=len(tableAlbum["tracks"]["items"])
        for i in range(10,borne):
            descip+=str(tableAlbum["tracks"]["items"][i]["track_number"])+". ["+tableAlbum["tracks"]["items"][i]["name"]+"]("+tableAlbum["tracks"]["items"][i]["external_urls"]["spotify"]+")\n"
        embedS.add_field(name="Titres",value=descip,inline=True)
    else:
        descip=""
        for i in range(0,len(tableAlbum["tracks"]["items"])):
            descip+=str(tableAlbum["tracks"]["items"][i]["track_number"])+". ["+tableAlbum["tracks"]["items"][i]["name"]+"]("+tableAlbum["tracks"]["items"][i]["external_urls"]["spotify"]+")\n"
        embedS.add_field(name="Titres",value=descip,inline=True)
    return embedS