import asyncio
import random
from time import time

from Core.Fonctions.Embeds import createEmbed
from Stats.SQL.ConnectSQL import connectSQL

emotes=["<:ot1:705766186909958185>","<:ot2:705766186989912154>","<:ot3:705766186930929685>","<:ot4:705766186947706934>","<:ot5:705766186713088042>","<:ot6:705766187182850148>","<:ot7:705766187115741246>","<:ot8:705766187132256308>","<:ot9:705766187145101363>","<:ot10:705766186909958206>"]
ids=[705766186909958185,705766186989912154,705766186930929685,705766186947706934,705766186713088042,705766187182850148,705766187115741246,705766187132256308,705766187145101363,705766186909958206]

class Proposition:
    def __init__(self,emoji,id,prop,count=None):
        self.emoji=emoji
        self.id=id
        self.prop=prop
        if count==None:
            self.count=0
        else:
            self.count=count

class PollTime():
    def __init__(self,message,guild,temps,props,question,option,counts=None,votants={}):
        self.message=message
        self.id=message.id
        self.guild=guild
        self.temps=temps
        self.question=question
        self.start=time()
        self.chan=message.channel
        self.active=True
        self.option=option
        self.end=self.start+self.temps

        self.votants=votants

        if counts==None:
            self.propositions={ids[i]:Proposition(emotes[i],ids[i],props[i]) for i in range(len(props))}
            self.total=0
        else:
            self.propositions={ids[i]:Proposition(emotes[i],ids[i],props[i],count=counts[i]) for i in range(len(props))}
            self.total=sum(counts)

    async def trigger(self, bot):
        await asyncio.sleep(self.temps)
        try:
            message=await self.chan.fetch_message(self.id)
        except:
            self.active=False
            return

        if self.option=="polltime":
            for react in message.reactions:
                if type(react)!=str and react.emoji.id in ids:
                    self.propositions[react.emoji.id].count=react.count-1
                    self.total+=react.count-1

        embed=self.affichage(self.total,self.guild)
        await self.message.reply(embed=embed)
        await self.message.clear_reactions()
        self.active=False
        if self.total==0:
            return None
        else:
            all=list(map(lambda x:self.propositions[x].count, self.propositions))
            propMax=max(self.propositions, key=lambda x:self.propositions[x].count)
            if all.count(self.propositions[propMax].count)>1:
                return None
            else:
                return propMax

    def affichage(self,total,guild):
        descip=""
        if total==0:
            embed=createEmbed(self.question+"\nRésultats","Personne n'a répondu au sondage.",0xfc03d7,self.option,guild)
        else:
            table=dict(sorted(self.propositions.items(), key=lambda item: item[1].count, reverse=True))
            for i in table:
                if table[i].count>=0:
                    descip+="{0} {1} : {2}% ({3})\n".format(table[i].emoji,table[i].prop,round(table[i].count/total*100,2),table[i].count)
            embed=createEmbed(self.question+"\nRésultats",descip,0xfc03d7,self.option,guild)
        return embed


class Petition():
    def __init__(self,message,temps,question,votes,votants=[]):
        self.message=message
        self.guild=message.guild
        self.id=message.id
        self.temps=temps
        self.question=question
        self.start=time()
        self.end=self.start+self.temps
        self.chan=message.channel
        self.active=True
        self.votes=votes
        self.total=0
        self.votants=votants

    async def trigger(self,bot):
        await asyncio.sleep(self.temps)

        try:
            await self.chan.fetch_message(self.id)
        except:
            self.active=False
            return

        embed=self.affichage(self.total>=self.votes,self.guild)
        await self.message.reply(embed=embed)
        await self.message.clear_reactions()
        self.active=False

    def affichage(self,valid,guild):
        if valid:
            return createEmbed(self.question,"La pétition a été validée !\nLes {0} signatures ont été atteintes, bravo !".format(self.votes),0xfc03d7,"petition",guild)
        else:
            return createEmbed(self.question,"La pétition n'a pas atteint ses objectifs...\nSur les {0} signatures attendues, seulement {1} ont été reçues.".format(self.votes,self.total),0xfc03d7,"petition",guild)

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
        embed=createEmbed("Rappel",self.remind,0xfc03d7,"reminder",user)
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
        embed=createEmbed("Rappel",self.remind,0xfc03d7,"reminder",user)
        await chan.send(embed=embed,content=":alarm_clock: Rappel pour <@{0}> :".format(self.user))
        self.active=False

class Giveaway():
    def __init__(self,id,guild,temps,lot,gagnants,chan):
        self.id=id
        self.guild=guild
        self.temps=temps
        self.lot=lot
        self.gagnants=gagnants
        self.start=time()
        self.chan=chan
        self.active=True

    async def trigger(self,bot):
        if self.temps>0:
            await asyncio.sleep(self.temps)
        channel=bot.get_channel(self.chan)
        try:
            message=await channel.fetch_message(self.id)
        except:
            self.active=False
            return
        users=None
        for i in range(len(message.reactions)):
            if type(message.reactions[i].emoji.id)!=str and message.reactions[i].emoji.id==711222160982540380:
                users=await message.reactions[i].users().flatten()
                if bot.user in users:
                    users.remove(bot.user)
        await message.clear_reactions()
        if users==None:
            self.active=False
            return
        if len(users)<self.gagnants:
            embed=createEmbed(self.lot,"<:otROUGE:868535622237818910> Il y a eu moins de participants ({0}) que de gagnants ({1}), le tirage est donc invalidé.".format(len(users),self.gagnants),0xff0000,"giveaway",message.guild)
            await message.edit(embed=embed)
            self.active=False
            return

        connexion,curseur=connectSQL(self.guild,"Giveaway","Guild",None,None)
        count=curseur.execute("SELECT COUNT() as Count FROM liste").fetchone()["Count"]+1
        curseur.execute("INSERT INTO liste VALUES({0},{1},{2},'{3}')".format(count,self.id,self.chan,self.lot))
        curseur.execute("CREATE TABLE {0} (ID BIGINT)".format("n{0}".format(count)))
        for i in users:
            curseur.execute("INSERT INTO {0} VALUES({1})".format("n{0}".format(count),i.id))
        connexion.commit()

        winner,descip=[],""
        for i in range(int(self.gagnants)):
            won=random.choice(users)
            winner.append(won)
            users.remove(won)
            descip+="<@"+str(won.id)+"> "
        embed=message.embeds[0]
        if len(winner)==1:
            embed.set_field_at(2,name="Gagnant",value="Bravo à <@{0}> !".format(winner[0].id))
            await message.reply("<:otVERT:868535645897912330> Bravo à <@{0}> qui a gagné {1} !".format(winner[0].id,self.lot))
        else:
            embed.set_field_at(2,name="Gagnants",value="Bravo à {0}!".format(descip))
            await message.reply("<:otVERT:868535645897912330> Bravo à {0}qui ont gagné {1} !".format(descip,self.lot))
        embed.add_field(name="||Numéro reroll||",value="||{0}||".format(count))
        await message.edit(embed=embed)
        self.active=False
