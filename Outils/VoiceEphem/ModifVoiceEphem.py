from Core.Fonctions.GetNom import getAuthor
from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.Embeds import createEmbed
from Core.Fonctions.Phrase import createPhrase


async def voiceEphemAdd(ctx,curseur):
    chan=getAuthor("Voicechan",ctx,2)
    assert chan!=None, "Vous devez me donner un salon vocal valide !"
    assert curseur.execute("SELECT * FROM hub WHERE ID={0}".format(chan)).fetchone()==None, "Le salon <#{0}> est déjà un hub !".format(chan)
    num=curseur.execute("SELECT COUNT() as Nombre FROM hub").fetchone()["Nombre"]+1
    curseur.execute("INSERT INTO hub VALUES({0},{1},0)".format(num,chan))

    return createEmbed("Hub créé","Numéro du hub : {0}\nSalon : <#{1}>\nNombre limite d'utilisateurs : aucune\n".format(num,chan),0xf54269,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)


async def voiceEphemLimite(ctx,args,curseur):
    assert len(args)>=2, "Il manque des éléments pour modifier la limite d'utilisateur dans chaque salon ! Donnez moi dans l'ordre : le numéro du hub voulu et la nouvelle limite."
    try:
        hub=curseur.execute("SELECT * FROM hub WHERE Nombre={0}".format(args[0])).fetchone()
    except:
        raise AssertionError("Le numéro donné n'est pas valide.")
    assert hub!=None, "Le numéro donné ne correspond à aucun hub actif."
    assert hub["Limite"]!=args[1], "Le nombre d'utilisations donné est le même que celui actuel."

    curseur.execute("UPDATE hub SET Limite={0} WHERE Nombre={1}".format(args[1],hub["Nombre"]))
    return createEmbed("Limite modifiée","Numéro du hub : {0}\nNouveau nombre limite d'utilisateurs : {1}".format(args[0],args[1]),0xf54269,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)
    

async def voiceEphemDel(ctx,args,curseur):
    assert len(args)>=1, "Il manque le numéro du hub pour le supprimer !"
    try:
        hub=curseur.execute("SELECT * FROM hub WHERE Nombre={0}".format(args[0])).fetchone()
    except:
        raise AssertionError("Le numéro donné n'est pas valide.")
    assert hub!=None, "Le numéro donné ne correspond à aucun hub actif."

    curseur.execute("DELETE FROM hub WHERE Nombre={0}".format(args[0]))

    for i in curseur.execute("SELECT * FROM hub WHERE Nombre>{0} ORDER BY Nombre ASC".format(args[0])).fetchall():
        curseur.execute("UPDATE hub SET Nombre={0} WHERE Nombre={1}".format(i["Nombre"]-1,i["Nombre"]))

    return createEmbed("Hub supprimé","Numéro du hub : {0}".format(args[0]),0xf54269,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)


async def voiceEphemEdit(ctx,args,curseur):
    assert len(args)>=1, "Il manque le numéro du salon pour le modifier !"
    try:
        hub=curseur.execute("SELECT * FROM salons WHERE Nombre={0}".format(args[0])).fetchone()
    except:
        raise AssertionError("Le numéro donné n'est pas valide.")
    assert hub!=None, "Le numéro donné ne correspond à aucun salon pouvant exister."

    nom=createPhrase(args[1:])
    assert len(nom)<20, "Le nom du salon ne doit pas dépasser les 20 caractères !"

    curseur.execute("UPDATE salons SET Nom='{0}' WHERE Nombre={1}".format(nom,args[0]))

    return createEmbed("Nom de salon modifié","Numéro du salon : {0}\nNouveau nom du salon : {1}".format(args[0],nom),0xf54269,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)
