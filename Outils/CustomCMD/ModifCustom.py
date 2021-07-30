from Core.Fonctions.Embeds import createEmbed
from Core.Fonctions.Phrase import createPhrase

async def addCCMD(ctx,args,nom,command,curseur):
    """Ajoute une commande custom"""
    for i in nom:
        assert (ord(i)>=65 and ord(i)<=122) or (ord(i)>=48 and ord(i)<=57), "Le nom de la commande ne doit pas avoir de caractères spéciaux."
    assert command==None, "Cette commande existe déjà ! Pour la modifier, faites edit au lieu de add."
    quote=createPhrase(args[1:len(args)])
    curseur.execute("INSERT INTO custom VALUES('{0}','{1}',False,'None','None','olbor','OT!{0}','None','None')".format(nom,quote))
    curseur.execute("INSERT INTO help VALUES('{0}','*Pas de description*')".format(nom))
    return createEmbed("Commande ajoutée","Nom : {0}\nContenu : {1}".format(nom,quote),0xf54269,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)

async def delCCMD(ctx,nom,curseur):
    """Supprime une commande custom"""
    quote=curseur.execute("SELECT Description FROM custom WHERE Nom='{0}'".format(nom)).fetchone()["Description"]
    curseur.execute("DELETE FROM custom WHERE Nom='{0}'".format(nom))
    curseur.execute("DELETE FROM help WHERE Nom='{0}'".format(nom))
    return createEmbed("Commande supprimée","Nom : {0}\nContenu : {1}".format(nom,quote),0xf54269,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)

async def editCCMD(ctx,args,nom,curseur):
    """Edite le contenu d'une commande custom / modifie la description d'un embed custom"""
    quote=createPhrase(args[1:len(args)])
    curseur.execute("UPDATE custom SET Description='{0}' WHERE Nom='{1}'".format(quote,nom))
    return createEmbed("Commande modifiée","Nom : {0}\nNouveau contenu : {1}".format(nom,quote),0xf54269,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)

async def helpCCMD(ctx,args,nom,curseur):
    """Modifie le texte d'aide d'une commande custom"""
    if args[1].lower()=="del":
        quote="*Pas de description*"
    else:
        quote=createPhrase(args[1:len(args)])
    curseur.execute("UPDATE help SET Description='{0}' WHERE Nom='{1}'".format(quote,nom))
    return createEmbed("Contenu d'aide modifié","Commande : {0}\nDescription : {1}".format(nom,quote),0xf54269,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)

async def embedCCMD(ctx,nom,command,curseur):
    """Active ou désactive un embed custom pour une commande custom"""
    dictBool={False:"",True:"dés"}
    curseur.execute("UPDATE custom SET Embed={0} WHERE Nom='{1}'".format(bool(command["Embed"]-1),nom))
    return createEmbed("Embed {0}activé".format(dictBool[bool(command["Embed"])]),"Commande : {0}".format(nom),0xf54269,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)

async def authorCCMD(ctx,args,nom,curseur):
    """Change l'auteur pour un embed custom"""
    if args[1].lower()=="user" or args[1].lower()=="guild":
        author=args[1].lower()
    elif len(ctx.message.mentions)>0:
        author=ctx.message.mentions[0].id
    elif args[1].lower()=="del":
        author="None"
    else:
        author=createPhrase(args[1:len(args)])
    curseur.execute("UPDATE custom SET Author='{0}' WHERE Nom='{1}'".format(author,nom))
    return createEmbed("Auteur d'embed modifié","Commande : {0}\nAuteur : {1}".format(nom,author),0xf54269,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)

async def titleCCMD(ctx,args,nom,curseur):
    """Change le titre pour un embed custom"""
    if args[1]=="del":
        titre="None"
    else:
        titre=createPhrase(args[1:len(args)])
    curseur.execute("UPDATE custom SET Title='{0}' WHERE Nom='{1}'".format(titre,nom))
    return createEmbed("Titre d'embed modifié","Commande : {0}\nTitre : {1}".format(nom,titre),0xf54269,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)

async def footerCCMD(ctx,args,nom,curseur):
    """Change le pied de page pour un embed custom"""
    if args[1]=="del":
        footer="OT!{0}".format(nom)
    else:
        footer=createPhrase(args[1:len(args)])
    curseur.execute("UPDATE custom SET Footer='{0}' WHERE Nom='{1}'".format(footer,nom))
    return createEmbed("Bas d'embed modifié","Commande : {0}\nBas de page : {1}".format(nom,footer),0xf54269,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)

async def imageCCMD(ctx,args,nom,curseur,option):
    """Change l'image ou la miniature pour un embed custom"""
    if len(ctx.message.attachments)>0:
        lien=ctx.message.attachments[0].url
        assert ctx.message.attachments[0].url[len(lien)-4:len(lien)].lower()==".png" or ctx.message.attachments[0].url[len(lien)-4:len(lien)].lower()==".jpg" or ctx.message.attachments[0].url[len(lien)-4:len(lien)].lower()==".gif", "L'image donnée n'est pas dans un format valide (formats compatibles : PNG, JPG et GIF)."
        for i in range(len(ctx.message.attachments[0].url)):
            assert ctx.message.attachments[0].url[i]!="'", "Le nom de l'image contient une apostrophe, ce qui m'empêche de l'ajouter à la commande."
        image=lien
    else:
        if args[1]=="del":
            image="None"
        else:
            image=args[1]
    curseur.execute("UPDATE custom SET {0}='{1}' WHERE Nom='{2}'".format(option,image,nom))
    return createEmbed("{0} d'embed modifiée".format(option),"Commande : {0}\n{1} : {2}".format(nom,option,image),0xf54269,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)

async def colorCCMD(ctx,args,nom,curseur):
    """Change la couleur pour un embed custom"""
    listColor=["blue","yellow","orange","green","pink","black","white","violet","cyan","red","turquoise","dblue","dgreen","user","olbor"]
    assert args[1].lower() in listColor, "Cette couleur n'est pas disponible. Liste des couleurs : blue, yellow, orange, green, pink, black, white, violet, cyan, red, turquoise, dblue, dgreen, user ou olbor"
    curseur.execute("UPDATE custom SET Color='{0}' WHERE Nom='{1}'".format(args[1].lower(),nom))
    return createEmbed("Couleur d'embed modifiée","Commande : {0}\nCouleur : {1}".format(nom,args[1].lower()),0xf54269,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)