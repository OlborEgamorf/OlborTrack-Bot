from Core.Fonctions.Embeds import embedAssert, exeErrorExcept
from discord.ext import commands
from Stats.SQL.ConnectSQL import connectSQL

from Outils.CustomCMD.ModifCustom import *


async def exeSCMD(ctx:commands.Context,bot:commands.Bot,args:str,listeOS:list):
    """Cette fonction gère la création, la modification et la suppression de commandes custom.
    
    Elle regarde les différents arguments donnés pour savoir quoi faire.
    
    Tout est stocké dans la base de données du serveur."""
    try:
        connexion,curseur=connectSQL(ctx.guild.id,"CustomCMD","Guild",None,None)
        args=args.split(" ")
        assert len(args)!=0, "Il faut le nom de la commande !"
        nom=args[0].lower().split(" ")
        if nom[0].startswith("ot!"):
            nom=nom[0][3:len(nom[0])]
        else:
            nom=nom[0]
        assert nom!="", "Il faut le nom de la commande !"
        assert nom not in listeOS, "Cette commande est une commande système !"
        command=curseur.execute("SELECT * FROM custom WHERE Nom='{0}'".format(nom)).fetchone()

        if ctx.invoked_with not in ("add","+"):
            assert command!=None, "Cette commande perso n'existe pas !"
        if ctx.invoked_with in ("image","miniature"):
            assert len(args)!=1 or len(ctx.message.attachments)>0 , "Pour définir une image ou une miniature :\nMettez un lien vers une image à la suite de cette commande ou alors ajoutez une image en pièce jointe (avec la commande).\nPour la supprimer, mettez *del* à la suite de la commande."
        elif ctx.invoked_with not in ("del","embed","len","delete","-"):
            assert len(args)!=1, "Il manque le contenu que vous voulez ajouter/modifier !"
        if ctx.invoked_with in ("auteur","titre","description","bas","image","miniature","couleur") and bool(command["Embed"])==False:
            await ctx.send(embed=await embedCCMD(ctx,nom,command,curseur))
        
        if ctx.invoked_with in ("add","+"):
            embed=await addCCMD(ctx,args,nom,command,curseur)
        elif ctx.invoked_with in ("del","delete","-"):
            embed=await delCCMD(ctx,nom,curseur)
        elif ctx.invoked_with in ("edit","description"):
            embed=await editCCMD(ctx,args,nom,curseur)
        elif ctx.invoked_with=="help":
            embed=await helpCCMD(ctx,args,nom,curseur)
        elif ctx.invoked_with=="embed":
            embed=await embedCCMD(ctx,nom,command,curseur)
        elif ctx.invoked_with=="auteur":
            embed=await authorCCMD(ctx,args,nom,curseur)
        elif ctx.invoked_with=="titre":
            embed=await titleCCMD(ctx,args,nom,curseur)
        elif ctx.invoked_with=="bas":
            embed=await footerCCMD(ctx,args,nom,curseur)
        elif ctx.invoked_with=="image":
            embed=await imageCCMD(ctx,args,nom,curseur,"Image")
        elif ctx.invoked_with=="miniature":
            embed=await imageCCMD(ctx,args,nom,curseur,"Miniature")
        elif ctx.invoked_with=="couleur":
            embed=await colorCCMD(ctx,args,nom,curseur)
        elif ctx.invoked_with=="len":
            embed=createEmbed("Longueur de la commande","Nom : {0}\nLongueur : {1}".format(nom,len(command["Description"])+len(command["Footer"])+len(command["Author"])+len(command["Title"])),0x220cc9,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)
        else:
            raise AssertionError("Rien ne correspond à votre demande !")

        command=curseur.execute("SELECT * FROM custom WHERE Nom='{0}'".format(nom)).fetchone()
        if command!=None:
            assert len(command["Description"])+len(command["Footer"])+len(command["Author"])+len(command["Title"])<5000, "La commande que vous avez créé ou modifié dépasse la limite de caractères maximale. La limite de Discord est de 6000, mais par mesure de sécurité elle est à 5000 pour moi."

        connexion.commit()
    except AssertionError as er:
        embed=embedAssert(str(er)) 
    except:
        embed=await exeErrorExcept(ctx,bot,args)
    await ctx.send(embed=embed)