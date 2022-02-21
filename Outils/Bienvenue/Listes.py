import discord
from Core.Decorator import OTCommand
from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.Embeds import sendEmbed
from Core.Fonctions.setMaxPage import setMax, setPage
from Core.Fonctions.WebRequest import getAvatar
from Outils.Bienvenue.Manipulation import fusion, fusionAdieu, squaretoround
from Stats.SQL.ConnectSQL import connectSQL

dictTitres={"BV":"de bienvenue","AD":"d'adieu"}

@OTCommand
async def commandeMessBV(ctx,option,turn,react,ligne,bot):
    connexionCMD,curseurCMD=connectSQL(ctx.guild.id,"Commandes","Guild",None,None)
    connexion,curseur=connectSQL(ctx.guild.id,"Guild","Guild",None,None)
    if not react:
        table=curseur.execute("SELECT * FROM messages{0}".format(option)).fetchall()
        assert table!=[], "Vous n'avez ajouté aucun message {0} !".format(dictTitres[option])
        pagemax=setMax(len(table))
        curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'messagesBV','{2}','None','None','None','None',1,{3},'countDesc',False)".format(ctx.message.id,ctx.author.id,option,pagemax))
        ligne=curseurCMD.execute("SELECT * FROM commandes WHERE MessageID={0}".format(ctx.message.id)).fetchone()
    else:
        table=curseur.execute("SELECT * FROM messages{0}".format(option)).fetchall()
        pagemax=setMax(len(table))

    page=setPage(ligne["Page"],pagemax,turn)
    option=ligne["Option"]

    embed=embedMessBV(table,page,pagemax,option)
    embed=auteur(ctx.guild.id,ctx.guild.name,ctx.guild.icon,embed,"guild")
    await sendEmbed(ctx,embed,react,False,curseurCMD,connexionCMD,page,pagemax)

@OTCommand
async def commandeImageBV(ctx,option,turn,react,ligne,bot):
    connexionCMD,curseurCMD=connectSQL(ctx.guild.id,"Commandes","Guild",None,None)
    connexion,curseur=connectSQL(ctx.guild.id,"Guild","Guild",None,None)
    if not react:
        table=curseur.execute("SELECT * FROM images{0}".format(option)).fetchall()
        assert table!=[], "Vous n'avez ajouté aucune image {0} !".format(dictTitres[option])
        pagemax=len(table)
        curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'imagesBV','{2}','None','None','None','None',1,{3},'countDesc',False)".format(ctx.message.id,ctx.author.id,option,pagemax))
        ligne=curseurCMD.execute("SELECT * FROM commandes WHERE MessageID={0}".format(ctx.message.id)).fetchone()
    else:
        table=curseur.execute("SELECT * FROM images{0}".format(option)).fetchall()
        pagemax=len(table)

    page=setPage(ligne["Page"],pagemax,turn)
    option=ligne["Option"]

    embed=embedImageBV(table,page,pagemax,option)
    embed=auteur(ctx.guild.id,ctx.guild.name,ctx.guild.icon,embed,"guild")

    await getAvatar(bot.user)
    squaretoround(bot.user.id)

    if option=="BV":
        fusion(table[page-1]["Path"],bot.user,table[page-1]["Message"],table[page-1]["Couleur"],table[page-1]["Taille"],ctx.guild)
    else:
        fusionAdieu(table[page-1]["Path"],bot.user,table[page-1]["Message"],table[page-1]["Couleur"],table[page-1]["Taille"],ctx.guild,table[page-1]["Filtre"])

    message=await sendEmbed(ctx,embed,react,False,curseurCMD,connexionCMD,page,pagemax)
    if react:
        await ctx.reply(file=discord.File("Temp/{0}{1}.png".format(option,bot.user.id)))
    else:
        await message.reply(file=discord.File("Temp/{0}{1}.png".format(option,bot.user.id)))
    

def embedMessBV(table,page,pagemax,option):
    descip=""
    stop=15*page if 15*page<len(table) else len(table)
    for i in range(15*(page-1),stop):
        if len(table[i]["Message"])>110:
            descip+="`{0}` : {1}...\n".format(table[i]["Nombre"],table[i]["Message"][0:110])
        else:
            descip+="`{0}` : {1}\n".format(table[i]["Nombre"],table[i]["Message"])
    embed=discord.Embed(title="Messages {0}".format(dictTitres[option]),description=descip,color=0xf54269)
    embed.set_footer(text="Page {0}/{1}".format(page,pagemax))
    return embed

def embedImageBV(table,page,pagemax,option):
    dictTitres={"BV":"de bienvenue","AD":"d'adieu"}
    descip="Numéro : `{0}`\nTexte : {1}\nTaille : {2}\nCouleur : {3}\nMode : {4}".format(table[page-1]["Nombre"],table[page-1]["Message"],table[page-1]["Taille"],table[page-1]["Couleur"],table[page-1]["Mode"])
    if option=="AD":
        descip+="\nFiltre : {0}".format(table[page-1]["Filtre"])
    embed=discord.Embed(title="Images {0}".format(dictTitres[option]),description=descip,color=0xf54269)
    embed.set_footer(text="Page {0}/{1}".format(page,pagemax))
    return embed
