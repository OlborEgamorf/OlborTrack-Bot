import asyncio
from random import choice, randint

import discord
from Core.Fonctions.Embeds import createEmbed, embedAssert, exeErrorExcept
from Jeux.CodeNames.ClasseCodeNames import JeuCN
from Jeux.Paris import Pari

dictColor={1:0xFF4600,2:0x5C99EC}


async def startGameCodeNames(ctx,bot,inGame,gamesCN):
    try:
        assert ctx.author.id not in inGame, "Terminez votre partie en cours avant de lancer ou rejoindre une partie."
        game=JeuCN(ctx.guild,ctx.author.id)
        game.ids.append(ctx.author.id)
        inGame.append(ctx.author.id)
        message=await ctx.send(embed=createEmbed("Code Names","Vous connaissez les règles",0xad917b,ctx.invoked_with.lower(),ctx.guild))
        gamesCN[message.id]=game

        await message.add_reaction("<:otVALIDER:772766033996021761>")
        await message.add_reaction("<:otANNULER:811242376625782785>")

        for i in range(60):
            if not game.playing:
                await asyncio.sleep(1)
            else:
                break

        game.playing=True
        await message.clear_reactions()
        if await game.checkPlayers(message,inGame,ctx,4,bot):
            descip="<:otVERT:868535645897912330> La partie commence "
            for i in game.joueurs:
                descip+="<@{0}> ".format(i.userid)
            await message.channel.send(descip)
            messAd=await bot.get_channel(870598360296488980).send("{0} - {1} : partie OT!codenames débutée\n{2} joueurs".format(ctx.guild.name,ctx.guild.id,len(game.joueurs)))
        else:
            return

        begin=True
        turn=game.generateGame()
        game.showPlateau(True)
        game.showPlateau(False)
        for i in game.joueurs:
            if i.role=="mj":
                await i.user.send(file=discord.File("Images/Plateau{0}True.png".format(game.guild.id)),embed=game.embedMJ(i.equipe,i.user),content="Vous avez 2 minutes pour réfléchir...")
        message=await message.channel.send(file=discord.File("Images/Plateau{0}False.png".format(game.guild.id)),embed=game.embedCompo())
        gamesCN[message.id]=game
        await asyncio.sleep(120)
        game.paris=Pari(game.ids,"CodeNames")
        while game.playing:
            for i in game.equipe[turn]:
                if i.role=="mj":
                    if not begin:
                        await i.user.send(file=discord.File("Images/Plateau{0}True.png".format(game.guild.id)),embed=game.embedMJ(i.equipe,i.user))
                    mj=i.user
                else:
                    joueur=i

            def check(mess):
                try:
                    assert mess.author.id==mj.id
                    assert mess.channel.type==discord.ChannelType.private
                    content=mess.content.split(" ")
                    assert len(content)>=2
                    valid=True
                    for i in game.plateau:
                        if i.mot.lower()==content[0].lower():
                            valid=False
                            break
                    assert valid
                    nb=int(content[1][0])
                except AssertionError:
                    return False
                return True
            
            await mj.send(embed=createEmbed("C'est votre tour !","Vous devez faire deviner des mots à votre coéquipier !\nVous avez une minute pour me donner un mot indice et le nombre de mots que vous voulez faire deviner avec.\nVous pouvez mettre un '+' juste après le nombre pour laisser votre partenaire en deviner plus !",dictColor[turn],"codenames",mj))
            try:
                mess=await bot.wait_for("message",check=check,timeout=60)
            except asyncio.TimeoutError:
                await mj.send("<:otROUGE:868535622237818910> Temps écoulé, votre tour est passé.")
                await message.channel.send("<:otROUGE:868535622237818910> <@{0}> a mis trop de temps. Le tour est passé.".format(mj.id))
                turn+=1
                if turn==3:
                    turn=1
                continue

            content=mess.content.split(" ")
            mot,nb,plus=content[0],int(content[1][0]),(len(content[1])>=2 and content[1][1]=="+")

            embed=createEmbed("Devinez !","C'est à vous de deviner les mots !\nCliquez sur <:otVALIDER:772766033996021761> pour faire vos propositions. Elles démareront automatiquement dans 1 minute et 30 secondes",dictColor[turn],"codenames",joueur.user)
            embed.add_field(name="Indice",value=mot,inline=True)
            embed.add_field(name="Nombre de mots",value=nb,inline=True)
            embed.add_field(name="Mots supplémentaires",value=str(plus),inline=True)
            messGuess=await message.channel.send(embed=embed,content="<@{0}>".format(joueur.userid))
            await messGuess.add_reaction("<:otVALIDER:772766033996021761>")

            def check(react,user):
                if type(react.emoji)==str:
                        return False
                return user.id==joueur.userid and react.message.id==messGuess.id and react.emoji.id==772766033996021761

            try:
                await bot.wait_for("reaction_add",check=check,timeout=90)
            except asyncio.TimeoutError:
                pass

            guess=True
            nombre=0
            await message.channel.send("<:otVERT:868535645897912330> Ecrivez à quel mot vous pensez ! Vous avez 20 secondes par mot.")
            while guess and (nombre!=nb or plus):

                def check(mess):
                    try:
                        assert mess.author.id==joueur.userid
                        content=mess.content.split()
                        valid=False
                        for i in game.plateau:
                            if i.mot.lower()==content[0].lower():
                                return True
                    except:
                        return False
                    return False

                try:
                    mess=await bot.wait_for("message",check=check,timeout=20)
                except asyncio.TimeoutError:
                    break
                mot=mess.content.split()[0].lower()
                for i in game.plateau:
                    if i.mot.lower()==mot:
                        i.setFind(joueur)
                        if i.equipe!=turn:
                            guess=False
                        else:
                            await mess.add_reaction("<:otOUI:726840394150707282>")
                
                nombre+=1
            
            game.showPlateau(True)
            game.showPlateau(False)
            begin=False
            win=game.checkWin()
            if win!=None:
                game.playing=False
                embed=game.embedWin(win)
                await message.channel.send(embed=embed)
                await message.channel.send(file=discord.File("Images/Plateau{0}True.png".format(game.guild.id)))
                await game.stats(win,message.channel)
                for j in range(2):
                    game.paris.distribParis(game.equipe[win][j].userid)
            else:
                await message.channel.send(file=discord.File("Images/Plateau{0}False.png".format(game.guild.id)),content="<:otVERT:868535645897912330> Voici le nouveau plan de jeu !")
            
            game.fermeture()
            
            turn+=1
            if turn==3:
                turn=1

        if "messAd" in locals():
            await messAd.delete()
    except AssertionError as er:
        await ctx.send(embed=embedAssert(er))
        return
    except:
        await ctx.send(embed=await exeErrorExcept(ctx,bot,""))
    try:
        await game.delEmotes()
    except:
        pass
    for i in game.ids:
        inGame.remove(i)
    del gamesCN[message.id]