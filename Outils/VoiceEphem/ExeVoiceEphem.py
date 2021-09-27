from Stats.SQL.ConnectSQL import connectSQL
import discord
from Core.Fonctions.Embeds import addtoFields, createFields, embedAssert, exeErrorExcept, sendEmbed
from Outils.VoiceEphem.ModifVoiceEphem import voiceEphemAdd, voiceEphemDel, voiceEphemEdit, voiceEphemLimite 
from Core.Fonctions.setMaxPage import setMax, setPage
from Core.Fonctions.AuteurIcon import auteur

async def exeVoiceEphem(ctx,bot,args,guildOT):
    try:
        connexion,curseur=connectSQL(ctx.guild.id,"VoiceEphem","Guild",None,None)
        if ctx.invoked_with=="hubs":
            await commandeVoiceEphem(ctx,None,False,None,bot,guildOT,curseur,"hubs")
            return
        elif ctx.invoked_with=="salons":
            await commandeVoiceEphem(ctx,None,False,None,bot,guildOT,curseur,"salons")
            return
        elif ctx.invoked_with=="add":
            embed=await voiceEphemAdd(ctx,curseur)
        elif ctx.invoked_with=="limit":
            embed=await voiceEphemLimite(ctx,args,curseur)
        elif ctx.invoked_with=="del":
            embed=await voiceEphemDel(ctx,args,curseur)
        elif ctx.invoked_with=="edit":
            embed=await voiceEphemEdit(ctx,args,curseur)
        guildOT.getHubs(curseur)
        connexion.commit()
    except AssertionError as er:
        embed=embedAssert(str(er))
    except:
        embed=await exeErrorExcept(ctx,bot,args)
    await ctx.send(embed=embed)


async def commandeVoiceEphem(ctx,turn,react,ligne,bot,guildOT,curseur,option):
    connexionCMD,curseurCMD=connectSQL(ctx.guild.id,"Commandes","Guild",None,None)
    if not react:
        assert guildOT.voicehub!={}, "Aucun hub de salon éphémère n'est actif sur votre serveur."
        if option=="hubs":
            pagemax=setMax(len(guildOT.voicehub))
        else:
            pagemax=setMax(50)
        curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'voiceephem','{2}','None','None','None','None',1,{3},'countDesc',False)".format(ctx.message.id,ctx.author.id,option,pagemax))
        ligne=curseurCMD.execute("SELECT * FROM commandes WHERE MessageID={0}".format(ctx.message.id)).fetchone()
    else:
        connexion,curseur=connectSQL(ctx.guild.id,"Guild","Guild",None,None)
        if option=="hubs":
            pagemax=setMax(len(guildOT.voicehub))
        else:
            pagemax=setMax(50)

    mobile=ligne["Mobile"]
    page=setPage(ligne["Page"],pagemax,turn)

    if option=="hubs":
        table=curseur.execute("SELECT * FROM hub ORDER BY Nombre ASC").fetchall()
        embed=embedVoiceEphem(table,page,pagemax,mobile)
    else:
        table=curseur.execute("SELECT * FROM salons ORDER BY Nombre ASC").fetchall()
        embed=embedVoiceEphemNoms(table,page,pagemax,mobile)
    
    embed=auteur(ctx.guild.id,ctx.guild.name,ctx.guild.icon,embed,"guild")
    message=await sendEmbed(ctx,embed,react,False,curseurCMD,connexionCMD,page,pagemax)
    if not react:
        await message.add_reaction("<:otMOBILE:833736320919797780>")


def embedVoiceEphem(table,page,pagemax,mobile):
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


def embedVoiceEphemNoms(table,page,pagemax,mobile):
    embed=discord.Embed(title="Liste des noms des Salons Ephémères sur votre serveur",color=0xf54269)
    stop=15*page if 15*page<len(table) else len(table)
    field1,field2,field3="","",""
    for i in range(15*(page-1),stop):
        nombre="`{0}`".format(table[i]["Nombre"])
        nom=table[i]["Nom"]
        used="Oui" if table[i]["ID"]!=0 else "Non"

        field1,field2,field3=addtoFields(field1,field2,field3,mobile,nombre,nom,used)

    embed=createFields(mobile,embed,field1,field2,field3,"Numéro","Nom","Utilisé") 
    embed.set_footer(text="Page {0}/{1}".format(page,pagemax))
    return embed