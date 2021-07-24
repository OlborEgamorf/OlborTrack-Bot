### A METTRE A JOUR

import discord
from Core.Fonctions.AuteurIcon import auteur

async def exeUtile(ctx,bot,option):
    """Cette fonction envoie les textes des commandes utilitaires du bot"""
    if option=="about":
        embedF=discord.Embed(title="A propos", description="Olbor Track est un bot discord français et fait maison par mes soins sur mon temps libre depuis le 15 avril 2020. Sa principale fonction était de donner des statistiques sur l'activité d'un serveur, et de ses membres.\nDepuis, il s'est étoffé de nombreuses fonctionnalités : jeux, outils et plus.\nToutes les données récoltées par le bot ne sortent pas de votre serveur et de la base de donnée du bot. Personne ne peut y accèder à part vous, et sur votre demande.\nEn cas de problème, n'hésitez pas à rejoindre le serveur de support.\nSi vous appréciez le projet, vous pouvez regarder comment le soutenir avec la commande OT!support.\nBeaucoup reste à venir...\n**Merci infiniment de l'avoir ajouté.**\n\nOlborEgamorf.",color=ctx.author.color)
    elif option=="invite":
        embedF=discord.Embed(title="Liens d'invitation : ", description="Invitation avec les permissions nécessaires : https://discord.com/api/oauth2/authorize?client_id=699728606493933650&permissions=912582&scope=bot \nInvitation avec la permission administrateur (conseillé) : https://discord.com/api/oauth2/authorize?client_id=699728606493933650&permissions=8&scope=bot", color=0xfcfc03)
    elif option=="test":
        embedF=discord.Embed(title="Serveur d'aide : ", description="https://discord.gg/kMQz7nF \nVous pouvez y proposer des idées, voir les annonces de mise à jour ou rapporter des erreurs du bot.", color=0xfcfc03)
    elif option=="support":
        embedF=discord.Embed(title="Me soutenir : ", description="**Comment soutenir OlborTrack :** \n- [Inviter le bot sur votre serveur](https://bit.ly/OlborTrack) \n- [Partager ce tweet](https://twitter.com/OlborEgamorf/status/1302003450964783105?s=20)\n- [Partager ce post Instagram](https://www.instagram.com/p/CEwGXbjC1r5/?utm_source=ig_web_button_share_sheet)\n- [Faire une donnation](https://paypal.me/OlborTrack) (OlborTrack me coute 6$ par mois et ne me rapporte rien. Si vous souhaitez participer n'hésitez pas !)\n- [Rejoindre le serveur de test pour proposer des idées](https://discord.gg/kMQz7nF)",color=0xfcfc03)
    elif option=="credit":
        embedF=discord.Embed(title="Crédits",description="**Créateur :** OlborEgamorf\n**Contributeurs :** Tonton Mathias, Zeynah, ZAGUE, Lexadi, Souaip\n**Donateurs :** Alfashield, NatG34\n**Bibliothèques Python :** discord.py, asyncio, aiohttp, wikiquote, wikipediaapi, shutil, matplotlib, pandas, seaborn, geoplot, geopandas, colorthief, circlify et rule34\n**APIs :** Spotify API, NASA API, Open Notify, Open Cage Data, Jikan, Wikipedia, On This Day\n**Meilleur supporter :** vous <:otLove2:768456004991057951>\n[Contribuez en rejoignant le serveur de tests et en donnant des idées](https://discord.gg/kMQz7nF) - [Devenez un donateur](https://paypal.me/OlborTrack)", color=0xfcfc03)
    elif option=="reseaux":
        embedF=discord.Embed(title="Réseaux sociaux",description="**Twitter** : https://twitter.com/OlborTrack\n **Instagram** : https://www.instagram.com/OlborTrack \nCes comptes servent à donner les mises à jours et contenus à venir du bot ! [Rejoindre le serveur de test](https://discord.com/invite/kMQz7nF) permet aussi d'avoir ces informations, en plus détaillé.",color=0xfcfc03)
    embedF.set_footer(text="OT!"+option)
    embedF=auteur(bot.user,0,0,embedF,"olbor")
    
    embedF.set_thumbnail(url=bot.user.avatar_url)
    await ctx.send(embed=embedF)
    return