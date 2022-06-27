from Core.Fonctions.AuteurIcon import auteur

tableauMois={"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre","TO":"TOTAL","1":"janvier","2":"février","3":"mars","4":"avril","5":"mai","6":"juin","7":"juillet","8":"aout","9":"septembre","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12"}

def embedRapport(guild,embed,date,title,page,pagemax,period):
    embed=auteur(guild.id,guild.name,guild.icon,embed,"guild")
    if period=="mois":
        embed.title="Rapport du {0}/{1}\n{2}".format(tableauMois[date[0]],date[1],title)
    elif period=="annee":
        embed.title="Rapport de l'année 20{0}\n{1}".format(date[1],title)
    elif period=="global":
        embed.title="Rapport global\n{0}".format(title)
    embed.colour=0x3366ff
    embed.set_footer(text="Page {0}/{1}".format(page,pagemax))
    return embed