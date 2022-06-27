from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.Embeds import embedAssertClassic, newDescip
from Core.Fonctions.GetTable import getTablePerso
from Core.Fonctions.SendView import sendView
from Core.Fonctions.setMaxPage import setMax, setPage
from Stats.Embeds.Mois import embedMois
from Stats.SQL.ConnectSQL import connectSQL

dictTriField={"countAsc":"Compteur croissant","rankAsc":"Rang croissant","countDesc":"Compteur décroissant","rankDesc":"Rang décroissant","dateAsc":"Date croissante","dateDesc":"Date décroissante","periodAsc":"Date croissante","periodDesc":"Date décroissante","moyDesc":"Moyenne décroissante","nombreDesc":"Compteur décroissant","winAsc":"Victoires croissant","winDesc":"Victoires décroissant","loseAsc":"Défaites croissant","loseDesc":"Défaites décroissant","expDesc":"Expérience décroissant","expAsc":"Expérience croissant"}

async def statsPeriodsView(interaction,curseurCMD,connexionCMD,turn,ligne,guildOT,bot):
    try:
        connexionCMD,curseurCMD=connectSQL(interaction.guild_id,"Commandes","Guild",None,None)
        author=ligne["AuthorID"]
        option=ligne["Option"]

        if option in ("Salons","Voicechan"):
            assert not guildOT.chan[int(author)]["Hide"]

        table=getTablePerso(interaction.guild_id,option,author,False,"M",ligne["Tri"])
        pagemax=setMax(len(table))+1
        page=setPage(ligne["Page"],pagemax,turn)

        if page==pagemax:
            table=getTablePerso(interaction.guild_id,option,author,False,"A","countDesc")
            embed=embedMois(table,1,ligne["Mobile"],ligne["Option"])
            embed.add_field(name="Tri <:otTRI:833666016491864114>",value=dictTriField["countDesc"],inline=True)
            embed.set_footer(text="Page {0}/{1}".format(page,pagemax))
        else:
            embed=embedMois(table,page,ligne["Mobile"],ligne["Option"])
            embed.add_field(name="Tri <:otTRI:833666016491864114>",value=dictTriField[ligne["Tri"]],inline=True)
            embed.set_footer(text="Page {0}/{1}".format(page,pagemax))
            
        embed.title="Périodes {0}".format(option.lower())
        if option in ("Voice","Messages","Mots","Mentions","Mentionne"):
            user=interaction.guild.get_member(author)
            if user!=None:
                embed=auteur(user.id,user.name,user.avatar,embed,"user")
                embed.colour=user.color.value
            else:
                embed=auteur(bot.user.id,"Ancien membre",bot.user.avatar,embed,"user")
                embed.colour=0x3498dbed.colour=user.color.value
        else:
            embed.description=newDescip(embed.description,option,author,guildOT,bot)
            embed=auteur(interaction.guild_id,interaction.guild.name,interaction.guild.icon,embed,"guild")
            embed.colour=0x3498db
        await sendView(interaction,embed,curseurCMD,connexionCMD,page,pagemax)
        
    except:
        await interaction.response.send_message(embed=embedAssertClassic("Impossible de trouver ce que vous cherchez.\nSoit le module de stats est désactivé, soit la table cherchée n'existe plus ou alors est masqué par un administrateur."))
 
