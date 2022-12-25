from Core.Decorator import OTCommand
from Core.Fonctions.Embeds import createEmbed
from Stats.SQL.ConnectSQL import connectSQL

dictMax={"janvier":31,"février":29,"mars":31,"avril":30,"mai":31,"juin":30,"juillet":31,"aout":31,"septembre":30,"octobre":31,"novembre":30,"décembre":31}

@OTCommand
async def setAnniversaire(interaction,bot,jour,mois):
    connexion,curseur=connectSQL("OT")
    user=curseur.execute("SELECT * FROM anniversaires WHERE ID={0}".format(interaction.user.id)).fetchone()
    
    if user==None or user["Nombre"]!=0:
        assert jour<=dictMax[mois.lower()], "Le jour donné n'est pas possible dans le calendrier !"
        if user==None:
            curseur.execute("INSERT INTO anniversaires VALUES({0},{1},'{2}',3)".format(interaction.user.id,jour,mois.lower()))
            embed=createEmbed("Ajout d'anniversaire","Anniversaire ajouté ! Un message sera envoyé dans les serveurs où vous êtes et qui ont activé la fonctionnalité tous les **{0} {1}** !\nVous pouvez le changer 3 fois.".format(jour,mois),0x11f738,interaction.command.qualified_name,interaction.user)
        else:
            curseur.execute("UPDATE anniversaires SET Jour={0}, Mois='{1}', Nombre=Nombre-1 WHERE ID={2}".format(jour,mois.lower(),interaction.user.id))
            embed=createEmbed("Mise à jour d'anniversaire","Anniversaire mis à jour ! Un message sera envoyé dans les serveurs où vous êtes et qui ont activé la fonctionnalité tous les **{0} {1}** !\nVous pouvez le changer encore {2} fois.".format(jour,mois,user["Nombre"]-1),0x11f738,interaction.command.qualified_name,interaction.user)
        connexion.commit()
    else:
        raise AssertionError("Vous avez trop mis à jour votre anniversaire !")
    
    await interaction.response.send_message(embed=embed)
