from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.Embeds import embedAssertClassic, sendEmbed
from Core.Fonctions.setMaxPage import setMax, setPage
from Stats.Embeds.Central import statsEmbed
from Stats.SQL.ConnectSQL import connectSQL

tableauMois={"01":"Janvier","02":"Février","03":"Mars","04":"Avril","05":"Mai","06":"Juin","07":"Juillet","08":"Aout","09":"Septembre","10":"Octobre","11":"Novembre","12":"Décembre","TO":"Année","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","glob":"GL","to":"TO"}
dictOption={"tortues":"Tortues","tortuesduo":"TortuesDuo","trivialversus":"TrivialVersus","trivialbr":"TrivialBR","trivialparty":"TrivialParty","p4":"P4","bataillenavale":"BatailleNavale"}
dictNoms={"culture":0,"divertissement":1,"sciences":2,"mythologie":3,"sport":4,"géographie":5,"histoire":6,"politique":7,"art":8,"célébrités":9,"animaux":10,"véhicules":11,"streak":"Streak"}

async def statsTrivial(ctx,turn,react,ligne,bot,option):
    try:
        connexionCMD,curseurCMD=connectSQL(ctx.guild.id,"Commandes","Guild",None,None)
        if not react:
            if option=="trivialperso":
                table="trivial{0}".format(ctx.author.id)
                db=ctx.author.id
                mode="perso"
                tri="expDesc"
            else:
                db="ranks"
                tri="countDesc"
                if len(ctx.args)>2:
                    table="trivial{0}".format(dictNoms[ctx.args[2].lower()])
                    mode=ctx.args[2].lower()
                else:
                    table="trivial12"
                    mode="général"

            curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'trivial','{2}','{3}','{4}','{5}','None',1,1,'{6}',False)".format(ctx.message.id,ctx.author.id,option,db,table,mode,tri))
            ligne=curseurCMD.execute("SELECT * FROM commandes WHERE MessageID={0}".format(ctx.message.id)).fetchone()
        else:
            db,table,mode=ligne["Args1"],ligne["Args2"],ligne["Args3"]
        
        connexion,curseur=connectSQL("OT",db,"Trivial",None,None)

        pagemax=setMax(curseur.execute("SELECT COUNT() as Nombre FROM {0}".format(table)).fetchone()["Nombre"])

        page=setPage(ligne["Page"],pagemax,turn)

        embed=await statsEmbed(table,ligne,page,pagemax,option,ctx.guild,bot,False,False,curseur)
        embed.title="Classement Trivial Mondial {0}".format(mode)
        if option=="trivialperso":
            user=ctx.guild.get_member(ligne["AuthorID"])
            embed=auteur(user.name,user.avatar,embed,"user")
        else:
            embed=auteur("Olbor Track Bot",interaction.guild.get_member(699728606493933650).display_avatar,embed,"user")
        embed.colour=0x3498db
        await sendEmbed(ctx,embed,react,True,curseurCMD,connexionCMD,page,pagemax)
    except:
        if react:
            await ctx.reply(embed=embedAssertClassic("Impossible de trouver ce que vous cherchez.\nLe classement cherché n'existe plus ou alors il y a un problème de mon côté."))
        else:
            await ctx.reply(embed=embedAssertClassic("Impossible de trouver ce que vous cherchez.\Le classement cherché n'existe pas ou alors il y a un problème de mon côté.\nVérifiez les arguments de la commande : {0}".format(ctx.command.usage)))
