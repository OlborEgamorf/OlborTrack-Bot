from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.Embeds import embedAssertClassic, newDescip
from Core.Fonctions.GetTable import getTablePerso
from Core.Fonctions.setMaxPage import setMax
from Core.Fonctions.SendSlash import sendSlash
from Stats.Embeds.Mois import embedMois
from Stats.SQL.ConnectSQL import connectSQL
from Stats.SQL.Verification import verifCommands

dictTriField={"countAsc":"Compteur croissant","rankAsc":"Rang croissant","countDesc":"Compteur décroissant","rankDesc":"Rang décroissant","dateAsc":"Date croissante","dateDesc":"Date décroissante","periodAsc":"Date croissante","periodDesc":"Date décroissante","moyDesc":"Moyenne décroissante","nombreDesc":"Compteur décroissant","winAsc":"Victoires croissant","winDesc":"Victoires décroissant","loseAsc":"Défaites croissant","loseDesc":"Défaites décroissant","expDesc":"Expérience décroissant","expAsc":"Expérience croissant"}

async def statsPeriodsInter(interaction,option,obj,guildOT,bot):
    try:
        assert verifCommands(guildOT,option)
        connexionCMD,curseurCMD=connectSQL(interaction.guild_id,"Commandes","Guild",None,None)

        author=interaction.user.id
        obj=obj.id
        assert obj!=None
        curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'periodsInter','{2}','{3}','None','None','None',1,1,'countDesc',False)".format(interaction.id,author,option,obj))
        ligne=curseurCMD.execute("SELECT * FROM commandes WHERE MessageID={0}".format(interaction.id)).fetchone()

        if option in ("Salons","Voicechan"):
            assert not guildOT.chan[int(obj)]["Hide"]
        table=getTablePerso(interaction.guild_id,option,author,obj,"M",ligne["Tri"])
        pagemax=setMax(len(table))+1
        page=1

        if page==pagemax:
            table=getTablePerso(interaction.guild_id,option,author,obj,"A","countDesc")
            embed=embedMois(table,1,ligne["Mobile"],ligne["Option"])
            embed.add_field(name="Tri <:otTRI:833666016491864114>",value=dictTriField["countDesc"],inline=True)
            embed.set_footer(text="Page {0}/{1}".format(page,pagemax))
        else:
            embed=embedMois(table,page,ligne["Mobile"],ligne["Option"])
            embed.add_field(name="Tri <:otTRI:833666016491864114>",value=dictTriField[ligne["Tri"]],inline=True)
            embed.set_footer(text="Page {0}/{1}".format(page,pagemax))
            
        embed.title="Périodes {0}".format(option.lower())
        embed.description=newDescip(embed.description,option,obj,guildOT,bot)
        user=interaction.guild.get_member(author)
        if user!=None:
            embed=auteur(user.id,user.name,user.avatar,embed,"user")
            embed.colour=user.color.value
        else:
            embed=auteur(bot.user.id,"Ancien membre",bot.user.avatar,embed,"user")
            embed.colour=0x3498db
        embed.colour=user.color.value

        await sendSlash(interaction,embed,curseurCMD,connexionCMD,page,pagemax)
        
    except:
        await interaction.response.send_message(embed=embedAssertClassic("Impossible de trouver ce que vous cherchez.\nSoit le module de stats est désactivé, soit la table cherchée cherché n'existe pas ou alors est masqué par un administrateur."))
