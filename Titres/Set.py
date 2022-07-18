from Core.Fonctions.Embeds import createEmbed
from Core.Decorator import OTCommand
from Stats.SQL.ConnectSQL import connectSQL


@OTCommand
async def setTitre(interaction,bot,idtitre):
    connexion,curseur=connectSQL("OT","Titres","Titres",None,None)
    connexionUser,curseurUser=connectSQL("OT",interaction.user.id,"Titres",None,None)

    titre=curseurUser.execute("SELECT * FROM titresUser WHERE ID={0}".format(idtitre)).fetchone()
    assert titre!=None, "Vous ne possèdez pas ce titre."
    if curseur.execute("SELECT * FROM active WHERE MembreID={0}".format(interaction.user.id)).fetchone()==None:
        curseur.execute("INSERT INTO active VALUES({0},{1})".format(idtitre,interaction.user.id))
    else:
        curseur.execute("UPDATE active SET TitreID={0} WHERE MembreID={1}".format(idtitre,interaction.user.id))

    connexion.commit()

    embed=createEmbed("Titre équipé","Titre équipé avec succès !\nVotre nouveau titre est maintenant : **{0}**.".format(titre["Nom"]),0xf58d1d,interaction.command.qualified_name,interaction.user)
    await interaction.response.send_message(embed=embed)
