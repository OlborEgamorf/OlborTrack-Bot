from random import choice
import sqlite3
from Core.Fonctions.GetTable import getTablePerso
from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.TempsVoice import tempsVoice
from Core.Fonctions.GetNom import nomsOptions
from Core.Fonctions.Embeds import createEmbed
import discord

tableauMois={"01":"Janvier","02":"Février","03":"Mars","04":"Avril","05":"Mai","06":"Juin","07":"Juillet","08":"Aout","09":"Septembre","10":"Octobre","11":"Novembre","12":"Décembre","TO":"to","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","glob":"GL","to":"TO"}

async def commandeRandom(interaction,user,react,guildOT,bot):
    liste=[]
    for i in guildOT.mstats:
        if i["Statut"]==True and i["Module"] not in ("Roles","Mentions","Divers"):
            liste.append(i["Module"])
    assert liste!=[]
    option=choice(liste)
    cible=choice(["user","guild","guild"])
    period=choice(["annee","mois"])
    connexion,curseur=connectSQL(interaction.guild_id,option,"Stats","GL","")
    author=user.id
    
    if cible=="user" or option in ("Moyennes","Mots","Messages","Voice"):
        if option in ("Mots","Messages","Voice"):
            dictEnv={"Mots":"envoyé","Messages":"envoyé","Voice":"passé"}
            dictEnv2={"Mots":"mots","Messages":"messages","Voice":"en vocal"}
            sub=choice(["evol","perso"])

            if period=="mois":
                table=getTablePerso(interaction.guild_id,option,author,None,"M","random")
            else:
                table=getTablePerso(interaction.guild_id,option,author,None,"A","random")
            periodStr=randomPeriod(period,table)

            if sub=="evol":
                if table["Annee"]=="GL":
                    subTable=curseur.execute("SELECT * FROM evolglob{0} ORDER BY RANDOM()".format(author)).fetchone()
                else:
                    connexion,curseur=connectSQL(interaction.guild_id,option,"Stats",table["Mois"],table["Annee"])
                    subTable=curseur.execute("SELECT * FROM evol{0}{1}{2} ORDER BY RANDOM()".format(tableauMois[table["Mois"]].lower(),table["Annee"],author)).fetchone()
                count=tempsVoice(subTable["Count"]) if option=="Voice" else subTable["Count"]
                descip="Au __{0}/{1}/{2}__ tu avais {3} **{4}** {5} {6}.\nTon rang était **{7}e**, avec une évolution de {8} !".format(subTable["Jour"],subTable["Mois"],subTable["Annee"],dictEnv[option],count,dictEnv2[option],periodStr.lower(),subTable["Rank"],subTable["Evol"])
            else:
                count=tempsVoice(table["Count"]) if option=="Voice" else table["Count"]
                descip="{0}, tu as {1} **{2}** {3}.\nTon rang sur ce serveur est **{4}e** !".format(periodStr,dictEnv[option],count,dictEnv2[option],table["Rank"])
        elif option=="Moyennes":
            sub=choice(["Annee","Heure","Jour","Mois"])
            table=curseur.execute("SELECT * FROM moy{0}{1} ORDER BY RANDOM()".format(sub,author)).fetchone()
            if sub=="Annee":
                descip="Tu as envoyé en moyenne **{0}** messages par __année d'activité__, depuis toujours.".format(round(table["Moyenne"],2))
            elif sub=="Mois":
                descip="Lors de l'année __20{0}__, tu as envoyé en moyenne **{1}** messages par mois d'activité".format(table["Annee"],round(table["Moyenne"],2))
            elif sub=="Jour":
                descip="En __{0} 20{1}__, tu as envoyé en moyenne **{2}** messages par jour d'activité".format(tableauMois[table["Mois"]].lower(),table["Annee"],round(table["Moyenne"],2))
            elif sub=="Heure":
                descip="Pendant chaque heure d'activité, tu as envoyé en moyenne **{0}** messages, lors du mois de __{1} 20{2}__".format(round(table["Moyenne"],2),tableauMois[table["Mois"]].lower(),table["Annee"])
        else:   
            count=0
            while True:
                if count==50:
                    await commandeRandom(interaction,author,react,guildOT,bot)
                    return
                try:
                    if period=="mois":
                        table=curseur.execute("SELECT * FROM firstM ORDER BY RANDOM()").fetchone()
                    else:
                        table=curseur.execute("SELECT * FROM firstA ORDER BY RANDOM()").fetchone()
                    connexion,curseur=connectSQL(interaction.guild_id,option,"Stats",table["Mois"],table["Annee"])
                    periodStr=randomPeriod(period,table)
                    tableUser=curseur.execute("SELECT * FROM perso{0}{1}{2} ORDER BY RANDOM()".format(table["Mois"],table["Annee"],author)).fetchone()    
                    break
                except sqlite3.OperationalError:
                    count+=1
            dictPhrase={"Salons":"{0}, tu as envoyé **{1}** messages dans le salon {2}.\nTon rang dans ce salon est **{3}e** !",
                        "Freq":"{0}, tu as envoyé **{1}** messages entre {2}.\nTon rang à cette heure ci est **{3}e** !",
                        "Emotes":"{0}, tu as utilisé **{1}** fois l'emote {2}.\nTon rang pour cette emote est **{3}e** !",
                        "Reactions":"{0}, tu as utilisé **{1}** fois la réaction {2}.\nTon rang cette réaction est **{3}e** !"}
            descip=dictPhrase[option].format(periodStr,tableUser["Count"],nomsOptions(option,tableUser["ID"],guildOT,bot),tableUser["Rank"])
        if user!=None:
            embed=createEmbed("Statistique aléatoire",descip,user.color.value,"random",user)
        else:
            embed=createEmbed("Statistique aléatoire",descip,0x6ec8fa,"random",bot.user)
    
    else:
        if option in ("Reactions","Emotes"):
            table=curseur.execute("SELECT * FROM glob WHERE Rank<400 ORDER BY RANDOM()").fetchone()
        else:
            table=curseur.execute("SELECT * FROM glob ORDER BY RANDOM()").fetchone()
        if period=="mois":
            tableObj=getTablePerso(interaction.guild_id,option,author,table["ID"],"M","random")
        else:
            tableObj=getTablePerso(interaction.guild_id,option,author,table["ID"],"A","random")
        periodStr=randomPeriod(period,tableObj)
        dictPhrase={"Salons":"{0}, le salon {1} a vu **{2}** messages envoyés.\nSon rang est **{3}e** !",
                    "Freq":"{0}, **{2}** messages ont été envoyés entre {1}.\nLe rang de cette heure ci est **{3}e** !",
                    "Emotes":"{0}, l'emote {1} a été utilisée **{2}** fois.\nSon rang est **{3}e** !",
                    "Reactions":"{0}, la réaction {1} a été utilisée **{2}** fois.\nSon rang est **{3}e** !"}
        descip=dictPhrase[option].format(periodStr,nomsOptions(option,tableObj["ID"],guildOT,bot),tableObj["Count"],tableObj["Rank"])
        embed=createEmbed("Statistique aléatoire",descip,0x3498db,"random",interaction.guild)
    
    if react:
        await interaction.response.edit_message(embed=embed)
    else:
        await interaction.response.send_message(embed=embed,view=ViewReload())

class ViewReload(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Encore !",emoji="<:otRELOAD:772766034356076584>",style=discord.ButtonStyle.blurple, custom_id="ot:reload")
    async def reload(self,interaction:discord.Interaction, button:discord.ui.Button):
        await commandeRandom(interaction,interaction.user,True,interaction.client.dictGuilds[interaction.guild_id],interaction.client)


def randomPeriod(period,table):
    if period=="mois":
        periodStr="Sur la période de __{0} 20{1}__".format(tableauMois[table["Mois"]].lower(),table["Annee"])
    else:
        if table["Annee"]=="GL":
            periodStr="__Depuis le début__"
        else:
            periodStr="Sur l'année __20{0}__".format(table["Annee"])
    return periodStr