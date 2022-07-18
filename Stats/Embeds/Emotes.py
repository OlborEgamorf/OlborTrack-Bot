import discord
from Core.Fonctions.Embeds import addtoFields, createFields, defEvol

def embedEmote(table,bot,mobile,evol):
    embed=discord.Embed()
    field1,field2,field3="","",""
    for ligne in table:
        rank="{0} {1}".format(ligne["Rank"],defEvol(ligne,evol))
        count=ligne["Count"]
        try:
            nom=chr(ligne["ID"])
        except:
            emote=bot.get_emoji(ligne["ID"])
            if type(emote)!=discord.emoji.Emoji:
                nom="*Emote inconnue*"
            else:
                nom=str(emote)
        field1,field2,field3=addtoFields(field1,field2,field3,mobile,rank,nom,count)
        
    embed=createFields(mobile,embed,field1,field2,field3,"Rang","Emote","Utilisations")
    return embed