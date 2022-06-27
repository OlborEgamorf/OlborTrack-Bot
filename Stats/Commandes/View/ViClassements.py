from time import strftime

from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.Embeds import embedAssertClassic, newDescip
from Core.Fonctions.SendView import sendView
from Core.Fonctions.setMaxPage import setMax, setPage
from Stats.Embeds.Central import statsEmbed
from Stats.SQL.ConnectSQL import connectSQL

tableauMois={"01":"Janvier","02":"Février","03":"Mars","04":"Avril","05":"Mai","06":"Juin","07":"Juillet","08":"Aout","09":"Septembre","10":"Octobre","11":"Novembre","12":"Décembre","TO":"Année","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","glob":"GL","to":"TO"}

async def statsRankView(interaction,curseurCMD,connexionCMD,turn,ligne,guildOT,bot):
    try:
        mois,annee=ligne["Args1"],ligne["Args2"]
        option=ligne["Option"]
        connexion,curseur=connectSQL(interaction.guild_id,option,"Stats",tableauMois[mois],annee)

        if ligne["Args3"]=="None":
            pagemax=setMax(curseur.execute("SELECT COUNT() as Nombre FROM {0}{1}".format(mois,annee)).fetchone()["Nombre"])
        else:
            pagemax=setMax(curseur.execute("SELECT COUNT() as Nombre FROM {0}{1}{2}".format(mois,annee,ligne["Args3"])).fetchone()["Nombre"])

        page=setPage(ligne["Page"],pagemax,turn)
        print(page,pagemax,turn)
        obj="" if ligne["Args3"]=="None" else ligne["Args3"]
        if obj!="":
            if option in ("Salons","Voicechan"):
                assert not guildOT.chan[int(obj)]["Hide"]
            tempOption=option
            if option=="Voicechan":
                option="Voice"
            else:
                option="Messages"

        if mois=="glob":
            title="Classement général {0}".format(option.lower())
            evol=True if obj=="" else False
        elif mois=="to":
            title="Classement {0} 20{1}".format(option.lower(),annee)
            evol=True if annee==strftime("%y") and obj=="" else False
        else:
            title="Classement {0} {1} 20{2}".format(option.lower(),mois,annee)
            evol=True if tableauMois[mois]==strftime("%m") and annee==strftime("%y") and obj=="" else False

        embed=await statsEmbed("{0}{1}{2}".format(mois,annee,obj),ligne,page,pagemax,option,guildOT,bot,evol,False,curseur)
        embed.title=title
        embed=auteur(interaction.guild_id,interaction.guild.name,interaction.guild.icon,embed,"guild")
        embed.colour=0x3498db
        if obj!="":
            embed.description=newDescip(embed.description,tempOption,obj,guildOT,bot)
        await sendView(interaction,embed,curseurCMD,connexionCMD,page,pagemax)
    
    except:
        await interaction.response.send_message(embed=embedAssertClassic("Impossible de trouver ce que vous cherchez.\nSoit le module de stats est désactivé, soit le classement cherché n'existe pas ou alors est masqué par un administrateur."))