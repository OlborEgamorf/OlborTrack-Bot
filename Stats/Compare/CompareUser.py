
from time import strftime

import discord
from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.Embeds import addtoFields, countRankCompare, createFields, embedAssert, newDescip, sendEmbed
from Core.Fonctions.GetNom import getObj, nomsOptions
from Core.Fonctions.GetPeriod import getAnnee, getMois
from Core.Fonctions.setMaxPage import setMax, setPage
from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.DichoTri import triPeriod
from Stats.SQL.Verification import verifCommands

tableauMois={"01":"Janvier","02":"Février","03":"Mars","04":"Avril","05":"Mai","06":"Juin","07":"Juillet","08":"Aout","09":"Septembre","10":"Octobre","11":"Novembre","12":"Décembre","TO":"Année","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","glob":"GL","to":"TO","GL":"GL"}
dictTriArg={"countAsc":"Count","rankAsc":"Rank","countDesc":"Count","rankDesc":"Rank","dateAsc":"DateID","dateDesc":"DateID","periodAsc":"None","periodDesc":"None","moyDesc":"Moyenne","nombreDesc":"Nombre"}
dictTriSens={"countAsc":"ASC","rankAsc":"ASC","countDesc":"DESC","rankDesc":"DESC","dateAsc":"ASC","dateDesc":"DESC","periodAsc":"None","periodDesc":"None","moyDesc":"DESC","nombreDesc":"DESC"}
dictNameF3={"Messages":"Messages","Salons":"Messages","Freq":"Messages","Mots":"Mots","Emotes":"Utilisations","Reactions":"Utilisations","Voice":"Temps","Voicechan":"Temps","Mentions":"Mentions","Mentionne":"Mentions","Divers":"Nombre"}
dictTriField={"countAsc":"Compteur {0} croissant","rankAsc":"Rang {0} croissant","countDesc":"Compteur {0} décroissant","rankDesc":"Rang {0} décroissant","periodAsc":"Date {0} croissante","periodDesc":"Date {0} décroissante"}


async def compareUser(ctx,option,turn,react,ligne,guildOT,bot):
    try:
        assert verifCommands(guildOT,option)
        connexionCMD,curseurCMD=connectSQL(ctx.guild.id,"Commandes","Guild",None,None)
        if not react:
            assert ctx.message.mentions!=[]
            mention=ctx.message.mentions[0].id
            assert not guildOT.users[mention]["Hide"]
            if getObj(option,ctx,2)==None:
                if option in ("Messages","Mots","Voice"):
                    curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'compareUser','{2}','user','{3}','None','None',1,1,'countDesc',False)".format(ctx.message.id,ctx.author.id,option,mention))
                else:
                    if len(ctx.args)==2 or ctx.args[2].lower() not in ("mois","annee"):
                        try:
                            mois,annee=tableauMois[getMois(ctx.args[2].lower())],getAnnee(ctx.args[3].lower())
                        except:
                            try:
                                mois,annee="TO",getAnnee(ctx.args[2].lower())
                            except:
                                mois,annee="TO","GL"
                    elif ctx.args[2].lower()=="mois":
                        mois,annee=strftime("%m").lower(),strftime("%y")
                    elif ctx.args[2].lower()=="annee":
                        mois,annee="TO",strftime("%y")
                    curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'compareUser','{2}','userPeriod','{3}','{4}','{5}',1,1,'countDesc',False)".format(ctx.message.id,ctx.author.id,option,mois,annee,mention))
            else:
                obj=getObj(option,ctx,2)
                curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'compareUser','{2}','userObj','{3}','{4}','None',1,1,'countDesc',False)".format(ctx.message.id,ctx.author.id,option,mention,obj))
            ligne=curseurCMD.execute("SELECT * FROM commandes WHERE MessageID={0}".format(ctx.message.id)).fetchone()

        if ligne["Args1"]=="user":
            connexion,curseur=connectSQL(ctx.guild.id,option,"Stats","GL","")
            pagemax=setMax(curseur.execute("SELECT COUNT() as Nombre FROM persoM{0}".format(ligne["AuthorID"])).fetchone()["Nombre"])+1
            nom,mention,obj="persoM",ligne["Args2"],""
            titre="Comparaison membres, périodes\n{0}".format(option)
        elif ligne["Args1"]=="userPeriod":
            mois,annee=ligne["Args2"],ligne["Args3"]
            connexion,curseur=connectSQL(ctx.guild.id,option,"Stats",mois,annee)
            pagemax=setMax(curseur.execute("SELECT COUNT() as Nombre FROM perso{0}{1}{2}".format(mois,annee,ligne["AuthorID"])).fetchone()["Nombre"])
            nom,mention,obj="perso{0}{1}".format(mois,annee),ligne["Args4"],""
            titre="Comparaison membres, perso, {0}/{1}\n{2}".format(mois,annee,option)
        else:
            connexion,curseur=connectSQL(ctx.guild.id,option,"Stats","GL","")
            pagemax=setMax(curseur.execute("SELECT COUNT() as Nombre FROM persoM{0}{1}".format(ligne["AuthorID"],ligne["Args3"])).fetchone()["Nombre"])+1
            nom,mention,obj="persoM",ligne["Args2"],ligne["Args3"]
            titre="Comparaison membres, périodes\n{0}".format(option)
        
        page=setPage(ligne["Page"],pagemax,turn)
        if ligne["Args1"] in ("user","userObj") and page==pagemax:
            ligne["Tri"]="countDesc"
            nom="persoA"

        embed=embedCompare(nom,ligne["AuthorID"],mention,option,ligne["Args1"],curseur,ligne,page,guildOT,bot,obj)
        if obj=="":
            embed.description="{0}, {1}".format(nomsOptions("Messages",int(ligne["AuthorID"]),guildOT,bot),newDescip(embed.description,"Messages",mention,guildOT,bot))
        else:
            if option in ("Salons","Voicechan"):
                assert not guildOT.chan[int(obj)]["Hide"]
            embed.description="{0}, {1}, {2}".format(nomsOptions("Messages",int(ligne["AuthorID"]),guildOT,bot),nomsOptions("Messages",int(mention),guildOT,bot),newDescip(embed.description,option,obj,guildOT,bot))
        embed=auteur(ctx.guild.id,ctx.guild.name,ctx.guild.icon,embed,"guild")
        embed.colour=0x3498db
        embed.title=titre
        embed.add_field(name="Tri <:otTRI:833666016491864114>",value=dictTriField[ligne["Tri"]].format(nomsOptions("Messages",int(ligne["AuthorID"]),guildOT,bot)),inline=True)
        embed.set_footer(text="Page {0}/{1}".format(page,pagemax))

        await sendEmbed(ctx,embed,react,True,curseurCMD,connexionCMD,page,pagemax)
    except:
        if react:
            await ctx.reply(embed=embedAssert("Impossible de trouver ce que vous cherchez.\nSoit le module de stats est désactivé, soit le classement cherché n'existe plus ou alors est masqué par un administrateur."))
        else:
            await ctx.reply(embed=embedAssert("Impossible de trouver ce que vous cherchez.\nSoit le module de stats est désactivé, soit le classement cherché n'existe pas ou alors est masqué par un administrateur.\nVérifiez les arguments de la commande : {0}".format(ctx.command.usage)))
        

def embedCompare(nom,id1,id2,option,optionCompare,curseur,ligne,page,guildOT,bot,obj):
    embed=discord.Embed()
    field1,field2,field3="","",""
    tri=ligne["Tri"]
    mobile=ligne["Mobile"]
    if optionCompare in ("user","userObj"):
        if tri in ("periodAsc","periodDesc"):
            table=triPeriod(curseur,"{0}{1}{2}".format(nom,id1,obj),tri)
        else:
            table=curseur.execute("SELECT * FROM {0}{1}{2} ORDER BY {3} {4}".format(nom,id1,obj,dictTriArg[tri],dictTriSens[tri])).fetchall()
        if nom=="persoA":
            page=1
        stop=15*page if 15*page<len(table) else len(table)
        for i in range(15*(page-1),stop):
            if table[i]["Annee"]=="GL":
                period="Général"
            else:
                period="{0} 20{1}".format(tableauMois[table[i]["Mois"]],table[i]["Annee"])
            table2=curseur.execute("SELECT * FROM {0}{1}{2} WHERE Mois='{3}' AND Annee='{4}'".format(nom,id2,obj,table[i]["Mois"],table[i]["Annee"])).fetchone()
            rang1,rang2,count1,count2=countRankCompare(table,table2,i,option)
            field1,field2,field3=addtoFields(field1,field2,field3,mobile,period,"{0} | {1}".format(rang1,count1),"{0} | {1}".format(rang2,count2))
        nomF1="Période"
    elif optionCompare=="userPeriod":
        table=curseur.execute("SELECT * FROM {0}{1} ORDER BY {2} {3}".format(nom,id1,dictTriArg[tri],dictTriSens[tri])).fetchall()
        stop=15*page if 15*page<len(table) else len(table)
        for i in range(15*(page-1),stop):
            nom2=nomsOptions(option,table[i]["ID"],guildOT,bot)
            table2=curseur.execute("SELECT * FROM {0}{1} WHERE ID={2}".format(nom,id2,table[i]["ID"])).fetchone()
            rang1,rang2,count1,count2=countRankCompare(table,table2,i,option)
            field1,field2,field3=addtoFields(field1,field2,field3,mobile,nom2,"{0} | {1}".format(rang1,count1),"{0} | {1}".format(rang2,count2))
        nomF1=option
    
    user1=bot.get_user(int(id1))
    user2=bot.get_user(int(id2))
    if user1!=None:
        nomU1=user1.name
    else:
        nomU1="??"
    if user2!=None:
        nomU2=user2.name
    else:
        nomU2="??"
    
    embed=createFields(mobile,embed,field1,field2,field3,nomF1,nomU1,nomU2)

    return embed
