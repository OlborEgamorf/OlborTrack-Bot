import os

import aiofiles
import aiohttp


async def webRequest(link):
    """Effectue une requête Get sur un lien donné."""
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=3.0)) as session:
        async with session.get(link) as reponse:
            if reponse.status!=200:
                return False
            return await reponse.json()

async def webRequestHD(link,head,data):
    """Effectue une requête Get sur un lien donné avec des arguments."""
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=3.0),headers=head) as session:
        async with session.get(link,params=data) as reponse:
            if reponse.status==401:
                return None
            if reponse.status!=200:
                return False
            return await reponse.json()

async def getImage(id):
    """Récupère et enregistre un emoji en format PNG avec d'ID de l'emoji."""
    async with aiohttp.ClientSession() as session:
        async with session.get("https://cdn.discordapp.com/emojis/"+str(id)+".png") as resp:
            if resp.status == 200:
                f = await aiofiles.open("PNG/"+str(id)+".png", mode='wb')
                await f.write(await resp.read())
                await f.close()

async def getAvatar(user):
    """Récupère et enregistre l'avatar d'un utilisateur Discord."""
    async with aiohttp.ClientSession() as session:
        async with session.get(str(user.avatar_url_as(format="png",size=128))) as resp:
            if resp.status == 200:
                f = await aiofiles.open("PNG/"+str(user.id)+".png", mode='wb')
                await f.write(await resp.read())
                await f.close()


async def getAttachment(message):
    assert message.attachments[0].filename[-4:].lower() in ("jpg","png","jpeg"), "Le format de l'image n'est pas bon, veuillez me donner un PNG ou un JPG !"
    async with aiohttp.ClientSession() as session:
        async with session.get(message.attachments[0].url) as resp:
            if resp.status == 200:
                if not os.path.exists("BV/{0}".format(message.guild.id)):
                    os.makedirs("BV/{0}".format(message.guild.id))
                count=0
                path="BV/{0}/{1}.png".format(message.guild.id,message.attachments[0].filename)
                while os.path.isfile(path): 
                    path="BV/{0}/{1}{2}.png".format(message.guild.id,message.attachments[0].filename,count)
                    count+=1
                f = await aiofiles.open(path, mode='wb')
                await f.write(await resp.read())
                await f.close()
                return path
