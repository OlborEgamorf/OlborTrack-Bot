from Core.OS.Keys3 import headerTwit
from Core.Fonctions.WebRequest import webRequestHD
import asyncio
from Stats.SQL.ConnectSQL import connectSQL

async def boucleTwitter(bot,dictGuilds):
    while True:
        await asyncio.sleep(150)
        for i in dictGuilds:
            for j in dictGuilds[i].twitter:
                try:
                    data=await webRequestHD("https://api.twitter.com/2/tweets/search/recent",headerTwit,(("query","from:{0}".format(j.compte)),("tweet.fields","id,referenced_tweets"),("max_results",20)))
                    assert data!=False
                    count=0
                    liste=[]
                    while int(data["data"][count]["id"])!=j.last:
                        liste.append(data["data"][count])
                        count+=1
                        if count==len(data["data"]):
                            break
                    liste.reverse()
                    for h in liste:
                        special=False
                        if "referenced_tweets" in h:
                            for k in h["referenced_tweets"]:
                                if k["type"]=="replied_to":
                                    special=True
                                    await bot.get_channel(j.salon).send(content="{0} (**Réponse**)\nhttps://twitter.com/{1}/status/{2}".format(j.descip,j.compte,h["id"]))
                                elif k["type"]=="retweeted":
                                    special=True
                                    await bot.get_channel(j.salon).send(content="{0} (**RT**)\nhttps://twitter.com/{1}/status/{2}".format(j.descip,j.compte,h["id"]))
                        if not special:
                            await bot.get_channel(j.salon).send(content="{0}\nhttps://twitter.com/{1}/status/{2}".format(j.descip,j.compte,h["id"]))
                    connexion,curseur=connectSQL(dictGuilds[i].id)
                    curseur.execute("UPDATE twitter SET LastID={0} WHERE Nombre={1}".format(data["data"][0]["id"],j.numero))
                    j.last=int(data["data"][0]["id"])
                    connexion.commit()
                except:
                    pass