
import json
import os
from time import time

import discord
from Core.Decorator import OTCommand
from Core.Fonctions.Embeds import createEmbed
from Core.Fonctions.Phrase import createPhrase
from Core.Fonctions.TempsVoice import tempsVoice
from Stats.SQL.ConnectSQL import connectSQL

from Sondages.Classes import PetiGive, PollTime, Reminder, ReminderGuild
from Sondages.Temps import footerTime, gestionTemps

emotes=["<:ot1:705766186909958185>","<:ot2:705766186989912154>","<:ot3:705766186930929685>","<:ot4:705766186947706934>","<:ot5:705766186713088042>","<:ot6:705766187182850148>","<:ot7:705766187115741246>","<:ot8:705766187132256308>","<:ot9:705766187145101363>","<:ot10:705766186909958206>"]
dictPolls={}

@OTCommand
async def exePoll(interaction,question,propositions,image):
    descip=""
    for i in range(len(propositions)):
        descip=descip+emotes[i]+" "+propositions[i]+"\n"

    embedPoll=createEmbed(question,"<@{0}> a lancé un sondage !\nFaites votre choix parmi les propositions !".format(interaction.user.id),0x6ec8fa,interaction.command.qualified_name,interaction.guild)
    embedPoll.add_field(name="Propositions",value=descip,inline=False)
    if image!=None:
        embedPoll.set_image(url=image.url)
    await interaction.response.send_message(embed=embedPoll)
    message=await interaction.original_message()
    for i in range(len(propositions)):
        await message.add_reaction(emotes[i])
    
@OTCommand
async def exePolltime(interaction,bot,question,propositions,temps,multiple,image):
   
    descip=""
    for i in range(len(propositions)):
        descip=descip+emotes[i]+" "+propositions[i]+"\n"

    embedPoll=createEmbed(question,"<@{0}> a lancé un sondage !\nFaites votre choix parmi les propositions !".format(interaction.user.id),0x6ec8fa,interaction.command.qualified_name,interaction.guild)
    embedPoll.add_field(name="Propositions",value=descip,inline=False)

    somme=gestionTemps(temps)
    format=footerTime(somme)
    embedPoll.add_field(name="Fin des votes",value=format,inline=False)

    if image!=None:
        embedPoll.set_image(url=image.url)
    if multiple:
        embedPoll.add_field(name="Choix multiple",value="Vous pouvez choisir plusieurs propositions à la fois",inline=True)
    else:
        embedPoll.add_field(name="Choix unique",value="Une seule proposition vous est imposée",inline=True)

    await interaction.response.send_message(embed=embedPoll,view=ViewPoll(propositions,multiple))

    allProps=[]
    for i in propositions:
        allProps.append(createPhrase(i))
    dictPolls[interaction.id]=PollTime(await interaction.original_message(),interaction.guild,somme,allProps,createPhrase(question),multiple,interaction.user.id)
    await dictPolls[interaction.id].trigger(bot)
    del dictPolls[interaction.id]

@OTCommand
async def exePetition(interaction,bot,objet,signatures,temps,image):

    #assert signatures>=2, "Vous ne pouvez pas mettre moins de deux signatures."

    somme=gestionTemps(temps)
    format=footerTime(somme)

    embedPoll=createEmbed(objet,"<@{0}> a lancé une pétition !\nSignez pour participer à la cause !".format(interaction.user.id,interaction.guild.id),0x6ec8fa,"petition",interaction.guild)
    embedPoll.add_field(name="Objectif",value="**{0}** signatures".format(signatures),inline=True)
    embedPoll.add_field(name="Fin des signatures",value=format,inline=True)

    if image!=None:
        embedPoll.set_image(url=image.url)

    await interaction.response.send_message(embed=embedPoll,view=ViewPetition())

    dictPolls[interaction.id]=PetiGive(await interaction.original_message(),somme,createPhrase(objet),signatures,interaction.user.id,"petition")
    await dictPolls[interaction.id].triggerPeti(bot)
    del dictPolls[interaction.id]

@OTCommand
async def exeGiveaway(interaction,bot,lot,gagnants,temps,image):
    if gagnants==None:
        gagnants=1
    assert gagnants>=1 and gagnants<=20, "Le nombre de gagnants doit être compris entre 1 et 20 !"

    somme=gestionTemps(temps)
    format=footerTime(somme)

    embedPoll=createEmbed(lot,"<@{0}> a lancé un giveaway !\nTentez de gagner ce lot !".format(interaction.user.id,lot),0x6ec8fa,interaction.command.name,interaction.guild)
    embedPoll.add_field(name="Nombre de gagnants",value=str(gagnants),inline=True)
    embedPoll.add_field(name="Date du tirage au sort",value=format,inline=True)

    if image!=None:
        embedPoll.set_image(url=image.url)

    await interaction.response.send_message(embed=embedPoll,view=ViewGiveaway())

    dictPolls[interaction.id]=PetiGive(await interaction.original_message(),somme,createPhrase(lot),gagnants,interaction.user.id,"giveaway")
    await dictPolls[interaction.id].triggerGA(bot)
    del dictPolls[interaction.id]

@OTCommand
async def exeReminder(interaction,bot,rappel,temps,option):

    temps=gestionTemps(temps)
    format=tempsVoice(temps)

    if option=="mp":
        embed=createEmbed("Rappel","Très bien ! Je t'enverrai un message privé dans {0} pour te rappeler de **{1}** !".format(format,rappel),0x6ec8fa,interaction.command.qualified_name,interaction.user)
        await interaction.response.send_message(embed=embed)
        message=await interaction.original_message()
        dictPolls[interaction.id]=Reminder(message.id,interaction.user.id,temps,rappel)
    else:
        embed=createEmbed("Rappel","Très bien ! J'enverrai un message dans ce salon dans {0} pour te rappeler de **{1}** !".format(format,rappel),0x6ec8fa,interaction.command.qualified_name,interaction.user)
        await interaction.response.send_message(embed=embed)
        message=await interaction.original_message()
        dictPolls[interaction.id]=ReminderGuild(message.id,interaction.user.id,temps,rappel,interaction.channel.id)

    await dictPolls[interaction.id].trigger(bot)
    del dictPolls[interaction.id]



def sauvegardePoll(bot):
    connexion,curseur=connectSQL("OT")
    curseur.execute("CREATE TABLE IF NOT EXISTS Polls (ID INT, Guild INT, Temps INT, Question TEXT, Start INT, Salon INT, Multiple BOOL, Author INT)")
    curseur.execute("CREATE TABLE IF NOT EXISTS Petitions (ID INT, Guild INT, Temps INT, Question TEXT, Start INT, Salon INT, Signatures INT, Author INT, Option TEXT)")
    curseur.execute("CREATE TABLE IF NOT EXISTS Reminders (ID INT, User INT, Temps INT, Remind TEXT, Start INT)")
    curseur.execute("CREATE TABLE IF NOT EXISTS RemindersGuild (ID INT, User INT, Temps INT, Remind TEXT, Start INT, Chan INT)")
    for i in dictPolls:
        if dictPolls[i].active:
            if type(dictPolls[i])==PollTime:
                curseur.execute("INSERT INTO Polls VALUES({0},{1},{2},'{3}',{4},{5},{6})".format(dictPolls[i].id,dictPolls[i].guild.id,dictPolls[i].temps,createPhrase(dictPolls[i].question),dictPolls[i].start,dictPolls[i].chan.id,dictPolls[i].multiple,dictPolls[i].author))

                curseur.execute("CREATE TABLE p{0} (Prop TEXT, Count INT)".format(dictPolls[i].id))
                for j in dictPolls[i].propositions:
                    curseur.execute("INSERT INTO p{0} VALUES ('{1}',{2})".format(dictPolls[i].id,createPhrase(dictPolls[i].propositions[j].prop),dictPolls[i].propositions[j].count))
                
                curseur.execute("CREATE TABLE v{0} (ID INT, Prop TEXT)".format(dictPolls[i].id))
                for j in dictPolls[i].votants:
                    curseur.execute("INSERT INTO v{0} VALUES ({1},'{2}')".format(dictPolls[i].id,j,";".join(dictPolls[i].votants[j])))
                        
            elif type(dictPolls[i])==Reminder:
                curseur.execute("INSERT INTO Reminders VALUES({0},{1},{2},'{3}',{4})".format(dictPolls[i].id,dictPolls[i].user,dictPolls[i].temps,createPhrase(dictPolls[i].remind),dictPolls[i].start))

            elif type(dictPolls[i])==ReminderGuild:
                curseur.execute("INSERT INTO RemindersGuild VALUES({0},{1},{2},'{3}',{4},{5})".format(dictPolls[i].id,dictPolls[i].user,dictPolls[i].temps,createPhrase(dictPolls[i].remind),dictPolls[i].start,dictPolls[i].chan))

            elif type(dictPolls[i])==PetiGive:
                curseur.execute("INSERT INTO Petitions VALUES({0},{1},{2},'{3}',{4},{5},{6})".format(dictPolls[i].id,dictPolls[i].guild.id,dictPolls[i].temps,createPhrase(dictPolls[i].question),dictPolls[i].start,dictPolls[i].chan.id,dictPolls[i].votes,dictPolls[i].author,dictPolls[i].option))

                curseur.execute("CREATE TABLE v{0} (ID INT)".format(dictPolls[i].id))
                for j in dictPolls[i].votants:
                    curseur.execute("INSERT INTO v{0} VALUES ({1})".format(dictPolls[i].id,j))

    connexion.commit()

async def recupPoll(bot):
    connexion,curseur=connectSQL("OT")
    curseur.execute("CREATE TABLE IF NOT EXISTS Polls (ID INT, Guild INT, Temps INT, Question TEXT, Start INT, Salon INT, Multiple BOOL, Author INT)")
    curseur.execute("CREATE TABLE IF NOT EXISTS Petitions (ID INT, Guild INT, Temps INT, Question TEXT, Start INT, Salon INT, Signatures INT, Author INT)")
    curseur.execute("CREATE TABLE IF NOT EXISTS Reminders (ID INT, User INT, Temps INT, Remind TEXT, Start INT)")
    curseur.execute("CREATE TABLE IF NOT EXISTS RemindersGuild (ID INT, User INT, Temps INT, Remind TEXT, Start INT, Chan INT)")
    curseur.execute("CREATE TABLE IF NOT EXISTS Giveaways (ID INT, Guild INT, Temps INT, Lot TEXT, Gagnants INT, Start INT, Salon INT)")
    for i in curseur.execute("SELECT * FROM Polls").fetchall():
        liste=[]
        listeC=[]
        for j in curseur.execute("SELECT * FROM p{0}".format(i["ID"])).fetchall():
            liste.append(j["Prop"])
            listeC.append(j["Count"])
        
        votants={}
        for j in curseur.execute("SELECT * FROM v{0}".format(i["ID"])).fetchall():
            votants[j["ID"]]=j["Prop"].split(";")
        
        try:
            mess=await bot.get_channel(i["Salon"]).fetch_message(i["ID"])
        except:
            continue
        
        dictPolls[i["ID"]]=PollTime(mess,bot.get_guild(i["Guild"]),i["Temps"]-(time()-i["Start"]),liste,i["Question"],i["Option"],i["Author"],counts=listeC,votants=votants)
    for i in curseur.execute("SELECT * FROM Reminders").fetchall():
        dictPolls[i["ID"]]=Reminder(i["ID"],i["User"],i["Temps"]-(time()-i["Start"]),i["Remind"])
    for i in curseur.execute("SELECT * FROM RemindersGuild").fetchall():
        dictPolls[i["ID"]]=ReminderGuild(i["ID"],i["User"],i["Temps"]-(time()-i["Start"]),i["Remind"],i["Chan"])
    for i in curseur.execute("SELECT * FROM Petitions").fetchall():
        try:
            mess=await bot.get_channel(i["Salon"]).fetch_message(i["ID"])
        except:
            continue
        votants=[]
        for j in curseur.execute("SELECT * FROM v{0}".format(i["ID"])).fetchall():
            votants.append(j["ID"])
        dictPolls[i["ID"]]=PetiGive(mess,i["Temps"]-(time()-i["Start"]),i["Question"],i["Signatures"],i["Author"],i["Option"],votants=votants,new=False)

    connexion.close()
    os.remove("SQL/OT/Guild/Polls.db")

    for i in dictPolls:
        bot.loop.create_task(dictPolls[i].trigger(bot))

async def vote(interaction):
    try:
        pollid=interaction.message.interaction.id
        user=interaction.user
        assert pollid in dictPolls
        poll=dictPolls[pollid]

        if user.id in poll.votants:
            for i in poll.votants[user.id]:
                poll.propositions[int(i)].count-=1
                poll.total-=1

        descip=""
        for i in interaction.data["values"]:
            poll.propositions[int(i)].count+=1
            poll.total+=1
            descip+="{0}, ".format(poll.propositions[int(i)].prop)
        
        poll.votants[user.id]=interaction.data["values"]
            
        await interaction.response.send_message(embed=createEmbed("Confirmation choix\n{0}".format(poll.question),"Votre vote a bien été pris en compte !\nVous avez choisi : **{0}**".format(descip[:-2]),0x6ec8fa,"sondage",poll.guild),ephemeral=True)
        
    except AssertionError:
        pass
    except discord.Forbidden:
        pass

class ViewPoll(discord.ui.View):
    def __init__(self,options,multiple):
        super().__init__(timeout=None)

        emotes=["<:ot1:705766186909958185>","<:ot2:705766186989912154>","<:ot3:705766186930929685>","<:ot4:705766186947706934>","<:ot5:705766186713088042>","<:ot6:705766187182850148>","<:ot7:705766187115741246>","<:ot8:705766187132256308>","<:ot9:705766187145101363>","<:ot10:705766186909958206>"]
        liste=[]

        for i in range(len(options)):
            liste.append(discord.SelectOption(label=options[i],emoji=emotes[i],value=i))
        
        if multiple:
            select=discord.ui.Select(options=liste,placeholder="Répondez au sondage",custom_id="ot:pollanswer",max_values=len(liste))
        else:
            select=discord.ui.Select(options=liste,placeholder="Répondez au sondage",custom_id="ot:pollanswer")

        select.callback=vote
        self.add_item(select)

class ViewPetition(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Signer",emoji="<:otOUI:726840394150707282>",style=discord.ButtonStyle.blurple, custom_id="ot:petition")
    async def petition(self,interaction:discord.Interaction, button:discord.ui.Button):
        try:
            pollid=interaction.message.interaction.id
            user=interaction.user
            assert pollid in dictPolls
            poll=dictPolls[pollid]

            if user.id not in poll.participants:
                poll.total+=1
                poll.participants.append(user.id)
                if poll.total>=poll.personnes:
                    embed=createEmbed("Pétition réussie !","L'objectif de {0} signatures vient d'être atteint ! Vous pouvez continuer à signer pour le dépasser !".format(poll.personnes),0x6ec8fa,"petition",poll.guild)
                    await interaction.response.send_message(embed=embed)
                    await interaction.followup.send(embed=createEmbed("Pétition signée\n{0}".format(poll.proposition),"Votre participation à la pétition a été validée.",0x6ec8fa,"petition",user),ephemeral=True)
                else:
                    await interaction.response.send_message(embed=createEmbed("Pétition signée\n{0}".format(poll.proposition),"Votre participation à la pétition a été validée.",0x6ec8fa,"petition",user),ephemeral=True)

        except AssertionError:
            pass 
        except discord.Forbidden:
            pass

class ViewGiveaway(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Entrer dans le tirage !",emoji="<:otOUI:726840394150707282>",style=discord.ButtonStyle.blurple, custom_id="ot:giveaway")
    async def giveaway(self,interaction:discord.Interaction, button:discord.ui.Button):
        try:
            pollid=interaction.message.interaction.id
            user=interaction.user
            assert pollid in dictPolls
            poll=dictPolls[pollid]

            if str(user.id) not in poll.participants:
                poll.total+=1
                poll.participants.append(str(user.id))

                await interaction.response.send_message(embed=createEmbed(poll.proposition,"Vous êtes dans le tirage au sort ! Vous serez alerté par une mention si vous remportez le lot.",0x6ec8fa,"giveaway",user),ephemeral=True)

        except AssertionError:
            pass 
        except discord.Forbidden:
            pass
#582607250850447372
