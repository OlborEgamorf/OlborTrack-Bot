import asyncio
import os
import sys
from time import time

import discord
from Core.Fonctions.Embeds import createEmbed, embedAssertClassic
from Core.Fonctions.TempsVoice import tempsVoice
from Stats.GetData.EmbedGetData import embedStatut
from Stats.SQL.ConnectSQL import connectSQL
from Stats.SQL.EmoteDetector import emoteDetector
from Stats.SQL.Execution import executeStats, executeStatsFreq, executeStatsObj
from Stats.SQL.Verification import verifExecGD

dictTrivia={"Images":3,"GIFs":2,"Fichiers":1,"Liens":4,"Réponse":5,"Réactions":6,"Edits":7,"Emotes":8,"Messages":9,"Mots":10,"Vocal":11,"Stickers":12}

async def newGetData(guild,channel,bot,guildOT):
    messEdit=await channel.send(embed=discord.Embed(title="Olbor Track GetData - Lancement", description="Patientez... Les anciennes données de votre serveur vont être supprimées.", color=0x220cc9))

    if guildOT.gd or os.path.exists("SQL/{0}/GETING".format(guild.id)):
        embedT=embedAssertClassic("Vous avez déjà lancé la procédure GetData !")
        await messEdit.edit(embed=embedT)
        return

    if not guildOT.stats:
        embedT=embedAssertClassic("Vous avez désactivé les statistiques pour votre serveur. Utilisez la commande OT!statson pour les réactiver.")
        await messEdit.edit(embed=embedT)
        return

    if guild.get_member(699728606493933650).guild_permissions.read_message_history==False:
        embedT=embedAssertClassic("Je ne peux pas accèder au passé de votre serveur. Donnez moi la permission 'lire l'historique des messages' pour pouvoir lancer la procédure.")
        await messEdit.edit(embed=embedT)
        return

    guildOT.gd=True
    temps=time()
    to=0

    try:
        await bot.get_channel(990654847936241735).send("Procédure get data enclenchée : "+guild.name+" | "+str(guild.member_count)+" | "+str(guild.id))

        connexion,curseur=connectSQL(guild.id)

        connexion.start_transaction()
        curseur.execute("DROP TABLE IF EXISTS messages_ranks;")
        curseur.execute("DROP TABLE IF EXISTS messages_freq;")
        curseur.execute("DROP TABLE IF EXISTS emotes_objs;")
        curseur.execute("DROP TABLE IF EXISTS reactions_objs;")
        curseur.execute("DROP TABLE IF EXISTS divers_objs;")

        messEdit=await messEdit.edit(embed=embedStatut(None,"Suppression",temps,temps,guild))
        
        for guildChan in guild.text_channels:
            tempsI=time()
            try:
                if not verifExecGD(guildOT,guildChan,None):
                    continue
                async for message in guildChan.history(limit=None,oldest_first=True):
                    if message.author.bot or not verifExecGD(guildOT,guildChan,message.author):
                        continue

                    if len(str(message.created_at.month))==1:
                        mois="0"+str(message.created_at.month)
                    else:
                        mois=str(message.created_at.month)
                    if len(str(message.created_at.day))==1:
                        jour="0"+str(message.created_at.day)
                    else:
                        jour=str(message.created_at.day)
                    if len(str(message.created_at.hour))==1:
                        heure="0"+str(message.created_at.hour)
                    else:
                        heure=str(message.created_at.hour)
                    annee=str(message.created_at.year)[2:]

                    dictDivers={"Images":0,"GIFs":0,"Fichiers":0,"Liens":0,"Réponse":0,"Stickers":0,"Mots":0}
                    if guildOT.mstats[10]["Statut"]==True:
                        for i in message.attachments:
                            lien=i.url
                            if lien[len(lien)-4:len(lien)].lower() in (".png",".jpg"):
                                dictDivers["Images"]+=1
                            elif lien[len(lien)-4:len(lien)].lower()==".gif":
                                dictDivers["GIFs"]+=1
                            else:
                                dictDivers["Fichiers"]+=1
                        if message.content.startswith("https://tenor.com/view/"):
                            dictDivers["GIFs"]+=1
                        for i in message.embeds:
                            dictDivers["Liens"]+=1
                        if message.reference!=None:
                            dictDivers["Réponse"]+=1
                        for i in message.stickers:
                            dictDivers["Stickers"]+=1
                        if message.content!=None:
                            dictDivers["Mots"]+=len(message.content.split(" "))

                    if guildOT.mstats[0]["Statut"]==True:
                        executeStats("messages",message.author.id,guildChan.id,1,curseur,jour=jour,mois=mois,annee=annee)
                        executeStatsFreq("messages",message.author.id,guildChan.id,heure,1,curseur,mois=mois,annee=annee)

                    if guildOT.mstats[8]["Statut"]==True:
                        listeEmotes=emoteDetector(message.content)
                        if listeEmotes!=[]:
                            dictDivers["Emotes"]=len(listeEmotes)
                            dictEmotes={}
                            for i in listeEmotes:
                                if i not in dictEmotes:
                                    dictEmotes[i]=0
                                dictEmotes[i]+=1
                            for i in dictEmotes:
                                executeStatsObj("emotes",message.author.id,guildChan.id,i,dictEmotes[i],curseur,jour=jour,mois=mois,annee=annee)
                    
                    if guildOT.mstats[10]["Statut"]==True:
                        for i in dictDivers:
                            if dictDivers[i]!=0:
                                executeStatsObj("divers",message.author.id,guildChan.id,dictTrivia[i],dictDivers[i],curseur,jour=jour,mois=mois,annee=annee)
                
                guildOT.gdlist.append(guildChan.id)
                messEdit=await messEdit.edit(embed=embedStatut(messEdit.embeds[0],guildChan.name,tempsI,temps,guild))         
            except discord.errors.Forbidden:
                pass    
            except asyncio.TimeoutError:
                to+=1
                await bot.get_channel(990654847936241735).send("Timeout {0}, **{1}**".format(guild.name,to))
                await asyncio.sleep(15)
                assert to<28

        connexion.commit()
        guildOT.getHBM()

        await bot.get_channel(990654847936241735).send("Procédure get data **TERMINEE** : "+guild.name+" | "+str(guild.member_count)+" | "+str(guild.id)+" | "+tempsVoice(int(time()-temps)))
        await messEdit.channel.send(embed=createEmbed("OlborTrack GetData - Succès","Terminé ! Sans accroc. Temps écoulé : "+tempsVoice(int(time()-temps)),0x220cc9,"getdata",guild))

    except:
        connexion.rollback()
        error=str(sys.exc_info()[0])+"\n"+str(sys.exc_info()[1])+"\n"+str(sys.exc_info()[2].tb_frame)+"\n"+str(sys.exc_info()[2].tb_lineno)
        await bot.get_channel(990654847936241735).send("Procédure get data **ECHEC** : "+guild.name+" | "+str(guild.member_count)+" | "+str(guild.id)+" | "+tempsVoice(time()-tempsI)+"\n"+error)
        await messEdit.channel.send(embed=createEmbed("OlborTrack GetData - Erreur","Une erreur innatendue est arrivée. Vos statistiques ont été captées que partiellement.\nUn rapport a été envoyé au support.\n"+tempsVoice(time()-tempsI)+" "+str(sys.exc_info()[0]),0x220cc9,"getdata",guild))
    
    guildOT.gd=False
    guildOT.gdlist=[]
