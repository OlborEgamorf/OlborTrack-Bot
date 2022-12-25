

import discord
from Core.Fonctions.TempsVoice import tempsVoice
from Stats.Rapports.CreateEmbed import embedRapport
from Stats.Rapports.Description import descipGlobal
from Stats.SQL.ConnectSQL import connectSQL

listeType=["Messages","Voice","Salons","Freq","Emotes","Reactions","Voicechan"]
dictFieldG={"Emotes":"Meilleures emotes","Salons":"Salons les plus actifs","Freq":"Heures les plus actives","Reactions":"Meilleures réactions","Messages":"Messages envoyés","Voice":"Temps en vocal","Mots":"Mots envoyés","Voicechan":"Salons vocaux"}
dictFieldS={"Emotes":"Détails emotes","Salons":"Détails salons","Freq":"Détails heures","Reactions":"Détails réactions","Messages":"Détails messages","Voice":"Détails vocal"}
dictTrivia={3:"Images",2:"GIFs",1:"Fichiers",4:"Liens",5:"Réponses",6:"Réactions",7:"Edits",8:"Emotes",9:"Messages",10:"Mots",11:"Vocal"}
dictReact={"Voice":"<:otVOICE:835928773718835260>","Reactions":"<:otREACTIONS:835928773740199936>","Emotes":"<:otEMOTES:835928773705990154>","Salons":"<:otSALONS:835928773726699520>","Freq":"<:otFREQ:835929144579326003>"}
dictSection={"Voice":"vocal","Reactions":"réactions","Emotes":"emotes","Salons":"salons","Freq":"heures","Messages":"salons","Voicechan":"vocal"}
tableauMois={"01":"janvier","02":"février","03":"mars","04":"avril","05":"mai","06":"juin","07":"juillet","08":"aout","09":"septembre","10":"octobre","11":"novembre","12":"décembre","TO":"TOTAL","1":"janvier","2":"février","3":"mars","4":"avril","5":"mai","6":"juin","7":"juillet","8":"aout","9":"septembre","janvier":"01","février":"02","mars":"03","avril":"04","mai":"05","juin":"06","juillet":"07","aout":"08","septembre":"09","octobre":"10","novembre":"11","décembre":"12","to":"TO","glob":"GL"}

def homeGlobal(date,guildOT,bot,guild,pagemax,period):
    """Première page de la section principale"""
    embed=discord.Embed()
    connexion,curseur=connectSQL(guild.id)
    if period in ("mois","annee","global"):
        liste=[]
        for j in listeType:
            try:
                
                result=curseur.execute("SELECT * FROM {0}{1} ORDER BY Rank ASC".format(date[0],date[1])).fetchall()
                if result!=[]:
                    stop=3 if len(result)>3 else len(result)
                    embed.add_field(name=dictFieldG[j],value=descipGlobal(j,result,0,stop,guildOT,bot,None,period),inline=True)
                if j!="Messages":
                    liste.append(j)
            except:
                continue
        divers=curseur.execute("SELECT * FROM {0}{1} ORDER BY Rank ASC".format(date[0],date[1])).fetchall()

    if "Messages" in liste:
        liste.remove("Messages")
    if "Voicechan" in liste:
        liste.remove("Voicechan")
        
    if divers!=[]:
        descip=""
        for i in divers:
            if i["Count"]<=1:
                multi=""
            else:
                multi="s"
            if i["ID"] in (3,2,1,4,9):
                descip+="{0} {1}{2} envoyé{2} / ".format(i["Count"],dictTrivia[i["ID"]][0:-1].lower(),multi)
            elif i["ID"] in (5,7):
                descip+="{0} {1}{2} effectué{2} / ".format(i["Count"],dictTrivia[i["ID"]][0:-1].lower(),multi)
            elif i["ID"] in (6,8):
                descip+="{0} {1}{2} utilisée{2} / ".format(i["Count"],dictTrivia[i["ID"]][0:-1].lower(),multi)
            elif i["ID"]==10:
                descip+="{0} mot{1} écrit{1} / ".format(i["Count"],multi)
            elif i["ID"]==1:
                descip+="{0} passé en vocal / ".format(tempsVoice(i["Count"]))
        embed.add_field(name="Divers",value=descip[0:-2],inline=False)
    
    descipHelp="<:otHOME:835930140571729941> : section principale |"
    for i in range(len(liste)):
        if i%3==1:
            descipHelp+=" {0} : section {1}\n".format(dictReact[liste[i]],dictSection[liste[i]])
        else:
            descipHelp+=" {0} : section {1} |".format(dictReact[liste[i]],dictSection[liste[i]])
    descipHelp=descipHelp[0:-1]
    if period!="global":
        descipHelp+="\n<:otARCHIVES:836947337808314389> : archives de cette date"
    embed.add_field(name="Sections",value=descipHelp,inline=False)

    return embedRapport(guild,embed,date,"Section principale : résumé global",1,pagemax,period)
