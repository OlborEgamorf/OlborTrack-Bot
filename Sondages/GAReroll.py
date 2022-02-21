import random

from Core.Decorator import OTCommand
from Core.Fonctions.Embeds import createEmbed, sendEmbed
from Core.Fonctions.setMaxPage import setMax, setPage
from Stats.SQL.ConnectSQL import connectSQL


@OTCommand
async def exeGaReroll(ctx,args,bot):
    if len(args)==0:
        await commandeGAR(ctx,None,False,None)
        return
        
    connexion,curseur=connectSQL(ctx.guild.id,"Giveaway","Guild",None,None)
    try:
        etat=curseur.execute("SELECT * FROM liste WHERE Nombre={0}".format(args[0])).fetchone()
    except:
        raise AssertionError("Le numéro de giveaway donné n'est pas valide.")
    assert etat!=None, "Ce numéro de giveaway n'existe pas."
    try:
        await ctx.guild.get_channel(etat["IDChan"]).fetch_message(etat["IDMess"])
    except:
        raise AssertionError("Ce giveaway est introuvable. Soit je n'ai plus accès au salon où il a eu lieu, soit il a été supprimé.")
    choix=random.choice(curseur.execute("SELECT * FROM {0}".format("n{0}".format(args[0]))).fetchall())
    await ctx.send("<:otVERT:718396570638483538> Bravo à <@{0}> qui a gagné {1} !".format(choix["ID"],etat["Lot"]))


async def commandeGAR(ctx,turn,react,ligne):
    connexionCMD,curseurCMD=connectSQL(ctx.guild.id,"Commandes","Guild",None,None)
    connexion,curseur=connectSQL(ctx.guild.id,"Giveaway","Guild",None,None)
    if not react:
        table=curseur.execute("SELECT * FROM liste").fetchall()
        assert table!=[], "Vous n'avez jamais lancé de giveaway sur votre serveur !"
        pagemax=setMax(len(table))
        curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'gareroll','None','None','None','None','None',1,{2},'countDesc',False)".format(ctx.message.id,ctx.author.id,pagemax))
        ligne=curseurCMD.execute("SELECT * FROM commandes WHERE MessageID={0}".format(ctx.message.id)).fetchone()
    else:
        table=curseur.execute("SELECT * FROM giveway").fetchall()
        pagemax=setMax(len(table))

    page=setPage(ligne["Page"],pagemax,turn)

    embed=embedGAR(table,page,pagemax,ctx.guild)
    await sendEmbed(ctx,embed,react,False,curseurCMD,connexionCMD,page,pagemax)
    

def embedGAR(table,page,pagemax,guild):
    descip=""
    stop=15*page if 15*page<len(table) else len(table)
    for i in range(15*(page-1),stop):
        if len(table[i]["Lot"])>110:
            descip+="`{0}` : {1}...\n".format(table[i]["Nombre"],table[i]["Lot"][0:110])
        else:
            descip+="`{0}` : {1}\n".format(table[i]["Nombre"],table[i]["Lot"])
    embed=createEmbed("Liste des giveaway lancés",descip,0xfc03d7,"giveaway",guild)
    return embed
