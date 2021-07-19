from Core.Fonctions.Embeds import createEmbed, exeErrorExcept,embedAssert
import os
import shutil
listeDel={}

async def deleteStats(ctx,bot):
    try:
        print(ctx.args)
        if len(ctx.args)==2:
            stat="all"
        else:
            stat=ctx.args[2].lower()
            assert stat in ("all","voice","messages","moyennes","salons","emotes","reactions","divers","mentions","freq","mots"), "La statistique donnée n'est pas bonne. Veuillez choisir entre : all, voice, messages, moyennes, salons, emotes, reactions, divers, mentions, freq, mots"
        embed=createEmbed("Suppression des statistiques","Veuillez confirmer la suppression des statistiques : **{0}**. \nUne fois que ce sera fait, vous ne pourrez plus les récupérer sauf en réinitialisant toutes les statistiques avec OT!getdata.".format(stat),0x220cc9,ctx.invoked_with.lower(),ctx.guild)
        message=await ctx.send(embed=embed)
        await message.add_reaction("<:OTdelete:866705696505200691>")
        await message.add_reaction("<:otANNULER:811242376625782785>")
        listeDel[message.id]=stat
    except AssertionError as er:
        embedTable=embedAssert(str(er))
    except:
        embedTable=await exeErrorExcept(ctx,bot,"")

async def confirmDel(ctx,author,bot):
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
                        os.remove("SQL/{0}/{1}/{2}/{3}.db".format(ctx.guild.id,i,j,listeDel[ctx.message.id]))
                    except:
                        pass
            try:
                os.remove("SQL/{0}/GL/{1}.db".format(ctx.guild.id,listeDel[ctx.message.id]))
            except:
                pass
            
        embed=createEmbed("Statistiques supprimées avec succès.","Si vous voulez qu'elles ne soient plus jamais traquées, utilisez la commande OT!modulestat ou OT!statsoff.",0x220cc9,"OT!delstats",ctx.guild)
        await ctx.send(embed=embed)
    except AssertionError as er:
        pass
    except:
        await ctx.send(embed=await exeErrorExcept(ctx,bot,""))

async def cancelDel(ctx,author,bot):
    try:
        assert not author.bot
        assert author.guild_permissions.administrator
        assert ctx.message.id in listeDel
        await ctx.message.clear_reactions()
        embed=createEmbed("Suppression des statistiques","Opération annulée.",0x220cc9,"delstats",ctx.guild)
        await ctx.message.edit(embed=embed)
    except AssertionError as er:
        pass
    except:
        await ctx.send(embed=await exeErrorExcept(ctx,bot,""))