from time import strftime
from Wiki.Events import embedWikiEvents
from Wiki.Quote import embedWikiQOTD, embedWikiQuote
from Wiki.Search import embedWikiSearch
import asyncio
from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.Phrase import createPhrase
from Core.Fonctions.setMaxPage import setPage
from Core.Fonctions.Embeds import embedAssert, exeErrorExcept

dictOption={"deaths":"deaths","morts":"deaths","death":"deaths","décès":"deaths","births":"births","naissances":"births","anniv":"births","birth":"births"}
dictPage={"+":1,"-":-1,None:0}

async def exeWikipedia(ctx,bot,option,turn,ligne):
    if option in ("events","search"):
        connexionCMD,curseurCMD=connectSQL(ctx.guild.id,"Commandes","Guild",None,None)
    try:
        if ligne==None:
            args=createPhrase(ctx.args[2:len(ctx.args)])[0:-1]
            if option=="search":
                assert args!="", "Votre recherche est vide !"
                embedF=await embedWikiSearch(args,1)
            elif option=="wikiquote":
                assert args!="", "Votre recherche est vide !"
                embedF=await embedWikiQuote(args)
            elif option=="qotd":
                embedF=await embedWikiQOTD()
            elif option=="events":
                try:
                    args=dictOption[args]
                except:
                    args="events"
                embedF=await embedWikiEvents(args,strftime("%d"),strftime("%m"))

            message=await ctx.send(embed=embedF)
            if option=="events":
                await message.add_reaction("<:otRELOAD:772766034356076584>")
                curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'wikipedia','events','{2}','{3}','{4}','None',1,1,'None',False)".format(message.id,ctx.author.id,args,strftime("%d"),strftime("%m")))
                connexionCMD.commit()
            elif option=="search":
                await message.add_reaction("<:otGAUCHE:772766034335236127>")
                await message.add_reaction("<:otDROITE:772766034376523776>")
                curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'wikipedia','search','{2}','None','None','None',1,2,'None',False)".format(message.id,ctx.author.id,args))
                connexionCMD.commit()
        else:
            if option=="search":
                page=setPage(ligne["Page"]+dictPage[turn],2)
                embedF=await embedWikiSearch(ligne["Args1"],page)
                curseurCMD.execute("UPDATE commandes SET Page={0} WHERE MessageID={1}".format(page,ctx.message.id))
                connexionCMD.commit()
            elif option=="events":
                embedF=await embedWikiEvents(ligne["Args1"],ligne["Args2"],ligne["Args3"])
            await ctx.message.edit(embed=embedF)
        
    except AssertionError as er:
        await ctx.send(embed=embedAssert(str(er)))
    except asyncio.exceptions.TimeoutError:
        await ctx.send(embed=embedAssert("Temps de requête écoulé, veuillez réessayer."))
    except:
        await ctx.send(embed=await exeErrorExcept(ctx,bot,""))