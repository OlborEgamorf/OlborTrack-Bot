
from Core.Fonctions.Embeds import createEmbed, embedAssert, exeErrorExcept
from Sondages.Temps import gestionTemps, footerTime
from Sondages.Classes import Giveaway, PollTime, Reminder, ReminderGuild 
from Core.Fonctions.TempsVoice import tempsVoice
from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.Phrase import createPhrase
from time import time
import sqlite3
import os

emotes=["<:ot1:705766186909958185>","<:ot2:705766186989912154>","<:ot3:705766186930929685>","<:ot4:705766186947706934>","<:ot5:705766186713088042>","<:ot6:705766187182850148>","<:ot7:705766187115741246>","<:ot8:705766187132256308>","<:ot9:705766187145101363>","<:ot10:705766186909958206>"]
dictPolls={}

async def exePoll(ctx,args,bot):
    try:
        assert len(args)!=0, "Oui, effectivement, c'est la commande, mais il faut une question et des propositions !"
        assert len(args)!=1, "Bonne question, mais il faut des propositions maintenant !"
        assert len(args)!=2, "Il faut donner plusieurs propositions !"
        assert len(args)<12, "Pas plus de 10 propositions !"
        descip=""
        for i in range(1,len(args)):
            descip=descip+emotes[i-1]+" "+args[i]+"\n"
        embedPoll=createEmbed(args[0],descip,0xfc03d7,ctx.invoked_with.lower(),ctx.guild)
        await ctx.message.delete()
        message=await ctx.send(embed=embedPoll)
        for i in range(len(args)-1):
            await message.add_reaction(emotes[i])
    except AssertionError as er:
        await ctx.send(embed=embedAssert(str(er)))
    except:
        await ctx.send(embed=await exeErrorExcept(ctx,bot,args))
    

async def exePolltime(ctx,args,bot):
    try:
        success,somme=True,0
        assert len(args)!=0, "Oui, effectivement, c'est la commande, mais il faut une question, le temps et des propositions !"
        assert len(args)!=1, "Bonne question, mais il faut des propositions et le temps maintenant !"
        assert len(args)!=2, "Il faut une question, maximum 10 propositions et du temps !"
        assert len(args)!=3, "Il doit manquer soit le temps soit des propositions..."
        assert len(args)<13, "Pas plus de 10 propositions !"
        descip=""
        for i in range(1,len(args)-1):
            descip=descip+emotes[i-1]+" "+args[i]+"\n"
        tempo=args[-1]
        somme=gestionTemps(tempo)
        foot=footerTime(somme)
        embedPoll=createEmbed(args[0],descip,0xfc03d7,"{0} | {1}".format(ctx.invoked_with.lower(),foot),ctx.guild)
        await ctx.message.delete()
        message=await ctx.send(embed=embedPoll)
        for i in range(len(args)-2):
            await message.add_reaction(emotes[i])
        dictPolls[message.id]=PollTime(message.id,ctx.guild.id,somme,args[1:-1],args[0],message.channel.id)
        await dictPolls[message.id].trigger(bot)
        del dictPolls[message.id]
    except AssertionError as er:
        await ctx.send(embed=embedAssert(str(er)))
    except:
        await ctx.send(embed=await exeErrorExcept(ctx,bot,args))


async def exeGiveaway(ctx,args,bot):
    try:
        success,gagnants,somme=True,0,0
        assert len(args)!=0, "Oui, effectivement, c'est la commande, mais il faut le temps et la récompense du tirage !"
        assert len(args)!=1, "Il manque soit le temps soit la récompense !"
        descip=""
        nb=1
        gagnants=1
        if args[len(args)-1][len(args[len(args)-1])-1].lower()=="g":
            try:
                gagnants=int(args[len(args)-1][0:len(args[len(args)-1])-1])
                assert gagnants>0, "Vous ne pouvez pas mettre un nombre de gagnants négatif ou nul !"
                assert gagnants<=20, "Vous ne pouvez pas désigner plus de 20 gagnants à la fois."
                nb=2
            except:
                pass
        for i in range(0,len(args)-nb):
            descip=descip+args[i]+" "
        tempo=args[len(args)-nb]
        somme=gestionTemps(tempo)
        foot=footerTime(somme)
        embedPoll=createEmbed("Giveaway : {0}".format(descip),"Cliquez sur la réaction <a:MusicMakeYouLoseControl:711222160982540380> pour tenter d'être tiré au sort !\nNombre de gagnants : {0}".format(gagnants),0xfc03d7,"{0} | {1}".format(ctx.invoked_with.lower(),foot),ctx.guild)
        await ctx.message.delete()
        message=await ctx.send(embed=embedPoll)
        dictPolls[message.id]=Giveaway(message.id,ctx.guild.id,somme,createPhrase([descip])[0:-1],gagnants,message.channel.id)
        await message.add_reaction("<a:MusicMakeYouLoseControl:711222160982540380>")
        await dictPolls[message.id].trigger(bot)
        del dictPolls[message.id]
    except AssertionError as er:
        await ctx.send(embed=embedAssert(str(er)))
    except:
        await ctx.send(embed=await exeErrorExcept(ctx,bot,args))


async def exeReminder(ctx,bot,args,option):
    try:
        assert len(args)!=0, "Votre demande est vide. Donnez moi ce dont vous voulez que je vous rappelle et dans combien de temps ! \nLe temps doit être un nombre suivi de s (pour secondes), m (pour minutes), h (pour heures) ou d (pour jours)."
        assert len(args)>1, "Donnez moi du temps !\nLe temps doit être un nombre suivi de s (pour secondes), m (pour minutes), h (pour heures) ou j (pour jours)."
        phrase=""
        for i in range(0,len(args)-1):
            phrase+=" "+args[i]
        temps=gestionTemps(args[len(args)-1])
        tempsstr=tempsVoice(temps)
        if option=="mp":
            embed=createEmbed("Rappel","Très bien ! Je t'enverrai un message privé dans {0} pour te rappeler de {1} !".format(tempsstr,phrase),0xfc03d7,"reminder",ctx.author)
            message=await ctx.send(embed=embed)
            dictPolls[message.id]=Reminder(message.id,ctx.author.id,temps,phrase)
        else:
            embed=createEmbed("Rappel","Très bien ! J'enverrai un message dans ce salon dans {0} pour te rappeler de {1} !".format(tempsstr,phrase),0xfc03d7,"reminder",ctx.author)
            message=await ctx.send(embed=embed)
            dictPolls[message.id]=ReminderGuild(message.id,ctx.author.id,temps,phrase,ctx.message.channel.id)
        await dictPolls[message.id].trigger(bot)
        del dictPolls[message.id]
    except AssertionError as er:
        await ctx.send(embed=embedAssert(str(er)))
    except:
        await ctx.send(embed=await exeErrorExcept(ctx,bot,args))


def sauvegardePoll(bot):
    connexion,curseur=connectSQL("OT","Polls","Guild",None,None)
    curseur.execute("CREATE TABLE IF NOT EXISTS Polls (ID INT, Guild INT, Temps INT, Question TEXT, Start INT, Salon INT)")
    curseur.execute("CREATE TABLE IF NOT EXISTS Reminders (ID INT, User INT, Temps INT, Remind TEXT, Start INT)")
    curseur.execute("CREATE TABLE IF NOT EXISTS RemindersGuild (ID INT, User INT, Temps INT, Remind TEXT, Start INT, Chan INT)")
    curseur.execute("CREATE TABLE IF NOT EXISTS Giveaways (ID INT, Guild INT, Temps INT, Lot TEXT, Gagnants INT, Start INT, Salon INT)")
    for i in dictPolls:
        if dictPolls[i].active:
            if type(dictPolls[i])==PollTime:
                curseur.execute("INSERT INTO Polls VALUES({0},{1},{2},'{3}',{4},{5})".format(dictPolls[i].id,dictPolls[i].guild,dictPolls[i].temps,createPhrase([dictPolls[i].question]),dictPolls[i].start,dictPolls[i].chan))
                curseur.execute("CREATE TABLE p{0} (Prop TEXT)".format(dictPolls[i].id))
                for j in dictPolls[i].propositions:
                    curseur.execute("INSERT INTO p{0} VALUES ('{1}')".format(dictPolls[i].id,createPhrase([j])))
            elif type(dictPolls[i])==Reminder:
                curseur.execute("INSERT INTO Reminders VALUES({0},{1},{2},'{3}',{4})".format(dictPolls[i].id,dictPolls[i].user,dictPolls[i].temps,createPhrase([dictPolls[i].remind]),dictPolls[i].start))
            elif type(dictPolls[i])==ReminderGuild:
                curseur.execute("INSERT INTO RemindersGuild VALUES({0},{1},{2},'{3}',{4},{5})".format(dictPolls[i].id,dictPolls[i].user,dictPolls[i].temps,createPhrase([dictPolls[i].remind]),dictPolls[i].start,dictPolls[i].chan))
            elif type(dictPolls[i])==Giveaway:
                curseur.execute("INSERT INTO Giveaways VALUES({0},{1},{2},'{3}',{4},{5},{6})".format(dictPolls[i].id,dictPolls[i].guild,dictPolls[i].temps,createPhrase([dictPolls[i].lot]),dictPolls[i].gagnants,dictPolls[i].start,dictPolls[i].chan))
    
    connexion.commit()

async def recupPoll(bot):
    connexion,curseur=connectSQL("OT","Polls","Guild",None,None)
    try:
        for i in curseur.execute("SELECT * FROM Polls").fetchall():
            liste=[]
            for j in curseur.execute("SELECT * FROM p{0}".format(i["ID"])).fetchall():
                liste.append(j["Prop"])
            dictPolls[i["ID"]]=PollTime(i["ID"],i["Guild"],i["Temps"]-(time()-i["Start"]),liste,i["Question"],i["Salon"])
        for i in curseur.execute("SELECT * FROM Reminders").fetchall():
            dictPolls[i["ID"]]=Reminder(i["ID"],i["User"],i["Temps"]-(time()-i["Start"]),i["Remind"])
        for i in curseur.execute("SELECT * FROM RemindersGuild").fetchall():
            dictPolls[i["ID"]]=ReminderGuild(i["ID"],i["User"],i["Temps"]-(time()-i["Start"]),i["Remind"],i["Chan"])
        for i in curseur.execute("SELECT * FROM Giveaways").fetchall():
            dictPolls[i["ID"]]=Giveaway(i["ID"],i["Guild"],i["Temps"]-(time()-i["Start"]),i["Lot"],i["Gagnants"],i["Salon"])
        
        connexion.close()
        os.remove("SQL/OT/Guild/Polls.db")

        for i in dictPolls:
            bot.loop.create_task(dictPolls[i].trigger(bot))
    except sqlite3.OperationalError:
        pass