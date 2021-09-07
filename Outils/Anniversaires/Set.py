from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.GetPeriod import getAnnee, getMois
from Core.Fonctions.Embeds import createEmbed, embedAssert

async def setAnniversaire(ctx,bot,args):
    try:
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
            jour,mois=getAnnee(args[0].lower()),getMois(args[1].lower())
            assert mois!=None, "Le mois n'a pas été reconnu."
            if user==None:
                curseur.execute("INSERT INTO anniversaires VALUES({0},{1},'{2}',3)".format(ctx.author.id,jour,mois))
                embed=createEmbed("Ajout d'anniversaire","Anniversaire ajouté ! Un message sera envoyé dans les serveurs où vous êtes et qui ont activé la fonctionnalité tous les {0} {1} !\nVous pouvez le changer 3 fois.".format(jour,mois),0xf54269,ctx.invoked_with.lower(),ctx.author)
            else:
                curseur.execute("UPDATE anniversaires SET Jour={0}, Mois='{1}', Nombre=Nombre-1 WHERE ID={2}".format(jour,mois,ctx.author.id))
                embed=createEmbed("Mise à jour d'anniversaire","Anniversaire mis à jour ! Un message sera envoyé dans les serveurs où vous êtes et qui ont activé la fonctionnalité tous les {0} {1} !\nVous pouvez le changer encore {2} fois.".format(jour,mois,user["Nombre"]-1),0xf54269,ctx.invoked_with.lower(),ctx.author)
        else:
            raise AssertionError("Vous avez trop mis à jour votre anniversaire !")
        connexion.commit()

        await ctx.reply(embed=embed)
    except AssertionError as er:
        await ctx.reply(embed=embedAssert(er))
    except:
        await ctx.reply(embed=embedAssert("Il y a eu une erreur dans l'entrée de la date."))