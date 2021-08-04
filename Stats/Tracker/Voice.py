from time import strftime
from Stats.SQL.ConnectSQL import connectSQL
from Stats.SQL.Execution import exeClassic, exeObj
from Stats.SQL.Compteur import compteurSQL
from Stats.SQL.Historique import histoSQL
from Stats.SQL.Verification import verifExecSQL
from Stats.Tracker.Divers import exeDiversSQL
from Core.OTGuild import OTGuild
listeCo={}
dictMois={1:31,2:28,3:31,4:30,5:31,6:30,7:31,8:31,9:30,10:31,11:30,12:31}

class Voice:
    def __init__(self,member,chan,guild,client):
        self.user=member
        self.userid=member.id
        self.channelid=chan.id
        self.guildid=guild.id
        self.guild=guild
        self.trigsec=int(strftime("%S"))
        self.trigmin=int(strftime("%M"))
        self.trigheu=int(strftime("%H"))
        self.trigjou=int(strftime("%d"))
        self.trigmoi=int(strftime("%m"))
        self.trigann=int(strftime("%y"))
        self.client=client
        self.connect=True

    def calcul(self):
        endann,endmoi,endjou,endheu,endmin,endsec=int(strftime("%y")),int(strftime("%m")),int(strftime("%d")),int(strftime("%H")),int(strftime("%M")),int(strftime("%S"))
        if endann-self.trigann!=0:
            count=(endann-self.trigann)*31536000
            count+=(endmoi-self.trigmoi)*dictMois[self.trigmoi]*86400
            count+=(endjou-self.trigjou)*86400
            count+=(endheu-self.trigheu)*3600
            count+=(endmin-self.trigmin)*60
            count+=endsec-self.trigsec 
        elif endmoi-self.trigmoi!=0:
            count=(endmoi-self.trigmoi)*dictMois[self.trigmoi]*86400
            count+=(endjou-self.trigjou)*86400
            count+=(endheu-self.trigheu)*3600
            count+=(endmin-self.trigmin)*60
            count+=endsec-self.trigsec
        elif endjou-self.trigjou!=0:
            count=(endjou-self.trigjou)*86400
            count+=(endheu-self.trigheu)*3600
            count+=(endmin-self.trigmin)*60
            count+=endsec-self.trigsec
        elif endheu-self.trigheu!=0:
            count=(endheu-self.trigheu)*3600
            count+=(endmin-self.trigmin)*60
            count+=endsec-self.trigsec
        elif endmin-self.trigmin!=0:
            count=(endmin-self.trigmin)*60
            count+=endsec-self.trigsec
        elif endsec-self.trigsec!=0:
            count=endsec-self.trigsec
        else:
            count=0
        return count

    async def exeStat(self,guild):
        self.connect=False
        count=self.calcul()
        if count!=0:
            exeVoiceSQL(self.userid,self.channelid,count,guild)


async def voiceConnect(member,before,after,client,guild):
    if member.bot==False and guild.mstats[5]["Statut"]==True:
        if before.channel==None:
            if verifExecSQL(guild,after.channel,member)==True:
                listeCo[member.id]=Voice(member,after.channel,member.guild,client)
        elif after.channel==None:
            if verifExecSQL(guild,before.channel,member)==True:
                await listeCo[member.id].exeStat(guild)
        elif after.channel.id!=before.channel.id:
            if verifExecSQL(guild,before.channel,member)==True:
                await listeCo[member.id].exeStat(guild)
            if verifExecSQL(guild,after.channel,member)==True:
                listeCo[member.id]=Voice(member,after.channel,member.guild,client)
    return

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
                if member.bot==False and verifExecSQL(dictGuilds[member.guild.id],member,j)==True:
                    listeCo[member.id]=Voice(member,j,i,client)
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