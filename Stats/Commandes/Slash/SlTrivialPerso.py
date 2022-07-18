from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.Embeds import embedAssertClassic
from Core.Fonctions.SendSlash import sendSlash
from Stats.Embeds.Central import statsEmbed
from Stats.SQL.ConnectSQL import connectSQL

async def statsTrivialPersoSlash(interaction,bot):
    try:
        connexionCMD,curseurCMD=connectSQL(interaction.guild_id,"Commandes","Guild",None,None)
        table="trivial{0}".format(interaction.user.id)
        mode="perso"

        curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'trivialperso','trivial','{2}','{3}','None','None',1,1,'expDesc',False)".format(interaction.id,interaction.user.id,table,mode))
        ligne=curseurCMD.execute("SELECT * FROM commandes WHERE MessageID={0}".format(interaction.id)).fetchone()
        
        connexion,curseur=connectSQL("OT",interaction.user.id,"Trivial",None,None)

        embed=await statsEmbed(table,ligne,1,1,"trivialperso",interaction.guild,bot,False,False,curseur)
        embed.title="Classement Trivial Mondial {0}".format(mode)
        user=interaction.guild.get_member(ligne["AuthorID"])
        embed=auteur(user.name,user.avatar,embed,"user")
        embed.colour=0x3498db
        await sendSlash(interaction,embed,curseurCMD,connexionCMD,1,1)
    except:
        await interaction.response.send_message(embed=embedAssertClassic("Impossible de trouver ce que vous cherchez.\nLe classement cherché n'existe pas ou alors il y a un problème de mon côté."))
