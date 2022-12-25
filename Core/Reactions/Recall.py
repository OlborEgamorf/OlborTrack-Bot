from Autre.ViHelp import commandeHelpView
from Savezvous.ListModoView import svPersoModoView
from Stats.Commandes.Slash.Classements import statsRank
from Stats.Commandes.Slash.Periods import statsPeriods
from Stats.Commandes.View.ViJeux import statsJeuxView
from Stats.Commandes.Slash.PeriodsInter import statsPeriodsInter
from Stats.Commandes.View.ViPerso import statsPersoView
from Stats.Commandes.View.ViRapports import changePage
from Stats.Commandes.View.ViRapportsUser import changePageUser
from Stats.Commandes.View.ViTrivial import statsTrivialView
from Stats.Commandes.View.ViTrivialPerso import statsTrivialPersoView
from Titres.ViListesTitres import listesTitresView


def getFunction(command):
    if command=="rank":
        return statsRank
    if command=="periods":
        return statsPeriods
    if command=="periodsInter":
        return statsPeriodsInter
    if command=="perso":
        return statsPersoView
    if command=="jeux":
        return statsJeuxView
    if command=="trivialrank":
        return statsTrivialView
    if command=="trivialperso":
        return statsTrivialPersoView
    if command=="help":
        return commandeHelpView


async def recall(interaction,ligne,curseur,connexion):
    sens=None
    if ligne["Commande"] in ("rank","periods","periodsInter","perso","jeux","trivialrank","trivialperso","help"):
        embed=await getFunction(ligne["Commande"])(interaction.message.interaction.id,interaction,interaction.client,interaction.client.dictGuilds[interaction.guild_id],curseur,ligne)
    elif ligne["Commande"]=="rapport":
        await changePage(interaction,connexion,curseur,sens,ligne,interaction.client.dictGuilds[interaction.guild_id],interaction.client)
    elif ligne["Commande"]=="rapportUser":
        await changePageUser(interaction,connexion,curseur,sens,ligne,interaction.client.dictGuilds[interaction.guild_id],interaction.client)
    elif ligne["Commande"]=="savezvous":
        await svPersoModoView(interaction,interaction.client,ligne,curseur,connexion,sens)
    elif ligne["Commande"]=="titres":
        await listesTitresView(interaction,ligne,connexion,curseur,sens)
    await interaction.response.edit_message(embed=embed)