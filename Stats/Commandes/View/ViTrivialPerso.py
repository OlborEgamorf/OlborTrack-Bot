from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.Embeds import embedAssertClassic
from Core.Fonctions.SendView import sendView
from Stats.Embeds.Central import statsEmbed
from Stats.SQL.ConnectSQL import connectSQL


async def statsTrivialPersoView(interaction,curseurCMD,connexionCMD,turn,ligne,guildOT,bot):
    try:
        table,mode=ligne["Args1"],ligne["Args2"]
        author=ligne["AuthorID"]
        connexion,curseur=connectSQL("OT",author,"Trivial",None,None)

        embed=await statsEmbed(table,ligne,1,1,"trivialperso",interaction.guild,bot,False,False,curseur)
        embed.title="Classement Trivial Mondial {0}".format(mode)
        user=interaction.guild.get_member(author)
        embed=auteur(user.name,user.avatar,embed,"user")
        embed.colour=0x3498db
        await sendView(interaction,embed,curseurCMD,connexionCMD,1,1)
    except:
        await interaction.response.send_message(embed=embedAssertClassic("Impossible de trouver ce que vous cherchez.\nLe classement cherché n'existe plus ou alors il y a un problème de mon côté."))
