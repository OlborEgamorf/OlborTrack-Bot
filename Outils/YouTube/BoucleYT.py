from Outils.YouTube.EmbedsYT import embedAlertYT
from Core.Fonctions.WebRequest import webRequest
from Core.OS.Keys3 import ytKey
from Stats.SQL.ConnectSQL import connectSQL
import asyncio

async def boucleYT(bot,dictGuilds):
    while True:
        await asyncio.sleep(300)
        for i in dictGuilds:
            for j in dictGuilds[i].yt:
                try:
                    data=await webRequest("https://www.googleapis.com/youtube/v3/search?key={0}&channelId={1}&part=snippet,id&order=date&maxResults=7&type=video".format(ytKey,j.chaine))
                    assert data!=False
                    count=0
                    liste=[]
                    while data["items"][count]["id"]["videoId"]!=j.last:
                        liste.append(data)
                        count+=1
                    for i in liste.reverse():
                        await bot.get_channel(j.salon).send(embed=await embedAlertYT(i,j),content=j.descip)
                    connexion,curseur=connectSQL(dictGuilds[i].id,"Guild","Guild",None,None)
                    curseur.execute("UPDATE youtube SET LastID='{0}' WHERE Nombre={1}".format(data["items"][0]["id"]["videoId"],j.numero))
                    j.last=data["items"][0]["id"]["videoId"]
                    connexion.commit()
                except:
                    pass