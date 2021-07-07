from Core.Fonctions.WebRequest import webRequestHD
from Core.Fonctions.AuteurIcon import auteur
import discord

async def embedSpotifyPlaylist(table,code):
    total=str(table["playlists"]["items"][0]["tracks"]["total"])
    headers = {'Authorization': code, 'Content-Type': 'application/json', 'Accept': 'application/json'}
    params = (('market', 'FR'),('limit',10))
    id=table["playlists"]["items"][0]["id"]
    tableAlbum=await webRequestHD('https://api.spotify.com/v1/playlists/'+id,headers,params)
    embedS=discord.Embed(title=tableAlbum["name"],color=0x1DB954)
    embedS=auteur(tableAlbum["external_urls"]["spotify"],0,0,embedS,"spo")
    if tableAlbum["description"]!="":
        embedS.add_field(name="Description", value=tableAlbum["description"],inline=True)
    if tableAlbum["images"]!=[]:
        embedS.set_thumbnail(url=tableAlbum["images"][0]["url"])
    if tableAlbum["owner"]["id"]=="spotify":
        owner=tableAlbum["owner"]["display_name"]+" <:otVERIF:763841329046224946>"
    else:
        owner=tableAlbum["owner"]["display_name"]
    embedS.add_field(name="Infos", value="Créateur : "+owner+"\nAbonnés : "+str(tableAlbum["followers"]["total"])+"\nPublic : "+str(tableAlbum["public"])+"\nMorceaux : "+total,inline=True)
    embedS.add_field(name="Liens", value="[Playlist]("+tableAlbum["external_urls"]["spotify"]+")\n[Créateur]("+tableAlbum["owner"]["external_urls"]["spotify"]+")",inline=True)
    embedS.set_footer(text="OT!spoplaylist")
    return embedS