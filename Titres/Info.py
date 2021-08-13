from Stats.SQL.ConnectSQL import connectSQL
import discord
from Core.Fonctions.AuteurIcon import auteur

dictStatut={0:"Fabuleux",1:"Rare",2:"Légendaire",3:"Unique"}
dictSell={1:150,2:400,3:2500,0:"Inestimable"}
dictValue={0:"Inestimable",1:300,2:800,3:5000}

async def infosTitre(ctx,idtitre,bot):
    connexion,curseur=connectSQL("OT","Titres","Titres",None,None)
    titre=curseur.execute("SELECT * FROM titres WHERE ID={0}".format(idtitre)).fetchone()
    assert titre!=None, "Cet ID ne correspond à aucun titre."
    embed=discord.Embed(color=0xf58d1d)
    if titre["Known"]==True:
        embed.title="{0} - {1}".format(titre["ID"],titre["Nom"])
    else:
        embed.title="{0} - ??".format(titre["ID"])
    embed.add_field(name="Description",value=titre["Description"],inline=False)
    embed.add_field(name="Collection",value=titre["Collection"],inline=True)
    embed.add_field(name="Rareté",value=dictStatut[titre["Rareté"]],inline=True)
    embed.add_field(name="Valeur marchande",value="Achat : {0}\nVente : {1}".format(dictValue[titre["Rareté"]],dictSell[titre["Rareté"]]),inline=True)
    embed.set_footer(text="OT!titre infos")
    embed=embed=auteur(bot.user,None,None,embed,"olbor")
    await ctx.reply(embed=embed)