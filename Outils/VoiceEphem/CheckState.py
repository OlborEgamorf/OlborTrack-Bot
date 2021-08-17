from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.Embeds import embedAssert

async def connectionVoiceEphem(guildOT,before,after,member):
    try:
        if after.channel!=None:
            assert after.channel.id in guildOT.voicehub
            connexion,curseur=connectSQL(member.guild.id,"VoiceEphem","Guild",None,None)
            chan=curseur.execute("SELECT * FROM salons WHERE ID=0 ORDER BY Nombre ASC").fetchone()
            if chan==None:
                await member.send(embed=embedAssert("Désolé, il n'y a plus de salon éphémère disponible sur le serveur {0}. Veuillez réessayer plus tard.".format(member.guild.name)))
            else:
                if guildOT.voicehub[after.channel.id]==0:
                    limite=None
                else:
                    limite=guildOT.voicehub[after.channel.id]
                voice=await member.guild.create_voice_channel(chan["Nom"],overwrites=after.channel.overwrites,category=after.channel.category,bitrate=after.channel.bitrate,user_limit=limite)
                await member.move_to(voice)
                curseur.execute("UPDATE salons SET ID={0} WHERE Nombre={1}".format(voice.id,chan["Nombre"]))
                guildOT.voiceephem.append(voice.id)
                connexion.commit()
    except AssertionError:
        pass
    
    try:
        if before.channel!=None:
            assert before.channel.id in guildOT.voiceephem
            assert len(before.channel.voice_states)==0
            connexion,curseur=connectSQL(member.guild.id,"VoiceEphem","Guild",None,None)
            guildOT.voiceephem.remove(before.channel.id)
            curseur.execute("UPDATE salons SET ID=0 WHERE ID={0}".format(before.channel.id))
            connexion.commit()
            await before.channel.delete()
    except AssertionError:
        pass

async def checkAll(guildOT,bot):
    if guildOT.voiceephem!=[]:
        connexion,curseur=connectSQL(guildOT.id,"VoiceEphem","Guild",None,None)
        for i in guildOT.voiceephem:
            chan=bot.get_channel(i)
            assert len(chan.voice_states)==0
            guildOT.voiceephem.remove(chan.id)
            curseur.execute("UPDATE salons SET ID=0 WHERE ID={0}".format(chan.id))
            await chan.delete()
        connexion.commit()


