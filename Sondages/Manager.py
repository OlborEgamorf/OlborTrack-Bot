import asyncio
from Core.Decorator import OTCommand
from Core.Fonctions.Embeds import createEmbed
from Core.Fonctions.Phrase import createPhrase

from Sondages.Classes import PollTime
from Sondages.Temps import footerTime, gestionTemps
from Sondages.exePolls import dictPolls

emotes=["<:ot1:705766186909958185>","<:ot2:705766186989912154>","<:ot3:705766186930929685>","<:ot4:705766186947706934>","<:ot5:705766186713088042>","<:ot6:705766187182850148>","<:ot7:705766187115741246>","<:ot8:705766187132256308>","<:ot9:705766187145101363>","<:ot10:705766186909958206>"]

@OTCommand
async def pollManager(ctx,bot):
    option="poll"
    message=await ctx.reply(embed=createEmbed("Assistant sondage","Bienvenue dans l'assistant sondage !\nCet outil vous permet de créer un sondage étape par étape, avec plus d'options possibles !\nToutes les indications seront affichées sur ce message.\nCommençons ! **Donnez moi la question que vous voulez poser.**",0xfc03d7,ctx.invoked_with.lower(),ctx.guild))

    def checkValid(reaction,user):
        if type(reaction.emoji)==str:
            return False
        return reaction.emoji.id in (772766033996021761,811242376625782785) and reaction.message.id==message.id and user.id==ctx.author.id
    
    def checkMess(mess):
        return mess.author.id==ctx.author.id and mess.channel.id==ctx.channel.id

    def checkImage(mess):
        return mess.author.id==ctx.author.id and mess.channel.id==ctx.channel.id and len(mess.attachments)!=0

    def checkSalon(mess):
        return mess.author.id==ctx.author.id and mess.channel.id==ctx.channel.id and len(mess.channel_mentions)!=0
    
    messWait=await bot.wait_for("message",check=checkMess,timeout=45)
    question=createPhrase(messWait.content.split(" "))

    apercu=createEmbed(question,"<@{0}> a lancé un sondage !".format(ctx.author.id),0xfc03d7,"poll",ctx.guild)
    apercu.add_field(name="Propositions",value="Pour le moment vide...",inline=False)
    apercuMess=await ctx.send("Aperçu du sondage :", embed=apercu)

    await message.edit(embed=createEmbed("Assistant sondage","Désormais, **indiquez moi vos propositions** ! Minimum 2 et maximum 10.\nEnvoyez 'stop' pour arrêter et 'del [n° de proposition]' pour supprimer la proposition que vous souhaitez.",0xfc03d7,ctx.invoked_with.lower(),ctx.guild))

    liste=[]
    reponse=""
    count=0
    while reponse.lower()!="stop":
        try:
            messWait=await bot.wait_for("message",check=checkMess,timeout=120)
        except asyncio.exceptions.TimeoutError:
            if len(liste)>=2:
                reponse="stop"
            else:
                raise asyncio.exceptions.TimeoutError()
        reponse=createPhrase(messWait.content.split(" "))[:-1]
        split=reponse.split(" ")
        if split[0].lower()=="del" and len(liste)!=0:
            if len(split)>1:
                try:
                    del liste[int(split[1])-1]
                except:
                    await messWait.reply("Impossible d'effacer cette proposition.")
                    continue
            else:
                liste.pop()
            if len(liste)==0:
                apercu.set_field_at(0,name="Propositions",value="Pour le moment vide...")
            else:
                descip=""
                for i,b in enumerate(liste):
                    descip+=emotes[i]+" "+b+"\n"
                apercu.set_field_at(0,name="Propositions",value=descip)
        elif reponse.lower()!="stop":
            if len(liste)==0:
                apercu.set_field_at(0,name="Propositions",value=emotes[0]+" "+reponse+"\n")
            else:
                apercu.set_field_at(0,name="Propositions",value=apercu.fields[0].value+emotes[len(liste)]+" "+reponse+"\n")
            liste.append(reponse)
        else:
            if len(liste)<2:
                reponse=""
                await messWait.reply("Vous ne pouvez pas arrêter les propositions alors qu'il en a moins de 2 !")
        if len(liste)==10:
            reponse="stop"
        await apercuMess.edit(embed=apercu)

    await message.edit(embed=createEmbed("Assistant sondage","**Voulez vous ajouter une image d'illustration ?**\nAppuyez sur <:otVALIDER:772766033996021761> pour en ajouter un, ou <:otANNULER:811242376625782785> pour continuer",0xfc03d7,ctx.invoked_with.lower(),ctx.guild))

    await message.add_reaction("<:otVALIDER:772766033996021761>")
    await message.add_reaction("<:otANNULER:811242376625782785>")

    try:
        reaction,user=await bot.wait_for('reaction_add', check=checkValid, timeout=60)
        await reaction.remove(user)
        if reaction.emoji.id==772766033996021761:
            await message.edit(embed=createEmbed("Assistant sondage","Envoyez moi l'image de votre choix.",0xfc03d7,ctx.invoked_with.lower(),ctx.guild))
            messWait=await bot.wait_for("message",check=checkImage,timeout=120)
            image=messWait.attachments[0].url
            apercu.set_image(url=image)
            await apercuMess.edit(embed=apercu)
    except asyncio.exceptions.TimeoutError:
        pass

    await message.edit(embed=createEmbed("Assistant sondage","**Voulez vous ajouter du temps ?**\nAppuyez sur <:otVALIDER:772766033996021761> pour en ajouter un, ou <:otANNULER:811242376625782785> pour continuer",0xfc03d7,ctx.invoked_with.lower(),ctx.guild))
    reaction,user=await bot.wait_for('reaction_add', check=checkValid, timeout=120)

    if reaction.emoji.id==772766033996021761:
        option="polltime"
        await reaction.remove(user)
        await message.edit(embed=createEmbed("Assistant sondage","**Donnez moi le temps que vous souhaitez.**\nIndiquer un nombre suivi de s (pour secondes) ou m (pour minutes) ou h (pour heures) ou j (pour jours). Si vous voulez mettre des nombres à virgule, utilisez un point (.).\nExemples : 20m (20 minutes), 1.5j (1 jour et 12 heures), 10h (10 heures), 20h20m10s (20 heures, 20 minutes et 10 secondes.",0xfc03d7,ctx.invoked_with.lower(),ctx.guild))
        flag=True
        try:
            while flag:
                try:
                    messWait=await bot.wait_for("message",check=checkMess,timeout=120)
                    temps=gestionTemps(messWait.content)
                    format=footerTime(temps)
                    flag=False
                except AssertionError:
                    pass
            apercu.set_footer(text="OT!polltime")
            apercu.add_field(name="Fin des votes",value=format,inline=False)
            await apercuMess.edit(embed=apercu)
        except asyncio.exceptions.TimeoutError:
            pass
        
        if not flag:
            try:
                await message.edit(embed=createEmbed("Assistant sondage","**Voulez vous que les membres ne puissent choisir uniquement une réponse ?**\nAppuyez sur <:otVALIDER:772766033996021761> pour en ajouter un, ou <:otANNULER:811242376625782785> pour continuer",0xfc03d7,ctx.invoked_with.lower(),ctx.guild))     
                reaction,user=await bot.wait_for('reaction_add', check=checkValid, timeout=120)

                if reaction.emoji.id==772766033996021761:
                    option="vote"
                    await reaction.remove(user)
                    apercu.set_footer(text="OT!vote")
                    apercu.add_field(name="Vote",value="Seulement votre première réponse sera prise en compte.",inline=True)
                    await apercuMess.edit(embed=apercu)

                    await message.edit(embed=createEmbed("Assistant sondage","**Voulez vous que les votes soient masqués ?**\nAppuyez sur <:otVALIDER:772766033996021761> pour en ajouter un, ou <:otANNULER:811242376625782785> pour continuer",0xfc03d7,ctx.invoked_with.lower(),ctx.guild))
                    reaction,user=await bot.wait_for('reaction_add', check=checkValid, timeout=120)

                    if reaction.emoji.id==772766033996021761:
                        option="election"
                        apercu.set_footer(text="OT!election")
                        apercu.add_field(name="Élection",value="Votre choix sera masqué et anonyme.",inline=True)
                        await apercuMess.edit(embed=apercu)
                apercu.set_field_at(1,name="Fin des votes",value=footerTime(temps))
            except asyncio.exceptions.TimeoutError:
                pass

    await message.clear_reactions()

    await message.edit(embed=createEmbed("Assistant sondage","Dernière étape !\n**Dans quel salon voulez vous envoyer le sondage ?**\nMentionnez le salon que vous souhaitez. Le sondage s'enverra automatiquement dans ce salon.",0xfc03d7,ctx.invoked_with.lower(),ctx.guild))
    messWait=await bot.wait_for("message",check=checkSalon,timeout=120)

    await apercuMess.delete()
    messageSend=await messWait.channel_mentions[0].send(embed=apercu)
    await message.edit(embed=createEmbed("Assistant sondage","Sondage créé !",0xfc03d7,ctx.invoked_with.lower(),ctx.guild))
    
    for i in range(len(liste)):
        await messageSend.add_reaction(emotes[i])
    if option!="poll":
        dictPolls[messageSend.id]=PollTime(messageSend,ctx.guild,temps,liste,question,option)
        await dictPolls[messageSend.id].trigger(bot)
        del dictPolls[messageSend.id]