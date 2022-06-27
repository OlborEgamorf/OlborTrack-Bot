import discord
from discord.ext import commands
from Outils.CommandesAuto import boucleAutoCMD, boucleAutoStats
from Outils.Twitch.Boucle import boucleTwitch
from Outils.Twitter.BoucleTwitter import boucleTwitter
from Outils.VoiceEphem.CheckState import checkAll
from Outils.YouTube.BoucleYT import boucleYT
from Sondages.exePolls import recupPoll
from Stats.Commandes.Slash.Random import ViewReload
from Stats.SQL.NewGuild import alterHBM, createDirSQL
from Stats.Tracker.Voice import disconnect, reconnect

from Core.Companion.CompConnect import connectCompanion
from Core.OTGuild import OTGuildCMD
from Core.Reactions.exeReactions import (ViewControls, ViewPageGraph,
                                         ViewRapports)


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
        self.version=version

    async def setup_hook(self):
        print("-----\nConnecté dans {0.user} \nLatence : {0.latency}".format(self))

        self.dictGuilds[None]=OTGuildCMD("MP",False)

        guild=discord.Object(id=990575111193116682)
        self.tree.copy_global_to(guild=guild)
        await self.tree.sync(guild=guild)
        self.add_view(ViewControls())
        self.add_view(ViewPageGraph())
        self.add_view(ViewReload())
        self.add_view(ViewRapports(["Salons","Voice","Emotes","Reactions","Freq"]))


        for i in self.commands:
            self.listeOS.append(i.name)
            for j in i.aliases:
                self.listeOS.append(j)

        if self.version=="ot":
            self.dictTasks["auto"]=self.loop.create_task(boucleAutoCMD(self,self.dictGuilds))
            self.dictTasks["twitch"]=self.loop.create_task(boucleTwitch(self,self.dictGuilds))
            self.dictTasks["yt"]=self.loop.create_task(boucleYT(self,self.dictGuilds))
            self.dictTasks["twitter"]=self.loop.create_task(boucleTwitter(self,self.dictGuilds))
            self.dictTasks["stats"]=self.loop.create_task(boucleAutoStats(self,self.dictGuilds))
    
        await connectCompanion(self)
        self.loop.create_task(self.callsAfter())

        print("TOUS LES PROCESSUS SONT TERMINES")
    
    async def callsAfter(self):
        await self.wait_until_ready()

        for i in self.guilds:
            try:
                self.dictGuilds[i.id]=OTGuildCMD(i.id,True)
            except:
                alterHBM(self)
                createDirSQL(i)
                self.dictGuilds[i.id]=OTGuildCMD(i.id,True)
    
        await self.get_channel(712753819447984248).send("TrackOS Commandes : Executé ")
        await disconnect(self)
        await reconnect(self,self.dictGuilds)
        await recupPoll(self)
        for i in self.guilds:
            await checkAll(self.dictGuilds[i.id],self)
