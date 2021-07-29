import sys

import discord
from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.Embeds import embedAssert
from Stats.SQL.ConnectSQL import connectSQL

async def exeCustom(guild:discord.Guild,message:discord.Message,author:discord.Member,listeOS:list):
    """Cette fonction est activée quand le préfixe 'OT!' est détecté dans un message. Elle vérifie si la commande demandée ensuite est une commande custom du serveur.
    
    Si oui, elle génère la commande avec tout ce qui a été paramétré."""
    try:
        mode="Initialisation"
        listeMots=message.content.split(" ")
        command=listeMots[0][3:len(listeMots[0])].lower()
        if command in listeOS:
            return False, 0
        connexion,curseur=connectSQL(guild.id,"CustomCMD","Guild",None,None)
        tableCommande=curseur.execute("SELECT * FROM custom WHERE Nom='{0}'".format(command)).fetchone()
        if tableCommande!=None:
            if bool(tableCommande["Embed"])==True:
                dictColor={"olbor":0x6ec8fa,"blue":0x3498db,"yellow":0xfcfc03,"orange":0xe0a31f,"green":0x14e330,"pink":0xed0ce2,"black":0x000000,"white":0xffffff,"violet":0x8f2aa1,"cyan":0x0ff2eb,"red":0xff0800,"turquoise":0x23b098,"dblue":0x220ce8,"dgreen":0x0c8733,"user":author.color.value}
                embedC=discord.Embed()
                embedC.colour=dictColor[tableCommande["Color"]]
                if tableCommande["Title"]!="None":
                    mode="embedTitle"
                    embedC.title=tableCommande["Title"]
                if tableCommande["Description"]!="None":
                    mode="embedDescription"
                    embedC.description=tableCommande["Description"]
                if tableCommande["Author"]!="None":
                    mode="embedAuthor"
                    if tableCommande["Author"]=="guild":
                        embedC=auteur(guild.id,guild.name,guild.icon,embedC,"guild")
                    elif tableCommande["Author"]=="user":
                        embedC=auteur(author.id,author.name,author.avatar,embedC,"user")
                    else:
                        try:
                            author=guild.get_member(int(tableCommande["Author"]))
                            embedC=auteur(author.id,author.name,author.avatar,embedC,"user")
                        except:
                            embedC.set_author(name=tableCommande["Author"])
                if tableCommande["Footer"]!="None":
                    mode="embedFooter"
                    embedC.set_footer(text=tableCommande["Footer"])
                if tableCommande["Image"]!="None":
                    mode="embedImage"
                    embedC.set_image(url=tableCommande["Image"])
                if tableCommande["Miniature"]!="None":
                    mode="embedThumbnail"
                    embedC.set_thumbnail(url=tableCommande["Miniature"])
                mode="Envoi vers Discord"
                await message.channel.send(embed=embedC)
            else:
                await message.channel.send(tableCommande["Description"])
    except:
        embedErr=embedAssert("Votre commande personnalisée présente une erreur qui m'empêche de l'envoyer : \nEmplacement : "+mode+"\nType : "+str(sys.exc_info()[0])) 
        await message.channel.send(embed=embedErr)