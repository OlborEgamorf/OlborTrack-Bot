import discord
from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.SeekMessage import seekMessage
from Core.OTGuild import OTGuild
from discord.ext import commands
from Stats.Graphiques.BarRanks import graphRank
from Stats.Graphiques.Circle import graphCircle
from Stats.Graphiques.Evol import (graphEvol, graphEvolAA, graphEvolAutour,
                                   graphEvolBest, graphEvolBestUser,
                                   graphEvolJoursAA, graphEvolRank)
from Stats.Graphiques.Grouped import graphGroupedMois
from Stats.Graphiques.Heat.HeatAnnee import graphHeatAnnee
from Stats.Graphiques.Heat.HeatGlobal import graphHeatGlobal
from Stats.Graphiques.Heat.HeatMois import graphHeat
from Stats.Graphiques.Line import graphLine
from Stats.Graphiques.Moyennes import (graphGroupedMoy, graphHeatMoy,
                                       graphPersoMoy)
from Stats.Graphiques.Perso import graphPerso
from Stats.Graphiques.Scatter.ScatterPerso import graphScatterPerso
from Stats.Graphiques.Scatter.ScatterPositions import graphScatter
from Stats.Graphiques.Scatter.ScatterUsers import graphScatterUsers
from Stats.Graphiques.Spider import graphSpider
from Stats.SQL.ConnectSQL import connectSQL


async def reactGraph(message:int,bot:commands.Bot,guildOT:OTGuild,payload,emoji):
    """Génère et envoie les graphiques pour toutes les commandes du bot.
    
    Regarde dans la base de données des commandes du serveur si le message est valide et regarde les informations enregistrées.
    
    Ensuite, appelle les graphiques adaptés à la commande.
    
    Envoie tous les graphiques dans un salon privé et récupère les liens de images, afin de les utiliser lors des changements de page."""
    connexionCMD,curseurCMD=connectSQL(guildOT.id,"Commandes","Guild",None,None)
    ligne=curseurCMD.execute("SELECT * FROM commandes WHERE MessageID={0}".format(message)).fetchone()
    listeG=[]
    if ligne!=None:
        message,user=await seekMessage(bot,payload)
        ctx=await bot.get_context(message)            
        if ligne["Commande"] in ("periods","periodsInter"):
            ligne["Args3"]=ligne["AuthorID"]

            if ligne["Option"] not in ("Divers","Mentions","Mentionne"):
                liste=[1,2,3,4,5]
            else:
                liste=[1,2,3,4]

            graphPerso(ligne,ctx,ligne["Option"],bot,"mois","Compteur")
            messageGraph=await bot.get_channel(786175275418517554).send(file=discord.File("Graphs/otGraph.png"))
            embedM,embed=await embedGraph(liste,messageGraph,ctx,message)
            listeG.append(messageGraph.attachments[0].url)

            graphGroupedMois(ligne,ctx,ligne["Option"],bot)
            messageGraph=await bot.get_channel(786175275418517554).send(file=discord.File("Graphs/otGraph.png"))
            listeG.append(messageGraph.attachments[0].url)

            graphPerso(ligne,ctx,ligne["Option"],bot,"annee","Compteur")
            messageGraph=await bot.get_channel(786175275418517554).send(file=discord.File("Graphs/otGraph.png"))
            listeG.append(messageGraph.attachments[0].url)

            graphPerso(ligne,ctx,ligne["Option"],bot,"mois","Rang")
            messageGraph=await bot.get_channel(786175275418517554).send(file=discord.File("Graphs/otGraph.png"))
            listeG.append(messageGraph.attachments[0].url)

            if ligne["Option"] not in ("Divers","Mentions","Mentionne"):
                await graphHeatGlobal(ligne,ctx,bot,ligne["Option"],guildOT)
                messageGraph=await bot.get_channel(786175275418517554).send(file=discord.File("Graphs/otGraph.png"))
                listeG.append(messageGraph.attachments[0].url)
        
        elif ligne["Commande"]=="moy":
            if ligne["Option"] in ("Jour","Heure"):
                connexion,curseur=connectSQL(ctx.guild.id,"Moyennes","Stats","GL","")

                graphPersoMoy(ligne,ctx,ligne["Option"],bot,"mois",guildOT,curseur)
                messageGraph=await bot.get_channel(786175275418517554).send(file=discord.File("Graphs/otGraph.png"))
                embedM,embed=await embedGraph([1,2,3],messageGraph,ctx,message)
                listeG.append(messageGraph.attachments[0].url)

                graphGroupedMoy(ligne,ctx,ligne["Option"],bot,guildOT,curseur)
                messageGraph=await bot.get_channel(786175275418517554).send(file=discord.File("Graphs/otGraph.png"))
                listeG.append(messageGraph.attachments[0].url)

                await graphHeatMoy(ligne,ctx,bot,ligne["Option"],guildOT,curseur)
                messageGraph=await bot.get_channel(786175275418517554).send(file=discord.File("Graphs/otGraph.png"))
                listeG.append(messageGraph.attachments[0].url)

            elif ligne["Option"]=="Mois":
                connexion,curseur=connectSQL(ctx.guild.id,"Moyennes","Stats","GL","")

                graphPersoMoy(ligne,ctx,ligne["Option"],bot,"annee",guildOT,curseur)
                messageGraph=await bot.get_channel(786175275418517554).send(file=discord.File("Graphs/otGraph.png"))
                embedM,embed=await embedGraph([1],messageGraph,ctx,message)
                listeG.append(messageGraph.attachments[0].url)

            else:
                await ctx.reply("Cette commande ne dispose pas de graphiques.")
                return
        
        elif ligne["Commande"]=="first":
            await graphRank(ligne,ctx,bot,ligne["Option"],guildOT)
            messageGraph=await bot.get_channel(786175275418517554).send(file=discord.File("Graphs/otGraph.png"))
            embedM,embed=await embedGraph([1,2,3,4],messageGraph,ctx,message)
            listeG.append(messageGraph.attachments[0].url)

            await graphCircle(ligne,ctx,bot,ligne["Option"],guildOT)
            messageGraph=await bot.get_channel(786175275418517554).send(file=discord.File("Graphs/otGraph.png"))
            listeG.append(messageGraph.attachments[0].url)

            graphPerso(ligne,ctx,ligne["Option"],bot,"mois","First")
            messageGraph=await bot.get_channel(786175275418517554).send(file=discord.File("Graphs/otGraph.png"))
            listeG.append(messageGraph.attachments[0].url)

            graphPerso(ligne,ctx,ligne["Option"],bot,"annee","First")
            messageGraph=await bot.get_channel(786175275418517554).send(file=discord.File("Graphs/otGraph.png"))
            listeG.append(messageGraph.attachments[0].url)

        else:
            if ligne["Commande"] in ("rank","jeux"):
                if ligne["Args1"]=="glob":
                    listeFonc=[graphRank,graphHeatGlobal,graphCircle]
                elif ligne["Args1"]=="to":
                    listeFonc=[graphRank,graphHeatAnnee,graphCircle,graphScatter,graphScatterUsers]
                else:
                    listeFonc=[graphRank,graphHeat,graphCircle,graphLine,graphScatter,graphScatterUsers]
                if ligne["Option"] in ("Divers","Mentions","Mentionne") or ligne["Commande"]=="jeux":
                    if graphScatter in listeFonc and ligne["Commande"]!="jeux":
                        listeFonc.remove(graphScatter)
                    if graphHeatGlobal in listeFonc:
                        listeFonc.remove(graphHeatGlobal)
                    if graphHeatAnnee in listeFonc:
                        listeFonc.remove(graphHeatAnnee)
                    if graphHeat in listeFonc:
                        listeFonc.remove(graphHeat)
            
            elif ligne["Commande"]=="trivial" and ligne["Option"]!="trivialperso":
                listeFonc=[graphRank,graphCircle]

            elif ligne["Commande"]=="roles":
                if ligne["Args1"]=="glob":
                    listeFonc=[graphRank,graphHeatGlobal,graphCircle]
                elif ligne["Args1"]=="to":
                    listeFonc=[graphRank,graphHeatAnnee,graphCircle]
                else:
                    listeFonc=[graphRank,graphHeat,graphCircle]
        
            elif ligne["Commande"]=="perso":
                if ligne["Args2"]=="GL":
                    listeFonc=[graphRank,graphCircle]
                else:
                    listeFonc=[graphRank,graphScatterPerso,graphCircle]
        
            elif ligne["Commande"]=="evol":
                if ligne["Args1"]=="glob":
                    listeFonc=[graphEvol,graphEvolAutour,graphEvolBestUser,graphEvolRank]
                else:
                    listeFonc=[graphEvol,graphEvolAA,graphEvolBest,graphEvolAutour,graphEvolBestUser,graphEvolRank]
            
            elif ligne["Commande"]=="day":
                if ligne["Args1"]=="glob":
                    listeFonc=[graphEvol]
                else:
                    listeFonc=[graphEvol,graphEvolJoursAA]
            
            elif ligne["Commande"]=="trivial" and ligne["Option"]=="trivialperso":
                listeFonc=[graphSpider]

            elif ligne["Commande"] in ("jeux","trivial"):
                await ctx.reply("Les graphiques pour les classements de jeux ne sont pas encore disponible ! Il manque des choses à régler pour cela...")
                return
            
            for i,fonc in enumerate(listeFonc):
                await fonc(ligne,ctx,bot,ligne["Option"],guildOT)
                messageGraph=await bot.get_channel(786175275418517554).send(file=discord.File("Graphs/otGraph.png"))
                listeG.append(messageGraph.attachments[0].url)
                if i==0:
                    embedM,embed=await embedGraph(listeFonc,messageGraph,ctx,message)

        descip=""
        for i in listeG:
            descip+="'{0}',".format(i)
        for i in range(len(listeG),7):
            descip+="'None',"
        curseurCMD.execute("INSERT INTO graphs VALUES({0},{1}1,{2})".format(embedM.id,descip,len(listeG)))
        connexionCMD.commit()
        embed.description=""
        if len(listeG)>1:
            await embedM.add_reaction("<:otGAUCHE:772766034335236127>")
            await embedM.add_reaction("<:otDROITE:772766034376523776>")
        await embedM.edit(embed=embed)
        await message.clear_reaction(emoji)
        

async def embedGraph(listeFonc:list,messageGraph:discord.Message,ctx:commands.Context,message:discord.Message) -> (discord.Message, discord.Embed):
    """Crée et envoie l'embed qui affichera les graphiques"""
    embed=discord.Embed(title="Graphiques",description="Tous vos graphiques sont en cours de préparation...",color=0x3498db)
    embed.set_footer(text="Page 1/{0}".format(len(listeFonc)))
    embed.set_image(url=messageGraph.attachments[0].url)
    embed=auteur(ctx.guild.id,ctx.guild.name,ctx.guild.icon,embed,"guild")
    embedM=await message.reply(embed=embed)
    return embedM,embed
