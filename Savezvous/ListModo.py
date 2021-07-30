import discord
from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.GetTable import getTableSV
from Core.Fonctions.setMaxPage import setMax, setPage
from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.Embeds import sendEmbed

async def commandeSV(ctx,option,turn,react,ligne,bot):
    connexionCMD,curseurCMD=connectSQL(ctx.guild.id,"Commandes","Guild",None,None)
    connexion,curseur=connectSQL(ctx.guild.id,"Guild","Guild",None,None)
    if not react:
        table=getTableSV(curseur,option,ctx.author.id)
        assert table!=[], "Vous devez commencer par ajouter une phrase avec `OT!savezvous add` !"
        pagemax=setMax(len(table))
        curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'savezvous','{2}','None','None','None','None',1,{3},'countDesc',False)".format(ctx.message.id,ctx.author.id,option,pagemax))
        ligne=curseurCMD.execute("SELECT * FROM commandes WHERE MessageID={0}".format(ctx.message.id)).fetchone()
    else:
        table=getTableSV(curseur,option,ligne["AuthorID"])
        pagemax=setMax(len(table))

    page=setPage(ligne["Page"],pagemax,turn)
    option=ligne["Option"]

    embed=embedSV(table,page,pagemax)
    if option=="list":
        user=ctx.guild.get_member(ligne["AuthorID"])
        embed=auteur(user.id,user.name,user.avatar,embed,"user")
    else:
        embed=auteur(ctx.guild.id,ctx.guild.name,ctx.guild.icon,embed,"guild")
    await sendEmbed(ctx,embed,react,False,curseurCMD,connexionCMD,page,pagemax)
    

def embedSV(table,page,pagemax):
    descip=""
    stop=15*page if 15*page<len(table) else len(table)
    for i in range(15*(page-1),stop):
        if table[i]["Image"]!="None":
            image="**+ Image**"
        else:
            image=""
        if len(table[i]["Texte"])>110:
            descip+="`{0}` : {1}... {2}\n".format(table[i]["Count"],table[i]["Texte"][0:110],image)
        else:
            descip+="`{0}` : {1} {2}\n".format(table[i]["Count"],table[i]["Texte"],image)
    embed=discord.Embed(title="Phrases OT!savezvous",description=descip,color=0x00ffd0)
    embed.set_footer(text="Page {0}/{1}".format(page,pagemax))
    return embed