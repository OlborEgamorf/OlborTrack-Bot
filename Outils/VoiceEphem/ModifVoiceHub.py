import asyncio

from Core.Fonctions.Embeds import createEmbed, embedAssertClassic
from Core.Fonctions.GetNom import getAuthor
from Core.Fonctions.Phrase import createPhrase
from Outils.VoiceEphem.FormatagePattern import formatageVoiceEphem


async def voiceHubAdd(ctx,curseur):
    chan=getAuthor("Voicechan",ctx,2)
    assert chan!=None, "Vous devez me donner un salon vocal valide !"
    assert curseur.execute("SELECT * FROM hub WHERE ID={0}".format(chan)).fetchone()==None, "Le salon <#{0}> est déjà un hub !".format(chan)
    num=curseur.execute("SELECT COUNT() as Nombre FROM hub").fetchone()["Nombre"]+1
    pattern="Salon de {user}"
    curseur.execute("INSERT INTO hub VALUES({0},{1},0,'{2}')".format(num,chan,pattern))

    return createEmbed("Hub créé","Numéro du hub : {0}\nSalon : <#{1}>\nNombre limite d'utilisateurs : aucune\nPattern de noms : défaut".format(num,chan),0xf54269,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)


async def voiceHubDel(ctx,args,curseur):
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


async def voiceHubEdit(ctx,args,curseur,bot):
    try:
        def checkAuthor(mess):
            return mess.author.id==ctx.author.id and mess.channel.id==ctx.channel.id
        def checkOption(mess):
            return mess.author.id==ctx.author.id and mess.channel.id==ctx.channel.id and mess.content.lower() in ("pattern","limite","role","stop")
        def checkNumber(mess):
            try:
                if mess.content.split(" ")[0].lower()!="inf":
                    int(mess.content.split(" ")[0])
            except:
                return False
            return mess.author.id==ctx.author.id and mess.channel.id==ctx.channel.id

        assert len(args)>=1, "Il manque le numéro du hub pour le modifier !"
        try:
            hub=curseur.execute("SELECT * FROM hub WHERE Nombre={0}".format(args[0])).fetchone()
        except:
            raise AssertionError("Le numéro donné n'est pas valide.")
        assert hub!=None, "Le numéro donné ne correspond à aucun hub actif."

        config=True 
        while config:
            hub=curseur.execute("SELECT * FROM hub WHERE Nombre={0}".format(args[0])).fetchone()
            embed=createEmbed("Modification de hub vocal","Bienvenue dans l'outil de modification des hubs vocaux.\nIci vous pouvez modifier la limite de membres par défaut et le pattern de nom des salons créés à partir du hub.\nQue voulez vous modifier ? Tapez la commande que vous souhaitez",0xf54269,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)
            embed.add_field(name="Pattern de noms",value="Actuel : {0}\nCommande : **pattern**".format(hub["Pattern"]),inline=True)
            embed.add_field(name="Limite de membres",value="Actuel : {0}\nCommande : **limite**".format(hub["Limite"]),inline=True)
            embed.add_field(name="Arrêter les modifications",value="Commande : **stop**",inline=True)
            
            message=await ctx.reply(embed=embed)
            messWait=await bot.wait_for('message', check=checkOption, timeout=60)
            option=messWait.content.lower()
            
            if option=="pattern":
                embed=createEmbed("Modification de hub vocal\nPattern de noms","Veuillez saisir votre pattern. Vous pouvez y ajouter des informations dynamiques avec ces balises :\n- {user} : créateur du salon\n- {nb} : numéro du salon\n - {lettre} : lettre associée au salon, dans l'ordre alphabétique\nVous pouvez aussi le réinitialiser en envoyant 'default'.",0xf54269,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)
                await message.edit(embed=embed)

                messWait=await bot.wait_for('message', check=checkAuthor, timeout=60)
                clean=createPhrase(messWait.content)
                exemple=formatageVoiceEphem(clean,bot.user,1)

                curseur.execute("UPDATE hub SET Pattern='{0}' WHERE Nombre={1}".format(clean,hub["Nombre"]))

                embed=createEmbed("Modification de hub vocal\nPattern de noms","Pattern modifié !\nBrut : {0}\nExemple : {1}".format(clean,exemple),0xf54269,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)
                await message.edit(embed=embed)
            
            elif option=="limite":
                embed=createEmbed("Modification de hub vocal\nLimite de membres","Donnez moi la limite de membre que vous souhaitez imposer.\nPour quelle soit infinie : écrivez 'inf'.",0xf54269,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)
                await message.edit(embed=embed)

                messWait=await bot.wait_for('message', check=checkNumber, timeout=60)
                nb=messWait.content.split(" ")[0].lower()
                if nb=="inf":
                    nb=0
                else:
                    nb=int(nb)

                curseur.execute("UPDATE hub SET Limite={0} WHERE Nombre={1}".format(nb,hub["Nombre"]))

                embed=createEmbed("Modification de hub vocal\nLimite de membres","Limite modifiée !\nNouvelle limite : {0}".format(nb),0xf54269,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)
                await message.edit(embed=embed)
            
            elif option=="stop":
                config=False
        
        return createEmbed("Modification de hub vocal","Toutes les modifications ont été appliquées !",0xf54269,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.guild)
    except asyncio.exceptions.TimeoutError:
        return embedAssertClassic("Une minute s'est écoulée et vous n'avez rien donné. Les modifications apportées sont appliquées.")
