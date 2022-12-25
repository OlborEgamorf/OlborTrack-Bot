from time import time

import discord
from Core.OTGuild import OTGuild
from Stats.SQL.Execution import executeStatsFreq
from Stats.SQL.ConnectSQL import connectSQL
from Stats.SQL.Execution import executeStats
from Stats.SQL.Verification import verifExecSQL

listeCo={}
dictMois={1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}

class Voice:
    """Classe qui régit les statistiques vocales. Chaque membre connecté à un salon vocal possède son objet Voice. Elle contient les informations sur le membre, le serveur et le salon où il est connecté, et le moment où il s'est connecté. Elle possède une méthode qui enregistre les stats quand elle est appelée."""
    def __init__(self,member:discord.Member,chan:discord.VoiceChannel,guild:discord.Guild):
        """
        Entrées :
            member : l'objet discord.Member du membre
            chan : l'objet discord.VoiceChannel du salon connecté
            guild : l'objet discord.Guild du serveur connecté"""
        self.user=member
        self.userid=member.id
        self.channelid=chan.id
        self.guildid=guild.id
        self.guild=guild
        self.time=time()
        self.connect=True

    def exeStat(self,guild:OTGuild):
        """Méthode qui calcule le temps passé en vocal, déclare l'utilisateur comme déconnecté et enregistre les stats.
        
        Entrée :
            guild : l'objet OTGuild du serveur concerné"""
        self.connect=False
        count=int(time()-self.time)
        if self.channelid in guild.voiceephem:
            self.channelid=0
        if count!=0:
            connexion,curseur=connectSQL(guild.id)
            executeStats("voice",self.userid,self.channelid,count,curseur)

            import datetime
            dateStart=datetime.datetime.fromtimestamp(self.time)
            dateStop=datetime.datetime.fromtimestamp(time())
            heureStart,minStart,secStart=int(dateStart.strftime("%H")),int(dateStart.strftime("%M")),int(dateStart.strftime("%S"))
            heureStop,minStop,secStop=int(dateStop.strftime("%H")),int(dateStop.strftime("%M")),int(dateStop.strftime("%S"))

            if heureStop<heureStart:
                heureStop+=24

            for i in range(heureStart,heureStop+1):
                if heureStart==heureStop:
                    count=(minStop-minStart)*60+(secStop-secStart)
                elif i==heureStart:
                    count=3600-minStart*60-secStart
                elif i==(heureStop):
                    count=minStop*60+secStop
                else:
                    count=3600
                
                executeStatsFreq("voice",self.userid,self.channelid,i%24,count,curseur)

            connexion.commit()



async def voiceConnect(member,before,after,guild):
    if member.bot==False and guild.mstats[1]["Statut"]==True and guild.stats:
        if before.channel!=None:
            if verifExecSQL(guild,before.channel,member) and member.id in listeCo:
                listeCo[member.id].exeStat(guild)
        if after.channel!=None:
            if verifExecSQL(guild,after.channel,member):
                listeCo[member.id]=Voice(member,after.channel,member.guild)

async def reconnect(client,dictGuilds):
    for i in client.guilds:
        for j in i.voice_channels:
            for h in j.voice_states:
                member=i.get_member(h)
                if not member.bot and verifExecSQL(dictGuilds[member.guild.id],j,member):
                    if member.id in listeCo and listeCo[member.id].guildid!=i.id and listeCo[member.id].connect:
                        listeCo[member.id].exestat(dictGuilds[listeCo[member.id].guildid])
                    elif member.id in listeCo and listeCo[member.id].connect:
                        continue
                    listeCo[member.id]=Voice(member,j,i)
    await client.get_channel(705390619538882641).send("Voice : Utilisateurs Connectés.")

async def disconnect(client):
    listeDeco=list(listeCo)
    for i in listeDeco:
        try:
            if listeCo[i].connect==True:
                listeCo[i].exeStat(OTGuild(listeCo[i].guildid,True))
        except:
            pass
    await client.get_channel(705390619538882641).send("Voice : Utilisateurs Déconnectés.")

async def endNight(client,dictGuilds):
    await disconnect(client)
    await reconnect(client,dictGuilds)
