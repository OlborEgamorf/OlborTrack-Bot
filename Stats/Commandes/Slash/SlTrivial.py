from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.Embeds import embedAssertClassic
from Core.Fonctions.setMaxPage import setMax
from Core.Fonctions.SendSlash import sendSlash
from Stats.Embeds.Central import statsEmbed
from Stats.SQL.ConnectSQL import connectSQL

dictNoms={"culture":0,"divertissement":1,"sciences":2,"mythologie":3,"sport":4,"géographie":5,"histoire":6,"politique":7,"art":8,"célébrités":9,"animaux":10,"véhicules":11,"streak":"Streak"}

async def statsTrivialSlash(interaction,categorie,bot):
    try:
        connexionCMD,curseurCMD=connectSQL(interaction.guild_id,"Commandes","Guild",None,None)
        
        if categorie!=None:
            table="trivial{0}".format(dictNoms[categorie.value.lower()])
            mode=categorie.value
        else:
            table="trivial12"
            mode="général"

        curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'trivialrank','trivial','{2}','{3}','None','None',1,1,'countDesc',False)".format(interaction.id,interaction.user.id,table,mode))
        ligne=curseurCMD.execute("SELECT * FROM commandes WHERE MessageID={0}".format(interaction.id)).fetchone()
        
        connexion,curseur=connectSQL("OT","ranks","Trivial",None,None)

        pagemax=setMax(curseur.execute("SELECT COUNT() as Nombre FROM {0}".format(table)).fetchone()["Nombre"])
        page=1

        embed=await statsEmbed(table,ligne,page,pagemax,"trivial",interaction.guild,bot,False,False,curseur)
        embed.title="Classement Trivial Mondial {0}".format(mode)
        embed=auteur("Olbor Track Bot",interaction.guild.get_member(990574563572187138).display_avatar,embed,"user")
        embed.colour=0x3498db
        await sendSlash(interaction,embed,curseurCMD,connexionCMD,page,pagemax)
    except:
        await interaction.response.send_message(embed=embedAssertClassic("Impossible de trouver ce que vous cherchez.\nLe classement cherché n'existe pas ou alors il y a un problème de mon côté."))
