from Core.Fonctions.Embeds import embedAssert, exeErrorExcept
from discord.ext import commands
from Stats.SQL.ConnectSQL import connectSQL

from CustomCMD.ModifCustom import *


async def exeSCMD(ctx:commands.Context,bot:commands.Bot,args:str,listeOS:list):
    """Cette fonction gère la création, la modification et la suppression de commandes custom.
    
    Elle regarde les différents arguments donnés pour savoir quoi faire.
    
    Tout est stocké dans la base de données du serveur."""
    try:
        connexion,curseur=connectSQL(ctx.guild.id,"CustomCMD","Guild",None,None)
        args=args.split(" ")
        assert len(args)!=0, "Il faut le nom de la commande et ce que vous voulez en faire !"
        assert len(args)!=1, "Il faut le nom de la commande !"
        nom=args[1].lower().split(" ")
        if nom[0].startswith("ot!"):
            nom=nom[0][3:len(nom[0])]
        else:
            nom=nom[0]
        assert nom!="", "Il faut le nom de la commande !"
        assert nom not in listeOS, "Cette commande est une commande système !"
        command=curseur.execute("SELECT * FROM custom WHERE Nom='{0}'".format(nom)).fetchone()

        if args[0].lower()!="add":
            assert command!=None, "Cette commande perso n'existe pas !"
        if args[0].lower() in ("image","miniature"):
            assert len(args)!=2 or len(ctx.message.attachments)>0 , "Pour définir une image ou une miniature :\nMettez un lien vers une image à la suite de cette commande ou alors ajoutez une image en pièce jointe (avec la commande).\nPour la supprimer, mettez *del* à la suite de la commande."
        elif args[0].lower() not in ("del","embed","len"):
            assert len(args)!=2, "Il manque le contenu que vous voulez ajouter/modifier !"
        if args[0].lower() in ("auteur","titre","description","bas","image","miniature","couleur") and bool(command["Embed"])==False:
            await ctx.send(embed=await embedCCMD(ctx,nom,command,curseur))
        
        if args[0].lower()=="add" or args[0].lower()=="+":
            embed=await addCCMD(ctx,args,nom,command,curseur)
        elif args[0].lower()=="del" or args[0].lower()=="delete" or args[0].lower()=="-":
            embed=await delCCMD(ctx,nom,curseur)
        elif args[0].lower()=="edit" or args[0].lower()=="description":
            embed=await editCCMD(ctx,args,nom,curseur)
        elif args[0].lower()=="help":
            embed=await helpCCMD(ctx,args,nom,curseur)
        elif args[0].lower()=="embed":
            embed=await embedCCMD(ctx,nom,command,curseur)
        elif args[0].lower()=="auteur":
            embed=await authorCCMD(ctx,args,nom,curseur)
        elif args[0].lower()=="titre":
            embed=await titleCCMD(ctx,args,nom,curseur)
        elif args[0].lower()=="bas":
            embed=await footerCCMD(ctx,args,nom,curseur)
        elif args[0].lower()=="image":
            embed=await imageCCMD(ctx,args,nom,curseur,"Image")
        elif args[0].lower()=="miniature":
            embed=await imageCCMD(ctx,args,nom,curseur,"Miniature")
        elif args[0].lower()=="couleur":
            embed=await colorCCMD(ctx,args,nom,curseur)
        elif args[0].lower()=="len":
            embed=createEmbed("Longueur de la commande","Nom : {0}\nLongueur : {1}".format(nom,len(command["Description"])+len(command["Footer"])+len(command["Author"])+len(command["Title"])),0x220cc9,ctx.invoked_with.lower(),ctx.guild)
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
