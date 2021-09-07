from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.Embeds import createEmbed
from Outils.Anniversaires.Formatage import formatageAnniv

tableauMois={"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre","TO":"TO","1":"janvier","2":"février","3":"mars","4":"avril","5":"mai","6":"juin","7":"juillet","8":"aout","9":"septembre","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","glob":"GL","to":"TO"}

async def autoAnniv(bot,dictGuilds,jour,mois):
    connexion,curseur=connectSQL("OT","Guild","Guild",None,None)
    users=curseur.execute("SELECT * FROM anniversaires WHERE Jour={0} AND Mois='{1}'".format(jour,tableauMois[mois])).fetchall()
    for i in users:
        user=bot.get_user(i["ID"])
        if user==None:
            continue
        for j in user.mutual_guilds:
            if dictGuilds[j.id].anniv!=None:
                try:
                    await bot.get_channel(dictGuilds[j.id].anniv.chan).send(embed=createEmbed("Joyeux anniversaire !",formatageAnniv(dictGuilds[j.id].anniv.descip,user),0x11f738,"anniversaire",user))
                except:
                    pass