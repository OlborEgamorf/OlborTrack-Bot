import discord
from Core.Fonctions.Embeds import createEmbed
from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.GetNom import getTitre
from Stats.SQL.ConnectSQL import connectSQL

from Titres.Couleur import getColorJeux
from Titres.Emote import getEmoteJeux
from Titres.Outils import createAccount

dictStatut={0:"Spécial",1:"Basique",2:"Rare",3:"Légendaire",4:"Haut-Fait",5:"Unique",6:"Fabuleux"}
dictSell={0:"Inestimable",1:150,2:300,3:500,4:"Inestimable",5:1250,6:"Inestimable"}
dictValue={0:"Inestimable",1:300,2:600,3:1000,4:"Inestimable",5:2500,6:"Inestimable"}

async def infosTitre(ctx,idtitre,bot):
    connexion,curseur=connectSQL("OT","Titres","Titres",None,None)
    titre=curseur.execute("SELECT * FROM titres WHERE ID={0}".format(idtitre)).fetchone()
    assert titre!=None, "Cet ID ne correspond à aucun titre."
    if titre["Known"]==True:
        title="{0} - {1}".format(titre["ID"],titre["Nom"])
    else:
        title="{0} - ??".format(titre["ID"])
    embed=createEmbed(title,"",0xf58d1d,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),bot.user)
    embed.add_field(name="Description",value=titre["Description"],inline=False)
    embed.add_field(name="Collection",value=titre["Collection"],inline=True)
    embed.add_field(name="Rareté",value=dictStatut[titre["Rareté"]],inline=True)
    embed.add_field(name="Valeur marchande",value="Achat : {0}\nVente : {1}".format(dictValue[titre["Rareté"]],dictSell[titre["Rareté"]]),inline=True)

    try:
        connexionUser,curseurUser=connectSQL("OT",ctx.author.id,"Titres",None,None)
        own=curseurUser.execute("SELECT * FROM titresUser WHERE ID={0}".format(idtitre)).fetchone()
        assert own!=None
        embed.add_field(name="Possédé",value="**Vous possèdez ce titre !**",inline=True)
    except:
        embed.add_field(name="Possédé",value="Vous ne possèdez pas ce titre...",inline=True)

    await ctx.reply(embed=embed)


async def profilUser(ctx,bot):
    connexion,curseur=connectSQL("OT","Titres","Titres",None,None)
    connexionUser,curseurUser=connectSQL("OT",ctx.author.id,"Titres",None,None)
    createAccount(connexionUser,curseurUser)
    color=getColorJeux(ctx.author.id)
    emote=getEmoteJeux(ctx.author.id)
    titre=getTitre(curseur,ctx.author.id)
    coins=curseurUser.execute("SELECT * FROM coins").fetchone()
    count=curseurUser.execute("SELECT Count() AS Count FROM titresUser").fetchone()["Count"]
    embed=discord.Embed(title=titre)
    if color!=None:
        embed.color=color
        embed.add_field(name="Couleur",value="#{0}".format(hex(color)[2:]))
    else:
        embed.add_field(name="Couleur",value="*Configurez avec OT!profil couleur*",inline=True)

    if emote!=None:
        embed.add_field(name="Emote",value=emote,inline=True)
    else:
        embed.add_field(name="Emote",value="*Configurez avec OT!profil emote*",inline=True)

    embed.add_field(name="OT Coins",value="{0} <:otCOINS:873226814527520809>".format(int(coins["Coins"])),inline=True)
    embed.add_field(name="Titres possédés",value=str(count),inline=True)

    embed.set_footer(text=ctx.invoked_with.lower())
    auteur(ctx.author.id,ctx.author.name,ctx.author.avatar,embed,"user")
    await ctx.reply(embed=embed)
