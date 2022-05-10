from Outils.VoiceEphem.FormatagePattern import formatageVoiceEphem
from Stats.SQL.ConnectSQL import connectSQL
# ID Hub, ID Salon, ID Owner, Locked
async def connectionVoiceEphem(guildOT,before,after,member):
    try:
        if after.channel!=None:
            hub=after.channel.id
            assert hub in guildOT.voicehub
            connexion,curseur=connectSQL(member.guild.id,"VoiceEphem","Guild",None,None)
            nb=curseur.execute("SELECT Count() AS Count FROM salons WHERE IDHub={0}".format(hub)).fetchone()
            if guildOT.voicehub[hub].limite==0:
                limite=None
            else:
                limite=guildOT.voicehub[hub].limite
            voice=await member.guild.create_voice_channel(formatageVoiceEphem(guildOT.voicehub[hub].pattern,member,nb["Count"]+1),overwrites=after.channel.overwrites,category=after.channel.category,bitrate=after.channel.bitrate,user_limit=limite)
            await member.move_to(voice)
            curseur.execute("INSERT INTO salons VALUES ({0},{1},{2},False)".format(hub,voice.id,member.id))
            guildOT.voiceephem.append(voice.id)
            connexion.commit()
    except AssertionError:
        pass
    
    try:
        if before.channel!=None:
            assert before.channel.id in guildOT.voiceephem
            connexion,curseur=connectSQL(member.guild.id,"VoiceEphem","Guild",None,None)
            if len(before.channel.voice_states)==0:
                guildOT.voiceephem.remove(before.channel.id)
                curseur.execute("DELETE FROM salons WHERE IDChannel={0}".format(before.channel.id))
                connexion.commit()
                await before.channel.delete()
            elif curseur.execute("SELECT * FROM salons WHERE IDChannel={0}".format(before.channel.id)).fetchone()["IDOwner"]==member.id:
                curseur.execute("UPDATE salons SET IDOwner={0} WHERE IDChannel={1}".format(before.channel.voice_states[0],before.channel.id))
                connexion.commit()
    except AssertionError:
        pass

async def checkAll(guildOT,bot):
    if guildOT.voiceephem!=[]:
        connexion,curseur=connectSQL(guildOT.id,"VoiceEphem","Guild",None,None)
        for i in guildOT.voiceephem:
            try:
                chan=bot.get_channel(i)
                assert len(chan.voice_states)==0
                guildOT.voiceephem.remove(chan.id)
                curseur.execute("DELETE FROM salons WHERE IDChannel={0}".format(chan.id))
                await chan.delete()
            except AssertionError:
                pass
        connexion.commit()
