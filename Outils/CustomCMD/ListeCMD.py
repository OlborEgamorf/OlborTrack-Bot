from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.setMaxPage import setMax, setPage
from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.Embeds import sendEmbed
import discord

async def commandeCMD(ctx,turn,react,ligne):
    connexionCMD,curseurCMD=connectSQL(ctx.guild.id,"Commandes","Guild",None,None)
    connexion,curseur=connectSQL(ctx.guild.id,"CustomCMD","Guild",None,None)
    if not react:
        table=curseur.execute("SELECT * FROM help").fetchall()
        assert table!=[], "Vous n'avez pas créé de commandes personnalisées."
        pagemax=setMax(len(table))
        curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'customCMD','None','None','None','None','None',1,{2},'countDesc',False)".format(ctx.message.id,ctx.author.id,pagemax))
        ligne=curseurCMD.execute("SELECT * FROM commandes WHERE MessageID={0}".format(ctx.message.id)).fetchone()
    else:
        table=curseur.execute("SELECT * FROM help").fetchall()
        pagemax=setMax(len(table))

    page=setPage(ligne["Page"],pagemax,turn)

    embed=embedCMD(table,page,pagemax)
    embed=auteur(ctx.guild.id,ctx.guild.name,ctx.guild.icon,embed,"guild")
    await sendEmbed(ctx,embed,react,False,curseurCMD,connexionCMD,page,pagemax)
    

def embedCMD(table,page,pagemax):
    descip=""
    stop=15*page if 15*page<len(table) else len(table)
    for i in range(15*(page-1),stop):
        if len(table[i]["Description"])>110:
            descip+="**OT!{0}** : {1}...\n".format(table[i]["Nom"],table[i]["Description"][0:110])
        else:
            descip+="**OT!{0}** : {1}\n".format(table[i]["Nom"],table[i]["Description"])
    embed=discord.Embed(title="Commandes de votre serveur",description=descip,color=0xf54269)
    embed.set_footer(text="Page {0}/{1}".format(page,pagemax))
    return embed