import os
import shutil

import discord
from Core.Decorator import OTCommand
from Core.Fonctions.Embeds import createEmbed, exeErrorExcept
from Core.OT import OlborTrack
from discord.ext import commands

listeDel={}

@OTCommand
async def deleteStats(ctx:commands.Context,bot:OlborTrack):
    """Commande qui déclenche la suppression des stats. Commande admin seulement. Possibilité de préciser quelle stat supprimer. Renvoie ensuite à un message de confirmation."""
    if len(ctx.args)==2:
        stat="all"
    else:
        stat=ctx.args[2].lower()
        assert stat in ("all","voice","messages","moyennes","salons","emotes","reactions","divers","freq","mots"), "La statistique donnée n'est pas bonne. Veuillez choisir entre : all, voice, messages, moyennes, salons, emotes, reactions, divers, mentions, freq, mots"
    embed=createEmbed("Suppression des statistiques","Veuillez confirmer la suppression des statistiques : **{0}**. \nUne fois que ce sera fait, vous ne pourrez plus les récupérer sauf en réinitialisant toutes les statistiques avec OT!getdata.".format(stat),0x220cc9,ctx.invoked_with.lower(),ctx.guild)
    message=await ctx.send(embed=embed)
    await message.add_reaction("<:OTdelete:866705696505200691>")
    await message.add_reaction("<:otANNULER:811242376625782785>")
    listeDel[message.id]=stat

async def confirmDel(ctx:commands.Context,author:discord.Member,bot:OlborTrack):
    """Fonction qui supprime les statistiques après confirmation par un membre. Si le membre n'est pas administrateur, rien ne se passe. Parcours les périodes possibles et supprime les fichiers qui correspondent. Action irréversible."""
    try:
        assert author.guild_permissions.administrator
        assert ctx.message.id in listeDel
        await ctx.message.clear_reactions()
        if listeDel[ctx.message.id]=="all":
            listePeriod=[15,16,17,18,19,20,21,22,23,"GL","Voice"]
            for i in listePeriod:
                try:
                    shutil.rmtree("SQL/{0}/{1}".format(ctx.guild.id,i))
                except:
                    pass
        elif listeDel[ctx.message.id]=="voice":
            try:
                shutil.rmtree("SQL/{0}/Voice".format(ctx.guild.id))
            except:
                pass
        else:
            listeAnnee=[15,16,17,18,19,20,21,22,23]
            listeMois=["01","02","03","04","05","06","07","08","09","10","11","12","TO"]
            for i in listeAnnee:
                for j in listeMois:
                    try:
                        if listeDel[ctx.message.id]=="mentions":
                            os.remove("SQL/{0}/{1}/{2}/Mentionne.db".format(ctx.guild.id,i,j))
                        os.remove("SQL/{0}/{1}/{2}/{3}.db".format(ctx.guild.id,i,j,listeDel[ctx.message.id]))
                    except:
                        pass
            try:
                if listeDel[ctx.message.id]=="mentions":
                    os.remove("SQL/{0}/GL/Mentionne.db".format(ctx.guild.id))
                os.remove("SQL/{0}/GL/{1}.db".format(ctx.guild.id,listeDel[ctx.message.id]))
            except:
                pass
            
        embed=createEmbed("Statistiques supprimées avec succès.","Si vous voulez qu'elles ne soient plus jamais traquées, utilisez la commande OT!modulestat ou OT!statsoff.",0x220cc9,"OT!delstats",ctx.guild)
        await ctx.send(embed=embed)
    except AssertionError as er:
        pass
    except:
        await exeErrorExcept(ctx,bot,True)

async def cancelDel(ctx:commands.Context,author:discord.Member,bot:OlborTrack):
    """Fonction qui annule la suppression des stats, si un membre a utilisé la réaction d'annulation. Si le membre n'est pas administrateur, rien ne se passe."""
    try:
        assert ctx.message.id in listeDel
        assert not author.bot
        assert author.guild_permissions.administrator
        await ctx.message.clear_reactions()
        embed=createEmbed("Suppression des statistiques","Opération annulée.",0x220cc9,"delstats",ctx.guild)
        await ctx.message.edit(embed=embed)
    except AssertionError as er:
        pass
    except:
        await exeErrorExcept(ctx,bot,True)
