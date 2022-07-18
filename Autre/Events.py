from random import randint
from time import strftime

from Core.Decorator import OTCommand
from Core.Fonctions.Embeds import createEmbed
from Core.Fonctions.WebRequest import webRequest
from Stats.SQL.ConnectSQL import connectSQL
import discord

tableauMois={"01":"Janvier","02":"Février","03":"Mars","04":"Avril","05":"Mai","06":"Juin","07":"Juillet","08":"Aout","09":"Septembre","10":"Octobre","11":"Novembre","12":"Décembre","TO":"Année","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","glob":"GL","to":"TO"}

async def embedWikiEvents(option,jour,mois):
    descip,hyper="",""
    table=await webRequest("https://byabbe.se/on-this-day/"+str(int(mois))+"/"+str(int(jour))+"/"+option+".json")
    assert table!=False, "Il y a eu une erreur lors de la recherche de la page."
    date1, date2=randint(0,len(table[option])-1),randint(0,len(table[option])-1)
    while date2==date1:
        date2=randint(0,len(table[option])-1)
    listeDates=[date1,date2]
    listeDates.sort()
    for i in range(2):
        descip+="**"+table[option][listeDates[i]]["year"]+": **"+table[option][listeDates[i]]["description"]+"\n"
        for k in range(len(table[option][listeDates[i]]["wikipedia"])):
            hyper+="["+table[option][listeDates[i]]["wikipedia"][k]["title"]+"]("+table[option][listeDates[i]]["wikipedia"][k]["wikipedia"]+"), "
    embed=createEmbed(jour+" "+tableauMois[mois],descip+"\nRéférences : "+hyper[0:len(hyper)-2],0xfcfcfc,option,None)
    embed.set_author(name="Wikipédia",icon_url="https://cdn.discordapp.com/attachments/726034739550486618/757641659285635142/Wikipedia-logo-v2.png",url=table["wikipedia"])
    return embed

async def autoEvents(bot,channel,guild):
    connexionCMD,curseurCMD=connectSQL(guild,"Commandes","Guild",None,None)
    embed=await embedWikiEvents("events",strftime("%d"),strftime("%m"))
    message=await bot.get_channel(channel).send(embed=embed)
    await message.add_reaction("<:otRELOAD:772766034356076584>")
    curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'wikipedia','events','events','{2}','{3}','None',1,1,'None',False)".format(message.id,bot.user.id,strftime("%d"),strftime("%m")))
    connexionCMD.commit()

@OTCommand
async def exeWikipedia(interaction,bot,option,ligne):
    if ligne==None:
        connexionCMD,curseurCMD=connectSQL(interaction.guild_id,"Commandes","Guild",None,None)
        embed=await embedWikiEvents(option,strftime("%d"),strftime("%m"))
        await interaction.response.send_message(embed=embed,view=ViewReloadWiki())

        curseurCMD.execute("INSERT INTO commandes VALUES({0},{1},'wikipedia','events','{2}','{3}','{4}','None',1,1,'None',False)".format(interaction.id,interaction.user.id,option,strftime("%d"),strftime("%m")))
        connexionCMD.commit()
    else:
        embed=await embedWikiEvents(ligne["Args1"],ligne["Args2"],ligne["Args3"])
        await interaction.response.edit_message(embed=embed)

class ViewReloadWiki(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Encore !",emoji="<:otRELOAD:772766034356076584>",style=discord.ButtonStyle.blurple, custom_id="ot:reloadwiki")
    async def reload(self,interaction:discord.Interaction, button:discord.ui.Button):
        connexionCMD,curseurCMD=connectSQL(interaction.guild_id,"Commandes","Guild",None,None)
        ligne=curseurCMD.execute("SELECT * FROM commandes WHERE MessageID={0}".format(interaction.message.interaction.id)).fetchone()
        if ligne!=None:
            await exeWikipedia(interaction,interaction.client,ligne["Option"],ligne)