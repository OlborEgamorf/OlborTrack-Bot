from Core.Decorator import OTCommand
from Core.Fonctions.Embeds import createEmbed
from Core.Fonctions.GetPeriod import getAnnee, getMois
from Stats.SQL.ConnectSQL import connectSQL

dictMax={"janvier":31,"février":29,"mars":31,"avril":30,"mai":31,"juin":30,"juillet":31,"aout":31,"septembre":30,"octobre":31,"novembre":30,"décembre":31}

@OTCommand
async def setAnniversaire(ctx,bot,args):
    connexion,curseur=connectSQL("OT","Guild","Guild",None,None)
    user=curseur.execute("SELECT * FROM anniversaires WHERE ID={0}".format(ctx.author.id)).fetchone()
    if user==None or user["Nombre"]!=0:
        print(args)
        if len(args)==1:
            assert "/" in args[0]
            args=args[0].split("/")
        elif len(args)==2:
            pass
        else:
            raise AssertionError("Il y a eu une erreur dans l'entrée de la date.")
        try:
            jour,mois=getAnnee(args[0].lower()),getMois(args[1].lower())
        except:
            raise AssertionError("Il y a eu une erreur dans l'entrée de la date.")
        assert mois!=None, "Le mois n'a pas été reconnu."
        assert jour<=dictMax[mois], "Le jour donné n'est pas possible dans le calendrier !"
        if user==None:
            curseur.execute("INSERT INTO anniversaires VALUES({0},{1},'{2}',3)".format(ctx.author.id,jour,mois))
            embed=createEmbed("Ajout d'anniversaire","Anniversaire ajouté ! Un message sera envoyé dans les serveurs où vous êtes et qui ont activé la fonctionnalité tous les **{0} {1}** !\nVous pouvez le changer 3 fois.".format(jour,mois),0x11f738,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.author)
        else:
            curseur.execute("UPDATE anniversaires SET Jour={0}, Mois='{1}', Nombre=Nombre-1 WHERE ID={2}".format(jour,mois,ctx.author.id))
            embed=createEmbed("Mise à jour d'anniversaire","Anniversaire mis à jour ! Un message sera envoyé dans les serveurs où vous êtes et qui ont activé la fonctionnalité tous les **{0} {1}** !\nVous pouvez le changer encore {2} fois.".format(jour,mois,user["Nombre"]-1),0x11f738,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.author)
    else:
        raise AssertionError("Vous avez trop mis à jour votre anniversaire !")
    connexion.commit()

    await ctx.reply(embed=embed)
