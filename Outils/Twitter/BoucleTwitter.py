from Core.OS.Keys3 import headerTwit

async def boucleTwitter(bot,dictGuilds):
    while True:
        await asyncio.sleep(90)
        for i in dictGuilds:
            for j in dictGuilds[i].twitter:
                try:
                    data=await webRequestHD("https://api.twitter.com/2/tweets/search/recent",headerTwit,(("query","from:{0}".format(accountID)),("tweet.fields","id"),("max_results",20)))
                    assert data!=False
                    count=0
                    liste=[]
                    while data["data"][count]["id"]!=j.last:
                        liste.append(data["data"][count]["id"])
                        count+=1
                    for i in liste.reverse():
                        await bot.get_channel(j.salon).send(content="{0}\nhttps://twitter.com/status/{1}".format(j.descip,i))
                    connexion,curseur=connectSQL(dictGuilds[i].id,"Guild","Guild",None,None)
                    curseur.execute("UPDATE twitter SET LastID={0} WHERE Nombre={1}".format(data["data"][0]["id"],j.numero))
                    j.last=data["data"][0]["id"]
                    connexion.commit()
                except:
                    pass