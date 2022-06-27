

from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.GetNom import nomsOptions
from Core.Fonctions.TempsVoice import formatCount, tempsVoice

tableauMois={"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre","TO":"TOTAL","1":"janvier","2":"février","3":"mars","4":"avril","5":"mai","6":"juin","7":"juillet","8":"aout","9":"septembre","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","to":"TO","glob":"GL"}

def descipGlobal(option,result,start,stop,guildOT,bot,hier,period,user):
    descip=""
    if hier!=None:
        curseur=connectSQL(guildOT.id,option,"Stats",tableauMois[hier[0]],hier[1])[1]
    for i in range(start,stop):
        try:
            assert hier!=None
            resultHier=curseur.execute("SELECT * FROM perso{0}{1}{2} WHERE ID={3}".format(tableauMois[hier[0]],hier[1],user,result[i]["ID"])).fetchone()
            assert resultHier!=None
            assert resultHier["Rank"]-result[i]["Rank"]!=0
            oldRank="*(+{0})*".format(resultHier["Rank"]-result[i]["Rank"]) if resultHier["Rank"]-result[i]["Rank"]>=0 else "*({0})*".format(resultHier["Rank"]-result[i]["Rank"])
        except AssertionError:
            oldRank=""
        nom=nomsOptions(option,result[i]["ID"],guildOT,bot)
        if nom in ("*Membre masqué*" or "*Salon masqué*"):
            count="??"
        else:
            count=formatCount(option,result[i]["Count"])
        descip+="**{0}e** {1} : {2} - {3}\n".format(result[i]["Rank"],oldRank,nom,count)
    return descip