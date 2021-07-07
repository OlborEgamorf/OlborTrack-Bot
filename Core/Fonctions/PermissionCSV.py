### OBSOLETE, BIENTOT PLUS UTILISE MAIS QUAND MEME LA POUR LE MOMENT
from Core.Fonctions.EcritureRecherche3 import rechercheCsv

def checkperms(guild,numb):
    tablePerms=rechercheCsv("perms",guild,0,0,0,0)[0]
    assert tablePerms[numb]["Statut"]=="True", "Le module de stats lié à cette commande est désactivé sur ce serveur."
    return
#####