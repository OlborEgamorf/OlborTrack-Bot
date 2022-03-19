
import asyncio
import os
from time import time

import discord
from Core.Decorator import OTCommand
from Core.Fonctions.Embeds import createEmbed
from Core.Fonctions.Phrase import createPhrase
from Core.Fonctions.TempsVoice import tempsVoice
from Stats.SQL.ConnectSQL import connectSQL

from Sondages.Classes import (Giveaway, Petition, PollTime, Reminder,
                              ReminderGuild)
from Sondages.Temps import footerTime, gestionTemps

emotes=["<:ot1:705766186909958185>","<:ot2:705766186989912154>","<:ot3:705766186930929685>","<:ot4:705766186947706934>","<:ot5:705766186713088042>","<:ot6:705766187182850148>","<:ot7:705766187115741246>","<:ot8:705766187132256308>","<:ot9:705766187145101363>","<:ot10:705766186909958206>"]
dictPolls={}

@OTCommand
async def exePoll(ctx,bot,args):
    assert len(args)!=0, "Oui, effectivement, c'est la commande, mais il faut une question et des propositions !"
    assert len(args)!=1, "Bonne question, mais il faut des propositions maintenant !"
    assert len(args)!=2, "Il faut donner plusieurs propositions !"
    assert len(args)<12, "Pas plus de 10 propositions !"

    if not ctx.author.guild_permissions.manage_messages:
        embed=createEmbed("Demande de création de sondage","<@{0}> souhaite créer un sondage !\nUn modérateur doit approuver la création en appuyant sur <:otVALIDER:772766033996021761>.".format(ctx.author.id),0xfc03d7,ctx.invoked_with.lower(),ctx.guild)
        embed.add_field(name="Question",value=args[0],inline=False)
        embed.add_field(name="Propositions",value=", ".join(args[1:]),inline=False)
        mess=await ctx.reply(embed=embed)
        await mess.add_reaction("<:otVALIDER:772766033996021761>")
        def check(reaction,user):
            if type(reaction.emoji)==str:
                return False
            return user.guild_permissions.manage_messages and reaction.message.id==mess.id and reaction.emoji.id==772766033996021761 and not user.bot
        try:
            reaction,user=await bot.wait_for('reaction_add', check=check, timeout=40)
        except asyncio.exceptions.TimeoutError:
            await mess.delete()
            await ctx.reply("<:otROUGE:868535622237818910> Votre sondage a été refusé.")
            return
        await mess.delete()
        
    descip=""
    for i in range(1,len(args)):
        descip=descip+emotes[i-1]+" "+args[i]+"\n"
    embedPoll=createEmbed(args[0],"<@{0}> a lancé un sondage !".format(ctx.author.id),0xfc03d7,ctx.invoked_with.lower(),ctx.guild)
    embedPoll.add_field(name="Propositions",value=descip,inline=False)
    if ctx.message.attachments!=[]:
        embedPoll.set_image(url=ctx.message.attachments[0].url)
    await ctx.message.delete()
    message=await ctx.send(embed=embedPoll)
    for i in range(len(args)-1):
        await message.add_reaction(emotes[i])
    
@OTCommand
async def exePolltime(ctx,bot,args,option):
    somme=0
    assert len(args)!=0, "Oui, effectivement, c'est la commande, mais il faut une question, le temps et des propositions !"
    assert len(args)!=1, "Bonne question, mais il faut des propositions et le temps maintenant !"
    assert len(args)!=2, "Il faut une question, maximum 10 propositions et du temps !"
    assert len(args)!=3, "Il doit manquer soit le temps soit des propositions..."
    assert len(args)<13, "Pas plus de 10 propositions !"
    descip=" ".join(args[1:-1])
    tempo=args[-1]
    somme=gestionTemps(tempo)
    format=footerTime(somme)
    embedPoll=createEmbed(args[0],"<@{0}> a lancé un sondage !".format(ctx.author.id),0xfc03d7,option,ctx.guild)
    embedPoll.add_field(name="Propositions",value=descip,inline=False)
    embedPoll.add_field(name="Fin des votes",value=format,inline=False)
    if ctx.message.attachments!=[]:
        embedPoll.set_image(url=ctx.message.attachments[0].url)
    if option!="polltime":
        embedPoll.add_field(name="Vote",value="Seulement votre première réponse sera prise en compte.",inline=True)
    if option=="election":
        embedPoll.add_field(name="Élection",value="Votre choix sera masqué et anonyme.",inline=True)
    await ctx.message.delete()
    message=await ctx.send(embed=embedPoll)
    for i in range(len(args)-2):
        await message.add_reaction(emotes[i])
    dictPolls[message.id]=PollTime(message,ctx.guild,somme,args[1:-1],args[0],option)
    await dictPolls[message.id].trigger(bot)
    del dictPolls[message.id]
    return result

@OTCommand
async def exePetition(ctx,bot,args):
    somme=0
    assert len(args)!=0, "Oui, effectivement, c'est la commande, mais il faut la proposition, les signatures nécessaires et le temps !"
    assert len(args)!=1, "Bonne pétition, mais il faut les signatures nécessaires et le temps !"
    assert len(args)!=2, "Il faut une question, le nombre de signatures nécessaires et du temps !"
    try:
        votes=int(args[-2])
        assert votes>0, "Le nombre de signatures ne peut pas être négatif !"
    except:
        raise AssertionError("Le nombre de signatures nécessaire doit être un entier !")
    descip=" ".join(args[:-2])
    tempo=args[-1]
    somme=gestionTemps(tempo)
    format=footerTime(somme)
    embedPoll=createEmbed(descip[:-1],"<@{0}> a lancé une pétition !".format(ctx.author.id),0xfc03d7,ctx.invoked_with.lower(),ctx.guild)
    embedPoll.add_field(name="Objectif",value="**{0}** signatures".format(votes),inline=True)
    embedPoll.add_field(name="Fin des signatures",value=format,inline=True)
    embedPoll.add_field(name="Comment participer ?",value="Appuyez sur <:PogCool:662410363219738636> pour signer !",inline=False)
    if ctx.message.attachments!=[]:
        embedPoll.set_image(url=ctx.message.attachments[0].url)
    await ctx.message.delete()
    message=await ctx.send(embed=embedPoll)
    await message.add_reaction("<:PogCool:662410363219738636>")
    #582607250850447372
    dictPolls[message.id]=Petition(message,somme,descip[:-1],votes)
    await dictPolls[message.id].trigger(bot)
    del dictPolls[message.id]

@OTCommand
async def exeGiveaway(ctx,bot,args):
    gagnants,somme=0,0
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
    descip=" ".join(args[:-nb])
    tempo=args[len(args)-nb]
    somme=gestionTemps(tempo)
    format=footerTime(somme)

    embedPoll=createEmbed("Giveaway","<@{0}> vous fait gagner **{1}** !".format(ctx.author.id,descip),0xfc03d7,ctx.invoked_with.lower(),ctx.guild)
    embedPoll.add_field(name="Nombre de gagnants",value=str(gagnants),inline=True)
    embedPoll.add_field(name="Date du tirage au sort",value=format,inline=True)
    embedPoll.add_field(name="Comment participer ?",value="Cliquez sur la réaction <a:MusicMakeYouLoseControl:711222160982540380> pour tenter d'être tiré au sort !",inline=False)

    if ctx.message.attachments!=[]:
        embedPoll.set_image(url=ctx.message.attachments[0].url)
    await ctx.message.delete()
    message=await ctx.send(embed=embedPoll)
    dictPolls[message.id]=Giveaway(message.id,ctx.guild.id,somme,descip,gagnants,message.channel.id)
    await message.add_reaction("<a:MusicMakeYouLoseControl:711222160982540380>")
    await dictPolls[message.id].trigger(bot)
    del dictPolls[message.id]

@OTCommand
async def exeReminder(ctx,bot,args,option):
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


def sauvegardePoll(bot):
    connexion,curseur=connectSQL("OT","Polls","Guild",None,None)
    curseur.execute("CREATE TABLE IF NOT EXISTS Polls (ID INT, Guild INT, Temps INT, Question TEXT, Start INT, Salon INT, Option TEXT)")
    curseur.execute("CREATE TABLE IF NOT EXISTS Petitions (ID INT, Guild INT, Temps INT, Question TEXT, Start INT, Salon INT, Signatures INT)")
    curseur.execute("CREATE TABLE IF NOT EXISTS Reminders (ID INT, User INT, Temps INT, Remind TEXT, Start INT)")
    curseur.execute("CREATE TABLE IF NOT EXISTS RemindersGuild (ID INT, User INT, Temps INT, Remind TEXT, Start INT, Chan INT)")
    curseur.execute("CREATE TABLE IF NOT EXISTS Giveaways (ID INT, Guild INT, Temps INT, Lot TEXT, Gagnants INT, Start INT, Salon INT)")
    for i in dictPolls:
        if dictPolls[i].active:
            if type(dictPolls[i])==PollTime:
                curseur.execute("INSERT INTO Polls VALUES({0},{1},{2},'{3}',{4},{5},'{6}')".format(dictPolls[i].id,dictPolls[i].guild.id,dictPolls[i].temps,createPhrase(dictPolls[i].question),dictPolls[i].start,dictPolls[i].chan.id,dictPolls[i].option))
                curseur.execute("CREATE TABLE p{0} (Prop TEXT, Count INT)".format(dictPolls[i].id))
                for j in dictPolls[i].propositions:
                    curseur.execute("INSERT INTO p{0} VALUES ('{1}',{2})".format(dictPolls[i].id,createPhrase(dictPolls[i].propositions[j].prop),dictPolls[i].propositions[j].count))
                if dictPolls[i].option!="polltime":
                    curseur.execute("CREATE TABLE v{0} (ID INT, Prop INT)".format(dictPolls[i].id))
                    for j in dictPolls[i].votants:
                        curseur.execute("INSERT INTO v{0} VALUES ({1},{2})".format(dictPolls[i].id,j,dictPolls[i].votants[j]))
            elif type(dictPolls[i])==Reminder:
                curseur.execute("INSERT INTO Reminders VALUES({0},{1},{2},'{3}',{4})".format(dictPolls[i].id,dictPolls[i].user,dictPolls[i].temps,createPhrase(dictPolls[i].remind),dictPolls[i].start))
            elif type(dictPolls[i])==ReminderGuild:
                curseur.execute("INSERT INTO RemindersGuild VALUES({0},{1},{2},'{3}',{4},{5})".format(dictPolls[i].id,dictPolls[i].user,dictPolls[i].temps,createPhrase(dictPolls[i].remind),dictPolls[i].start,dictPolls[i].chan))
            elif type(dictPolls[i])==Giveaway:
                curseur.execute("INSERT INTO Giveaways VALUES({0},{1},{2},'{3}',{4},{5},{6})".format(dictPolls[i].id,dictPolls[i].guild,dictPolls[i].temps,createPhrase(dictPolls[i].lot),dictPolls[i].gagnants,dictPolls[i].start,dictPolls[i].chan))
            elif type(dictPolls[i])==Petition:
                curseur.execute("INSERT INTO Petitions VALUES({0},{1},{2},'{3}',{4},{5},{6})".format(dictPolls[i].id,dictPolls[i].guild.id,dictPolls[i].temps,createPhrase(dictPolls[i].question),dictPolls[i].start,dictPolls[i].chan.id,dictPolls[i].votes))
                curseur.execute("CREATE TABLE v{0} (ID INT)".format(dictPolls[i].id))
                for j in dictPolls[i].votants:
                    curseur.execute("INSERT INTO v{0} VALUES ({1})".format(dictPolls[i].id,j))
    connexion.commit()

async def recupPoll(bot):
    connexion,curseur=connectSQL("OT","Polls","Guild",None,None)
    curseur.execute("CREATE TABLE IF NOT EXISTS Polls (ID INT, Guild INT, Temps INT, Question TEXT, Start INT, Salon INT, Option TEXT)")
    curseur.execute("CREATE TABLE IF NOT EXISTS Petitions (ID INT, Guild INT, Temps INT, Question TEXT, Start INT, Salon INT, Signatures INT)")
    curseur.execute("CREATE TABLE IF NOT EXISTS Reminders (ID INT, User INT, Temps INT, Remind TEXT, Start INT)")
    curseur.execute("CREATE TABLE IF NOT EXISTS RemindersGuild (ID INT, User INT, Temps INT, Remind TEXT, Start INT, Chan INT)")
    curseur.execute("CREATE TABLE IF NOT EXISTS Giveaways (ID INT, Guild INT, Temps INT, Lot TEXT, Gagnants INT, Start INT, Salon INT)")
    for i in curseur.execute("SELECT * FROM Polls").fetchall():
        liste=[]
        listeC=[]
        for j in curseur.execute("SELECT * FROM p{0}".format(i["ID"])).fetchall():
            liste.append(j["Prop"])
            listeC.append(j["Count"])
        if i["Option"]!="polltime":
            votants={}
            for j in curseur.execute("SELECT * FROM v{0}".format(i["ID"])).fetchall():
                votants[j["ID"]]=j["Prop"]
        else:
            votants=None
        try:
            mess=await bot.get_channel(i["Salon"]).fetch_message(i["ID"])
        except:
            continue
        dictPolls[i["ID"]]=PollTime(mess,bot.get_guild(i["Guild"]),i["Temps"]-(time()-i["Start"]),liste,i["Question"],i["Option"],counts=listeC,votants=votants)
    for i in curseur.execute("SELECT * FROM Reminders").fetchall():
        dictPolls[i["ID"]]=Reminder(i["ID"],i["User"],i["Temps"]-(time()-i["Start"]),i["Remind"])
    for i in curseur.execute("SELECT * FROM RemindersGuild").fetchall():
        dictPolls[i["ID"]]=ReminderGuild(i["ID"],i["User"],i["Temps"]-(time()-i["Start"]),i["Remind"],i["Chan"])
    for i in curseur.execute("SELECT * FROM Giveaways").fetchall():
        dictPolls[i["ID"]]=Giveaway(i["ID"],i["Guild"],i["Temps"]-(time()-i["Start"]),i["Lot"],i["Gagnants"],i["Salon"])
    for i in curseur.execute("SELECT * FROM Petitions").fetchall():
        try:
            mess=await bot.get_channel(i["Salon"]).fetch_message(i["ID"])
        except:
            continue
        votants=[]
        for j in curseur.execute("SELECT * FROM v{0}".format(i["ID"])).fetchall():
            votants.append(j["ID"])
        dictPolls[i["ID"]]=Petition(mess,i["Temps"]-(time()-i["Start"]),i["Question"],i["Signatures"],votants=votants)

    connexion.close()
    os.remove("SQL/OT/Guild/Polls.db")

    for i in dictPolls:
        bot.loop.create_task(dictPolls[i].trigger(bot))

async def vote(message,user,emoji):
    try:
        assert message in dictPolls

        poll=dictPolls[message]
        assert poll.option!="polltime"

        if user.id not in poll.votants:
            poll.propositions[emoji.id].count+=1
            poll.total+=1
            poll.votants[user.id]=emoji.id
            
            if poll.option=="election":
                await poll.message.remove_reaction(emoji,user)
            if poll.option in ("election","vote"):
                await user.send(embed=createEmbed("Confirmation vote\n{0}".format(poll.question),"Votre vote a bien été pris en compte !\nVous avez choisi : **{0}**\nPas de retour en arrière possible...".format(poll.propositions[emoji.id].prop),0xfc03d7,"vote",poll.guild))
        else:
            await poll.message.remove_reaction(emoji,user)
    except AssertionError:
        pass
    except discord.Forbidden:
        pass

async def petition(message,user):
    try:
        assert message in dictPolls

        poll=dictPolls[message]

        if user.id not in poll.votants:
            poll.total+=1
            poll.votants.append(user.id)
            await user.send(embed=createEmbed("Pétition\n{0}".format(poll.question),"Votre participation à la pétition a été validée.",0xfc03d7,"vote",poll.guild))
    except AssertionError:
        pass 
    except discord.Forbidden:
        pass
