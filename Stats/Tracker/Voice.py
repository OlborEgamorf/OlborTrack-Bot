import time
from time import strftime

import discord

from Core.OTGuild import OTGuild
from Stats.SQL.ConnectSQL import connectSQL
from Stats.SQL.Execution import exeClassic, exeObj
from Stats.SQL.Historique import histoSQL
from Stats.SQL.Verification import verifExecSQL
from Stats.Tracker.Divers import exeDiversSQL

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
        self.time=time.time()
        self.connect=True

    async def exeStat(self,guild:OTGuild):
        """Méthode qui calcule le temps passé en vocal, déclare l'utilisateur comme déconnecté et enregistre les stats.
        
        Entrée :
            guild : l'objet OTGuild du serveur concerné"""
        self.connect=False
        count=int(time.time()-self.time)
        if count!=0:
            exeVoiceSQL(self.userid,self.channelid,count,guild)


async def voiceConnect(member,before,after,guild):
    if member.bot==False and guild.mstats[5]["Statut"]==True:
        if before.channel==None:
            if verifExecSQL(guild,after.channel,member)==True:
                listeCo[member.id]=Voice(member,after.channel,member.guild)
        elif after.channel==None:
            await listeCo[member.id].exeStat(guild)
        elif after.channel.id!=before.channel.id:
            await listeCo[member.id].exeStat(guild)
            if verifExecSQL(guild,after.channel,member)==True:
                listeCo[member.id]=Voice(member,after.channel,member.guild)

def exeVoiceSQL(id,chan,count,guild):
    connexionGuild,curseurGuild=connectSQL(guild.id,"Guild","Guild",None,None)
    exeClassic(count,id,"Voice",curseurGuild,guild)

    connexion,curseur=connectSQL(guild.id,"Voice","Stats","GL","")
    histoSQL(curseur,count,id,strftime("%y")+strftime("%m")+strftime("%d"),chan)
    connexion.commit()

    if bool(guild.mstats[0]["Statut"])==True:
        exeClassic(count,chan,"Voicechan",curseurGuild,guild)
        exeObj(count,chan,id,True,guild,"Voicechan")
    
    exeDiversSQL(id,{"Vocal":count},"+",guild,connexionGuild,curseurGuild)

    connexionGuild.commit()

async def reconnect(client,dictGuilds):
    for i in client.guilds:
        for j in i.voice_channels:
            for h in j.voice_states:
                member=i.get_member(h)
                if member.bot==False and verifExecSQL(dictGuilds[member.guild.id],j,member)==True:
                    if member.id in listeCo and listeCo[member.id].guildid!=i.id and listeCo[member.id].connect:
                        listeCo[member.id].exestat(dictGuilds[listeCo[member.id].guildid])
                    elif member.id in listeCo and listeCo[member.id].connect:
                        continue
                    listeCo[member.id]=Voice(member,j,i)
    await client.get_channel(705390619538882641).send("Voice : Utilisateurs Connectés.")
    return

async def disconnect(client):
    listeDeco=list(listeCo)
    for i in listeDeco:
        try:
            if listeCo[i].connect==True:
                await listeCo[i].exeStat(OTGuild(listeCo[i].guildid,True))
        except:
            pass
    await client.get_channel(705390619538882641).send("Voice : Utilisateurs Déconnectés.")
    return

async def endNight(client,dictGuilds):
    await disconnect(client)
    await reconnect(client,dictGuilds)
