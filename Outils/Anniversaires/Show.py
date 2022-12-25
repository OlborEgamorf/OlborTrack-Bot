from Core.Decorator import OTCommand
from Core.Fonctions.Embeds import createEmbed
from Stats.SQL.ConnectSQL import connectSQL


@OTCommand
async def showAnniversaire(interaction,bot,user,ephem):
    connexion,curseur=connectSQL("OT")

    if user!=None:
        userAnniv=curseur.execute("SELECT * FROM anniversaires WHERE ID={0}".format(user.id)).fetchone()
        assert userAnniv!=None, "Cette personne n'a pas ajouté son anniversaire."
        embed=createEmbed("Anniversaire","L'anniversaire de <@{0}> est le **{1} {2}** !".format(user.id,userAnniv["Jour"],userAnniv["Mois"]),user.color.value,interaction.command.qualified_name,user)
    else:
        userAnniv=curseur.execute("SELECT * FROM anniversaires WHERE ID={0}".format(interaction.user.id)).fetchone()
        assert userAnniv!=None, "Vous n'avez pas ajouté votre anniversaire. Vous pouvez le faire avec la commande `/anniversaire set`"
        embed=createEmbed("Anniversaire","Vous avez affirmé que votre anniversaire est le **{0} {1}** !".format(userAnniv["Jour"],userAnniv["Mois"]),interaction.user.color.value,interaction.command.qualified_name,interaction.user)

    await interaction.response.send_message(embed=embed,ephemeral=ephem)
