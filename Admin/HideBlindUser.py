from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.Embeds import createEmbed, exeErrorExcept,embedAssert

async def exeHBUser(ctx,bot,option,guild):
    """Cette fonction permet à un utilisateur de se rendre masqué ou bloqué aux yeux du bot sur un serveur.
    
    L'utilisation de la commande suffit pour activer/désactiver l'une des options.
    
    L'option est donnée lors de l'exécution de la commande.
    
    Connexion à la base de données et reset dans l'objet OTGuild
    
    Options possibles : hide, blind, mute"""
    try:
        connexion,curseur=connectSQL(ctx.guild.id,"Guild","Guild",None,None)
        dictEmbed={"HideFalse":"masqué","BlindFalse":"invisible","HideTrue":"démasqué","BlindTrue":"visible"}
        etat=curseur.execute("SELECT * FROM users WHERE ID={0}".format(ctx.author.id)).fetchone()
        curseur.execute("UPDATE users SET {0}={1} WHERE ID={2}".format(option,bool(int(etat[option])-1),ctx.author.id))
        descip="Vous êtes désormais {0} à mes yeux sur ce serveur.".format(dictEmbed["{0}{1}".format(option,bool(etat[option]))])
        connexion.commit()
        guild.getHBM()
        embedTable=createEmbed("Changement d'état",descip,0x220cc9,ctx.invoked_with.lower(),ctx.author)
    except AssertionError as er:
        embedTable=embedAssert(str(er))
    except:
        embedTable=await exeErrorExcept(ctx,bot,"")
    await ctx.send(embed=embedTable)