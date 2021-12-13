import asyncio
from random import randint
from time import strftime

import discord
from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.Embeds import embedAssert, exeErrorExcept
from Core.Fonctions.Phrase import createPhrase
from Core.Fonctions.WebRequest import webRequest
from Stats.SQL.ConnectSQL import connectSQL

tableauMois={"01":"Janvier","02":"Février","03":"Mars","04":"Avril","05":"Mai","06":"Juin","07":"Juillet","08":"Aout","09":"Septembre","10":"Octobre","11":"Novembre","12":"Décembre","TO":"Année","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","glob":"GL","to":"TO"}
dictOption={"deaths":"deaths","morts":"deaths","death":"deaths","décès":"deaths","births":"births","naissances":"births","anniv":"births","birth":"births"}

async def embedWikiEvents(option,jour,mois):
    descip,hyper="",""
    table=await webRequest("https://byabbe.se/on-this-day/"+str(int(mois))+"/"+str(int(jour))+"/"+option+".json")
    assert table!=False, "Il y a eu une erreur lors de la recherche de la page."
    date1, date2=randint(0,len(table[option])-1),randint(0,len(table[option])-1)
    while date2==date1:
        date2=randint(0,len(table[option])-1)
    listeDates=[date1,date2]
    listeDates.sort()
    for i in range(2):
        descip+="**"+table[option][listeDates[i]]["year"]+": **"+table[option][listeDates[i]]["description"]+"\n"
        for k in range(len(table[option][listeDates[i]]["wikipedia"])):
            hyper+="["+table[option][listeDates[i]]["wikipedia"][k]["title"]+"]("+table[option][listeDates[i]]["wikipedia"][k]["wikipedia"]+"), "
    embedW=discord.Embed(title=jour+" "+tableauMois[mois],description=descip+"\nRéférences : "+hyper[0:len(hyper)-2],color=0xfcfcfc)
    embedW.set_footer(text="OT!events - "+option)
    embedW=auteur(table["wikipedia"],0,0,embedW,"wp")
    return embedW

async def autoEvents(bot,channel,guild):
    connexionCMD,curseurCMD=connectSQL(guild,"Commandes","Guild",None,None)
    embed=await embedWikiEvents("events",strftime("%d"),strftime("%m"))
    message=await bot.get_channel(channel).send(embed=embed)
    await message.add_reaction("<:otRELOAD:772766034356076584>")
    curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'wikipedia','events','events','{2}','{3}','None',1,1,'None',False)".format(message.id,bot.user.id,strftime("%d"),strftime("%m")))
    connexionCMD.commit()

async def exeWikipedia(ctx,bot,option,turn,ligne):
    if option in ("events","search"):
        connexionCMD,curseurCMD=connectSQL(ctx.guild.id,"Commandes","Guild",None,None)
    try:
        if ligne==None:
            args=createPhrase(ctx.args[2:len(ctx.args)])[0:-1]
            try:
                args=dictOption[args]
            except:
                args="events"
            embedF=await embedWikiEvents(args,strftime("%d"),strftime("%m"))

            message=await ctx.send(embed=embedF)
            await message.add_reaction("<:otRELOAD:772766034356076584>")
            curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'wikipedia','events','{2}','{3}','{4}','None',1,1,'None',False)".format(message.id,ctx.author.id,args,strftime("%d"),strftime("%m")))
            connexionCMD.commit()
        else:
            embedF=await embedWikiEvents(ligne["Args1"],ligne["Args2"],ligne["Args3"])
            await ctx.message.edit(embed=embedF)
        
    except AssertionError as er:
        await ctx.send(embed=embedAssert(str(er)))
    except asyncio.exceptions.TimeoutError:
        await ctx.send(embed=embedAssert("Temps de requête écoulé, veuillez réessayer."))
    except:
        await ctx.send(embed=await exeErrorExcept(ctx,bot,""))
