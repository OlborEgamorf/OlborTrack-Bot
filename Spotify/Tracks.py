import discord
from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.TempsVoice import tempsVoice
from Core.Fonctions.WebRequest import webRequestHD

async def embedSpotifyTrack(table,code):
    embedS=discord.Embed(title=table["tracks"]["items"][0]["name"],color=0x1DB954)
    embedS.set_footer(text="OT!spotitre")
    embedS=auteur(table["tracks"]["items"][0]["external_urls"]["spotify"],0,0,embedS,"spo")
    if table["tracks"]["items"][0]["album"]["images"]!=[]:
        embedS.set_thumbnail(url=table["tracks"]["items"][0]["album"]["images"][0]["url"])
    descip=""
    for i in table["tracks"]["items"][0]["artists"]:
        descip+="["+i["name"]+"]("+i["external_urls"]["spotify"]+"),"
    embedS.add_field(name="Infos",value="Artiste(s) : "+descip[0:len(descip)-1]+"\nAlbum : ["+table["tracks"]["items"][0]["album"]["name"]+"]("+table["tracks"]["items"][0]["album"]["external_urls"]["spotify"]+")\nPiste "+str(table["tracks"]["items"][0]["track_number"])+"/"+str(table["tracks"]["items"][0]["album"]["total_tracks"])+"\nDurée : "+tempsVoice(table["tracks"]["items"][0]["duration_ms"]/1000)+"\n[Lien]("+table["tracks"]["items"][0]["external_urls"]["spotify"]+")", inline=True)
    headers = {'Authorization': code, 'Content-Type': 'application/json', 'Accept': 'application/json'}
    params = (('market', 'FR'),('limit',10))
    id=table["tracks"]["items"][0]["id"]
    tableTrack=await webRequestHD('https://api.spotify.com/v1/audio-features/'+id,headers,params)
    embedS.add_field(name="Indicateurs (de 0 à 1)", value="Dansant : "+str(tableTrack["danceability"])+"\nEnergique : "+str(tableTrack["energy"])+"\nInstrumental : "+str(tableTrack["instrumentalness"])+"\nEn live : "+str(tableTrack["liveness"])+"\nPositivité : "+str(tableTrack["valence"]),inline=True)
    embedS.add_field(name="Autre",value="Tempo : "+str(tableTrack["tempo"])+" BPM\nIntensité : "+str(tableTrack["loudness"])+" dB",inline=True)
    return embedS