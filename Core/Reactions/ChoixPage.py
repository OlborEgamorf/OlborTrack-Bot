from Stats.SQL.ConnectSQL import connectSQL
from Core.Reactions.ChangePage import reactStats
import asyncio

async def choosePage(message:int,reaction,bot,guildOT,payload):
    """Permet de choisir rapidement quelle page consulter"""
    try:
        connexionCMD,curseurCMD=connectSQL(guildOT.id,"Commandes","Guild",None,None)
        ligne=curseurCMD.execute("SELECT * FROM commandes WHERE MessageID={0}".format(message)).fetchone()
        pagemax=ligne["PageMax"]
        mess=await bot.get_channel(payload.channel_id).send("<:otCHOIXPAGE:887022335578767420> : A quelle page voulez-vous aller ?")

        def check(messWait):
            try:
                int(messWait.content)
            except:
                return False
            return messWait.author.id==payload.user_id and messWait.channel.id==payload.channel_id and int(messWait.content)<=pagemax

        messWait=await bot.wait_for("message",check=check,timeout=15)
        await mess.delete()
        try:
            await messWait.delete()
        except:
            pass

        if ligne!=None:
            curseurCMD.execute("UPDATE commandes SET Page={0} WHERE MessageID={1}".format(int(messWait.content),message))
            connexionCMD.commit()
            await reactStats(message,reaction,bot,guildOT,payload)
    except asyncio.TimeoutError:
        await mess.delete()