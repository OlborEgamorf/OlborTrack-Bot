from time import strftime

import discord
from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.Embeds import addtoFields, countRankCompare, createFields, embedAssert, newDescip, sendEmbed
from Core.Fonctions.GetNom import getNomGraph, getObj, nomsOptions
from Core.Fonctions.GetPeriod import getAnnee, getMois
from Core.Fonctions.setMaxPage import setMax, setPage
from Stats.SQL.ConnectSQL import connectSQL
from discord.ext import commands
from Stats.SQL.Verification import verifCommands

tableauMois={"01":"Janvier","02":"Février","03":"Mars","04":"Avril","05":"Mai","06":"Juin","07":"Juillet","08":"Aout","09":"Septembre","10":"Octobre","11":"Novembre","12":"Décembre","TO":"Année","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","glob":"GL","to":"TO","GL":"GL"}
dictTriArg={"countAsc":"Count","rankAsc":"Rank","countDesc":"Count","rankDesc":"Rank","dateAsc":"DateID","dateDesc":"DateID","periodAsc":"None","periodDesc":"None","moyDesc":"Moyenne","nombreDesc":"Nombre"}
dictTriSens={"countAsc":"ASC","rankAsc":"ASC","countDesc":"DESC","rankDesc":"DESC","dateAsc":"ASC","dateDesc":"DESC","periodAsc":"None","periodDesc":"None","moyDesc":"DESC","nombreDesc":"DESC"}
dictNameF3={"Messages":"Messages","Salons":"Messages","Freq":"Messages","Mots":"Mots","Emotes":"Utilisations","Reactions":"Utilisations","Voice":"Temps","Voicechan":"Temps","Mentions":"Mentions","Mentionne":"Mentions","Divers":"Nombre"}
dictTriField={"countAsc":"Compteur {0} croissant","countDesc":"Compteur {0} décroissant"}

async def compareRank(ctx,option,turn,react,ligne,guildOT,bot):
    try:
        assert verifCommands(guildOT,option)
        connexionCMD,curseurCMD=connectSQL(ctx.guild.id,"Commandes","Guild",None,None)
        if not react:
            if len(ctx.args)==2 or ctx.args[2].lower() not in ("mois","annee"):
                try:
                    mois,annee,obj1,obj2=getMois(ctx.args[2].lower()),getAnnee(ctx.args[3].lower()),getObj(option,ctx,4),getObj(option,ctx,5)
                except:
                    try:
                        mois,annee,obj1,obj2="to",getAnnee(ctx.args[2].lower()),getObj(option,ctx,3),getObj(option,ctx,4)
                    except:
                        mois,annee,obj1,obj2="glob","",getObj(option,ctx,2),getObj(option,ctx,3)
            elif ctx.args[2].lower()=="mois":
                mois,annee,obj1,obj2=tableauMois[strftime("%m")].lower(),strftime("%y"),getObj(option,ctx,3),getObj(option,ctx,4)
            elif ctx.args[2].lower()=="annee":
                mois,annee,obj1,obj2="to",strftime("%y"),getObj(option,ctx,3),getObj(option,ctx,4)
            
            if option=="Salons":
                obj2=ctx.message.channel_mentions[1].id

            assert obj2!=None and obj1!=None
            curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'compareRank','{2}','{3}','{4}','{5}','{6}',1,1,'countDesc',False)".format(ctx.message.id,ctx.author.id,option,mois,annee,obj1,obj2))
            ligne=curseurCMD.execute("SELECT * FROM commandes WHERE MessageID={0}".format(ctx.message.id)).fetchone()
        else:
            mois,annee,obj1,obj2=ligne["Args1"],ligne["Args2"],int(ligne["Args3"]),int(ligne["Args4"])
            
        connexion,curseur=connectSQL(ctx.guild.id,option,"Stats",tableauMois[mois],annee)
        pagemax=setMax(curseur.execute("SELECT COUNT() as Nombre FROM {0}{1}{2}".format(mois,annee,obj1)).fetchone()["Nombre"])
        page=setPage(ligne["Page"],pagemax,turn)

        embed=embedCompare(mois,annee,curseur,obj1,obj2,ligne,page,guildOT,bot,option,ctx)
        embed.description="{0}, {1}".format(nomsOptions(option,int(obj1),guildOT,bot),newDescip(embed.description,option,int(obj2),guildOT,bot))
        embed=auteur(ctx.guild.id,ctx.guild.name,ctx.guild.icon,embed,"guild")
        embed.colour=0x3498db

        if mois=="glob":
            title="Comparaison rangs, classement général\n{0}".format(option)
        elif mois=="to":
            title="Comparaison rangs, classement 20{0}\n{1}".format(annee,option)
        else:
            title="Comparaison rangs, classement {0} 20{1}\n{2}".format(mois,annee,option)

        embed.title=title
        embed.add_field(name="Tri <:otTRI:833666016491864114>",value=dictTriField[ligne["Tri"]].format(nomsOptions(option,int(obj1),guildOT,bot)),inline=True)
        embed.set_footer(text="Page {0}/{1}".format(page,pagemax))

        await sendEmbed(ctx,embed,react,True,curseurCMD,connexionCMD,page,pagemax)
    except:
        if react:
            await ctx.reply(embed=embedAssert("Impossible de trouver ce que vous cherchez.\nSoit le module de stats est désactivé, soit le classement cherché n'existe plus."))
        else:
            await ctx.reply(embed=embedAssert("Impossible de trouver ce que vous cherchez.\nSoit le module de stats est désactivé, soit le classement cherché n'existe pas.\nVérifiez les arguments de la commande : {0}".format(ctx.command.usage)))

def embedCompare(mois,annee,curseur,obj1,obj2,ligne,page,guildOT,bot,option,ctx):
    embed=discord.Embed()
    field1,field2,field3="","",""
    tri=ligne["Tri"]
    mobile=ligne["Mobile"]
    table=curseur.execute("SELECT * FROM {0}{1}{2} ORDER BY {3} {4}".format(mois,annee,obj1,dictTriArg[tri],dictTriSens[tri])).fetchall()
    stop=15*page if 15*page<len(table) else len(table)
    for i in range(15*(page-1),stop):
        nom=nomsOptions("Messages",table[i]["ID"],guildOT,bot)
        table2=curseur.execute("SELECT * FROM {0}{1}{2} WHERE ID={3}".format(mois,annee,obj2,table[i]["ID"])).fetchone()
        rang1,rang2,count1,count2=countRankCompare(table,table2,i,option)
        field1,field2,field3=addtoFields(field1,field2,field3,mobile,nom,"{0} | {1}".format(rang1,count1),"{0} | {1}".format(rang2,count2))

    embed=createFields(mobile,embed,field1,field2,field3,"Membre",getNomGraph(ctx,bot,option,int(obj1)),getNomGraph(ctx,bot,option,int(obj2)))
    return embed