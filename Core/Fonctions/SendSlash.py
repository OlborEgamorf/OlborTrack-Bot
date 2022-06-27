import sqlite3

import discord
from Core.Fonctions.Embeds import embedAssert
from Core.Reactions.exeReactions import ViewControls


async def sendSlash(interaction:discord.Interaction,embed:discord.Embed,curseurCMD:sqlite3.Cursor,connexionCMD:sqlite3.Connection,page:int,pagemax:int,customView=None) -> (discord.Message or None):
    """Fonction qui envoie et modifie les embeds des commandes nécessitants des boutons. Elle permet aussi de mettre à jour la base de données des commandes du serveur d'où provient la commande, notamment quelle est la page actuelle et quel est le nombre de pages maximal.
    Entrées : 
        ctx : contexte de la commande
        embed : embed à envoyer
        react : s'il faut éditer ou envoyer le message
        boutons : s'il faut réagir avec les boutons spéciaux
        curseurCMD, connexionCMD : connexion à la base de données des commandes du serveur
        page : page actuelle
        pagemax : page maximale
    Sortie :
        Si react==True : rien, sinon le message envoyé."""

    try:
        if customView!=None:
            await interaction.response.send_message(embed=embed,view=customView)
        elif pagemax==1:
            await interaction.response.send_message(embed=embed,view=ViewControls(gauche=False,droite=False,page=False))
        else:
            await interaction.response.send_message(embed=embed,view=ViewControls())
        curseurCMD.execute("UPDATE commandes SET Page={0}, PageMax={1} WHERE MessageID={2}".format(page,pagemax,interaction.id))
        connexionCMD.commit()
    except discord.errors.Forbidden:
        await embedAssert(interaction,"Je n'ai pas pu envoyer les réactions de cette commande, qui servent à naviguer dedans. Donnez moi les permissions 'utiliser emojis externes' et 'ajouter des réactions' si vous ne voulez plus voir ce message, et profiter à fond de mes possibilités.",True)
