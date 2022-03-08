from time import strftime, time
from Stats.SQL.ConnectSQL import connectSQL
from Stats.SQL.Execution import exeClassic, exeObj
from Stats.SQL.Compteur import compteurSQL
from Stats.SQL.EmoteDetector import emoteDetector
from Stats.SQL.Moyennes import moySQL
from Core.Fonctions.Convertisseurs import inverse
from Stats.Tracker.Divers import exeDiversSQL
from Stats.SQL.Verification import verifExecSQL
from Stats.Tracker.Mentions import exeMentionsSQL

async def exeMessageClient(option,message,client,guild):

    if verifExecSQL(guild,message.channel,message.author)==False:
        return
    
    if bool(guild.mstats[10]["Statut"])==True:
        count=0
        dictType={"Images":0,"GIFs":0,"Fichiers":0,"Liens":0,"Réponse":0,"Stickers":0}
        for i in message.attachments:
            count+=1
            lien=i.url
            if lien[len(lien)-4:len(lien)].lower() in (".png",".jpg"):
                dictType["Images"]+=1
            elif lien[len(lien)-4:len(lien)].lower()==".gif":
                dictType["GIFs"]+=1
            else:
                dictType["Fichiers"]+=1
        if message.content.startswith("https://tenor.com/view/"):
            count+=1
            dictType["GIFs"]+=1
        for i in message.embeds:
            count+=1
            dictType["Liens"]+=1
        if message.reference!=None:
            count+=1
            dictType["Réponse"]+=1
        for i in message.stickers:
            count+=1
            dictType["Stickers"]+=1
        if count!=0:
            exeDiversSQL(message.author.id,dictType,option,guild,None,None)

    listeMots=message.content.split(" ")
    temps=exeStatsSQL(message.author.id,guild,message.channel.id,len(listeMots),option,message.content)
    if temps>2:
        await client.get_channel(804783800080400394).send("{0} dans {1}".format(temps,message.guild.name))
    return

def exeStatsSQL(id,guild,chan,mots,option,content):
    temps=time()
    dictDivers={}
    connexionGuild,curseurGuild=connectSQL(guild.id,"Guild","Guild",None,None)
    count=inverse(option,1)
    mots=inverse(option,mots)

    if guild.mstats[9]["Statut"]==True: 
        exeClassic(count,id,"Messages",curseurGuild,guild)
        dictDivers["Messages"]=count
    if guild.mstats[6]["Statut"]==True:
        exeClassic(mots,id,"Mots",curseurGuild,guild)
        dictDivers["Mots"]=mots
    if guild.mstats[2]["Statut"]==True:
        exeClassic(count,int(strftime("%H")),"Freq",curseurGuild,guild)
        exeObj(count,int(strftime("%H")),id,True,guild,"Freq")
    if guild.mstats[0]["Statut"]==True:
        exeClassic(count,chan,"Salons",curseurGuild,guild)
        exeObj(count,chan,id,True,guild,"Salons")
    if guild.mstats[8]["Statut"]==True:
        listeEmotes=emoteDetector(content)
        if listeEmotes!=[]:
            dictDivers["Emotes"]=len(listeEmotes)
            dictEmotes={}
            for i in listeEmotes:
                if i not in dictEmotes:
                    dictEmotes[i]=0
                dictEmotes[i]+=1
            for i in dictEmotes:
                dictEmotes[i]=inverse(option,dictEmotes[i])
                exeClassic(dictEmotes[i],i,"Emotes",curseurGuild,guild)
                exeObj(dictEmotes[i],i,id,True,guild,"Emotes")
    if guild.mstats[1]["Statut"]==True:
        connexion,curseur=connectSQL(guild.id,"Moyennes","Stats","GL","")
        moySQL(curseur,"Heure",int(strftime("%y")+strftime("%m")+strftime("%d")+strftime("%H")),(strftime("%m"),strftime("%y")),count,id)
        moySQL(curseur,"Jour",int(strftime("%y")+strftime("%m")+strftime("%d")),(strftime("%m"),strftime("%y")),count,id)
        moySQL(curseur,"Mois",int(strftime("%y")+strftime("%m")),("TO",strftime("%y")),count,id)
        moySQL(curseur,"Annee",int(strftime("%y")),("TO","GL"),count,id)
        connexion.commit()
        
    exeDiversSQL(id,dictDivers,option,guild,connexionGuild,curseurGuild)

    connexionGuild.commit()
    return time()-temps