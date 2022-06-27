import discord
import sqlite3
from Core.Fonctions.Embeds import embedAssert

async def sendView(interaction:discord.Interaction,embed:discord.Embed,curseurCMD:sqlite3.Cursor,connexionCMD:sqlite3.Connection,page:int,pagemax:int) -> (discord.Message or None):
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
        await interaction.response.edit_message(embed=embed)
        curseurCMD.execute("UPDATE commandes SET Page={0}, PageMax={1} WHERE MessageID={2}".format(page,pagemax,interaction.message.interaction.id))
        connexionCMD.commit()
    except discord.errors.Forbidden:
        await embedAssert(interaction,"Je n'ai pas pu envoyer les réactions de cette commande, qui servent à naviguer dedans. Donnez moi les permissions 'utiliser emojis externes' et 'ajouter des réactions' si vous ne voulez plus voir ce message, et profiter à fond de mes possibilités.",True)