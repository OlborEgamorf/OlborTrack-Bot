import discord
from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.Embeds import addtoFields, createFields, sendEmbed
from Core.Fonctions.setMaxPage import setMax, setPage
from Core.OTGuild import OTGuild
from OT3.Core.Fonctions.Embeds import createEmbed
from Stats.SQL.ConnectSQL import connectSQL


def embedStarBoard(user,content,channel,image,id,link):
    embedS=createEmbed("",content,user.color.value,"tableau",user)
    if image!=[]:
        embedS.set_image(url=image[0].url)
    embedS.add_field(name="Salon",value="<#{0}>".format(channel),inline=True)
    embedS.add_field(name="Contexte",value="[Lien vers le message !]({1})".format(channel,link),inline=True)
    return embedS

def embedSB(table,page,pagemax,mobile):
    embed=discord.Embed(title="Liste des tableux actifs sur votre serveur",color=0xf54269)
    stop=15*page if 15*page<len(table) else len(table)
    field1,field2,field3="","",""
    for i in range(15*(page-1),stop):
        nombre="`{0}`".format(table[i]["Nombre"])
        emote="{0} - {1}".format(table[i]["Emote"],table[i]["Count"])
        salon="<#{0}>".format(table[i]["Salon"])

        field1,field2,field3=addtoFields(field1,field2,field3,mobile,nombre,emote,salon)

    embed=createFields(mobile,embed,field1,field2,field3,"Numéro","Emote - Nombre min.","Salon")
    embed.set_footer(text="Page {0}/{1}".format(page,pagemax))
    return embed
        

async def commandeSB(ctx,turn,react,ligne,bot,guildOT:OTGuild,curseur):
    connexionCMD,curseurCMD=connectSQL(ctx.guild.id,"Commandes","Guild",None,None)
    if not react:
        assert guildOT.stardict!={}, "Aucun tableau n'est configuré pour votre serveur."
        pagemax=setMax(len(guildOT.stardict))
        curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'tableau','None','None','None','None','None',1,{2},'countDesc',False)".format(ctx.message.id,ctx.author.id,pagemax))
        ligne=curseurCMD.execute("SELECT * FROM commandes WHERE MessageID={0}".format(ctx.message.id)).fetchone()
    else:
        connexion,curseur=connectSQL(ctx.guild.id,"Guild","Guild",None,None)
        pagemax=setMax(len(guildOT.stardict))

    mobile=ligne["Mobile"]
    table=curseur.execute("SELECT * FROM sb ORDER BY Nombre ASC").fetchall()
    page=setPage(ligne["Page"],pagemax,turn)

    embed=embedSB(table,page,pagemax,mobile)
    embed=auteur(ctx.guild.id,ctx.guild.name,ctx.guild.icon,embed,"guild")
    message=await sendEmbed(ctx,embed,react,False,curseurCMD,connexionCMD,page,pagemax)
    if not react:
        await message.add_reaction("<:otMOBILE:833736320919797780>")