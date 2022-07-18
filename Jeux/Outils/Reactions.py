from Core.Fonctions.Embeds import createEmbed, embedAssertClassic
from Stats.SQL.ConnectSQL import connectSQL
from Titres.Outils import createAccount
import discord

dictMax={"Tortues":5,"TortuesDuo":4,"TrivialVersus":5,"TrivialBR":15,"TrivialParty":15,"P4":2,"Morpion":2,"CodeNames":4}
emotes=["<:ot1:705766186909958185>","<:ot2:705766186989912154>","<:ot3:705766186930929685>","<:ot4:705766186947706934>","<:ot5:705766186713088042>","<:ot6:705766187182850148>","<:ot7:705766187115741246>","<:ot8:705766187132256308>","<:ot9:705766187145101363>","<:ot10:705766186909958206>"]
emotesIds=[705766186909958185,705766186989912154,705766186930929685,705766186947706934,705766186713088042,705766187182850148,705766187115741246,705766187132256308,705766187145101363,705766186909958206]

async def trivialReact(interaction,choix):
    user=interaction.user
    gamesTrivial=interaction.client.dictJeux
    if interaction.message.interaction.id in gamesTrivial:
        tableQuestion=gamesTrivial[interaction.message.interaction.id]
    elif interaction.message.id in gamesTrivial:
        tableQuestion=gamesTrivial[interaction.message.id]
    else:
        return
    if user.id in tableQuestion.reponses:
        if tableQuestion.reponses[user.id]==None:
            tableQuestion.reponses[user.id]=choix
    await interaction.response.defer()

class ViewJoinGame(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Rejoindre la partie !", emoji="<:otVALIDER:772766033996021761>",style=discord.ButtonStyle.green, custom_id="ot:joingame")
    async def join(self,interaction:discord.Interaction, button:discord.ui.Button):
        try:
            user=interaction.user
            dictJeux=interaction.client.dictJeux
            inGame=interaction.client.inGame

            assert interaction.message.id in dictJeux
            if user.bot:
                return

            game=dictJeux[interaction.message.id]
            if user.id==game.invoke and user.id in game.ids:
                game.playing=True
                await interaction.response.defer()
                return
            assert user.id not in game.ids
            assert user.id not in inGame
            inGame.append(user.id)
            game.addPlayer(user,interaction)
            if len(game.ids)==dictMax[game.jeu]:
                game.playing=True
            await interaction.response.send_message("<:otVERT:868535645897912330> <@{0}> rejoint la partie !".format(user.id))
        except AssertionError:
            pass

    @discord.ui.button(label="Quitter la partie", emoji="<:otANNULER:811242376625782785>",style=discord.ButtonStyle.red, custom_id="ot:leavegame")
    async def leave(self,interaction:discord.Interaction, button:discord.ui.Button):
        user=interaction.user
        dictJeux=interaction.client.dictJeux
        inGame=interaction.client.inGame

        if interaction.message.id in dictJeux:
            game=dictJeux[interaction.message.id]
            if user.id not in game.ids:
                return
            inGame.remove(user.id)
            game.ids.remove(user.id)
            for i in game.joueurs:
                if i.id==user.id:
                    if game.jeu=="Tortues":
                        game.tortues.append(i.couleur)
                    game.joueurs.remove(i)
                
            await interaction.response.send_message("<:otROUGE:868535622237818910> <@{0}> ne souhaite plus jouer.".format(user.id))

class ViewTrivial(discord.ui.View):
    def __init__(self,pari=False):
        super().__init__(timeout=None)
        if pari:
            button=discord.ui.Button(label="Miser / Parier",emoji="<:otCOINS:873226814527520809>",style=discord.ButtonStyle.blurple,row=1)
            button.callback=setMisePari
            self.add_item(button)

    @discord.ui.button(emoji="<:ot1:705766186909958185>",style=discord.ButtonStyle.blurple, custom_id="ot:trivial1")
    async def rep1(self,interaction:discord.Interaction, button:discord.ui.Button):
        await trivialReact(interaction,0)
    @discord.ui.button(emoji="<:ot2:705766186989912154>",style=discord.ButtonStyle.blurple, custom_id="ot:trivial2")
    async def rep2(self,interaction:discord.Interaction, button:discord.ui.Button):
        await trivialReact(interaction,1)
    @discord.ui.button(emoji="<:ot3:705766186930929685>",style=discord.ButtonStyle.blurple, custom_id="ot:trivial3")
    async def rep3(self,interaction:discord.Interaction, button:discord.ui.Button):
        await trivialReact(interaction,2)
    @discord.ui.button(emoji="<:ot4:705766186947706934>",style=discord.ButtonStyle.blurple, custom_id="ot:trivial4")
    async def rep4(self,interaction:discord.Interaction, button:discord.ui.Button):
        await trivialReact(interaction,3)        

class ViewP4(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Colonne 1",emoji="<:ot1:705766186909958185>",style=discord.ButtonStyle.blurple, custom_id="ot:p4_1")
    async def p4_col1(self,interaction:discord.Interaction, button:discord.ui.Button):
        await interaction.response.defer()
    @discord.ui.button(emoji="<:ot2:705766186989912154>",style=discord.ButtonStyle.blurple, custom_id="ot:p4_2")
    async def p4_col2(self,interaction:discord.Interaction, button:discord.ui.Button):
        await interaction.response.defer()
    @discord.ui.button(emoji="<:ot3:705766186930929685>",style=discord.ButtonStyle.blurple, custom_id="ot:p4_3")
    async def p4_col3(self,interaction:discord.Interaction, button:discord.ui.Button):
        await interaction.response.defer()
    @discord.ui.button(emoji="<:ot4:705766186947706934>",style=discord.ButtonStyle.blurple, custom_id="ot:p4_4")
    async def p4_col4(self,interaction:discord.Interaction, button:discord.ui.Button):
        await interaction.response.defer() 
    @discord.ui.button(emoji="<:ot5:705766186713088042>",style=discord.ButtonStyle.blurple, custom_id="ot:p4_5")
    async def p4_col5(self,interaction:discord.Interaction, button:discord.ui.Button):
        await interaction.response.defer()
    @discord.ui.button(emoji="<:ot6:705766187182850148>",style=discord.ButtonStyle.blurple, custom_id="ot:p4_6")
    async def p4_col6(self,interaction:discord.Interaction, button:discord.ui.Button):
        await interaction.response.defer()
    @discord.ui.button(emoji="<:ot7:705766187115741246>",style=discord.ButtonStyle.blurple, custom_id="ot:p4_7")
    async def p4_col7(self,interaction:discord.Interaction, button:discord.ui.Button):
        await interaction.response.defer()

    @discord.ui.button(label="Miser / Parier",emoji="<:otCOINS:873226814527520809>",style=discord.ButtonStyle.blurple,row=1)
    async def pari(self,interaction:discord.Interaction, button:discord.ui.Button):
        await setMisePari(interaction)

class ViewTortues(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="Carte 1",emoji="<:ot1:705766186909958185>",style=discord.ButtonStyle.blurple, custom_id="ot:tortues1")
    async def carte1(self,interaction:discord.Interaction, button:discord.ui.Button):
        await interaction.response.defer()
    @discord.ui.button(emoji="<:ot2:705766186989912154>",style=discord.ButtonStyle.blurple, custom_id="ot:tortues2")
    async def carte2(self,interaction:discord.Interaction, button:discord.ui.Button):
        await interaction.response.defer()
    @discord.ui.button(emoji="<:ot3:705766186930929685>",style=discord.ButtonStyle.blurple, custom_id="ot:tortues3")
    async def carte3(self,interaction:discord.Interaction, button:discord.ui.Button):
        await interaction.response.defer()
    @discord.ui.button(emoji="<:ot4:705766186947706934>",style=discord.ButtonStyle.blurple, custom_id="ot:tortues4")
    async def carte4(self,interaction:discord.Interaction, button:discord.ui.Button):
        await interaction.response.defer()
    @discord.ui.button(emoji="<:ot5:705766186713088042>",style=discord.ButtonStyle.blurple, custom_id="ot:tortues5")
    async def carte5(self,interaction:discord.Interaction, button:discord.ui.Button):
        await interaction.response.defer()
    
    @discord.ui.button(emoji="<:OTTbleu:860119157491892255>",style=discord.ButtonStyle.blurple, custom_id="ot:tortuesbleu",row=1)
    async def bleu(self,interaction:discord.Interaction, button:discord.ui.Button):
        await interaction.response.defer()
    @discord.ui.button(emoji="<:OTTjaune:860119157688631316>",style=discord.ButtonStyle.blurple, custom_id="ot:tortuesjaune",row=1)
    async def jaune(self,interaction:discord.Interaction, button:discord.ui.Button):
        await interaction.response.defer()
    @discord.ui.button(emoji="<:OTTrouge:860119157495693343>",style=discord.ButtonStyle.blurple, custom_id="ot:tortuesrouge",row=1)
    async def rouge(self,interaction:discord.Interaction, button:discord.ui.Button):
        await interaction.response.defer()
    @discord.ui.button(emoji="<:OTTvert:860119157331853333>",style=discord.ButtonStyle.blurple, custom_id="ot:tortuesvert",row=1)
    async def vert(self,interaction:discord.Interaction, button:discord.ui.Button):
        await interaction.response.defer()
    @discord.ui.button(emoji="<:OTTviolet:860119157672247326>",style=discord.ButtonStyle.blurple, custom_id="ot:tortuesviolet",row=1)
    async def violet(self,interaction:discord.Interaction, button:discord.ui.Button):
        await interaction.response.defer()
    
    @discord.ui.button(label="Rappel tortue",emoji="<:TortueShow:992373121178943568>",style=discord.ButtonStyle.blurple,row=2)
    async def showTortue(self,interaction:discord.Interaction, button:discord.ui.Button):
        dictEmote={0:"<:otBlank:828934808200937492>","rouge":"<:OTTrouge:860119157495693343>","verte":"<:OTTvert:860119157331853333>","bleue":"<:OTTbleu:860119157491892255>","jaune":"<:OTTjaune:860119157688631316>","violette":"<:OTTviolet:860119157672247326>","last":"*dernière tortue*","multi":"*au choix*"}
        dictColor={"bleue":0x00CCFF,"violette":0x993366,"rouge":0xFF0000,"verte":0x77B255,"jaune":0xFFFF00}
        game=interaction.client.dictJeux[interaction.message.id]
        joueurs=game.joueurs  
        joueur=list(filter(lambda x:x.id==interaction.user.id, joueurs))
        if len(joueur)!=0:
            joueur=joueur[0]
            if game.jeu=="TortuesDuo":
                await interaction.response.send_message(embed=createEmbed("Course des tortues","Vos deux tortues à faire gagner sont : {0} {1} et {2} {3}".format(game.equipe[joueur.equipe][0].couleur,dictEmote[game.equipe[joueur.equipe][0].couleur],game.equipe[joueur.equipe][1].couleur,dictEmote[game.equipe[joueur.equipe][1].couleur]),dictColor[joueur.couleur],"tortuesduo",joueur.user),ephemeral=True)
            else:
                await interaction.response.send_message(embed=createEmbed("Course des tortues : {0}".format(joueur.couleur),"Votre couleur est : {0} {1}".format(joueur.couleur,dictEmote[joueur.couleur]),dictColor[joueur.couleur],"tortues",joueur.user),ephemeral=True)
        else:
            await interaction.response.defer()

    @discord.ui.button(label="Miser / Parier",emoji="<:otCOINS:873226814527520809>",style=discord.ButtonStyle.blurple,row=2)
    async def pari(self,interaction:discord.Interaction, button:discord.ui.Button):
        await setMisePari(interaction)

class ViewMorpion(discord.ui.View):
    def __init__(self,options):
        super().__init__(timeout=None)

        emotes=["<:ot1:705766186909958185>","<:ot2:705766186989912154>","<:ot3:705766186930929685>","<:ot4:705766186947706934>","<:ot5:705766186713088042>","<:ot6:705766187182850148>","<:ot7:705766187115741246>","<:ot8:705766187132256308>","<:ot9:705766187145101363>","<:ot10:705766186909958206>"]
        dictVal={0:"A",1:"B",2:"C"}
        liste=[]

        for i in range(len(options)):
            liste.append(discord.SelectOption(label="{0}{1}".format(dictVal[options[i][1]],options[i][0]+1),emoji=emotes[i],value="{0}{1}".format(dictVal[options[i][1]],options[i][0]+1)))
        
        select=discord.ui.Select(options=liste,placeholder="Sélectionnez les coordonnées",custom_id="ot:morpion")

        select.callback=interMorpion
        self.add_item(select)






async def interMorpion(interaction):
    await interaction.response.defer()

async def setMisePari(interaction):
    try:
        user=interaction.user
        message=interaction.message
        dictJeux=interaction.client.dictJeux

        assert message.id in dictJeux
        game=dictJeux[message.id]

        connexionUser,curseurUser=connectSQL("OT",user.id,"Titres",None,None)
        createAccount(connexionUser,curseurUser)
        coins=int(curseurUser.execute("SELECT * FROM coins").fetchone()["Coins"])
        connexionUser.close()

        assert coins>0, "Vous n'avez pas de OT Coins."
        if user.id in game.ids:

            class InputMisePari(discord.ui.Modal, title="Combien d'OT Coins voulez vous miser ?"):
                mise = discord.ui.TextInput(label="Vous avez actuellement {0} OT Coins".format(coins),style=discord.TextStyle.short,required=True,placeholder="Si vous perdez, la somme ira au gagnant de la partie")
                async def on_submit(self, interactionInput: discord.Interaction) -> None:
                    try:
                        await validMise(interactionInput,int(self.mise.value),game)
                    except:
                        await interactionInput.response.send_message("Le nombre d'OT Coins donné est incorrect.", ephemeral=True) 

            await interaction.response.send_modal(InputMisePari())

        else:
            assert game.paris.ouvert, "Les paris pour cette partie sont fermés !"
            assert user.id not in game.paris.paris, "Vous avez déjà parié !"

            listeID=[]
            listeName=[]
            for i in range(len(game.joueurs)):
                if game.paris.cotes[game.joueurs[i].id]==None or game.joueurs[i].guild!=message.guild.id:
                    continue
                listeID.append(game.joueurs[i].id)
                if game.joueurs[i].guild==interaction.guild_id:
                    listeName.append("{0} ({1})".format(game.joueurs[i].nom,game.paris.cotes[game.joueurs[i].id]))
                else:
                    listeName.append("{0} ({1})".format(game.joueurs[i].titre,game.paris.cotes[game.joueurs[i].id]))

            class InputMisePari(discord.ui.Modal, title="Sur qui voulez-vous parier ?"):
                joueur = discord.ui.Select(options=[discord.SelectOption(label=listeName[i],value=listeID[i],emoji=game.joueurs[i].emote) for i in range(len(listeID))],placeholder="Choisissez un joueur")
                pari = discord.ui.TextInput(label="Vous avez actuellement {0} OT Coins".format(coins),style=discord.TextStyle.short,required=True,placeholder="Le montant à parier sur le joueur")
                async def on_submit(self, interactionInput: discord.Interaction) -> None:
                    try:
                        await validPari(interactionInput,int(self.pari.value),int(self.joueur.values[0]),game)
                    except:
                        await interactionInput.response.send_message("Le nombre d'OT Coins donné est incorrect.", ephemeral=True) 

            await interaction.response.send_modal(InputMisePari())

    except AssertionError as er:
        if er!="":
            await interaction.response.send_message(embed=embedAssertClassic(er),ephemeral=True)

async def validMise(interaction,mise,game):
    assert mise>0, "Vous ne pouvez pas miser un nombre négatif d'OT Coins."
    connexionUser,curseurUser=connectSQL("OT",interaction.user.id,"Titres",None,None)
    coins=curseurUser.execute("SELECT * FROM coins").fetchone()["Coins"]
    assert mise<coins, "Vous ne pouvez pas miser plus que ce que vous n'avez !"
    game.paris.mises[interaction.user.id]+=mise
    curseurUser.execute("UPDATE coins SET Coins=Coins-{0}".format(mise))
    connexionUser.commit()
    await interaction.response.send_message(embed=createEmbed("Mise d'OT Coins","Vous avez misé {0} <:otCOINS:873226814527520809> !".format(mise),0xad917b,"",interaction.user),ephemeral=True)

async def validPari(interaction,mise,joueur,game):
    assert mise>0, "Vous ne pouvez pas miser un nombre négatif d'OT Coins."
    connexionUser,curseurUser=connectSQL("OT",interaction.user.id,"Titres",None,None)
    coins=curseurUser.execute("SELECT * FROM coins").fetchone()["Coins"]
    assert mise<coins, "Vous ne pouvez pas miser plus que ce que vous n'avez !"
    game.paris.paris[interaction.user.id]=joueur
    game.paris.parissomme[interaction.user.id]=mise
    curseurUser.execute("UPDATE coins SET Coins=Coins-{0}".format(mise))
    connexionUser.commit()
    if game.joueurs[joueur].guild==interaction.guild_id:
        await interaction.response.send_message(embed=createEmbed("Pari d'OT Coins","Vous avez parié {0} <:otCOINS:873226814527520809> sur {1} !".format(mise,game.joueurs[joueur].nom),0xad917b,"",interaction.user),ephemeral=True)
    else:
        await interaction.response.send_message(embed=createEmbed("Pari d'OT Coins","Vous avez parié {0} <:otCOINS:873226814527520809> sur {1} !".format(mise,game.joueurs[joueur].titre),0xad917b,"",interaction.user),ephemeral=True)
