from Stats.SQL.ConnectSQL import connectSQL
from Outils.Tableaux.EmbedsTab import embedStarBoard

async def checkTabEdit(message,bot,guild):
    connexion,curseur=connectSQL(guild.id,"Guild","Guild",None,None)
    for i in curseur.execute("SELECT * FROM sbmessages WHERE IDMess={0}".format(message.id)).fetchall():
        try:
            idchan=guild.stardict[i["Nombre"]].salon
            embed=embedStarBoard(message.author,message.content,message.channel.id,message.attachments,guild.stardict[i["Nombre"]].id,message.jump_url)
            messageStar=await bot.get_channel(idchan).fetch_message(i["IDStar"])
            await messageStar.edit(content=messageStar.content,embed=embed)
        except:
            pass



async def checkTabReact(message,emoji,count,bot,guild):
    try:
        assert message.author.bot==False
        if emoji.id==None:
            try:
                id=ord(str(emoji))
            except:
                return
        else:
            id=emoji.id
        if 0 in guild.starlist:
            id=0
        assert id in guild.starlist
        assert not guild.chan[message.channel.id]["Tab"]
        connexion,curseur=connectSQL(guild.id,"Guild","Guild",None,None)
        for i in guild.starlist[id]:
            if count>=guild.stardict[i].count:
                etat=curseur.execute("SELECT IDStar FROM sbmessages WHERE Nombre={0} AND IDMess={1}".format(guild.stardict[i].nombre,message.id)).fetchone()
                if etat==None:
                    embed=embedStarBoard(message.author,message.content,message.channel.id,message.attachments,guild.stardict[i].id,message.jump_url)
                    newMessage=await bot.get_channel(guild.stardict[i].salon).send(content="{0} **{1}**".format(emoji,count), embed=embed)
                    curseur.execute("INSERT INTO sbmessages VALUES({0},{1},{2})".format(message.id,newMessage.id,guild.stardict[i].nombre))
                else:
                    embed=embedStarBoard(message.author,message.content,message.channel.id,message.attachments,guild.stardict[i].id,message.jump_url)
                    messageStar=await bot.get_channel(guild.stardict[i].salon).fetch_message(etat["IDStar"])
                    await messageStar.edit(content="{0} **{1}**".format(emoji,count), embed=embed)
            else:
                etat=curseur.execute("SELECT IDStar FROM sbmessages WHERE Nombre={0} AND IDMess={1}".format(guild.stardict[i].nombre,message.id)).fetchone()
                if etat!=None:
                    messageStar=await bot.get_channel(guild.stardict[i].salon).fetch_message(etat["IDStar"])
                    await messageStar.delete()
                    curseur.execute("DELETE FROM sbmessages WHERE Nombre={0} AND IDMess={1}".format(guild.stardict[i].nombre,message.id))
        connexion.commit()
    except AssertionError:
        pass
    return



async def checkTabDelete(listeid,bot,guild):
    connexion,curseur=connectSQL(guild.id,"Guild","Guild",None,None)
    for messageid in listeid:
        for i in curseur.execute("SELECT * FROM sbmessages WHERE IDMess={0}".format(messageid)).fetchall():
            idchan=guild.stardict[i["Nombre"]].salon
            messageDel=await bot.get_channel(idchan).fetch_message(i["IDStar"])
            await messageDel.delete()
            curseur.execute("DELETE FROM sbmessages WHERE IDStar={0}".format(i["IDStar"]))
    connexion.commit()