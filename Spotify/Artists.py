import discord
from Core.Fonctions.WebRequest import webRequestHD
from Core.Fonctions.AuteurIcon import auteur

async def embedSpotifyArtist(table,code):
    embedS=discord.Embed(title=table["artists"]["items"][0]["name"],color=0x1DB954)
    embedS.set_footer(text="OT!spoartiste")
    descip=""
    if table["artists"]["items"][0]["genres"]!=[]:
        for i in table["artists"]["items"][0]["genres"]:
            descip+=i+"\n"
        embedS.add_field(name="Genres",value=descip,inline=True)
    embedS.add_field(name="Followers",value=table["artists"]["items"][0]["followers"]["total"],inline=True)
    embedS.add_field(name="Lien",value="[Lien]("+table["artists"]["items"][0]["external_urls"]["spotify"]+")",inline=True)
    if table["artists"]["items"][0]["images"]!=[]:
        embedS.set_thumbnail(url=table["artists"]["items"][0]["images"][0]["url"])
    embedS=auteur(table["artists"]["items"][0]["external_urls"]["spotify"],0,0,embedS,"spo")

    id=table["artists"]["items"][0]["external_urls"]["spotify"].split("/")[4]
    headers = {'Authorization': code, 'Content-Type': 'application/json', 'Accept': 'application/json'}
    params = (('include_groups', 'album'),('market', 'FR'),('limit',10))
    tableAlbum=await webRequestHD('https://api.spotify.com/v1/artists/'+id+'/albums',headers,params)
    titre="Albums"
    if tableAlbum["items"]==[]:
        params = (('include_groups', 'single'),('market', 'FR'),('limit',10))
        tableAlbum=await webRequestHD('https://api.spotify.com/v1/artists/'+id+'/albums',headers,params)
        titre="Singles"
        if tableAlbum["items"]==[]:
            params = (('include_groups', 'appears_on'),('market', 'FR'),('limit',10))
            tableAlbum=await webRequestHD('https://api.spotify.com/v1/artists/'+id+'/albums',headers,params)
            titre="Apparitions"
        else:
            return embedS
    descip=""
    for i in tableAlbum["items"]:
        descip+="["+i["name"]+"]("+i["external_urls"]["spotify"]+")\n"
    embedS.add_field(name=titre,value=descip,inline=True)

    headers = {'Authorization': code, 'Content-Type': 'application/json', 'Accept': 'application/json'}
    params = (('market', 'FR'),('limit',5))
    tableTop=await webRequestHD('https://api.spotify.com/v1/artists/'+id+'/top-tracks',headers,params)
    descip=""
    if tableTop["tracks"]!=[]:
        for i in tableTop["tracks"]:
            descip+="["+i["name"]+"]("+i["external_urls"]["spotify"]+")\n"
        embedS.add_field(name="Top titres",value=descip,inline=True)
    return embedS