import discord
from discord.ext import commands
from Outils.CommandesAuto import boucleAutoCMD, boucleAutoStats
from Outils.Twitch.Boucle import boucleTwitch
from Outils.Twitter.BoucleTwitter import boucleTwitter
from Outils.VoiceEphem.CheckState import checkAll
from Outils.YouTube.BoucleYT import boucleYT
from Sondages.exePolls import recupPoll
from Stats.SQL.NewGuild import alterHBM, createDirSQL
from Stats.Tracker.Voice import disconnect, reconnect

from Core.Companion.CompConnect import connectCompanion
from Core.OTGuild import OTGuildCMD


class OlborTrack(commands.Bot):
    def __init__(self,version:str,*args,**kwargs):
        super().__init__(*args,**kwargs) 
        self.listeMP=["help","rappel","dice","feedback","roulette","invite","support","avatar","about","test","credits","servcount","rappelmp","recap"]
        self.listeOS=["messganim","saloganim","emotganim","reacganim","motsganim","freqganim","voicganim","vchaganim","getdata"]
        self.dictGuilds={}
        self.dictJeux={}
        self.dictPolls={}
        self.dictVoice={}
        self.inGame=[]
        self.dictTasks={}
        self.loop.create_task(self.startBot(version))

    async def startBot(self,version:str):
        await self.wait_until_ready()
        await self.change_presence(status=discord.Status.online, activity=discord.Game(name="Commande d'aide : OT!help"))
        print("-----\nConnecté dans {0.user} \nLatence : {0.latency}".format(self))
        for i in self.guilds:
            try:
                self.dictGuilds[i.id]=OTGuildCMD(i.id,True)
            except:
                alterHBM(self)
                createDirSQL(i)
                self.dictGuilds[i.id]=OTGuildCMD(i.id,True)
            await checkAll(self.dictGuilds[i.id],self)
        self.dictGuilds[None]=OTGuildCMD("MP",False)

        for i in self.commands:
            self.listeOS.append(i.name)
            for j in i.aliases:
                self.listeOS.append(j)

        await recupPoll(self)
        if version=="ot":
            await self.get_channel(712753819447984248).send("TrackOS Commandes : Executé ")
            self.dictTasks["auto"]=self.loop.create_task(boucleAutoCMD(self,self.dictGuilds))
            self.dictTasks["twitch"]=self.loop.create_task(boucleTwitch(self,self.dictGuilds))
            self.dictTasks["yt"]=self.loop.create_task(boucleYT(self,self.dictGuilds))
            self.dictTasks["twitter"]=self.loop.create_task(boucleTwitter(self,self.dictGuilds))
            self.dictTasks["stats"]=self.loop.create_task(boucleAutoStats(self,self.dictGuilds))
            await disconnect(self)
            await reconnect(self,self.dictGuilds)

        await connectCompanion(self)

        print("TOUS LES PROCESSUS SONT TERMINES")
