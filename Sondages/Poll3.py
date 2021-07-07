############################################################################

 #######  #########     #########       #######
#       #     #                 #            #     Olbor Track Bot    
#       #     #                 #           #      Créé par OlborEgamorf  
#       #     #         #########          #       Sondages
#       #     #         #                 #                  
 #######      #         ############# #  #                         

############################################################################

import asyncio
import discord
import sys 
import random
sys.path.append('OT3/Exe')
sys.path.append('OT3/Fonctions')
from time import strftime
from Core.Fonctions.Convertisseurs import convZero
from Sondages.Temps import gestionTemps
from Core.Fonctions.Embeds import createEmbed, embedAssert, exeErrorExcept
from Core.Fonctions.DichoTri import nombre
from Core.Fonctions.TempsVoice import tempsVoice
from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.AuteurIcon import auteur
emotes=["<:ot1:705766186909958185>","<:ot2:705766186989912154>","<:ot3:705766186930929685>","<:ot4:705766186947706934>","<:ot5:705766186713088042>","<:ot6:705766187182850148>","<:ot7:705766187115741246>","<:ot8:705766187132256308>","<:ot9:705766187145101363>","<:ot10:705766186909958206>"]
listePoll=[]

dictLimite={"01":31,"02":28,"03":31,"04":30,"05":31,"06":30,"07":31,"08":31,"09":30,"10":31,"11":30,"12":31}
### Tache du OT!polltime
def timer_background(temps):
    '''Timer de la commande OT!polltime.\n
    Temps est un int, le nombre de secondes que la tache doit tenir.'''
    jours=(int(strftime("%d"))+temps//86400)
    if jours>dictLimite[strftime("%m")]:
        jours=jours-dictLimite[strftime("%m")]
        mois=int(strftime("%m"))+1
    else:
        mois=strftime("%m")
    minutes=(int(strftime("%M"))+temps//60)%60
    if (int(strftime("%M"))+temps//60)//60>0:
        heures=(int(strftime("%H")))+(int(strftime("%M"))+temps//60)//60%24
    else:
        heures=strftime("%H")
    secondes=(int(strftime("%S"))+temps)%60
    heures=convZero(heures)
    minutes=convZero(minutes)
    jours=convZero(jours)
    mois=convZero(mois)
    secondes=convZero(secondes)
    textFoot="Fin : "+str(jours)+"/"+str(mois)+" - "+str(heures)+":"+str(minutes)+":"+str(secondes)
    return textFoot
#####

async def exePoll(ctx,args,bot):
    try:
        success=True
        assert len(args)!=0, "Oui, effectivement, c'est la commande, mais il faut une question et des propositions !"
        assert len(args)!=1, "Bonne question, mais il faut des propositions maintenant !"
        assert len(args)!=2, "Définition Larousse de choix :"
        assert len(args)<12, "Pas plus de 10 propositions !"
        descip=""
        for i in range(1,len(args)):
            descip=descip+emotes[i-1]+" "+args[i]+"\n"
        embedPoll=createEmbed(args[0],descip,0xfc03d7,ctx.invoked_with.lower(),ctx.guild)
        await ctx.message.delete()
    except AssertionError as er:
        success=False
        embedPoll=embedAssert(str(er))
        if str(er)=="Définition Larousse de choix :":
            embedPoll.set_image(url="https://cdn.discordapp.com/attachments/726034739550486618/726034799906783262/choix.png")
    except:
        success=False
        embedPoll=await exeErrorExcept(ctx,bot,args)
    message=await ctx.send(embed=embedPoll)
    return message, success, len(args)-1

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
        tempo=args[len(args)-1]
        somme=gestionTemps(tempo)
        foot=timer_background(somme)
        embedPoll=createEmbed(args[0],descip,0xfc03d7,"{0} | {1}".format(ctx.invoked_with.lower(),foot),ctx.guild)
        await ctx.message.delete()
    except AssertionError as er:
        success=False
        embedPoll=embedAssert(str(er))
    except:
        success=False
        embedPoll=await exeErrorExcept(ctx,bot,args)
    message=await ctx.send(embed=embedPoll)
    return message, success, len(args)-2, somme 

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
                assert gagnants>0
                nb=2
            except:
                pass
        for i in range(0,len(args)-nb):
            descip=descip+args[i]+" "
        tempo=args[len(args)-nb]
        somme=gestionTemps(tempo)
        foot=timer_background(somme)
        embedPoll=createEmbed("OT!giveaway : {0}".format(descip),"Cliquez sur la réaction <a:MusicMakeYouLoseControl:711222160982540380> pour tenter d'être tiré au sort !\nNombre de gagnants : {0}".format(gagnants),0xfc03d7,"{0} | {1}".format(ctx.invoked_with.lower(),foot),ctx.guild)
        await ctx.message.delete()
    except AssertionError as er:
        success=False
        embedPoll=embedAssert(str(er)) 
    except:
        success=False
        embedPoll=await exeErrorExcept(ctx,bot,args)
    message=await ctx.send(embed=embedPoll)
    return message, success, gagnants, somme 

### Embed poll
def affichageEmbedPoll(question,table):
    total=0
    descip=""
    for i in table:
        i["Count"]=i["Count"]-1
        if i["Count"]>0:
            total=total+i["Count"]
    if total==0:
        embedP=discord.Embed(title=question, description="Personne n'a répondu au sondage", color=0xfc03d7)
        embedP.set_footer(text="Résultats poll - total : "+str(total))
        return embedP
    table.sort(key=nombre, reverse=True)
    for i in table:
        if i["Count"]>=0:
            per=i["Count"]/total*100
            descip=descip+(i["Emoji"]+" : "+str(round(per,2))+"% ("+str(i["Count"])+")\n")
    embedP=discord.Embed(title=question, description=descip, color=0xfc03d7)
    embedP.set_footer(text="Résultats poll - total : "+str(total))
    return embedP
#####

async def addPollEmotes(props,message):
    for i in range(props):
        await message.add_reaction(emotes[i])
    return

async def reminder_task(user,temps,phrase):
    counter=0
    while counter!=temps:
        counter+=1
        await asyncio.sleep(1)
    embedF=discord.Embed(title="Reminder",description=phrase,color=0xfc03d7)
    embedF.set_footer(text="OT!reminder")
    await user.send(embed=embedF)
    return
async def exeReminder(ctx,bot,args):
    try:
        assert len(args)!=0, "Votre demande est vide. Donnez moi ce dont vous voulez que je vous rappelle et dans combien de temps ! \nLe temps doit être un nombre suivi de s (pour secondes), m (pour minutes), h (pour heures) ou d (pour jours)."
        assert len(args)>1, "Donnez moi du temps !\nLe temps doit être un nombre suivi de s (pour secondes), m (pour minutes), h (pour heures) ou d (pour jours)."
        phrase=""
        for i in range(0,len(args)-1):
            phrase+=" "+args[i]
        temps=gestionTemps(args[len(args)-1])
        tempsstr=tempsVoice(temps,0)
        embedTable=discord.Embed(title="Reminder",description="Très bien ! Je t'enverrai un message privé dans "+str(tempsstr)+" pour te rappeler de "+phrase+" !",color=0xfc03d7)
        embedTable.set_footer(text="OT!reminder")
        bot.loop.create_task(reminder_task(ctx.author,temps,phrase))
    except AssertionError as er:
        embedTable=embedAssert(str(er))
    except:
        embedTable=await exeErrorExcept(ctx,bot,args)
    await ctx.send(embed=embedTable)
    return

async def exeMessagePoll(message,client,temps,props):
    if message.embeds!=[] and message.author==client.user:
        bas=message.embeds[0].footer.text
        reacts=[{"Emoji":"<:ot1:705766186909958185>","ID":705766186909958185, "Count":0},{"Emoji":"<:ot2:705766186989912154>","ID":705766186989912154,"Count":0},{"Emoji":"<:ot3:705766186930929685>","ID":705766186930929685,"Count":0},{"Emoji":"<:ot4:705766186947706934>","ID":705766186947706934,"Count":0},{"Emoji":"<:ot5:705766186713088042>","ID":705766186713088042,"Count":0},{"Emoji":"<:ot6:705766187182850148>","ID":705766187182850148,"Count":0},{"Emoji":"<:ot7:705766187115741246>","ID":705766187115741246,"Count":0},{"Emoji":"<:ot8:705766187132256308>","ID":705766187132256308,"Count":0},{"Emoji":"<:ot9:705766187145101363>","ID":705766187145101363,"Count":0},{"Emoji":"<:ot10:705766186909958206>","ID":705766186909958206,"Count":0}]        
        if bas[0:7]=="OT!poll":
            await addPollEmotes(props,message)
        if bas.split(" ")[0]=="OT!poll":
            embedPoll=discord.Embed(description="**Sondage lancé :** | {0.guild}".format(message),color=0xfc03d7)
            embedPoll.set_footer(text="OlborTrack Log")
            await client.get_channel(706177656059854888).send(embed=embedPoll)
            return

        elif bas.split(" ")[0]=="OT!polltime":
            question=message.embeds[0].title
            embedPoll=discord.Embed(description="**Sondage lancé :** "+question+" "+str(temps)+" | {0.guild}".format(message),color=0xfc03d7)
            embedPoll.set_footer(text="OlborTrack Log")
            await client.get_channel(706177656059854888).send(embed=embedPoll)
            await asyncio.sleep(temps)
            message=await message.channel.fetch_message(message.id)
            for i in range(len(message.reactions)):
                for j in reacts:
                    if message.reactions[i].emoji.id==j["ID"]:
                        j["Count"]=message.reactions[i].count
            embedResults=affichageEmbedPoll(question,reacts)
            await message.channel.send(embed=embedResults)
            await message.clear_reactions()
            return
            
        elif bas[0:11]=="OT!giveaway":
            winner=[]
            descip=""
            question=message.embeds[0].title
            await message.add_reaction("<a:MusicMakeYouLoseControl:711222160982540380>")
            embedPoll=discord.Embed(description="**Giveaway lancé :** "+question+" "+str(temps)+" | {0.guild}".format(message),color=0xfc03d7)
            embedPoll.set_footer(text="OlborTrack Log")
            await client.get_channel(706177656059854888).send(embed=embedPoll)
            await asyncio.sleep(temps)
            message=await message.channel.fetch_message(message.id)
            for i in range(len(message.reactions)):
                if message.reactions[i].emoji.id==711222160982540380:
                    users=await message.reactions[i].users().flatten()
                    users.remove(client.user)
            await message.clear_reactions()
            if len(users)<props:
                embedResults=discord.Embed(title=question, description="<:otRED:718392916061716481> Il y a eu moins de participants que de gagnants...", color=0xff0000)
                embedResults.set_footer(text="OT!giveaway")
                await message.edit(embed=embedResults)
                return

            connexion,curseur=connectSQL(message.guild.id,"Giveaway","Guild",None,None)
            count=curseur.execute("SELECT COUNT() as Count FROM liste").fetchone()["Count"]+1
            curseur.execute("INSERT INTO liste VALUES({0},{1},{2})".format(count,message.id,message.channel.id))
            curseur.execute("CREATE TABLE {0} (ID BIGINT)".format("n{0}".format(count)))
            for i in users:
                curseur.execute("INSERT INTO {0} VALUES({1})".format("n{0}".format(count),i.id))
            connexion.commit()

            for i in range(int(props)):
                won=random.choice(users)
                winner.append(won)
                users.remove(won)
                descip+="<@"+str(won.id)+"> "
            if len(winner)==1:
                embedResults=discord.Embed(title=question, description="Gagnant : <@"+str(winner[0].id)+">||\n`Numéro reroll : "+str(count)+"`||", color=winner[0].color.value)
                embedResults=auteur(winner[0].id,winner[0],winner[0].avatar,embedResults,"user")
                await message.channel.send("<:otVERT:718396570638483538> Bravo à <@"+str(winner[0].id)+"> qui a gagné "+question+" !")
            else:
                embedResults=discord.Embed(title=question, description="Gagnants : "+descip+"\n||`Numéro reroll : "+str(count)+"`||", color=0xfc03d7)
                embedResults=auteur(message.guild.id,message.guild.name,message.guild.icon,embedResults,"guild")
                await message.channel.send("<:otVERT:718396570638483538> Bravo à "+descip+"qui ont gagné "+question+" !")
            embedResults.set_footer(text="OT!giveaway")
            await message.edit(embed=embedResults)
            return
    else:
        return

async def exeGaReroll(ctx,args,bot):
    try:
        assert len(args)!=0, "Vous devez me donner le numéro du giveaway !"
        connexion,curseur=connectSQL(ctx.guild.id,"Giveaway","Guild",None,None)
        try:
            etat=curseur.execute("SELECT * FROM liste WHERE Nombre={0}".format(args[0])).fetchone()
        except:
            raise AssertionError("Le numéro de giveaway donné n'est pas valide.")
        assert etat!=None, "Ce numéro de giveaway n'existe pas."
        try:
            message=await ctx.guild.get_channel(etat["IDChan"]).fetch_message(etat["IDMess"])
        except:
            raise AssertionError("Ce giveaway est introuvable. Soit je n'ai plus accès au salon où il a eu lieu, soit il a été supprimé.")
        choix=random.choice(curseur.execute("SELECT * FROM {0}".format("n{0}".format(args[0]))).fetchall())
        await ctx.send("<:otVERT:718396570638483538> Bravo à <@"+str(choix["ID"])+"> qui a gagné "+message.embeds[0].title+" !")
        return
    except AssertionError as er:
        embedTable=embedAssert(str(er))
    except:
        embedTable=await exeErrorExcept(ctx,bot,args)
    await ctx.send(embed=embedTable)
    return