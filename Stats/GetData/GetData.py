import discord
import os
from time import time
from Stats.GetData.EmbedGetData import embedCreate
from Stats.GetData.Createurs import primeAll
from Stats.SQL.EmoteDetector import emoteDetector
from Stats.GetData.Compteurs import compteurGD28
from Stats.SQL.ConnectSQL import connectSQL
from Stats.GetData.Outils import sommeTable, hideGD
from Stats.GetData.Agregator import agregatorEvol
from Stats.GetData.AgregatorMoyennes import agregatorMoy
from Core.Fonctions.RankingClassic import rankingClassic
from Stats.GetData.Ecriture import ecritureSQL
import sys
import shutil
from Stats.SQL.Verification import verifExecGD
import csv
from Core.Fonctions.DichoTri import dichotomieID, dichotomiePlage, triID
from Core.Fonctions.TempsVoice import tempsVoice
from Core.Fonctions.AuteurIcon import auteur


async def newGetData(guild,channel,bot,guildOT):
    messEdit=await channel.send(embed=discord.Embed(title="OlborTrack GetData - Lancement", description="Patientez... Les anciennes données de votre serveur vont être supprimées.", color=0x220cc9))
    if os.path.exists("SQL/{0}/GETING".format(guild.id))==True:
        embedT=discord.Embed(title="OlborTrack GetData - Erreur",description="Le processus est déjà en cours !",color=0x220cc9)
        await messEdit.edit(embed=embedT)
        return
    os.makedirs("SQL/{0}/GETING".format(guild.id))
    temps=time()
    try:
        await bot.get_channel(717727027465289768).send("Procédure get data enclenchée : "+guild.name+" | "+str(guild.member_count)+" | "+str(guild.id))
        listeDel=[15,16,17,18,19,20,21,22,23,"GL"]
        for i in listeDel:
            try:
                shutil.rmtree("SQL/{0}/{1}".format(guild.id,i))
            except:
                pass
        listeMois,listeWords,listeMoy=[],[],[]
        listeChannels,listeEmotes,listeReact,listeFreq,listeDivers,listeMentions,listeMentionne={},{},{},{},{j:[] for j in range(1,11)},{},{}
        tableJours=[]
        await messEdit.edit(embed=embedCreate(None,"Suppression",temps,temps,guild))
        for guildChan in guild.text_channels:
            tempsI=time()
            try:
                if verifExecGD(guildOT,guildChan,bot.user)==False:
                    continue
                async for message in guildChan.history(limit=None,oldest_first=True):
                    if verifExecGD(guildOT,guildChan,message.author)==False or message.author.bot==True:
                        continue
                    if message.author.bot==False:
                        if len(str(message.created_at.month))==1:
                            mois="0"+str(message.created_at.month)
                        else:
                            mois=str(message.created_at.month)
                        if len(str(message.created_at.day))==1:
                            jour="0"+str(message.created_at.day)
                        else:
                            jour=str(message.created_at.day)
                        if len(str(message.created_at.hour))==1:
                            heureMoy="0"+str(message.created_at.hour)
                        else:
                            heureMoy=str(message.created_at.hour)

                        primeAll(listeMois,message.author.id,jour,mois,str(message.created_at.year)[2:4],1)

                        if guildOT.mstats[9]["Statut"]==True:
                            primeAll(listeDivers[9],message.author.id,jour,mois,str(message.created_at.year)[2:4],1)
                            compteurGD28(tableJours,"ID",1,int(str(message.created_at.year)[2:4]+mois+jour),jour,0,mois,str(message.created_at.year)[2:4],"day")

                        if guildOT.mstats[6]["Statut"]==True:
                            primeAll(listeWords,message.author.id,jour,mois,str(message.created_at.year)[2:4],len(message.content.split(" ")))
                            primeAll(listeDivers[10],message.author.id,jour,mois,str(message.created_at.year)[2:4],len(message.content.split(" ")))

                        if guildOT.mstats[0]["Statut"]==True:
                            if message.channel.id not in listeChannels:
                                listeChannels[message.channel.id]=[]
                            primeAll(listeChannels[message.channel.id],message.author.id,jour,mois,str(message.created_at.year)[2:4],1)

                        if guildOT.mstats[8]["Statut"]==True:
                            emotes=emoteDetector(message.content)
                            dictEmotes={}
                            total=len(emotes)
                            for em in emotes:
                                if em not in dictEmotes:
                                    dictEmotes[em]=0
                                dictEmotes[em]+=1
                            for em in dictEmotes:
                                if em not in listeEmotes:
                                    listeEmotes[em]=[]
                                primeAll(listeEmotes[em],message.author.id,jour,mois,str(message.created_at.year)[2:4],dictEmotes[em])
                            primeAll(listeDivers[8],message.author.id,jour,mois,str(message.created_at.year)[2:4],total)

                        if guildOT.mstats[2]["Statut"]==True:
                            if message.created_at.hour not in listeFreq:
                                listeFreq[message.created_at.hour]=[]
                            primeAll(listeFreq[message.created_at.hour],message.author.id,jour,mois,str(message.created_at.year)[2:4],1)

                        if guildOT.mstats[3]["Statut"]==True:
                            for z in message.reactions:
                                async for user in z.users(limit=None):
                                    if user.bot==False:
                                        primeAll(listeDivers[6],user.id,jour,mois,str(message.created_at.year)[2:4],1)
                                        if type(z.emoji)==str:
                                            try:
                                                reactid=ord(z.emoji)
                                            except:
                                                continue
                                        else:
                                            reactid=z.emoji.id
                                        if reactid not in listeReact:
                                            listeReact[reactid]=[]
                                        primeAll(listeReact[reactid],user.id,jour,mois,str(message.created_at.year)[2:4],1)

                        if guildOT.mstats[4]["Statut"]==True:
                            for ping in message.mentions:
                                if ping.bot==False:
                                    if message.author.id not in listeMentions:
                                        listeMentions[message.author.id]=[]
                                    if ping.id not in listeMentionne:
                                        listeMentionne[ping.id]=[]
                                    primeAll(listeMentions[message.author.id],ping.id,jour,mois,str(message.created_at.year)[2:4],1)
                                    primeAll(listeMentionne[ping.id],message.author.id,jour,mois,str(message.created_at.year)[2:4],1)
                        
                        if guildOT.mstats[10]["Statut"]==True:
                            if message.content.startswith("https://tenor.com/view/"):
                                primeAll(listeDivers[2],message.author.id,jour,mois,str(message.created_at.year)[2:4],1)
                            if message.attachments!=[]:
                                for z in range(len(message.attachments)):
                                    lien=message.attachments[z].url
                                    if message.attachments[z].url[len(lien)-4:len(lien)].lower()==".png" or message.attachments[z].url[len(lien)-4:len(lien)].lower()==".jpg":
                                        primeAll(listeDivers[3],message.author.id,jour,mois,str(message.created_at.year)[2:4],1)
                                    elif message.attachments[z].url[len(lien)-4:len(lien)].lower()==".gif":
                                        primeAll(listeDivers[2],message.author.id,jour,mois,str(message.created_at.year)[2:4],1)
                                    else:
                                        primeAll(listeDivers[1],message.author.id,jour,mois,str(message.created_at.year)[2:4],1)
                            if message.edited_at!=None:
                                primeAll(listeDivers[7],message.author.id,jour,mois,str(message.created_at.year)[2:4],1)
                            if len(message.embeds)!=0:
                                primeAll(listeDivers[4],message.author.id,jour,mois,str(message.created_at.year)[2:4],1)
                            if message.reference!=None:
                                primeAll(listeDivers[5],message.author.id,jour,mois,str(message.created_at.year)[2:4],1)

                        if guildOT.mstats[1]["Statut"]==True:
                            date=str(message.created_at.year)[2:4]+mois+jour+heureMoy
                            listeMoy.sort(key=triID)
                            add=dichotomieID(listeMoy,message.author.id,"ID")
                            ajout=add[0]
                            place=add[1]
                            if ajout==True:
                                listeMoy[place]["Plages"].sort()
                                add=dichotomiePlage(listeMoy[place]["Plages"],date)
                                ajout2=add[0]
                                if ajout2==False:
                                    listeMoy[place]["Plages"].append(date)
                            else:
                                listeMoy.append({"ID":message.author.id,"Plages":[date]})
                            
                await messEdit.edit(embed=embedCreate(messEdit.embeds[0],guildChan.name,tempsI,temps,guild))         
            except discord.errors.Forbidden:
                pass    
        
        chanGlob,emojiGlob,reactGlob,freqGlob,diversGlob,mentionGlob,mentionneGlob=[],[],[],[],[],[],[]
        allGlob=[chanGlob,emojiGlob,reactGlob,freqGlob,diversGlob,mentionGlob,mentionneGlob]
        allList=[listeChannels,listeEmotes,listeReact,listeFreq,listeDivers,listeMentions,listeMentionne]
        modules=[0,8,3,2,10,4,4]
        noms=["Salons","Emotes","Reactions","Freq","Divers","Mentions","Mentionne"]
        for i in range(len(allGlob)):
            for j in allList[i]:
                for y in allList[i][j]:
                    primeAll(allGlob[i],int(j),str(y.id)[4:6],str(y.id)[2:4],y.annee,sommeTable(y.table))

        coRap,curRap=connectSQL(guild.id,"Rapports","Stats","GL","")
        guildCo,guildCur=connectSQL(guild.id,"Guild","Guild",None,None)

        tempsI=time()
        etat=agregatorEvol(listeMois,guild,bool(guildOT.mstats[9]["Statut"]),"","Messages",{},{},curRap)
        dictConnexion=etat[0]
        dictCurseur=etat[1]
        
        try:
            rankingClassic(tableJours)
            ecritureSQL("dayRank",tableJours,dictCurseur["GL"],10)
        except:
            pass

        for i in dictConnexion:
            dictConnexion[i].commit()
        await messEdit.edit(embed=embedCreate(messEdit.embeds[0],"Messages",tempsI,temps,guild))
        
        if guildOT.mstats[1]["Statut"]==True:
            tempsI=time()
            agregatorMoy(listeMoy,etat[2],etat[3],guild)
            await messEdit.edit(embed=embedCreate(messEdit.embeds[0],"Moyennes",tempsI,temps,guild))
        
        hideGD(guild,etat[4].table,guildCur)
        del etat

        if guildOT.mstats[6]["Statut"]==True:
            tempsI=time()
            dictConnexion=agregatorEvol(listeWords,guild,True,"","Mots",{},{},curRap)[0]
            for j in dictConnexion:
                dictConnexion[j].commit()
            del listeWords
            await messEdit.edit(embed=embedCreate(messEdit.embeds[0],"Mots",tempsI,temps,guild))
        
        i=0
        while len(allList)>0:
            if guildOT.mstats[modules[i]]["Statut"]==True:
                tempsI=time()
                dictConnexion,dictCurseur=agregatorEvol(allGlob[i],guild,True,"",noms[i],{},{},curRap) 
                for j in allList[i]:
                    agregatorEvol(allList[i][j],guild,True,int(j),noms[i],dictConnexion,dictCurseur,curRap) 
                for j in dictConnexion:
                    dictConnexion[j].commit()
                await messEdit.edit(embed=embedCreate(messEdit.embeds[0],noms[i],tempsI,temps,guild))
                del allList[i], allGlob[i], noms[i], modules[i]
        
        coRap.commit()

        guildCo.commit()
        guildOT.getHBM()

        await bot.get_channel(717727027465289768).send("Procédure get data **TERMINEE** : "+guild.name+" | "+str(guild.member_count)+" | "+str(guild.id)+" | "+tempsVoice(int(time()-temps)))
        embedT=discord.Embed(title="OlborTrack GetData - Succès",description="Terminé ! Sans accroc. Temps écoulé : "+tempsVoice(int(time()-temps)),color=0x220cc9)
        embedT=auteur(guild.id,guild.name,guild.icon,embedT,"guild")
        await messEdit.channel.send(embed=embedT)
    except:
        embedT=discord.Embed(title="OlborTrack GetData - Erreur",description="Une erreur innatendue est arrivée. Contactez le support. "+tempsVoice(time()-tempsI)+" "+str(sys.exc_info()[0]),color=0x220cc9)
        embedT=auteur(guild.id,guild.name,guild.icon,embedT,"guild")
        await messEdit.channel.send(embed=embedT)
        error=str(sys.exc_info()[0])+"\n"+str(sys.exc_info()[1])+"\n"+str(sys.exc_info()[2].tb_frame)+"\n"+str(sys.exc_info()[2].tb_lineno)
        await bot.get_channel(717727027465289768).send("Procédure get data **ECHEC** : "+guild.name+" | "+str(guild.member_count)+" | "+str(guild.id)+" | "+tempsVoice(time()-tempsI)+"\n"+error)
    shutil.rmtree("SQL/{0}/GETING".format(guild.id)) 
    return


def reloadVoice(bot,dictGuilds):
    for j in bot.guilds:
        try:
            shutil.rmtree("SQL/{0}/{1}".format(j.id,"Voice"))
        except:
            pass
        listeMois,listeDivers,tableJours,listeChannels=[],{11:[]},[],{}
        for root, dirs, files in os.walk("CSV/_"+str(j.id)+"/voice/_histo/"):
            for i in files:
                tableStats=[]
                open(root+"/"+i, "a",encoding="utf-8-sig")
                with open(root+"/"+i, encoding="utf-8-sig", newline="") as fichier :
                    for ligne in csv.DictReader(fichier):
                        tableStats.append(dict(ligne))
                for h in tableStats:
                    primeAll(listeMois,int(i[1:len(i)-4]),h["Date"][3:5],h["Date"][0:2],h["Date"][6:8],int(h["Temps"]))
                    primeAll(listeDivers[11],int(i[1:len(i)-4]),h["Date"][3:5],h["Date"][0:2],h["Date"][6:8],int(h["Temps"]))
                    compteurGD28(tableJours,"ID",int(h["Temps"]),int(h["Date"][6:8]+h["Date"][0:2]+h["Date"][3:5]),h["Date"][3:5],0,h["Date"][0:2],h["Date"][6:8],"day")
                    if int(h["Chan"]) not in listeChannels:
                        listeChannels[int(h["Chan"])]=[]
                    primeAll(listeChannels[int(h["Chan"])],int(i[1:len(i)-4]),h["Date"][3:5],h["Date"][0:2],h["Date"][6:8],int(h["Temps"]))

        if listeMois==[]:
            continue

        chanGlob=[]
        allGlob=[chanGlob]
        allList=[listeChannels]
        noms=["Voicechan"]
        for i in range(len(allGlob)):
            for z in allList[i]:
                for y in allList[i][z]:
                    primeAll(allGlob[i],int(z),str(y.id)[4:6],str(y.id)[2:4],y.annee,sommeTable(y.table))

        coRap,curRap=connectSQL(j.id,"Rapports","Stats","GL","")
        guildCo,guildCur=connectSQL(j.id,"Guild","Guild",None,None)

        tempsI=time()
        etat=agregatorEvol(listeMois,j,True,"","Voice",{},{},curRap)
        dictConnexion=etat[0]
        dictCurseur=etat[1]

        rankingClassic(tableJours)
        ecritureSQL("dayRank",tableJours,dictCurseur["GL"],10)
        for i in dictConnexion:
            dictConnexion[i].commit()

        dictConnexion,dictCurseur=agregatorEvol(allGlob[0],j,True,"",noms[0],{},{},curRap) 
        for z in allList[0]:
            agregatorEvol(allList[0][z],j,True,int(z),noms[0],dictConnexion,dictCurseur,curRap) 
        for z in dictConnexion:
            dictConnexion[z].commit()
        
        coRap.commit()