import discord
from Core.Fonctions.WebRequest import webRequestHD
from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.TempsVoice import tempsVoice

async def embedSpotifyShow(table,code):
    embedS=discord.Embed(title=table["shows"]["items"][0]["name"],color=0x1DB954)
    embedS.add_field(name="Description",value=table["shows"]["items"][0]["description"],inline=False)
    langue="Langue(s) : "+table["shows"]["items"][0]["languages"][0]
    for i in range(1,len(table["shows"]["items"][0]["languages"])):
        langue=" / "+langue
    embedS.add_field(name="Infos",value="Épisodes : "+str(table["shows"]["items"][0]["total_episodes"])+"\n"+langue,inline=True)
    embedS.add_field(name="Créateur",value=table["shows"]["items"][0]["publisher"],inline=True)
    embedS.add_field(name="Lien",value="[Podcast]("+table["shows"]["items"][0]["external_urls"]["spotify"]+")",inline=True)
    embedS=auteur(table["shows"]["items"][0]["external_urls"]["spotify"],0,0,embedS,"spo")
    embedS.set_footer(text="OT!spopodcast")
    if table["shows"]["items"][0]["images"]!=[]:
        embedS.set_thumbnail(url=table["shows"]["items"][0]["images"][0]["url"])
    headers = {'Authorization': code, 'Content-Type': 'application/json', 'Accept': 'application/json'}
    params = (('market', 'FR'),('limit',10))
    id=table["shows"]["items"][0]["id"]
    tableAlbum=await webRequestHD('https://api.spotify.com/v1/shows/'+id,headers,params)
    embedS.add_field(name="Dernier épisode :", value="["+tableAlbum["episodes"]["items"][0]["name"]+"]("+tableAlbum["episodes"]["items"][0]["external_urls"]["spotify"]+")\nDate : "+tableAlbum["episodes"]["items"][0]["release_date"]+"\nDurée : "+tempsVoice(tableAlbum["episodes"]["items"][0]["duration_ms"]/1000),inline=False)
    return embedS