import asyncio
import aiohttp
from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.WebRequest import webRequestHD
from Core.OS.Keys3 import headersTwitch
import discord
from Outils.Twitch.EmbedsTwitch import embedAlert

async def boucleTwitch(bot,dictGuilds):
    while True:
        await asyncio.sleep(120)
        for i in dictGuilds:
            for j in dictGuilds[i].twitch:
                try:
                    data=await webRequestHD("https://api.twitch.tv/helix/streams",headersTwitch,(("user_login",j.stream),("first",1)))
                    if data["data"]!=[]:
                        live=True
                        if not j.sent:
                            await bot.get_channel(j.salon).send(embed=await embedAlert(data,j.stream),content=j.descip)
                    else:
                        live=False
                    if live!=j.sent:
                        connexion,curseur=connectSQL(dictGuilds[i].id,"Guild","Guild",None,None)
                        curseur.execute("UPDATE twitch SET Sent={0} WHERE Nombre={1}".format(live,j.numero))
                        j.sent=live
                        connexion.commit()
                except:
                    pass