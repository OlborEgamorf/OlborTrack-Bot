from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.Embeds import (addtoFields, createEmbed, createFields,
                                   embedAssert, sendEmbed)
from Core.Fonctions.setMaxPage import setMax, setPage
from Stats.SQL.ConnectSQL import connectSQL
import discord

dictSell={1:150,2:400,3:2500,0:"Aucune"}
dictValue={0:"?",1:300,2:800,3:5000}
dictStatut={0:"Fabuleux",1:"Rare",2:"Légendaire",3:"Unique"}

async def commandeTMP(ctx,turn,react,ligne,option):
    connexionCMD,curseurCMD=connectSQL(ctx.guild.id,"Commandes","Guild",None,None)
    connexion,curseur=connectSQL("OT","Titres","Titres",None,None)
    if not react:
        table=getTableTitres(curseur,option,ctx.author.id)
        assert table!=[], "Cette liste est vide."
        pagemax=setMax(len(table))
        curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'titres','{2}','None','None','None','None',1,{3},'countDesc',False)".format(ctx.message.id,ctx.author.id,option,pagemax))
        ligne=curseurCMD.execute("SELECT * FROM commandes WHERE MessageID={0}".format(ctx.message.id)).fetchone()
    else:
        table=getTableTitres(curseur,option,ligne["AuthorID"])
        pagemax=setMax(len(table))

    page=setPage(ligne["Page"],pagemax,turn)
    if option=="user":
        embed=embedTUser(table,page,ligne["Mobile"])
        user=ctx.guild.get_member(ligne["AuthorID"])
        embed=auteur(user.id,user.name,user.avatar,embed,"user")
    else:
        embed=embedTMP(table,page,ligne["Mobile"])
        embed=auteur(ctx.guild.get_member(699728606493933650),None,None,embed,"olbor")
    embed.set_footer(text="Page {0}/{1}".format(page,pagemax))
    if option=="marketplace":
        embed.title="Titres en vente aujourd'hui"
    else:
        embed.title="Liste des titres existants"
    embed.color=0xf58d1d
    
    message=await sendEmbed(ctx,embed,react,False,curseurCMD,connexionCMD,page,pagemax)
    if not react:
        await message.add_reaction("<:otMOBILE:833736320919797780>")
    
def getTableTitres(curseur,option,author):
    if option=="marketplace":
        table=curseur.execute("SELECT marketplace.ID,marketplace.Stock,titres.Rareté,titres.Nom,marketplace.Known FROM marketplace JOIN titres ON marketplace.ID=titres.ID ORDER BY Rareté DESC").fetchall()
    elif option=="user":
        connexionUser,curseurUser=connectSQL("OT",author,"Titres",None,None)
        table=curseurUser.execute("SELECT * FROM titresUser").fetchall()
    else:
        table=curseur.execute("SELECT * FROM titres ORDER BY Rareté DESC").fetchall()
    return table

def embedTMP(table,page,mobile):
    embed=discord.Embed()
    field1,field2,field3="","",""
    stop=15*page if 15*page<len(table) else len(table)
    for i in range(15*(page-1),stop):
        if table[i]["Known"]==True:
            nom="__{0}__ - {1}".format(table[i]["ID"],table[i]["Nom"])
            stock=table[i]["Stock"]
            statut="{0} <:otCOINS:873226814527520809> - {1}".format(dictValue[table[i]["Rareté"]],dictStatut[table[i]["Rareté"]])
            if table[i]["Stock"]==0:
                nom="~~{0}~~".format(nom)
                stock="~~{0}~~".format(stock)
                statut="~~{0}~~".format(statut)
            field1,field2,field3=addtoFields(field1,field2,field3,mobile,nom,stock,statut)
        else:
            field1,field2,field3=addtoFields(field1,field2,field3,mobile,"__{0}__ - ??".format(table[i]["ID"]),table[i]["Stock"],"{0} <:otCOINS:873226814527520809> - {1}".format(dictValue[table[i]["Rareté"]],dictStatut[table[i]["Rareté"]]))
    
    embed=createFields(mobile,embed,field1,field2,field3,"ID - Titre","Stock","Prix <:otCOINS:873226814527520809> - Type") 
    return embed

def embedTUser(table,page,mobile):
    embed=discord.Embed()
    field1,field2,field3="","",""
    stop=15*page if 15*page<len(table) else len(table)
    for i in range(15*(page-1),stop):
        nom="__{0}__ - {1}".format(table[i]["ID"],table[i]["Nom"])
        value="{0} <:otCOINS:873226814527520809>".format(dictSell[table[i]["Rareté"]])
        statut=dictStatut[table[i]["Rareté"]]
        
        field1,field2,field3=addtoFields(field1,field2,field3,mobile,nom,value,statut)
    
    embed=createFields(mobile,embed,field1,field2,field3,"ID - Titre","Valeur vente <:otCOINS:873226814527520809>","Type") 
    return embed