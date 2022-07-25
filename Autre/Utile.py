import discord
from Core.Fonctions.Embeds import createEmbed

async def exeUtile(interaction,bot):
    """Cette fonction envoie les textes des commandes utilitaires du bot"""
    if interaction.command.name=="about":
        embed=createEmbed("A propos","Olbor Track est un bot Discord français créé le 15 avril 2020 par OlborEgamorf. Son but premier était de fournir des statistiques d'activité sur les serveurs, avant de s'améliorer vers d'autres fonctionnalités : sondages, jeux et outils.\nLe premier tournant du bot fut la version 3.0, renovant toute son infrastructure et ses commandes, pour founir une expérience utilisateur plus qu'améliorée.\nDésormais il possède son site internet et son Companion, permettant de le configurer et de consulter de manière optimale les statistiques, tout en offrant de meilleures analyses.\nOT a obtenu sa vérification par Discord le 7 décembre 2021.\n\nToutes les statistiques stockées sont anonymes, et accessibles seulement par les membres de votre serveur. Elles sont modulables : vous pouvez les désactiver, bloquer des salons, et même toutes les supprimer si vous le souhaitez.\n\n**Merci beaucoup d'utiliser Olbor Track et de le faire grandir par votre soutien.**",0xfcfc03,interaction.command.name,bot.user)
        embed.add_field(name="Contributeurs",value="Tonton Mathias, Zey, ZAGUE, Lexadi, Souaip")
        embed.add_field(name="Donateurs",value="Alfashield, NatG34, Zey")
        embed.add_field(name="Badges <:DiamantGlobal:886707210560884778>",value="[Shimi](https://twitter.com/ShimiGazelle)")
        embed.add_field(name="Testeurs",value="Lexadi, Pingouin, Shimi, Brief, Souaip, ZAGUE, Zey, Tonton Mathias, Stevii, Diow, diopt_ase, Rivyss, Degre_")

    elif interaction.command.name=="invite":
        embed=createEmbed("Liens d'invitation","Invitation avec les permissions nécessaires : https://discord.com/oauth2/authorize?client_id=699728606493933650&permissions=328582163536&scope=bot \nInvitation avec la permission administrateur : https://discord.com/api/oauth2/authorize?client_id=699728606493933650&permissions=8&scope=bot\n\n*Retirer une des permissions nécessaire pourrait empêcher le bot de faire certaines actions et commandes, donc faites bien attention !*",0xfcfc03,interaction.command.name,bot.user)

    elif interaction.command.name=="support":
        embed=createEmbed("Me soutenir","",0xfcfc03,interaction.command.name,bot.user)
        embed.add_field(name="Meilleur soutien : ajoutez Olbor Track sur votre serveur",value="[Faites-le !](https://discord.com/oauth2/authorize?client_id=699728606493933650&permissions=328582163536&scope=bot)",inline=False)
        embed.add_field(name="Réseaux sociaux",value="[Serveur de support](https://discord.gg/kMQz7nF)\n[Twitter](https://twitter.com/OlborTrack)\n[Instagram](https://www.instagram.com/OlborTrack)")
        embed.add_field(name="Contribuez",value="[Sur GitHub](https://github.com/OlborEgamorf/OlborTrack-Bot)\n[Par une donation PayPal](https://paypal.me/OlborTrack)\n[Par Patreon](https://patreon.com/OlborTrack)")
        embed.add_field(name="Listes de bots",value="[Top.gg](https://top.gg/bot/699728606493933650)\n[DiscordBotList.com](https://discordbotlist.com/bots/olbor-track)")

    elif interaction.command.name=="servcount":
        embed=createEmbed("Nombre de serveurs","Je suis présent dans **{0}** serveurs actuellement !\nAidez-moi à grandir en m'invitant sur d'autres serveurs ! [(En cliquant ici par exemple...)](https://discord.com/oauth2/authorize?client_id=699728606493933650&permissions=328582163536&scope=bot)".format(len(bot.guilds)),0xfcfc03,interaction.command.name,bot.user)
    
    elif interaction.command.name=="companion":
        embed=createEmbed("Olbor Track Companion","+ d'infos en aout !",0xfcfc03,interaction.command.name,bot.user)
        embed.set_image(url="https://cdn.discordapp.com/attachments/702208752035692654/975873681525993522/OTC.png")

    embed.set_thumbnail(url=bot.user.display_avatar)
    await interaction.response.send_message(embed=embed)