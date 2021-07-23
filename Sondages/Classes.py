from time import time
import asyncio
from Core.Fonctions.Embeds import createEmbed
from Stats.SQL.ConnectSQL import connectSQL
import random
from Core.Fonctions.DichoTri import nombre

emotes=["<:ot1:705766186909958185>","<:ot2:705766186989912154>","<:ot3:705766186930929685>","<:ot4:705766186947706934>","<:ot5:705766186713088042>","<:ot6:705766187182850148>","<:ot7:705766187115741246>","<:ot8:705766187132256308>","<:ot9:705766187145101363>","<:ot10:705766186909958206>"]
ids=[705766186909958185,705766186989912154,705766186930929685,705766186947706934,705766186713088042,705766187182850148,705766187115741246,705766187132256308,705766187145101363,705766186909958206]

class PollTime():
    def __init__(self,id,guild,temps,props,question,chan):
        self.id=id
        self.guild=guild
        self.temps=temps
        self.propositions=props
        self.question=question
        self.start=time()
        self.chan=chan

    async def trigger(self,bot):
        reacts=[]
        for i in range(len(self.propositions)):
            reacts.append({"Emoji":emotes[i],"ID":ids[i],"Count":0,"Prop":self.propositions[i]})   
        if self.temps>0:
            await asyncio.sleep(self.temps)
        channel=bot.get_channel(self.chan)
        message=await channel.fetch_message(self.id)
        for i in range(len(message.reactions)):
            for j in reacts:
                if message.reactions[i].emoji.id==j["ID"]:
                    j["Count"]=message.reactions[i].count
        embed=self.affichage(reacts,message.guild)
        await message.reply(embed=embed)
        await message.clear_reactions()

    def affichage(self,table,guild):
        total=0
        descip=""
        for i in table:
            i["Count"]=i["Count"]-1
            if i["Count"]>0:
                total=total+i["Count"]
        if total==0:
            embed=createEmbed(self.question,"Personne n'a répondu au sondage.",0xfc03d7,"polltime",guild)
        else:
            table.sort(key=nombre, reverse=True)
            for i in table:
                if i["Count"]>=0:
                    per=i["Count"]/total*100
                    descip+="{0} {1} : {2}% ({3})\n".format(i["Emoji"],i["Prop"],round(per,2),i["Count"])
            embed=createEmbed(self.question,descip,0xfc03d7,"polltime",guild)
        return embed

class Reminder():
    def __init__(self,id,user,temps,remind):
        self.id=id
        self.user=user
        self.temps=temps
        self.remind=remind
        self.start=time()

    async def trigger(self,bot):
        if self.temps>0:
            await asyncio.sleep(self.temps)
        user=bot.get_user(self.user)
        embed=createEmbed("Rappel",self.remind,0xfc03d7,"reminder",user)
        await user.send(embed=embed)

class Giveaway():
    def __init__(self,id,guild,temps,lot,gagnants,chan):
        self.id=id
        self.guild=guild
        self.temps=temps
        self.lot=lot
        self.gagnants=gagnants
        self.start=time()
        self.chan=chan

    async def trigger(self,bot):
        if self.temps>0:
            await asyncio.sleep(self.temps)
        channel=bot.get_channel(self.chan)
        message=await channel.fetch_message(self.id)
        for i in range(len(message.reactions)):
            if message.reactions[i].emoji.id==711222160982540380:
                users=await message.reactions[i].users().flatten()
                if bot.user in users:
                    users.remove(bot.user)
        await message.clear_reactions()
        if len(users)<self.gagnants:
            embed=createEmbed(self.lot,"<:otRED:718392916061716481> Il y a eu moins de participants ({0}) que de gagnants ({1}), le tirage est donc invalidé.".format(len(users),self.gagnants),0xff0000,"giveaway",message.guild)
            await message.edit(embed=embed)
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
        if len(winner)==1:
            embed=createEmbed("Le gagnant de '{0}' est...".format(self.lot),"Félicitations à : <@{0}> !!||\n`Numéro reroll : {1}`||".format(winner[0].id,count),winner[0].color.value,"giveaway",winner[0])
            await message.reply("<:otVERT:718396570638483538> Bravo à <@{0}> qui a gagné {1} !".format(winner[0].id,self.lot))
        else:
            embed=createEmbed("Les gagnants de '{0}' sont...".format(self.lot),"Félicitations à : {0} !!||\n`Numéro reroll : {1}`||".format(descip,count),0xfc03d7,"giveaway",message.guild)
            await message.reply("<:otVERT:718396570638483538> Bravo à {0}qui ont gagné {1} !".format(descip,self.lot))
        await message.edit(embed=embed)