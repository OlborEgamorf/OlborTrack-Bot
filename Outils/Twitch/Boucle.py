import asyncio

import requests
from Core.Fonctions.WebRequest import webRequestHD
from Core.OS.Keys3 import headersTwitch, idTwitch, secretTwitch
from Outils.Twitch.EmbedsTwitch import embedAlert
from Stats.SQL.ConnectSQL import connectSQL

headers = {
    'client_id': idTwitch,
    "client_secret": secretTwitch,
    "grant_type":"client_credentials",
    "scope":""
}

async def boucleTwitch(bot,dictGuilds):
    while True:
        await asyncio.sleep(120)
        for i in dictGuilds:
            for j in dictGuilds[i].twitch:
                try:
                    data=await webRequestHD("https://api.twitch.tv/helix/streams",headersTwitch,(("user_login",j.stream),("first",1)))
                    if data==None:
                        response = requests.post('https://id.twitch.tv/oauth2/token', data=headers)
                        headersTwitch["Authorization"]="Bearer {0}".format(response.json()["access_token"])
                        await bot.get_channel(752150155276451993).send("TOKEN TWITCH : {0}".format(response.json()["access_token"]))
                    assert data!=False and data!=None
                    if data["data"]!=[]:
                        live=True
                        if not j.sent:
                            await bot.get_channel(j.salon).send(embed=await embedAlert(data,j.stream),content=j.descip)
                    else:
                        live=False
                    if live!=j.sent:
                        connexion,curseur=connectSQL(dictGuilds[i].id)
                        curseur.execute("UPDATE twitch SET Sent={0} WHERE Nombre={1}".format(live,j.numero))
                        j.sent=live
                        connexion.commit()
                except:
                    pass