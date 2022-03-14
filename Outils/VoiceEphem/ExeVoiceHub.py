import discord
from Core.Decorator import OTCommand
from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.Embeds import addtoFields, createFields, sendEmbed
from Core.Fonctions.setMaxPage import setMax, setPage
from Outils.VoiceEphem.ModifVoiceHub import (voiceHubAdd, voiceHubDel,
                                             voiceHubEdit)
from Stats.SQL.ConnectSQL import connectSQL


@OTCommand
async def exeVoiceHub(ctx,bot,args,guildOT):
    connexion,curseur=connectSQL(ctx.guild.id,"VoiceEphem","Guild",None,None)
    if ctx.invoked_with=="add":
        embed=await voiceHubAdd(ctx,curseur)
    elif ctx.invoked_with=="del":
        embed=await voiceHubDel(ctx,args,curseur)
    elif ctx.invoked_with=="edit":
        embed=await voiceHubEdit(ctx,args,curseur,bot)
    else:
        await commandeVoiceHub(ctx,None,False,None,bot,guildOT,curseur)
        return
    guildOT.getHubs(curseur)
    connexion.commit()
    await ctx.send(embed=embed)


async def commandeVoiceHub(ctx,turn,react,ligne,bot,guildOT,curseur):
    connexionCMD,curseurCMD=connectSQL(ctx.guild.id,"Commandes","Guild",None,None)
    if not react:
        assert guildOT.voicehub!={}, "Aucun hub de salon éphémère n'est actif sur votre serveur."
        pagemax=setMax(len(guildOT.voicehub))
        curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'voiceephem','hubs','None','None','None','None',1,{2},'countDesc',False)".format(ctx.message.id,ctx.author.id,pagemax))
        ligne=curseurCMD.execute("SELECT * FROM commandes WHERE MessageID={0}".format(ctx.message.id)).fetchone()
    else:
        connexion,curseur=connectSQL(ctx.guild.id,"Guild","Guild",None,None)
        pagemax=setMax(len(guildOT.voicehub))

    mobile=ligne["Mobile"]
    page=setPage(ligne["Page"],pagemax,turn)

    table=curseur.execute("SELECT * FROM hub ORDER BY Nombre ASC").fetchall()
    embed=embedVoiceHub(table,page,pagemax,mobile)

    
    embed=auteur(ctx.guild.id,ctx.guild.name,ctx.guild.icon,embed,"guild")
    message=await sendEmbed(ctx,embed,react,False,curseurCMD,connexionCMD,page,pagemax)
    if not react:
        await message.add_reaction("<:otMOBILE:833736320919797780>")


def embedVoiceHub(table,page,pagemax,mobile):
    embed=discord.Embed(title="Liste des hubs de Salons Ephémères sur votre serveur",color=0xf54269)
    stop=15*page if 15*page<len(table) else len(table)
    field1,field2,field3="","",""
    for i in range(15*(page-1),stop):
        nombre="`{0}`".format(table[i]["Nombre"])
        salon="<#{0}>".format(table[i]["ID"])
        limite=table[i]["Limite"]

        field1,field2,field3=addtoFields(field1,field2,field3,mobile,nombre,salon,limite)

    embed=createFields(mobile,embed,field1,field2,field3,"Numéro","Salon","Limite d'utilisateurs") 
    embed.set_footer(text="Page {0}/{1}".format(page,pagemax))
    return embed
