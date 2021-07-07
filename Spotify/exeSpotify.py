from Core.OS.Keys3 import spotifyID, spotifySecret
from Spotify.Albums import embedSpotifyAlbum 
from Spotify.Artists import embedSpotifyArtist
from Spotify.Playlists import embedSpotifyPlaylist
from Spotify.Podcasts import embedSpotifyShow
from Spotify.Tracks import embedSpotifyTrack
import asyncio
import base64
import requests
from Core.Fonctions.Embeds import embedAssert, exeErrorExcept
from Core.Fonctions.Phrase import createPhrase
from Core.Fonctions.WebRequest import webRequestHD

async def exeSpotify(ctx,bot,args,option):
    try:
        assert len(args)>0, "Donnez moi une recherche à faire !"
        dictOption={"spoartiste":"artist","spoalbum":"album","spotitre":"track","spopodcast":"show","spoplaylist":"playlist"}
        args=createPhrase(args)
        connect=await loginSpotify(dictOption[option], args)
        if option=="spoartiste":
            embedS=await embedSpotifyArtist(connect[0],connect[1])
        elif option=="spotitre":
            embedS=await embedSpotifyTrack(connect[0],connect[1])
        elif option=="spoalbum":
            embedS=await embedSpotifyAlbum(connect[0],connect[1])
        elif option=="spopodcast":
            embedS=await embedSpotifyShow(connect[0],connect[1])
        elif option=="spoplaylist":
            embedS=await embedSpotifyPlaylist(connect[0],connect[1])
    except AssertionError as er:
        embedS=embedAssert(str(er))
    except asyncio.exceptions.TimeoutError:
        await ctx.send(embed=embedAssert("Temps de requête écoulé, veuillez réessayer."))
    except:
        embedS=await exeErrorExcept(ctx,bot,args)
    await ctx.send(embed=embedS)
    return

async def loginSpotify(option, args):
    client_id = spotifyID
    client_secret = spotifySecret
    encodedData = base64.b64encode(bytes(f"{client_id}:{client_secret}", "ISO-8859-1")).decode("ascii")
    access = {'Authorization': "Basic "+encodedData}
    data = {'grant_type': 'client_credentials'}
    response = requests.post('https://accounts.spotify.com/api/token', headers=access, data=data)
    code='Bearer '+response.json()["access_token"]
    headers = {'Authorization': code, 'Content-Type': 'application/json', 'Accept': 'application/json'}
    params = (('q', args),('type', option),('market', 'FR'),('limit', '1'))
    table=await webRequestHD("https://api.spotify.com/v1/search",headers,params)
    assert table[option+"s"]["items"]!=[],"Je n'ai rien trouvé ! Vérifiez bien ce que vous cherchez."
    return table, code