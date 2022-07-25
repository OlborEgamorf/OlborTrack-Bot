import discord
from Core.Decorator import OTCommand
from Core.Fonctions.Embeds import createEmbed
from Stats.GetData.GetData import newGetData


@OTCommand
async def exeGetData(interaction,bot):
    embed=createEmbed("GetData - Avertissement","La procédure Olbor Track GetData analyse tous les messages du serveur de tous les salons que le bot peut voir, pour générer toutes les tables de statistiques qui seront utilisées dans les commandes.\nLes messages des autres bots sont ignorés.\nAvant toute chose, il va supprimer toutes les données déjà récoltées, pour repartir sur de nouvelles bases. Vous ne pourrez exécuter aucune commande pendant.\nVous pouvez continuer à parler et gérer votre serveur pendant l'opération. Il est juste déconseillé de retirer des permissions au bot avant la fin. Les messages envoyés pendant ne sont pas comptés dans les statistiques.\nNe pensez pas que le bot a planté, si c'est le cas vous le verrez.\nPour lancer la procédure, cliquez sur le bouton ci-dessous.\nCe sera peut-être long.\nMerci me m'avoir lu.",0x220cc9,"getdata",interaction.guild)
    await interaction.response.send_message(embed=embed,view=ViewGetData())


class ViewGetData(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=60)
    
    @discord.ui.button(label="Démarrer",emoji="<:otOUI:726840394150707282>",style=discord.ButtonStyle.blurple, custom_id="ot:getdatastart")
    async def start(self,interaction:discord.Interaction, button:discord.ui.Button):
        try:
            assert interaction.user.guild_permissions.administrator
            await interaction.response.edit_message(view=None,embed=createEmbed("Enclenchement...","GetData va débuter...",0x220cc9,"getdata",interaction.client.user))

            interaction.client.loop.create_task(newGetData(interaction.guild,interaction.channel,interaction.client,interaction.client.dictGuilds[interaction.guild_id]))

        except AssertionError:
            pass 
        except discord.Forbidden:
            pass
