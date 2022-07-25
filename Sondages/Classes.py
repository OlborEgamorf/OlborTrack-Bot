import asyncio
import random
from time import time

import discord
from Core.Fonctions.Embeds import createEmbed
from Stats.SQL.ConnectSQL import connectSQL

emotes=["<:ot1:705766186909958185>","<:ot2:705766186989912154>","<:ot3:705766186930929685>","<:ot4:705766186947706934>","<:ot5:705766186713088042>","<:ot6:705766187182850148>","<:ot7:705766187115741246>","<:ot8:705766187132256308>","<:ot9:705766187145101363>","<:ot10:705766186909958206>"]
ids=[705766186909958185,705766186989912154,705766186930929685,705766186947706934,705766186713088042,705766187182850148,705766187115741246,705766187132256308,705766187145101363,705766186909958206]

class Proposition:
    def __init__(self,emoji,prop,count=None):
        self.emoji=emoji
        self.prop=prop
        if count==None:
            self.count=0
        else:
            self.count=count

class PollTime():
    def __init__(self,message,guild,temps,props,question,multiple,author,counts=None,votants={}):
        self.message=message
        self.id=message.id
        self.guild=guild
        self.temps=temps
        self.question=question
        self.start=time()
        self.active=True
        self.multiple=multiple
        self.end=self.start+self.temps
        self.author=author
        self.votants=votants

        if counts==None:
            self.propositions=[Proposition(emotes[i],props[i]) for i in range(len(props))]
            self.total=0
            connexion,curseur=connectSQL(guild.id,"Guild","Guild",None,None)
            curseur.execute("CREATE TABLE IF NOT EXISTS polls (ID INT, Question TEXT, Propositions TEXT, Results TEXT, Active BOOL, Multiple BOOL, Total INT, Start INT, End INT, Auteur INT, Channel INT)")
            curseur.execute("INSERT INTO polls VALUES ({0},'{1}','{2}','0',True,{3},1,{4},{5},{6},{7})".format(message.id,question,";".join(props),multiple,self.start,self.end,author,message.channel.id))
            connexion.commit()
        else:
            self.propositions=[Proposition(emotes[i],props[i],count=counts[i]) for i in range(len(props))]
            self.total=sum(counts)

    async def trigger(self, bot):
        embed=self.message.embeds[0]
        restant=self.temps
        while restant>0:
            await asyncio.sleep(300 if restant>300 else restant)
            restant-=300
            descip=""
            for i in range(len(self.propositions)):
                descip+="{0} {1} - **{2} votes**\n".format(emotes[i],self.propositions[i].prop,self.propositions[i].count) 
            embed.set_field_at(0,name="Propositions",value=descip)
            try:
                await self.message.edit(embed=embed)
            except discord.NotFound:
                self.active=False
                connexion,curseur=connectSQL(self.guild.id,"Guild","Guild",None,None)
                curseur.execute("DELETE FROM polls WHERE ID={0}".format(self.id))
                connexion.commit()
                return

        embed=self.affichage(self.total,self.guild)
        await self.message.reply(embed=embed)
        await self.message.edit(view=None)
        self.active=False

        connexion,curseur=connectSQL(self.guild.id,"Guild","Guild",None,None)
        if self.total==0:
            total=1
        else:
            total=self.total
        curseur.execute("UPDATE polls SET Active=False, Results='{0}', Total={1} WHERE ID={2}".format(";".join(list(map(lambda x:str(x.count), self.propositions))),total,self.id))
        connexion.commit()

        if self.total==0:
            return None
        else:
            all=list(map(lambda x:x.count, self.propositions))
            propMax=max(self.propositions, key=lambda x:x.count)
            if all.count(self.propositions[propMax].count)>1:
                return None
            else:
                return propMax

    def affichage(self,total,guild):
        descip=""
        if total==0:
            embed=createEmbed(self.question+"\nRésultats","Personne n'a répondu au sondage.",0x6ec8fa,"sondage chrono",guild)
        else:
            table=self.propositions.copy()
            table.sort(key=lambda x:x.count, reverse=True)
            for i in table:
                if i.count>=0:
                    descip+="{0} {1} : {2}% ({3})\n".format(i.emoji,i.prop,round(i.count/total*100,2),i.count)
            embed=createEmbed(self.question+"\nRésultats",descip,0x6ec8fa,"sondage chrono",guild)
        return embed

class PetiGive():
    def __init__(self,message:discord.Message,temps:int,proposition:str,personnes:int,author:int,option:str,participants=[],new=True,description=None):
        self.message=message
        self.guild=message.guild
        self.id=message.id
        self.temps=temps
        self.proposition=proposition
        self.start=time()
        self.end=self.start+self.temps
        self.active=True
        self.personnes=personnes
        self.total=len(participants)
        self.participants=participants
        self.author=author
        self.option=option

        if new:
            connexion,curseur=connectSQL(message.guild.id,"Guild","Guild",None,None)
            if option=="petition":
                curseur.execute("CREATE TABLE IF NOT EXISTS petitions (ID INT, Petition INT, Nb INT, Final INT, Active INT, Debut INT, Fin INT, Auteur INT, Channel INT, Description TEXT)")
                curseur.execute("INSERT INTO petitions VALUES ({0},'{1}',{2},0,True,{3},{4},{5},{6},'{7}')".format(message.id,proposition,personnes,self.start,self.end,author,message.channel.id,description))
            else:
                curseur.execute("CREATE TABLE IF NOT EXISTS giveaways (ID INT, Lot INT, Gagnants INT, Winner TEXT, Participants TEXT, Active INT, Debut INT, Fin INT, Auteur INT, Channel INT, Description TEXT)")
                curseur.execute("INSERT INTO giveaways VALUES ({0},'{1}',{2},'0','0',True,{3},{4},{5},{6},'{7}')".format(message.id,proposition,personnes,self.start,self.end,author,message.channel.id,description))

            connexion.commit()

    async def triggerPeti(self,bot):
        restant=self.temps
        embed=self.message.embeds[0]
        while restant>0:
            await asyncio.sleep(300 if restant>300 else restant)
            restant-=300
            embed.set_field_at(0,name="Objectif",value="**{0}/{1}** signatures".format(self.total,self.personnes))
            try:
                await self.message.edit(embed=embed)
            except discord.NotFound:
                self.active=False
                connexion,curseur=connectSQL(self.guild.id,"Guild","Guild",None,None)
                curseur.execute("DELETE FROM petitions WHERE ID={0}".format(self.id))
                connexion.commit()
                return

        embed=self.affichage(self.total>=self.personnes,self.guild)
        await self.message.reply(embed=embed)
        await self.message.edit(view=None)
        self.active=False

        connexion,curseur=connectSQL(self.guild.id,"Guild","Guild",None,None)
        curseur.execute("UPDATE petitions SET Active=False, Final={0} WHERE ID={1}".format(self.total,self.id))
        connexion.commit()

    def affichage(self,valid,guild):
        if valid:
            return createEmbed(self.proposition,"La pétition est terminée et a été validée !\nVous avez eu **{0} signatures** sur les **{1}** demandées, bravo !".format(self.total,self.personnes),0x6ec8fa,"petition",guild)
        else:
            return createEmbed(self.proposition,"La pétition n'a pas atteint ses objectifs...\nSur les **{0} signatures attendues**, seulement **{1}** ont été reçues.".format(self.personnes,self.total),0x6ec8fa,"petition",guild)

    async def triggerGA(self,bot):
        await asyncio.sleep(self.temps)

        if len(self.participants)<self.personnes:
            embed=createEmbed(self.proposition,"<:otROUGE:868535622237818910> Il y a eu moins de participants ({0}) que de gagnants ({1}), le tirage est donc invalidé.".format(len(self.participants),self.personnes),0xff0000,"giveaway",self.guild)
            await self.message.reply(embed=embed)
            winner=0
        else:
            tirage=self.participants.copy()
            winner,descip=[],""
            for i in range(self.personnes):
                won=random.choice(tirage)
                winner.append(str(won))
                tirage.remove(won)
                descip+="<@"+str(won)+"> "
            embed=self.message.embeds[0]
            if len(winner)==1:
                embed.set_field_at(0,name="Gagnant",value="Bravo à <@{0}> !".format(winner[0]))
                await self.message.reply("<:otVERT:868535645897912330> Bravo à <@{0}> qui a gagné **{1}** !".format(winner[0],self.proposition))
            else:
                embed.set_field_at(0,name="Gagnants",value="Bravo à {0}!".format(descip))
                await self.message.reply("<:otVERT:868535645897912330> Bravo à {0}qui ont gagné **{1}** !".format(descip,self.proposition))
            await self.message.edit(embed=embed)

        connexion,curseur=connectSQL(self.guild.id,"Guild","Guild",None,None)
        curseur.execute("UPDATE giveaways SET Active=False, Winner='{0}', Participants='{1}' WHERE ID={2}".format(";".join(winner),";".join(self.participants),self.id))
        connexion.commit()
        self.active=False

class Reminder():
    def __init__(self,id,user,temps,remind):
        self.id=id
        self.user=user
        self.temps=temps
        self.remind=remind
        self.start=time()
        self.active=True

    async def trigger(self,bot):
        if self.temps>0:
            await asyncio.sleep(self.temps)
        user=bot.get_user(self.user)
        embed=createEmbed("Rappel",self.remind,0x6ec8fa,"rappel mp",user)
        await user.send(embed=embed)
        self.active=False

class ReminderGuild(Reminder):
    def __init__(self,id,user,temps,remind,channel):
        super().__init__(id,user,temps,remind)
        self.chan=channel
    
    async def trigger(self,bot):
        if self.temps>0:
            await asyncio.sleep(self.temps)
        user=bot.get_user(self.user)
        chan=bot.get_channel(self.chan)
        embed=createEmbed("Rappel",self.remind,0x6ec8fa,"rappel serv",user)
        await chan.send(embed=embed,content=":alarm_clock: Rappel pour <@{0}> :".format(self.user))
        self.active=False
