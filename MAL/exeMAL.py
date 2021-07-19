import asyncio
from MAL.User import embedMALuser
from MAL.List import embedMALlist
from MAL.Compare import embedMALcompare
from MAL.Search import embedMALsearch
from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.Phrase import createPhrase
from Core.Fonctions.setMaxPage import setPage
from Core.Fonctions.Embeds import embedAssert, exeErrorExcept, sendEmbed

dictPage={"+":1,"-":-1,None:0}

async def exeMAL(ctx,bot,option,turn,ligne):
    connexionCMD,curseurCMD=connectSQL(ctx.guild.id,"Commandes","Guild",None,None)
    try:
        if ligne==None:
            args=createPhrase(ctx.args[2:len(ctx.args)]).split(" ")
            print(args)
            if option=="user":
                assert len(args)!=0, "Il manque des arguments ! Vous devez me donner un utilisateur valide !"
                curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'mal','user','{2}','None','None','None',1,2,'None',False)".format(ctx.message.id,ctx.author.id,args[0]))
            elif option=="list":
                assert len(args)>=3, "Il manque des arguments ! Vous devez me donner dans l'ordre : un utilisateur, manga ou anime, et un mot-clé."
                curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'mal','list','{2}','{3}','{4}','None',1,2,'None',False)".format(ctx.message.id,ctx.author.id,args[0],args[1],args[2]))
            elif option=="compare":
                assert len(args)>=4, "Il manque des arguments ! Vous devez me donner dans l'ordre : un utilisateur, un autre utilisateur, manga ou anime, et un mot-clé."
                curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'mal','compare','{2}','{3}','{4}','{5}',1,2,'None',False)".format(ctx.message.id,ctx.author.id,args[0],args[1],args[2],args[3]))
            elif option=="search":
                assert len(args)>2, "Votre recherche est vide ou alors vous n'avez pas spécifié si vous vouliez des mangas ou des animes !"
                curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'mal','search','{2}','{3}','None','None',1,10,'None',False)".format(ctx.message.id,ctx.author.id,args[0],createPhrase(args[1:len(args)])))
            ligne=curseurCMD.execute("SELECT * FROM commandes WHERE MessageID={0}".format(ctx.message.id)).fetchone()
            react=False
        else:
            react=True
        
        page=setPage(ligne["Page"],ligne["PageMax"],turn)
        print(page,ligne["Page"],ligne["PageMax"])

        if option=="user":
            exe=await embedMALuser(ligne["Args1"],page-1)
        elif option=="list":
            exe=await embedMALlist(ligne["Args1"], ligne["Args2"], ligne["Args3"], page-1)
        elif option=="compare":
            exe=await embedMALcompare(ligne["Args1"], ligne["Args2"], ligne["Args3"], ligne["Args4"], page-1)
        elif option=="search":
            exe=await embedMALsearch(ligne["Args1"], ligne["Args2"], page-1)

        embedM=exe[0]
        pagemax=exe[1]
        await sendEmbed(ctx,embedM,react,False,curseurCMD,connexionCMD,page,pagemax)
        
    except asyncio.exceptions.TimeoutError:
        await ctx.send(embed=embedAssert("Temps de requête écoulé, veuillez réessayer."))
    except AssertionError as er:
        await ctx.send(embed=embedAssert(str(er)))
    except:
        await ctx.send(embed=await exeErrorExcept(ctx,bot,ctx.args))
    return