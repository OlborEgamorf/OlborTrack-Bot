import asyncio

from Core.Fonctions.Embeds import createEmbed, embedAssert, exeErrorExcept
from Jeux.CodeNames import JeuCodeNames
from Jeux.Matrice import JeuMatrice
from Jeux.Morpion import JeuMorpion
from Jeux.Puissance4 import JeuP4
from Jeux.Tortues import JeuTortues
from Jeux.TortuesDuo import JeuTortuesDuo
from Jeux.TrivialBR import JeuTrivialBR
from Jeux.TrivialParty import JeuTrivialParty
from Jeux.TrivialVersus import JeuTrivialVersus

listeCross=[]
dictMax={"Tortues":5,"TortuesDuo":4,"TrivialVersus":5,"TrivialBR":15,"TrivialParty":15,"P4":2,"Matrice":2,"Morpion":2}

async def gameLauncher(ctx,bot,jeu,inGame,dictJeux,cross):
    if True:
        assert ctx.author.id not in inGame, "Terminez votre partie en cours avant de lancer ou rejoindre une partie."
        mini=2
        if jeu=="P4":
            message=await ctx.reply(embed=createEmbed("Puissance 4","Appuyez sur la réaction <:otVALIDER:772766033996021761> pour défier <@{0}> au Puissance 4.\nL'objectif est d'aligner 4 jetons de votre couleur dans n'importe quel sens (horizontallement, verticalement ou diagonalement) en premier !\nLes réactions allant de <:ot1:705766186909958185> à <:ot7:705766187115741246> représentent les colonnes où vous pouvez placer votre jeton. Cliquez sur l'une d'entre elles et le jeton apparaîtra !\nLa personne qui a demandé la partie peut cliquer sur <:otANNULER:811242376625782785> pour se retirer de la partie.".format(ctx.author.id),0xad917b,ctx.invoked_with.lower(),ctx.guild))
            game=createGame(cross,JeuP4,ctx,message)
            emotes=["<:ot1:705766186909958185>","<:ot2:705766186989912154>","<:ot3:705766186930929685>","<:ot4:705766186947706934>","<:ot5:705766186713088042>","<:ot6:705766187182850148>","<:ot7:705766187115741246>"]
        elif jeu=="Tortues":
            message=await ctx.reply(embed=createEmbed("Course des tortues","Le jeu se joue de 2 à 5 joueurs.\nAu début de la partie, chaque joueur se voit attribuer une couleur secrète, envoyée en message privé, qui est celle de sa tortue.\nLe but est d'atteindre l'arrivée avant tout le monde, en jouant avec des cartes qui font avancer les tortues.\nLes joueurs jouent chacun leur tour. Les réactions <:ot1:705766186909958185> à <:ot5:705766186713088042> permettent de choisir sa carte.\nSi vous choisissez une carte 'au choix', cliquez ensuite sur la réaction de la tortue que vous voulez déplacer <:OTTbleu:860119157491892255> <:OTTjaune:860119157688631316> <:OTTrouge:860119157495693343> <:OTTvert:860119157331853333> <:OTTviolet:860119157672247326>.\nLes cartes 'dernière tortue' font avancer la dernière tortue.\nEn dehors de la case départ, les tortues s'empilent et avancent en même temps !\nSi plusieurs tortues arrivent en même temps, celle qui est le plus bas gagne !\nBonne chance !\n\nAppuyez sur la réaction <:otVALIDER:772766033996021761> pour rejoindre la partie de Course des tortues et <:otANNULER:811242376625782785> pour annuler votre participation.\n<@{0}> peut lancer la partie en appuyant sur <:otVALIDER:772766033996021761>, sinon elle se lancera automatiquement au bout de 1 minute.".format(ctx.author.id),0xad917b,ctx.invoked_with.lower(),ctx.guild))
            game=createGame(cross,JeuTortues,ctx,message)
            emotes=["<:ot1:705766186909958185>","<:ot2:705766186989912154>","<:ot3:705766186930929685>","<:ot4:705766186947706934>","<:ot5:705766186713088042>","<:OTTbleu:860119157491892255>", "<:OTTjaune:860119157688631316>", "<:OTTrouge:860119157495693343>", "<:OTTvert:860119157331853333>", "<:OTTviolet:860119157672247326>"]
        elif jeu=="TortuesDuo":
            message=await ctx.reply(embed=createEmbed("Course des tortues DUO","Le jeu se joue avec 4 joueurs, en 2 contre 2.\nAu début de la partie, chaque binome (aléatoire) se voit attribuer deux couleurs secrètes, envoyées en message privé, qui est celle de ses tortues.\nSauf que vous ne connaissez pas le deuxième membre de votre binome, qui doit faire gagner les mêmes tortues que vous !\nLe but est de faire atteindre l'arrivée avant tout le monde aux deux tortues, en jouant avec des cartes qui font avancer les tortues.\nLes joueurs jouent chacun leur tour. Les réactions <:ot1:705766186909958185> à <:ot5:705766186713088042> permettent de choisir sa carte.\nSi vous choisissez une carte 'au choix', cliquez ensuite sur la réaction de la tortue que vous voulez déplacer <:OTTbleu:860119157491892255> <:OTTjaune:860119157688631316> <:OTTrouge:860119157495693343> <:OTTvert:860119157331853333> <:OTTviolet:860119157672247326>.\nLes cartes 'dernière tortue' font avancer la dernière tortue.\nEn dehors de la case départ, les tortues s'empilent et avancent en même temps !\nSi plusieurs tortues arrivent en même temps, celle qui est le plus bas gagne !\nBonne chance !\n\nAppuyez sur la réaction <:otVALIDER:772766033996021761> pour rejoindre la partie et <:otANNULER:811242376625782785> pour annuler votre participation.\nLa partie se lancera automatiquement quand assez de joueurs auront rejoint, sinon au bout de 1 minute elle sera annulée.",0xad917b,ctx.invoked_with.lower(),ctx.guild))
            game=createGame(cross,JeuTortuesDuo,ctx,message)
            emotes=["<:ot1:705766186909958185>","<:ot2:705766186989912154>","<:ot3:705766186930929685>","<:ot4:705766186947706934>","<:ot5:705766186713088042>","<:OTTbleu:860119157491892255>", "<:OTTjaune:860119157688631316>", "<:OTTrouge:860119157495693343>", "<:OTTvert:860119157331853333>", "<:OTTviolet:860119157672247326>"]
            mini=4
        elif jeu=="Matrice":
            message=await ctx.reply(embed=createEmbed("Matrice","Le jeu se joue à 2 joueurs.\nLe jeu fonctionne avec un plateau de 16 cases, 4x4.Il y a aussi 16 pions. Chaque joueur possède 8 pions de sa couleur.\nChaque pion possède 4 caractéristiques : la taille (grand/petit), la couleur (bleu/rouge), la forme (carré/rond) et le remplissage (plein/creux).\nLe but est d'aligner 4 pions ayant au moins une caractéristique en commun.\nPour jouer, servez vous des réactions <:ot1:705766186909958185> à <:ot8:705766187132256308> pour sélectionner votre pion, puis écrivez les coordonnées de la case que vous voulez, de la forme lettreCHIFFRE\nBonne chance !\n\nAppuyez sur la réaction <:otVALIDER:772766033996021761> pour rejoindre la partie de Course des tortues et <:otANNULER:811242376625782785> pour annuler votre participation.\n<@{0}> peut lancer la partie en appuyant sur <:otVALIDER:772766033996021761>, sinon elle se lancera automatiquement au bout de 1 minute.".format(ctx.author.id),0xad917b,ctx.invoked_with.lower(),ctx.guild))
            game=createGame(cross,JeuMatrice,ctx,message)
            emotes=["<:ot1:705766186909958185>","<:ot2:705766186989912154>","<:ot3:705766186930929685>","<:ot4:705766186947706934>","<:ot5:705766186713088042>","<:ot6:705766187182850148>","<:ot7:705766187115741246>","<:ot8:705766187132256308>"]
        elif jeu=="Morpion":
            message=await ctx.reply(embed=createEmbed("Morpion","Appuyez sur la réaction <:otVALIDER:772766033996021761> pour défier <@{0}> au Morpion.\nL'objectif est d'aligner 3 jetons de votre couleur dans n'importe quel sens (horizontallement, verticalement ou diagonalement) en premier !\nÉcrivez les coordonnées de la case où vous voulez poser votre jeton dans le salon lorsque c'est votre tour ! En commençant par la lettre puis le chiffre.\nLa personne qui a demandé la partie peut cliquer sur <:otANNULER:811242376625782785> pour se retirer de la partie.".format(ctx.author.id),0xad917b,ctx.invoked_with.lower(),ctx.guild))
            game=createGame(cross,JeuMorpion,ctx,message)
            emotes=[]
        elif jeu=="TrivialVersus":
            message=await ctx.reply(embed=createEmbed("Trivial Versus","Appuyez sur la réaction <:otVALIDER:772766033996021761> pour rejoindre la partie de Trivial Versus et <:otANNULER:811242376625782785> pour annuler votre participation. La personne qui a demandé la partie peut cliquer sur <:otVALIDER:772766033996021761> pour lancer directement la partie. Sinon, elle va démarrer dans une minute.\n\n**Comment jouer ? : ** le Trivial Versus se joue de 2 à 5 joueurs. Des questions vont se suivre, l'objectif est d'atteindre 5 bonnes réponses avant tout le monde ! Le jeu se déroule dans ce salon et sur ce message. Les propositions sont numérotés de <:ot1:705766186909958185> à <:ot4:705766186947706934>, cliquez sur la réaction qui correspond pour choisir votre réponse. Au bout de 20s ou quand tout le monde a répondu, les résultats sont affichés. La prochaine question démarrera 7s après. Bonne chance !".format(ctx.author.id),0xad917b,ctx.invoked_with.lower(),ctx.guild))
            game=createGame(cross,JeuTrivialVersus,ctx,message)
            emotes=["<:ot1:705766186909958185>","<:ot2:705766186989912154>","<:ot3:705766186930929685>","<:ot4:705766186947706934>"]
        elif jeu=="TrivialBR":
            message=await ctx.reply(embed=createEmbed("Trivial Battle Royale","Appuyez sur la réaction <:otVALIDER:772766033996021761> pour rejoindre la partie de Trivial Battle Royale et <:otANNULER:811242376625782785> pour annuler votre participation. La personne qui a demandé la partie peut cliquer sur <:otVALIDER:772766033996021761> pour lancer directement la partie. Sinon, elle va démarrer dans une minute.\n\n**Comment jouer ? : ** le Trivial BR se joue de 2 à 15 joueurs. Des questions vont se suivre, l'objectif est d'être le dernier en vie ! Au début vous avez 3 vies, et vous en perdez une par mauvaise réponse. Le jeu se déroule dans ce salon et sur ce message. Les propositions sont numérotés de <:ot1:705766186909958185> à <:ot4:705766186947706934>, cliquez sur la réaction qui correspond pour choisir votre réponse. Au bout de 20s ou quand tout le monde a répondu, les résultats sont affichés. Bonne chance !".format(ctx.author.id),0xad917b,ctx.invoked_with.lower(),ctx.guild))
            game=createGame(cross,JeuTrivialBR,ctx,message)
            emotes=["<:ot1:705766186909958185>","<:ot2:705766186989912154>","<:ot3:705766186930929685>","<:ot4:705766186947706934>"]
        elif jeu=="TrivialParty":
            message=await ctx.reply(embed=createEmbed("Trivial Party""Appuyez sur la réaction <:otVALIDER:772766033996021761> pour rejoindre la partie de Trivial Party et <:otANNULER:811242376625782785> pour annuler votre participation. La personne qui a demandé la partie peut cliquer sur <:otVALIDER:772766033996021761> pour lancer directement la partie. Sinon, elle va démarrer dans une minute.\n\n**Comment jouer ? : ** le Trivial Party se joue de 2 à 15 joueurs. Des questions vont se suivre, il faut obtenir 12 points pour gagner ! De manière aléatoire, des évènement peuvent se dérouler pour changer complétement la partie ! Le jeu se déroule dans ce salon et sur ce message. Les propositions sont numérotés de <:ot1:705766186909958185> à <:ot4:705766186947706934>, cliquez sur la réaction qui correspond pour choisir votre réponse. Au bout de 20s ou quand tout le monde a répondu, les résultats sont affichés. La prochaine question démarrera peu de temps après. Bonne chance !".format(ctx.author.id),0xad917b,ctx.invoked_with.lower(),ctx.guild))
            game=createGame(cross,JeuTrivialParty,ctx,message)
            emotes=["<:ot1:705766186909958185>","<:ot2:705766186989912154>","<:ot3:705766186930929685>","<:ot4:705766186947706934>"]
        elif jeu=="CodeNames":
            return
            message=await ctx.send(embed=createEmbed("Code Names","Le jeu se joue en 2v2 !\nIl y a deux équipes : l'équipe rouge et l'équipe bleue. Chaque équipe se compose d'un **maître du jeu** et d'un **devineur**. L'attribution des rôles se fait manuellement au tout début de la partie.\nIl va apparaitre un plateau dans le salon avec **25 mots**. Le but du maitre du jeu est de **faire deviner les 8 (ou 9) mots de son équipe à son équipier**. Pour cela, il va recevoir en messages privé le même plateau avec **indiqué à quelle équipe il appartient** : rouge, bleu, mot interdit ou neutre.\nLe MJ aura une minute pour **trouver un lien** entre plusieurs de ses mots, **sous forme d'un indice (un mot)** et le **nombre de mots associés**. Une fois fait, il l'envoie en message privé au bot, et il est restranscrit de le salon du jeu.\nLe devineur a alors **une minute et 30 secondes pour trouver les mots**, puis doit les donner un par un. Si le mot **appartient bien à son équipe, il continue**. Sinon le tour passe à l'autre équipe.\nL'équipe qui fait deviner tous ses mots en premier gagne !\n**Attention : ** si un devineur prononce le mot interdit, c'est une défaite !\n\nCeci est un jeu basé sur la confiance. Ne trichez pas !\n***Ce jeu est aussi en TEST et doit être AMÉLIORÉ.***\n\nAppuyez sur la réaction <:otVALIDER:772766033996021761> pour rejoindre la partie et <:otANNULER:811242376625782785> pour annuler votre participation.\nLa partie se lancera automatiquement quand assez de joueurs auront rejoint, sinon au bout de 1 minute elle sera annulée.",0xad917b,ctx.invoked_with.lower(),ctx.guild))
            game=JeuCodeNames(message,ctx.author.id)

        game.addPlayer(ctx.author,message)
        inGame.append(ctx.author.id)
        dictJeux[message.id]=game

        await message.add_reaction("<:otVALIDER:772766033996021761>")
        await message.add_reaction("<:otANNULER:811242376625782785>")

        if len(game.guilds)>1:
            for mess in game.messages:
                if mess.id==message.id:
                    await mess.channel.send("<:otVERT:868535645897912330> Vous avez rejoint une partie ! Il y a {0} joueurs en attente.".format(len(game.ids)))
                else:
                    await mess.channel.send("<:otVERT:868535645897912330> Un joueur a rejoint en cross serveur !")
            if len(game.ids)==dictMax[jeu]:
                game.playing=True
            return
        elif cross:
            listeCross.append(game)
            """annonce=await bot.get_channel(878254347459366952).send("<:otVERT:868535645897912330> Partie de {0} Cross en recherche de joueurs !\n Faites OT!{1}cross pour rejoindre !".format(jeu,jeu.lower()))
            await annonce.publish()"""

        for i in range(60):
            if not game.playing:
                await asyncio.sleep(1)
            else:
                break
        
        if cross:
            listeCross.remove(game)
            #await annonce.edit(content="~~{0}~~\nRecherche terminée.".format(annonce.content))
        if not await game.startGame(inGame,emotes,mini):
            del dictJeux[message.id]
            return

        messAd=await bot.get_channel(870598360296488980).send("{0} - {1} : partie {2} débutée\n{3} joueurs".format(ctx.guild.name,ctx.guild.id,jeu,len(game.ids)))

        await game.boucle(bot)

    """except AssertionError as er:
        await embedAssert(ctx,er,True)
        return
    except:
        await exeErrorExcept(ctx,bot,True)"""
    
    if "messAd" in locals():
        await messAd.delete()
    
    for i in game.ids:
        inGame.remove(i)

    del dictJeux[message.id]


def createGame(cross,jeu,ctx,message):
    games=list(filter(lambda x:type(x)==jeu and ctx.guild.id not in x.guilds, listeCross))
    if not cross or games==[]:
        if jeu==JeuTrivialVersus:
            return jeu(message,ctx.author.id,"Versus",cross)
        elif jeu==JeuTortues:
            return jeu(message,ctx.author.id,"Tortues",cross)
        return jeu(message,ctx.author.id,cross)
    else:
        games[0].messages.append(message)
        games[0].guilds.append(message.guild.id)
        return games[0]