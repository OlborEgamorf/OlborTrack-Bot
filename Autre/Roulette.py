from random import choice

from Core.Fonctions.Embeds import createEmbed
from Core.Decorator import OTCommand

@OTCommand
async def exeRoulette(interaction,bot,propositions):
    """Cette fonction permet d'exécuter une roulette, qui choisit de manière aléatoire une proposition parmi plusieurs.
    
    En argument avec la commande est donné les propositions."""
    await interaction.response.send_message(embed=createEmbed("Roulette !",choice(propositions),0x2ba195,interaction.command.name,interaction.user))
