import discord
from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.GetPeriod import getMois
from Core.Fonctions.GetNom import getObj, nomsOptions
from Core.Fonctions.AuteurIcon import auteur

tableauMois={"01":"Janvier","02":"Février","03":"Mars","04":"Avril","05":"Mai","06":"Juin","07":"Juillet","08":"Aout","09":"Septembre","10":"Octobre","11":"Novembre","12":"Décembre","TO":"Année","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","glob":"GL","to":"TO"}

async def statsFirst(ctx,option,guildOT,bot):
    descip=""
    mois=getMois(ctx.args[2].lower())
    obj=getObj(option,ctx,3)
    tempOption=option
    if obj==None:
        obj=""
    else:
        option="Messages"
    connexion,curseur=connectSQL(ctx.guild.id,option,"Stats","GL","")
    if obj=="":
        for i in curseur.execute("SELECT * FROM firstM WHERE Mois='{0}'".format(tableauMois[mois])).fetchall():
            descip+="20{0} : {1} - {2}\n".format(i["Annee"],nomsOptions(option,i["ID"],guildOT,bot),i["Count"])
    else:
        dates=curseur.execute("SELECT DISTINCT Annee FROM firstA ORDER BY Annee ASC").fetchall()
        for i in dates:
            try:
                connexion,curseur=connectSQL(ctx.guild.id,option,"Stats",tableauMois[mois],i["Annee"])
                ligne=curseur.execute("SELECT * FROM {0}{1}{2} WHERE Rank=1".format(mois,i["Annee"],obj)).fetchone()
                descip+="20{0} : {1} - {2}\n".format(i["Annee"],nomsOptions(option,ligne["ID"],guildOT,bot),ligne["Count"])
            except:
                pass
    assert descip!=""
    if obj!="":
        descip="{0}\n\n{1}".format(nomsOptions(tempOption,int(obj),guildOT,bot),descip)
    embed=discord.Embed(title="Premiers en {0}, {1}".format(mois,tempOption.lower()),description=descip,color=0x3498db)
    embed=auteur(ctx.guild.id,ctx.guild.name,ctx.guild.icon,embed,"guild")
    embed.set_footer(text="Page 1/1")
    await ctx.reply(embed=embed)