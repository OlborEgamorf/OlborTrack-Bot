import discord
from Core.Fonctions.Embeds import createEmbed

async def exeUtile(ctx,bot):
    """Cette fonction envoie les textes des commandes utilitaires du bot"""
    if ctx.invoked_with.lower()=="about":
        embed=createEmbed("A propos","Olbor Track est un bot discord français et fait maison par mes soins sur mon temps libre depuis le 15 avril 2020. Sa principale fonction était de donner des statistiques sur l'activité d'un serveur, et de ses membres.\nDepuis, il s'est étoffé de nombreuses fonctionnalités : jeux, outils et plus.\nToutes les données récoltées par le bot ne sortent pas de votre serveur et de la base de donnée du bot. Personne ne peut y accèder à part vous, et sur votre demande.\nEn cas de problème, n'hésitez pas à rejoindre le serveur de support.\nSi vous appréciez le projet, vous pouvez regarder comment le soutenir avec la commande OT!support.\nBeaucoup reste à venir...\n**Merci infiniment de l'avoir ajouté.**\n\nOlborEgamorf.",0xfcfc03,ctx.invoked_with.lower(),bot.user)
    elif ctx.invoked_with.lower()=="invite":
        embed=createEmbed("Liens d'invitation","Invitation avec les permissions nécessaires : https://discord.com/oauth2/authorize?client_id=699728606493933650&permissions=120259472576&scope=bot \nInvitation avec la permission administrateur (conseillé) : https://discord.com/api/oauth2/authorize?client_id=699728606493933650&permissions=8&scope=bot",0xfcfc03,ctx.invoked_with.lower(),bot.user)
    elif ctx.invoked_with.lower()=="test":
        embed=createEmbed("Serveur d'aide","https://discord.gg/kMQz7nF \nVous pouvez y proposer des idées, voir les annonces de mise à jour ou rapporter des erreurs du bot.",0xfcfc03,ctx.invoked_with.lower())
    elif ctx.invoked_with.lower()=="support":
        embed=createEmbed("Me soutenir","**Comment soutenir OlborTrack :** \n- [Inviter le bot sur votre serveur](https://bit.ly/OlborTrack) \n- [Partager ce tweet](https://twitter.com/OlborEgamorf/status/1422473397573935104)\n- [Partager ce post Instagram](https://www.instagram.com/p/CSGtqCJAY6G)\n- [Faire une donnation](https://paypal.me/OlborTrack)\n- [Contribuer sur Patreon](https://patreon.com/OlborTrack)\n- [Rejoindre le serveur de test pour proposer des idées](https://discord.gg/kMQz7nF)\n- [Participez sur GitHub](https://github.com/OlborEgamorf/OlborTrack-Bot)",0xfcfc03,ctx.invoked_with.lower(),bot.user)
    elif ctx.invoked_with.lower()=="credits":
        embed=createEmbed("Crédits","**Créateur :** OlborEgamorf\n**Contributeurs :** Tonton Mathias, Zey, ZAGUE, Lexadi, Souaip\n**Donateurs :** Alfashield, NatG34, Zey\n**Badges <:DiamantGlobal:886707210560884778>** : [Shimi](https://twitter.com/ShimiGazelle)\n**Bibliothèques Python :** discord.py, asyncio, aiohttp, wikiquote, wikipediaapi, shutil, matplotlib, pandas, seaborn, geoplot, geopandas, colorthief, circlify, PIL et rule34\n**APIs :**  On This Day, Twitter API, YouTube API, Twitch API\n**Meilleur supporter :** vous <:otLove2:768456004991057951>\n[Contribuez en rejoignant le serveur de tests et en donnant des idées](https://discord.gg/kMQz7nF) - [Devenez un donateur](https://paypal.me/OlborTrack)",0xfcfc03,ctx.invoked_with.lower(),bot.user)
    elif ctx.invoked_with.lower()=="reseaux":
        embed=createEmbed("Réseaux sociaux","**Twitter** : https://twitter.com/OlborTrack\n **Instagram** : https://www.instagram.com/OlborTrack \nCes comptes servent à donner les mises à jours et contenus à venir du bot ! [Rejoindre le serveur de test](https://discord.com/invite/kMQz7nF) permet aussi d'avoir ces informations, en plus détaillé.",0xfcfc03,ctx.invoked_with.lower(),bot.user)
    elif ctx.invoked_with.lower()=="servcount":
        embed=createEmbed("Nombre de serveurs","Je suis présent dans **{0}** serveurs actuellement !\nAidez-moi à grandir en m'invitant sur d'autres serveurs ! (OT!invite)".format(len(bot.guilds)),0xfcfc03,ctx.invoked_with.lower(),bot.user)
    elif ctx.invoked_with.lower()=="botlists":
        embed=createEmbed("Olbor Track dans des listes de bots","Top.gg : https://top.gg/bot/699728606493933650 \nDiscord.Bots.gg : https://discord.bots.gg/bots/699728606493933650 \nDiscordBotList.com : https://discordbotlist.com/bots/olbor-track",0xfcfc03,ctx.invoked_with.lower(),bot.user)

    embed.set_thumbnail(url=bot.user.avatar_url)
    await ctx.send(embed=embed)