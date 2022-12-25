import discord
from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.Embeds import embedAssertClassic
from Core.Fonctions.GetTable import getTablePerso
from Core.Fonctions.setMaxPage import setMax
from Core.OTGuild import OTGuild
from Stats.Embeds.Central import statsEmbed
from Stats.SQL.ConnectSQL import CustomCursor

tableauMois={"01":"Janvier","02":"Février","03":"Mars","04":"Avril","05":"Mai","06":"Juin","07":"Juillet","08":"Aout","09":"Septembre","10":"Octobre","11":"Novembre","12":"Décembre","TO":"Année","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","glob":"GL","to":"TO"}
dictColumn = {"Messages":"User","Salons":"Salon","Voice":"User","Voicechan":"Salon"}

async def statsPerso(interID:int,interaction:discord.Interaction,guildOT:OTGuild,bot,curseur:CustomCursor,ligne:dict):
    if True:
        mois,annee = ligne["Args1"], ligne["Args2"]
        option = ligne["Option"]
        author=ligne["AuthorID"]

        table = getTablePerso(curseur,option,author,mois,annee,"Salon")
        pagemax=setMax(len(table))
        page=ligne["Page"]
        ligne["PageMax"] = pagemax

        curseur.execute("UPDATE commandes SET PageMax={0} WHERE MessageID={1}".format(pagemax,interID))

        if pagemax == 1:
            table = table[:15]
        elif page == pagemax:
            table = table[15*(page-1):]
        else:
            table = table[15*(page-1):15*(page)]

        if mois != "None":
            title="Perso {0} {1} 20{2}".format(option.lower(),tableauMois[mois].lower(),annee)       
        elif annee != "None":
            title="Perso {0} 20{1}".format(option.lower(),annee)
        else:
            title="Perso général {0}".format(option.lower())

        embed=await statsEmbed("perso{0}{1}{2}".format(mois,annee,author),ligne,page,pagemax,option,guildOT,bot,False,False,curseur)
        embed.title=title
        user=interaction.guild.get_member(author)
        if user!=None:
            embed=auteur(user.name,user.avatar,embed,"user")
            embed.colour=user.color.value
        else:
            embed=auteur("Ancien membre",bot.user.avatar,embed,"user")
            embed.colour=0x3498db
        return await statsEmbed(interaction,guildOT,bot,table,ligne,"user",title,option,dictColumn[option])
        
    else:
        return embedAssertClassic("Impossible de trouver ce que vous cherchez.\nSoit le module de stats est désactivé, soit la table cherchée cherché n'existe pas.")
