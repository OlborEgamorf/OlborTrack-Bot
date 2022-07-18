from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.Embeds import embedAssertClassic
from Core.Fonctions.setMaxPage import setMax, setPage
from Core.Fonctions.SendView import sendView
from Stats.Embeds.Central import statsEmbed
from Stats.SQL.ConnectSQL import connectSQL

async def statsTrivialView(interaction,curseurCMD,connexionCMD,turn,ligne,guildOT,bot):
    try:
        table,mode=ligne["Args1"],ligne["Args2"]
        
        connexion,curseur=connectSQL("OT","ranks","Trivial",None,None)

        pagemax=setMax(curseur.execute("SELECT COUNT() as Nombre FROM {0}".format(table)).fetchone()["Nombre"])

        page=setPage(ligne["Page"],pagemax,turn)

        embed=await statsEmbed(table,ligne,page,pagemax,"trivial",interaction.guild,bot,False,False,curseur)
        embed.title="Classement Trivial Mondial {0}".format(mode)
        embed=auteur("Olbor Track Bot",interaction.guild.get_member(990574563572187138).display_avatar,embed,"user")
        embed.colour=0x3498db
        await sendView(interaction,embed,curseurCMD,connexionCMD,page,pagemax)
    except:
        await interaction.response.send_message(embed=embedAssertClassic("Impossible de trouver ce que vous cherchez.\nLe classement cherché n'existe plus ou alors il y a un problème de mon côté."))
