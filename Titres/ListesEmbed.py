import discord
from Core.Fonctions.Embeds import addtoFields, createFields
from Stats.SQL.ConnectSQL import connectSQL

dictStatut={0:"Spécial",1:"Basique",2:"Rare",3:"Légendaire",4:"Haut-Fait",5:"Unique",6:"Fabuleux"}
dictSell={0:"Inestimable",1:150,2:300,3:500,4:"Inestimable",5:"Inestimable",6:"Inestimable"}
dictValue={0:"Inestimable",1:300,2:600,3:1000,4:"Inestimable",5:2500,6:"Inestimable"}

def getTableTitres(curseur,option,author):
    if option=="marketplace":
        table=curseur.execute("SELECT marketplace.ID,marketplace.Stock,titres.Rareté,titres.Nom,marketplace.Known FROM marketplace JOIN titres ON marketplace.ID=titres.ID ORDER BY Rareté DESC").fetchall()
    elif option=="user":
        connexionUser,curseurUser=connectSQL("OT",author,"Titres",None,None)
        table=curseurUser.execute("SELECT * FROM titresUser").fetchall()
    else:
        table=curseur.execute("SELECT * FROM titres ORDER BY Rareté ASC").fetchall()
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
