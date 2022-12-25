import discord
from Core.Fonctions.Embeds import embedAssertClassic
from Core.Fonctions.GetTable import getTablePeriodsInter
from Core.Fonctions.setMaxPage import setMax
from Core.OTGuild import OTGuild
from Stats.Embeds.Central import statsEmbed
from Stats.SQL.ConnectSQL import CustomCursor

dictColumn = {"Messages":"User","Salons":"Salon","Voice":"User","Voicechan":"Salon"}

async def statsPeriodsInter(interID:int,interaction:discord.Interaction,guildOT:OTGuild,bot,curseur:CustomCursor,ligne:dict):
    if True:
        author=ligne["AuthorID"]
        obj=ligne["Args3"]
        option=ligne["Option"]

        if option in ("Salons","Voicechan"):
            assert not guildOT.chan[int(obj)]["Hide"]

        table=getTablePeriodsInter(curseur,option,author,obj,"M",dictColumn[option],ligne["Tri"])

        pagemax=setMax(len(table))
        page=ligne["Page"]
        ligne["PageMax"] = pagemax+1

        curseur.execute("UPDATE commandes SET PageMax={0} WHERE MessageID={1}".format(pagemax+1,interID))

        if pagemax == 1:
            table = table[:15]
        elif page == pagemax:
            table = table[15*(page-1):]
        elif page > pagemax:
            table=getTablePeriodsInter(curseur,option,author,obj,"A",dictColumn[option],ligne["Tri"])
        else:
            table = table[15*(page-1):15*(page)]

        return await statsEmbed(interaction,guildOT,bot,table,ligne,"user","Périodes {0}".format(option.lower()),option,"Mois",obj=obj)
        
    else:
        return embedAssertClassic("Impossible de trouver ce que vous cherchez.\nSoit le module de stats est désactivé, soit la table cherchée cherché n'existe pas ou alors est masqué par un administrateur.")
