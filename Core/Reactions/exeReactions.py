import discord
from Core.Fonctions.AuteurIcon import auteur
from Core.Fonctions.setMaxPage import setPage
from Core.Reactions.Recall import recall
from Stats.Commandes.View.ViRapports import switchRapport
from Stats.Commandes.View.ViRapportsUser import (switchRapportUser)
from Stats.Graphiques.BarRanks import graphRank
from Stats.Graphiques.Circle import graphCircle
from Stats.Graphiques.Grouped import graphGroupedMois
from Stats.Graphiques.Heat.HeatAnnee import graphHeatAnnee
from Stats.Graphiques.Heat.HeatGlobal import graphHeatGlobal
from Stats.Graphiques.Heat.HeatMois import graphHeat
from Stats.Graphiques.Line import graphLine
from Stats.Graphiques.Perso import graphPerso
from Stats.Graphiques.Scatter.ScatterPerso import graphScatterPerso
from Stats.Graphiques.Scatter.ScatterPositions import graphScatter
from Stats.Graphiques.Scatter.ScatterUsers import graphScatterUsers
from Stats.Graphiques.Spider import graphSpider
from Stats.SQL.ConnectSQL import connectSQL


class InputNbPage(discord.ui.Modal, title="A quelle page voulez-vous aller ?"):
    name = discord.ui.TextInput(label="A quelle page voulez vous aller ?",style=discord.TextStyle.short,required=True)
    async def on_submit(self, interaction: discord.Interaction) -> None:
        try:
            connexion,curseur=connectSQL(interaction.guild_id)
            ligne=curseur.execute("SELECT * FROM commandes WHERE MessageID={0}".format(interaction.message.interaction.id)).fetchone()
            if ligne!=None:
                pagemax=ligne["PageMax"]
                assert int(self.name.value)<=pagemax
                curseur.execute("UPDATE commandes SET Page={0} WHERE MessageID={1}".format(int(self.name.value),interaction.message.interaction.id))
                connexion.commit()
                ligne["Page"]=int(self.name.value)
                await recall(interaction,ligne,curseur,connexion)
        except:
            await interaction.response.send_message("La page fournie n'est pas correcte.", ephemeral=True) 


class ViewControls(discord.ui.View):
    def __init__(self,gauche=True,droite=True,page=True,mobile=True,tri=True,graph=True):
        super().__init__(timeout=None)
        if gauche:
            bouton=discord.ui.Button(label="Page -1",emoji="<:otGAUCHE:772766034335236127>",style=discord.ButtonStyle.blurple, custom_id="ot:gauche")
            bouton.callback=buttonDirection
            self.add_item(bouton)
        if droite:
            bouton=discord.ui.Button(label="Page +1",emoji="<:otDROITE:772766034376523776>",style=discord.ButtonStyle.blurple, custom_id="ot:droite")
            bouton.callback=buttonDirection
            self.add_item(bouton)
        if page:
            bouton=discord.ui.Button(label="Choisir page",emoji="<:otCHOIXPAGE:887022335578767420>",style=discord.ButtonStyle.blurple, custom_id="ot:page")
            bouton.callback=buttonPage
            self.add_item(bouton)
        if mobile:
            bouton=discord.ui.Button(label="Version mobile",emoji="<:otMOBILE:833736320919797780>",style=discord.ButtonStyle.blurple, custom_id="ot:mobile")
            bouton.callback=buttonMobile
            self.add_item(bouton)
        if tri:
            bouton=discord.ui.Button(label="Trier",emoji="<:otTRI:833666016491864114>",style=discord.ButtonStyle.blurple, custom_id="ot:tri")
            bouton.callback=buttonTri
            self.add_item(bouton)
        if graph:
            bouton=discord.ui.Button(label="Graphiques",emoji="<:otGRAPH:772766034558058506>",style=discord.ButtonStyle.blurple, custom_id="ot:graph")
            bouton.callback=buttonGraph
            self.add_item(bouton)

class ViewRapports(discord.ui.View):
    def __init__(self,listeOptions,archives=True):
        super().__init__(timeout=None)

        bouton=discord.ui.Button(label="Accueil",emoji="<:otHOME:835930140571729941>",style=discord.ButtonStyle.blurple, custom_id="ot:homerapport")
        bouton.callback=buttonSwithRapport
        self.add_item(bouton)

        if "Salons" in listeOptions:
            bouton=discord.ui.Button(label="Messages",emoji="<:otSALONS:835928773726699520>",style=discord.ButtonStyle.blurple, custom_id="ot:salonsrapport")
            bouton.callback=buttonSwithRapport
            self.add_item(bouton)
        if "Voice" in listeOptions:
            bouton=discord.ui.Button(label="Vocal",emoji="<:otVOICE:835928773718835260>",style=discord.ButtonStyle.blurple, custom_id="ot:voicerapport")
            bouton.callback=buttonSwithRapport
            self.add_item(bouton)
        if "Emotes" in listeOptions:
            bouton=discord.ui.Button(label="Emotes",emoji="<:otEMOTES:835928773705990154>",style=discord.ButtonStyle.blurple, custom_id="ot:emotesrapport")
            bouton.callback=buttonSwithRapport
            self.add_item(bouton)
        if "Reactions" in listeOptions:
            bouton=discord.ui.Button(label="Réactions",emoji="<:otREACTIONS:835928773740199936>",style=discord.ButtonStyle.blurple, custom_id="ot:reactionsrapport")
            bouton.callback=buttonSwithRapport
            self.add_item(bouton)
        if "Freq" in listeOptions:
            bouton=discord.ui.Button(label="Fréquences",emoji="<:otFREQ:835929144579326003>",style=discord.ButtonStyle.blurple, custom_id="ot:freqrapport")
            bouton.callback=buttonSwithRapport
            self.add_item(bouton)
        if archives:
            bouton=discord.ui.Button(label="Archives",emoji="<:otARCHIVES:836947337808314389>",style=discord.ButtonStyle.blurple, custom_id="ot:archiverapport")
            bouton.callback=buttonSwithRapport
            self.add_item(bouton)

        bouton=discord.ui.Button(label="Page -1",emoji="<:otGAUCHE:772766034335236127>",style=discord.ButtonStyle.blurple, custom_id="ot:gaucherapport")
        bouton.callback=buttonDirection
        self.add_item(bouton)

        bouton=discord.ui.Button(label="Page +1",emoji="<:otDROITE:772766034376523776>",style=discord.ButtonStyle.blurple, custom_id="ot:droiterapport")
        bouton.callback=buttonDirection
        self.add_item(bouton)

        bouton=discord.ui.Button(label="Choisir page",emoji="<:otCHOIXPAGE:887022335578767420>",style=discord.ButtonStyle.blurple, custom_id="ot:pagerapport")
        bouton.callback=buttonPage
        self.add_item(bouton)


class ViewPageGraph(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @discord.ui.button(label="Page -1",emoji="<:otGAUCHE:772766034335236127>",style=discord.ButtonStyle.blurple, custom_id="ot:gauchegraph")
    async def gauche(self,interaction:discord.Interaction, button:discord.ui.Button):
        await buttonDirectionGraph(interaction)
    @discord.ui.button(label="Page +1",emoji="<:otDROITE:772766034376523776>",style=discord.ButtonStyle.blurple, custom_id="ot:droitegraph")
    async def droite(self,interaction:discord.Interaction, button:discord.ui.Button):
        await buttonDirectionGraph(interaction)


async def buttonDirection(interaction):
    connexion,curseur=connectSQL(interaction.guild_id)
    ligne=curseur.execute("SELECT * FROM commandes WHERE MessageID={0}".format(interaction.message.interaction.id)).fetchone()

    if interaction.data["custom_id"] in ("ot:gauche","ot:gaucherapport"):
        page=setPage(ligne["Page"],ligne["PageMax"],"-")
    elif interaction.data["custom_id"] in ("ot:droite","ot:droiterapport"):
        page=setPage(ligne["Page"],ligne["PageMax"],"+")
    else:
        page=ligne["Page"]

    ligne["Page"]=page

    curseur.execute("UPDATE commandes SET Page={0} WHERE MessageID={1}".format(page,interaction.message.interaction.id))
    connexion.commit()
    await recall(interaction,ligne,curseur,connexion)


async def buttonMobile(interaction):
    connexion,curseur=connectSQL(interaction.guild_id)
    ligne=curseur.execute("SELECT * FROM commandes WHERE MessageID={0}".format(interaction.message.interaction.id)).fetchone()
    if ligne!=None:
        curseur.execute("UPDATE commandes SET Mobile={0} WHERE MessageID={1}".format(bool(int(ligne["Mobile"])-1),interaction.message.interaction.id))
        ligne["Mobile"]=bool(int(ligne["Mobile"])-1)
        connexion.commit()
        await recall(interaction,ligne,curseur,connexion) 
        

async def buttonTri(interaction):
    connexion,curseur=connectSQL(interaction.guild_id)
    ligne=curseur.execute("SELECT * FROM commandes WHERE MessageID={0}".format(interaction.message.interaction.id)).fetchone()
    if ligne!=None:
        if ligne["Commande"]=="rank":
            dictNext={"countDesc":"countAsc","countAsc":"countDesc"}
        elif ligne["Commande"] in ("periods","periodsInter"):
            dictNext={"countDesc":"periodAsc","periodAsc":"periodDesc","periodDesc":"rankAsc","rankAsc":"countDesc"}
        elif ligne["Commande"]=="perso":
            dictNext={"countDesc":"rankAsc","rankAsc":"countAsc","countAsc":"rankDesc","rankDesc":"countDesc"}
        elif ligne["Commande"]=="jeux":
            dictNext={"countDesc":"winDesc","winDesc":"loseDesc","loseDesc":"countAsc","countAsc":"winAsc","winAsc":"loseAsc","loseAsc":"countDesc"}
        elif ligne["Commande"]=="trivial" and ligne["Option"]=="trivial":
            dictNext={"countDesc":"countAsc","countAsc":"countDesc"}
        elif ligne["Commande"]=="trivial" and ligne["Option"]=="trivialperso":
            dictNext={"expDesc":"expAsc","expAsc":"expDesc"}
        
        curseur.execute("UPDATE commandes SET Tri='{0}' WHERE MessageID={1}".format(dictNext[ligne["Tri"]],interaction.message.interaction.id))
        connexion.commit()

        ligne["Tri"]=dictNext[ligne["Tri"]]
        await recall(interaction,ligne,curseur,connexion)

async def buttonGraph(interaction):
    await interaction.response.defer(thinking=True) 

    connexionCMD,curseurCMD=connectSQL(interaction.guild_id)
    ligne=curseurCMD.execute("SELECT * FROM commandes WHERE MessageID={0}".format(interaction.message.interaction.id)).fetchone()
    listeG=[]
    guildOT=interaction.client.dictGuilds[interaction.guild_id]
    ctx=await interaction.client.get_context(interaction.message)

    if ligne["PageMax"]==1:
        await interaction.followup.edit_message(interaction.message.id,view=ViewControls(gauche=False,droite=False,page=False,graph=False))
    else:
        await interaction.followup.edit_message(interaction.message.id,view=ViewControls(graph=False))

    if ligne!=None:         
        if ligne["Commande"] in ("periods","periodsInter"):
            ligne["Args3"]=ligne["AuthorID"]

            graphPerso(ligne,ctx,ligne["Option"],interaction.client,"mois","Compteur")
            messageGraph=await interaction.client.get_channel(990654847936241735).send(file=discord.File("Graphs/otGraph.png"))
            listeG.append(messageGraph.attachments[0].url)

            graphGroupedMois(ligne,ctx,ligne["Option"],interaction.client)
            messageGraph=await interaction.client.get_channel(990654847936241735).send(file=discord.File("Graphs/otGraph.png"))
            listeG.append(messageGraph.attachments[0].url)

            graphPerso(ligne,ctx,ligne["Option"],interaction.client,"annee","Compteur")
            messageGraph=await interaction.client.get_channel(990654847936241735).send(file=discord.File("Graphs/otGraph.png"))
            listeG.append(messageGraph.attachments[0].url)

            graphPerso(ligne,ctx,ligne["Option"],interaction.client,"mois","Rang")
            messageGraph=await interaction.client.get_channel(990654847936241735).send(file=discord.File("Graphs/otGraph.png"))
            listeG.append(messageGraph.attachments[0].url)

            if ligne["Option"] not in ("Divers","Mentions","Mentionne"):
                await graphHeatGlobal(ligne,ctx,interaction.client,ligne["Option"],guildOT)
                messageGraph=await interaction.client.get_channel(990654847936241735).send(file=discord.File("Graphs/otGraph.png"))
                listeG.append(messageGraph.attachments[0].url)
        
        elif ligne["Commande"]=="first":
            await graphRank(ligne,ctx,interaction.client,ligne["Option"],guildOT)
            messageGraph=await interaction.client.get_channel(990654847936241735).send(file=discord.File("Graphs/otGraph.png"))
            listeG.append(messageGraph.attachments[0].url)

            await graphCircle(ligne,ctx,interaction.client,ligne["Option"],guildOT)
            messageGraph=await interaction.client.get_channel(990654847936241735).send(file=discord.File("Graphs/otGraph.png"))
            listeG.append(messageGraph.attachments[0].url)

            graphPerso(ligne,ctx,ligne["Option"],interaction.client,"mois","First")
            messageGraph=await interaction.client.get_channel(990654847936241735).send(file=discord.File("Graphs/otGraph.png"))
            listeG.append(messageGraph.attachments[0].url)

            graphPerso(ligne,ctx,ligne["Option"],interaction.client,"annee","First")
            messageGraph=await interaction.client.get_channel(990654847936241735).send(file=discord.File("Graphs/otGraph.png"))
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
            
            elif ligne["Commande"]=="trivialrank":
                listeFonc=[graphRank,graphCircle]
        
            elif ligne["Commande"]=="perso":
                if ligne["Args2"]=="GL":
                    listeFonc=[graphRank,graphCircle]
                else:
                    listeFonc=[graphRank,graphScatterPerso,graphCircle]
            
            elif ligne["Commande"]=="trivialperso":
                listeFonc=[graphSpider]
            
            for i,fonc in enumerate(listeFonc):
                await fonc(ligne,ctx,interaction.client,ligne["Option"],guildOT)
                messageGraph=await interaction.client.get_channel(990654847936241735).send(file=discord.File("Graphs/otGraph.png"))
                listeG.append(messageGraph.attachments[0].url)

        embed=discord.Embed(title="Graphiques",color=0x3498db)
        embed.set_footer(text="Page 1/{0}".format(len(listeG)))
        embed.set_image(url=listeG[0])
        embed=auteur(ctx.guild.name,ctx.guild.icon,embed,"guild")

        if len(listeG):
            message=await interaction.followup.send(embed=embed,view=ViewPageGraph())
        else:
            message=await interaction.followup.send(embed=embed)

        descip=""
        for i in listeG:
            descip+="'{0}',".format(i)
        for i in range(len(listeG),7):
            descip+="'None',"
        curseurCMD.execute("INSERT INTO graphs VALUES({0},{1}1,{2})".format(message.id,descip,len(listeG)))
        connexionCMD.commit()

async def buttonDirectionGraph(interaction):
    connexionCMD,curseurCMD=connectSQL(interaction.guild_id)
    ligne=curseurCMD.execute("SELECT * FROM graphs WHERE MessageID={0}".format(interaction.message.id)).fetchone()
    if ligne!=None:
        if interaction.data["custom_id"]=="ot:gauchegraph":
            sens="-"
        else:
            sens="+"

        page=setPage(ligne["Page"],ligne["PageMax"],sens)
        embed=interaction.message.embeds[0]
        embed.set_image(url=ligne["Graph{0}".format(page)])
        embed.set_footer(text="Page {0}/{1}".format(page,ligne["PageMax"]))
        curseurCMD.execute("UPDATE graphs SET Page={0} WHERE MessageID={1}".format(page,interaction.message.id))
        connexionCMD.commit()
        await interaction.response.edit_message(embed=embed)

async def buttonPage(interaction):
    await interaction.response.send_modal(InputNbPage())

async def buttonSwithRapport(interaction):
    connexionCMD,curseurCMD=connectSQL(interaction.guild_id)
    ligne=curseurCMD.execute("SELECT * FROM commandes WHERE MessageID={0}".format(interaction.message.interaction.id)).fetchone()
    if ligne!=None:
        if ligne["Commande"]=="rapport":
            await switchRapport(interaction,connexionCMD,curseurCMD,ligne,interaction.client.dictGuilds[interaction.guild_id],interaction.client)
        else:
            await switchRapportUser(interaction,connexionCMD,curseurCMD,ligne,interaction.client.dictGuilds[interaction.guild_id],interaction.client)



