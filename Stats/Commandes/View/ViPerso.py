from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.Embeds import embedAssertClassic
from Core.Fonctions.SendView import sendView
from Core.Fonctions.setMaxPage import setMax, setPage
from Stats.Embeds.Central import statsEmbed
from Stats.SQL.ConnectSQL import connectSQL

tableauMois={"01":"Janvier","02":"Février","03":"Mars","04":"Avril","05":"Mai","06":"Juin","07":"Juillet","08":"Aout","09":"Septembre","10":"Octobre","11":"Novembre","12":"Décembre","TO":"Année","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","glob":"GL","to":"TO"}

async def statsPersoView(interaction,curseurCMD,connexionCMD,turn,ligne,guildOT,bot):
    try:
        mois,annee=ligne["Args1"],ligne["Args2"]
        option=ligne["Option"]
        connexion,curseur=connectSQL(interaction.guild.id,option,"Stats",mois,annee)

        author=ligne["AuthorID"]
        pagemax=setMax(curseur.execute("SELECT COUNT() as Nombre FROM perso{0}{1}{2}".format(mois,annee,author)).fetchone()["Nombre"])
        page=setPage(ligne["Page"],pagemax,turn)
        
        if annee=="GL":
            title="Perso général {0}".format(option.lower())
        elif mois=="TO":
            title="Perso {0} 20{1}".format(option.lower(),annee)
        else:
            title="Perso {0} {1} 20{2}".format(option.lower(),tableauMois[mois].lower(),annee)

        embed=await statsEmbed("perso{0}{1}{2}".format(mois,annee,author),ligne,page,pagemax,option,guildOT,bot,False,False,curseur)
        embed.title=title
        user=interaction.guild.get_member(author)
        if user!=None:
            embed=auteur(user.name,user.avatar,embed,"user")
            embed.colour=user.color.value
        else:
            embed=auteur("Ancien membre",bot.user.avatar,embed,"user")
            embed.colour=0x3498db
        await sendView(interaction,embed,curseurCMD,connexionCMD,page,pagemax)
        
    except:
        await interaction.response.send_message(embed=embedAssertClassic("Impossible de trouver ce que vous cherchez.\nSoit le module de stats est désactivé, soit la table cherchée n'existe plus."))
    