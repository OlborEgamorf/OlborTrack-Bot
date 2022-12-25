from time import strftime

import discord
from Core.Decorator import OTCommand
from Core.Fonctions.Embeds import createEmbed
from Core.Fonctions.Phrase import createPhrase
from discord.ext import commands
from Stats.SQL.ConnectSQL import connectSQL


@OTCommand
async def randomSV(interaction,bot):
    await interaction.response.send_message(embed=showSV(interaction.guild,bot,number=10))


def showSV(guild:discord.Guild,bot:commands.Bot,number=None) -> discord.Embed:
    """Fonction qui génère un Embed contenant une phrase venant de la boîte SavezVous d'un serveur donné. Fonctionne pour la commande normale et la commande automatique.
    Renvoie une erreur si la boîte est vide."""
    connexion,curseur=connectSQL(guild.id)
    
    if number==None:
        ligne=curseur.execute("SELECT * FROM savezvous ORDER BY RANDOM() ASC").fetchone()
    else:
        ligne=curseur.execute("SELECT * FROM savezvous WHERE Count={0}".format(number)).fetchone()
    assert ligne!=None, "Vous devez commencer par ajouter une phrase avec `OT!savezvous add` !"

    user=guild.get_member(ligne["ID"])
    if user==None:
        embed=createEmbed("","",guild.get_member(bot.user.id).color.value,"savezvous",bot.user)
    else:
        embed=createEmbed("","",user.color.value,"savezvous",user)

    embed.add_field(name="Savez-vous ?",value=ligne["Texte"],inline=False)
    
    if ligne["Image"]!="None":
        embed.set_image(url=ligne["Image"])
    
    embed.add_field(name="N°",value="`{0}`".format(ligne["Count"]),inline=True)

    updates=curseur.execute("SELECT * FROM svcomment WHERE Count={0} AND ID={1}".format(ligne["Count"],ligne["ID"])).fetchall()
    if updates!=[]:
        descip=""
        for i in updates:
            descip+="- {0} : {1}\n".format(i["Date"],i["Texte"])
        embed.add_field(name="Mises à jour de l'auteur",value=descip,inline=True)

    if ligne["Source"]!="None":
        embed.add_field(name="Source",value=ligne["Source"],inline=True)

    comment=curseur.execute("SELECT * FROM svcomment WHERE Count={0} AND ID<>{1} ORDER BY RANDOM() ASC".format(ligne["Count"],ligne["ID"])).fetchone()
    if comment!=None:
        user=guild.get_member(comment["ID"])
        if user==None:
            embed.add_field(name="Commentaire d'un ancien membre",value=comment["Texte"],inline=False)
        else:
            embed.add_field(name="Commentaire de {0}".format(user.nick or user.name),value=comment["Texte"],inline=False)

    return embed


@OTCommand
async def addSV(interaction,bot,phrase,source,image) -> None:
    """Fonction qui ajoute une phrase à la boîte SavezVous d'un serveur. Renvoie une erreur si la phrase contenue dans args est vide ou si la phrase dépasse les 2000 caractères."""
    connexion,curseur=connectSQL(interaction.guild_id)

    if image!=None:
        image=image.url

    descip=createPhrase(phrase)
    if source!=None:
        source=createPhrase(source)
    else:
        source="None"
    assert len(descip)+len(source)<2000, "Votre phrase est trop longue."
    count=curseur.execute("SELECT MAX(Count) AS Max FROM savezvous").fetchone()
    if count==None:
        count=0
    else:
        count=count["Max"]
    curseur.execute("INSERT INTO savezvous VALUES('{0}',{1},'{2}',{3},'{4}')".format(descip,interaction.user.id,image,count+1,source))
    embed=createEmbed("Phrase ajoutée","`{0}` : {1}".format(count+1,descip),0x00ffd0,interaction.command.qualified_name,interaction.guild)

    if image!=None:
        embed.set_image(url=image)

    connexion.commit()
    await interaction.response.send_message(embed=embed)

@OTCommand
async def deleteSV(interaction:commands.Context,bot,numero:int) -> None:
    """Fonction qui supprime une phrase de la boite SavezVous d'un serveur. Doit être accompagné d'un numéro de phrase valide pour le serveur dans args, sinon renvoie une erreur. Une phrase ne peut être supprimée que par son auteur ou un modérateur."""
    connexion,curseur=connectSQL(interaction.guild_id)
    try:
        descip=curseur.execute("SELECT * FROM savezvous WHERE Count={0}".format(numero)).fetchone()
    except:
        raise AssertionError("Le numéro donné n'est pas valide.")
    assert descip!=None, "Le numéro donné ne correspond à aucune phrase."
    assert interaction.user.id==descip["ID"] or interaction.user.guild_permissions.manage_messages==True, "Cette phrase ne vous appartient pas."
    curseur.execute("DELETE FROM savezvous WHERE Count={0}".format(numero))
    connexion.commit()
    await interaction.response.send_message(embed=createEmbed("Phrase supprimée","`{0}` : {1}".format(numero,descip["Texte"]),0x00ffd0,interaction.command.qualified_name,interaction.guild))

@OTCommand
async def editSV(interaction:commands.Context,bot,numero,newphrase,source) -> None:
    """Fonction qui édite une phrase de la boite SavezVous d'un serveur. La phrase doit appartenir à l'auteur de la commande, doit être accompagné d'un numéro de phrase valide pour le serveur dans args, et d'une nouvelle phrase, sinon renvoie une erreur."""

    connexion,curseur=connectSQL(interaction.guild_id)
    assert newphrase!=None or source!=None, "Vous devez modifier soit votre phrase soit sa source !"
    try:
        phrase=curseur.execute("SELECT * FROM savezvous WHERE Count={0}".format(numero)).fetchone()
        assert phrase!=None, "Le numéro donné ne correspond à aucune phrase."
    except:
        raise AssertionError("Le numéro donné n'est pas valide.")
    assert interaction.user.id==phrase["ID"], "Cette phrase ne vous appartient pas."
    
    embed=createEmbed("Phrase modifiée","",0x00ffd0,interaction.command.qualified_name,interaction.guild)
    embed.add_field(name="Numéro",value="`{0}`".format(numero))

    if newphrase!=None:
        descip=createPhrase(newphrase)
        assert len(descip)<2000, "Votre phrase est trop longue."
        curseur.execute("UPDATE savezvous SET Texte='{0}' WHERE Count={1}".format(descip,numero))
        embed.add_field(name="Phrase modifiée",value=newphrase)
    if source!=None:
        descip=createPhrase(source)
        assert len(descip)<200, "Votre phrase est trop longue."
        curseur.execute("UPDATE savezvous SET Source='{0}' WHERE Count={1}".format(descip,numero))
        embed.add_field(name="Source modifiée",value=source)

    connexion.commit()
    
    await interaction.response.send_message(embed=embed)


@OTCommand
async def commentSV(interaction:discord.Interaction,bot:commands.Bot,numero,commentaire) -> discord.Embed:
    """Fonction qui ajoute une source à une phrase de la boite SavezVous d'un serveur. La phrase doit appartenir à l'auteur de la commande, doit être accompagné d'un numéro de phrase valide pour le serveur dans args, et d'une nouvelle phrase, sinon renvoie une erreur."""
    
    connexion,curseur=connectSQL(interaction.guild_id)
    try:
        phrase=curseur.execute("SELECT * FROM savezvous WHERE Count={0}".format(numero)).fetchone()
        assert phrase!=None, "Le numéro donné ne correspond à aucune phrase."
    except:
        raise AssertionError("Le numéro donné n'est pas valide.")

    descip=createPhrase(commentaire)
    assert len(descip)<300, "Votre commentaire est trop long."
    if interaction.user.id==phrase["ID"]:
        curseur.execute("INSERT INTO svcomment VALUES ({0},{1},'{2}','{3}')".format(phrase["Count"],interaction.user.id,descip,strftime("%d/%m/%Y")))
        connexion.commit()
        embed=createEmbed("Mise à jour ajoutée","",0x00ffd0,interaction.command.qualified_name,interaction.guild)
        
    else:
        assert curseur.execute("SELECT * FROM svcomment WHERE Count={0} AND ID={1}".format(phrase["Count"],interaction.user.id)).fetchone()==None, "Vous avez déjà mis un commentaire sur cette phrase."
        curseur.execute("INSERT INTO svcomment VALUES ({0},{1},'{2}','{3}')".format(phrase["Count"],interaction.user.id,descip,strftime("%d/%m/%Y")))
        connexion.commit()
        embed=createEmbed("Commentaire ajouté","",0x00ffd0,interaction.command.qualified_name,interaction.guild)
    
    embed.add_field(name="Numéro",value="`{0}`".format(numero))
    embed.add_field(name="Commentaire",value=descip)

    await interaction.response.send_message(embed=embed)
