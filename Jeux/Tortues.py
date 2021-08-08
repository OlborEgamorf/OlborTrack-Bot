from random import choice, randint
import asyncio
import discord
from Core.Fonctions.AuteurIcon import auteur
from Stats.SQL.ConnectSQL import connectSQL
from Stats.SQL.Execution import exeJeuxSQL
from Core.Fonctions.Embeds import createEmbed, embedAssert, exeErrorExcept
from Titres.Outils import gainCoins

inGameTortues=[]
gamesTortues={}
listeCouleurs=("rouge","jaune","bleue","verte","violette")
emotes=["<:ot1:705766186909958185>","<:ot2:705766186989912154>","<:ot3:705766186930929685>","<:ot4:705766186947706934>","<:ot5:705766186713088042>","<:OTTbleu:860119157491892255>", "<:OTTjaune:860119157688631316>", "<:OTTrouge:860119157495693343>", "<:OTTvert:860119157331853333>", "<:OTTviolet:860119157672247326>"]
dictEmote={0:"<:otBlank:828934808200937492>","rouge":"<:OTTrouge:860119157495693343>","verte":"<:OTTvert:860119157331853333>","bleue":"<:OTTbleu:860119157491892255>","jaune":"<:OTTjaune:860119157688631316>","violette":"<:OTTviolet:860119157672247326>","last":"*dernière tortue*","multi":"*au choix*"}
dictColor={"bleue":0x00CCFF,"violette":0x993366,"rouge":0xFF0000,"verte":0x77B255,"jaune":0xFFFF00}


class Carte:
    def __init__(self,couleur,valeur):
        self.couleur=couleur
        self.valeur=valeur


class Cellule:
    def __init__(self,v,s):
        self.valeur=v
        self.suivante=s


class Pile:
    def __init__(self):
        self.contenu=None
    def est_vide(self):
        return self.contenu is None
    def empiler(self,v):
        self.contenu=Cellule(v,self.contenu)
    def depiler(self):
        if self.est_vide()==True:
            raise IndexError("La liste est vide")
        v=self.contenu.valeur
        self.contenu=self.contenu.suivante
        return v     
    def __len__(self):
        count=0
        cel=self.contenu
        while cel is not None:
            count+=1
            cel=cel.suivante
        return count


class JeuTortues:
    def __init__(self,guild,user):
        self.joueurs=[]
        self.tortues=[Tortue("bleue"),Tortue("verte"),Tortue("jaune"),Tortue("rouge"),Tortue("violette")]
        self.ids=[]
        self.historique={}
        self.emotes={}
        self.plateau=[Pile() for i in range(10)]
        self.cartes=[Carte(i,1) for i in listeCouleurs]*5+[Carte(i,2) for i in listeCouleurs]+[Carte(i,-1) for i in listeCouleurs]*2+[Carte("multi",1) for i in range(5)]+[Carte("last",1) for i in range(3)]+[Carte("last",2) for i in range(2)]+[Carte("multi",-1) for i in range(2)]
        self.playing=False
        self.guild=guild
        self.action={}
        for i in self.tortues:
            self.plateau[0].empiler(i)
        self.invoke=user

    def embedGame(self,user):
        embed=discord.Embed(title="Course de tortues",color=user.color.value)
        embed=auteur(user.id,"Au tour de {0}".format(user.name),user.avatar,embed,"user")
        embed.set_footer(text="OT!tortues")
        liste=[[0 for i in range(10)] for j in range(5)]
        descip=""
        for j in range(len(self.plateau)):
            i=5-len(self.plateau[j])
            cel=self.plateau[j].contenu
            while cel is not None:
                liste[i][j]=cel.valeur.couleur
                cel=cel.suivante 
                i+=1
        for i in range(5):
            for j in range(10):
                if j==9 and liste[i][j]==0:
                    descip+="<:OTTarrivee:860185134895726622>"
                else:
                    descip+=dictEmote[liste[i][j]]
            descip+="\n"
        embed.description=descip

        for i in self.joueurs:
            if i.userid==user.id:
                sup="__"
            else:
                sup=""
            descip=""
            for j in range(len(i.jeu)):
                if i.jeu[j].valeur>0:
                    form="+{0}".format(i.jeu[j].valeur)
                else:
                    form=i.jeu[j].valeur
                descip+="{0} : {1} {2}\n".format(emotes[j],form,dictEmote[i.jeu[j].couleur])
            if i.userid in self.historique:
                if self.historique[i.userid].valeur>0:
                    form="+{0}".format(self.historique[i.userid].valeur)
                else:
                    form=self.historique[i.userid].valeur
                descip+="Dernier coup : {0} {1}".format(form,dictEmote[self.historique[i.userid].couleur])
            embed.add_field(name="{0} {2}Cartes de {1}{2}".format(self.emotes[i.userid],i.user.name,sup),value=descip)
        return embed
                
    def mouvement(self,couleur,valeur):
        if couleur=="last":
            i=0
            while self.plateau[i].est_vide():
                i+=1
            if i==0:
                cel=self.plateau[i].contenu
                liste=[]
                while cel is not None:
                    liste.append(cel.valeur.couleur)
                    cel=cel.suivante
                choix=choice(liste)
                self.mouvement(choix,valeur)
                return
            else:
                count=len(self.plateau[i])
        else:
            for i in range(len(self.plateau)):
                cel=self.plateau[i].contenu
                count=0
                while cel is not None:
                    count+=1
                    if cel.valeur.couleur==couleur:
                        break
                    cel=cel.suivante
                if cel!=None:
                    if cel.valeur.couleur==couleur:
                        break  
        if i==0:
            if valeur<0:
                pass 
            else:
                temp=Pile()
                for j in range(count-1):
                    temp.empiler(self.plateau[i].depiler())
                self.plateau[i+valeur].empiler(self.plateau[i].depiler())
                cel=temp.contenu
                while cel is not None:
                    self.plateau[i].empiler(cel.valeur)
                    cel=cel.suivante
        elif i==9:
            return False
        else:
            if i+valeur<0:
                stop=0
            elif i+valeur>9:
                stop=9
            else:
                stop=i+valeur
            temp=Pile()
            for j in range(count):
                temp.empiler(self.plateau[i].depiler())
            for j in range(count):
                self.plateau[stop].empiler(temp.depiler())
            
            if stop==9:
                return True
        return False

    def giveCards(self):
        for i in self.joueurs:
            for j in range(5):
                carte=randint(0,len(self.cartes)-1)
                i.jeu.append(self.cartes.pop(carte))
    
    def addPlayer(self,user):
        tortue=choice(self.tortues)
        self.tortues.remove(tortue)
        tortue.setPlayer(user)
        self.joueurs.append(tortue)

    async def emotesUser(self,bot):
        idServ=[759688015676309525,759690251521622016,776417458386763778,776417488698212383]
        for i in self.joueurs:
            for j in range(4):
                try:
                    emote=await bot.get_guild(idServ[j]).create_custom_emoji(name=i.name.split(" ")[0],image=await i.user.avatar_url_as(size=128).read(),roles=None,reason=None)
                    break
                except:
                    if j==3:
                        emote="<:otBlank:828934808200937492>"
            self.emotes[i.userid]=emote

    async def delEmotes(self):
        for i in self.ids:
            if self.emotes[i]!="<:otBlank:828934808200937492>":
                await self.emotes[i].delete()

    def getWinner(self):
        cel=self.plateau[9].contenu
        win=cel.valeur.couleur
        while cel is not None:
            win=cel.valeur.couleur
            cel=cel.suivante
        return win

    def embedWin(self,win):
        descip=""
        play=False
        for i in self.joueurs:
            if i.couleur==win:
                embed=discord.Embed(title="Victoire de {0}".format(i.name), description="Il/elle était la tortue {0} ! {1}".format(win,dictEmote[win]), color=dictColor[win])
                embed=auteur(i.userid,i.name,i.user.avatar,embed,"user")
                play=True
            descip+="{0} : <@{1}>\n".format(dictEmote[i.couleur],i.userid)

        if play==False: 
            embed=discord.Embed(title="Personne n'a gagné !", description="La tortue {0} n'était jouée par personne ! {1}".format(win,dictEmote[win]), color=dictColor[win])
        embed.set_footer(text="OT!tortues")
        embed.description+="\n\n"+descip
        return embed

    def stats(self,win):
        connexionGuild,curseurGuild=connectSQL(self.guild.id,"Guild","Guild",None,None)
        connexionOT,curseurOT=connectSQL("OT","Guild","Guild",None,None)
        for i in self.joueurs:
            if i.couleur==win:
                gainCoins(i.userid,len(self.ids)*25)
                count,state=2,"W"
            else:
                count,state=-1,"L"
            exeJeuxSQL(i.userid,None,state,self.guild.id,curseurGuild,count,"Tortues",None)
            exeJeuxSQL(i.userid,None,state,"OT",curseurOT,count,"Tortues",None)
        connexionGuild.commit()
        connexionOT.commit()


class JeuTortuesDuo(JeuTortues):
    def __init__(self,guild,user):
        super().__init__(guild,user)
        self.tortues=[TortueDuo("bleue"),TortueDuo("verte"),TortueDuo("jaune"),TortueDuo("rouge"),TortueDuo("violette")]
        self.equipe={1:[],2:[]}
        self.score={1:0,2:0}
        self.plateau=[Pile() for i in range(10)]
        for i in self.tortues:
            self.plateau[0].empiler(i)
    
    def embedWin(self):
        descip=""
        play=False
        for i in self.score:
            if self.score[i]==2:
                embed=discord.Embed(title="Victoire de {0} et {1} !".format(self.equipe[i][0].name,self.equipe[i][1].name), description="Ils étaient les tortues {0} et {1} ! {2} {3}".format(self.equipe[i][0].couleur,self.equipe[i][1].couleur,dictEmote[self.equipe[i][0].couleur],dictEmote[self.equipe[i][1].couleur]), color=dictColor[self.equipe[i][0].couleur])

        for i in self.joueurs:
            descip+="{0} : <@{1}>\n".format(dictEmote[i.couleur],i.userid)

        embed=auteur(self.guild.id,self.guild.name,self.guild.icon,embed,"guild")
        embed.set_footer(text="OT!tortues")
        embed.description+="\n\n"+descip
        return embed

    def getWinner(self):
        already=True
        cont=len(self.plateau[9])
        temp=Pile()
        for j in range(cont):
            temp.empiler(self.plateau[9].depiler())
        cel=temp.contenu
        while cel is not None:
            win=cel.valeur
            if not cel.valeur.fini:
                already=False
                cel.valeur.fini=True
                break 
            cel=cel.suivante
        for j in range(cont):
            self.plateau[9].empiler(temp.depiler())
        if already:
            return None
        return win
    
    def stats(self,team):
        connexionGuild,curseurGuild=connectSQL(self.guild.id,"Guild","Guild",None,None)
        connexionOT,curseurOT=connectSQL("OT","Guild","Guild",None,None)
        for i in self.joueurs:
            if i.equipe==team:
                gainCoins(i.userid,100)
                count,state=2,"W"
            else:
                count,state=-1,"L"
            exeJeuxSQL(i.userid,None,state,self.guild.id,curseurGuild,count,"TortuesDuo",None)
            exeJeuxSQL(i.userid,None,state,"OT",curseurOT,count,"TortuesDuo",None)
        connexionGuild.commit()
        connexionOT.commit()


class Tortue:
    def __init__(self,couleur):
        self.couleur=couleur
        self.user=None
        self.userid=None
        self.name=None
        self.fini=False
        self.jeu=[]
        
    def setPlayer(self,user):
        self.user=user
        self.userid=user.id
        self.name=user.name
    
    def pioche(self,listeCartes):
        carte=randint(0,len(listeCartes)-1)
        self.jeu.append(listeCartes.pop(carte))
    
    def __str__(self):
        return self.couleur


class TortueDuo(Tortue):
    def __init__(self,couleur):
        super().__init__(couleur)
        self.equipe=0

    def setEquipe(self,equipe):
        self.equipe=equipe
    



async def startGameTortues(ctx,bot):
    try:
        assert ctx.author.id not in inGameTortues, "Terminez votre partie en cours avant de lancer ou rejoindre une partie."
        game=JeuTortues(ctx.guild,ctx.author.id)
        game.ids.append(ctx.author.id)
        inGameTortues.append(ctx.author.id)
        message=await ctx.send(embed=createEmbed("Course des tortues","Le jeu se joue de 2 à 5 joueurs.\nAu début de la partie, chaque joueur se voit attribuer une couleur secrète, envoyée en message privé, qui est celle de sa tortue.\nLe but est d'atteindre l'arrivée avant tout le monde, en jouant avec des cartes qui font avancer les tortues.\nLes joueurs jouent chacun leur tour. Les réactions <:ot1:705766186909958185> à <:ot5:705766186713088042> permettent de choisir sa carte.\nSi vous choisissez une carte 'au choix', cliquez ensuite sur la réaction de la tortue que vous voulez déplacer <:OTTbleu:860119157491892255> <:OTTjaune:860119157688631316> <:OTTrouge:860119157495693343> <:OTTvert:860119157331853333> <:OTTviolet:860119157672247326>.\nLes cartes 'dernière tortue' font avancer la dernière tortue.\nEn dehors de la case départ, les tortues s'empilent et avancent en même temps !\nSi plusieurs tortues arrivent en même temps, celle qui est le plus bas gagne !\nBonne chance !\n\nAppuyez sur la réaction <:otVALIDER:772766033996021761> pour rejoindre la partie de Course des tortues et <:otANNULER:811242376625782785> pour annuler votre participation.\n<@{0}> peut lancer la partie en appuyant sur <:otVALIDER:772766033996021761>, sinon elle se lancera automatiquement au bout de 1 minute.".format(ctx.author.id),0xad917b,ctx.invoked_with.lower(),ctx.guild))
        gamesTortues[message.id]=game

        await message.add_reaction("<:otVALIDER:772766033996021761>")
        #await message.add_reaction("<:pepoG:825979653876482048>")
        await message.add_reaction("<:otANNULER:811242376625782785>")

        for i in range(60):
            if not game.playing:
                await asyncio.sleep(1)
            else:
                break
        
        game.playing=True
        await message.clear_reactions()
        if len(game.ids)<2:
            await message.edit(embed=createEmbed("Course des tortues","Une minute s'est écoulée et pas assez de personnes n'ont répondu à l'invitation.",0xad917b,ctx.invoked_with.lower(),ctx.guild))
            for i in game.ids:
                inGameTortues.remove(i)
            return
        else:
            listeDel=[]
            for i in game.ids:
                user=ctx.guild.get_member(i)
                try:
                    await user.send("<:otVERT:868535645897912330> Vous m'avez bel et bien autorisé à vous envoyer des messages privés, vous êtes dans la partie !")
                    game.addPlayer(user)
                except discord.Forbidden:
                    await ctx.send("<:otROUGE:868535622237818910> <@{0}> n'a pas activé ses messages privés, je ne peux pas lui communiquer sa tortue et ne jouera donc pas la partie.".format(i))
                    inGameTortues.remove(i)
                    listeDel.append(i)
            for i in listeDel:
                game.ids.remove(i)
            
            if len(game.ids)<2:
                await message.edit(embed=createEmbed("Course des tortues","Sur les joueurs qui ont voulu rejoindre la partie, pas assez ont activé leurs messages privés pour recevoir leur couleur. La partie est annulée.",0xad917b,ctx.invoked_with.lower(),ctx.guild))
                for i in game.ids:
                    inGameTortues.remove(i)
                return

            await game.emotesUser(bot)
            descip="<:otVERT:868535645897912330> La partie commence "
            for i in game.joueurs:
                descip+="<@{0}> ".format(i.userid)
                await i.user.send(embed=createEmbed("Course des tortues : {0}".format(i.couleur),"Votre couleur est : {0} {1}".format(i.couleur,dictEmote[i.couleur]),dictColor[i.couleur],ctx.invoked_with.lower(),i.user))
            await message.channel.send(descip)
            message=await message.channel.send(embed=discord.Embed(title="Votre couleur vous a été envoyée par MP..."))
            gamesTortues[message.id]=game
            try:
                await message.pin()
            except:
                pass
            for i in emotes:
                await message.add_reaction(i)
            messAd=await bot.get_channel(870598360296488980).send("{0} - {1} : partie OT!tortues débutée\n{2} joueurs".format(ctx.guild.name,ctx.guild.id,len(game.joueurs)))

        game.giveCards()
        turn=randint(0,len(game.joueurs)-1)
        while game.playing:
            await message.edit(embed=game.embedGame(game.joueurs[turn].user))
            game.action={game.joueurs[turn].userid:None}
            await attente(game,40,None)
            if game.action[game.joueurs[turn].userid] in (None,"bleue","jaune","rouge","verte","violette"):
                carte=game.joueurs[turn].jeu[randint(0,4)]
                couleur,valeur=carte.couleur,carte.valeur
                if couleur=="multi":
                    couleur=choice(listeCouleurs)
            elif game.joueurs[turn].jeu[game.action[game.joueurs[turn].userid]].couleur=="multi":
                carte=game.joueurs[turn].jeu[game.action[game.joueurs[turn].userid]]
                valeur=carte.valeur
                game.action={game.joueurs[turn].userid:None}
                eff=await message.channel.send("<@{0}>, choisissez une tortue avec les réactions <:OTTbleu:860119157491892255> <:OTTjaune:860119157688631316> <:OTTrouge:860119157495693343> <:OTTvert:860119157331853333> <:OTTviolet:860119157672247326>.".format(game.joueurs[turn].userid))
                await attente(game,20,"multi")
                await eff.delete()
                if game.action[game.joueurs[turn].userid]==None:
                    couleur=choice(listeCouleurs)
                else:
                    couleur=game.action[game.joueurs[turn].userid]
            else:
                carte=game.joueurs[turn].jeu[game.action[game.joueurs[turn].userid]]
                couleur,valeur=carte.couleur,carte.valeur

            game.historique[game.joueurs[turn].userid]=carte

            if game.mouvement(couleur,valeur):            
                game.playing=False
                await message.edit(embed=game.embedGame(game.joueurs[turn].user))
                embed=game.embedWin(game.getWinner())
                await message.channel.send(embed=embed)
                await message.clear_reactions()
                await message.unpin()
                game.stats(game.getWinner())
                
            game.joueurs[turn].jeu.remove(carte)
            game.joueurs[turn].pioche(game.cartes)
            turn+=1
            if turn==len(game.joueurs):
                turn=0
            if len(game.cartes)==0:
                game.cartes=[Carte(i,1) for i in listeCouleurs]*5+[Carte(i,2) for i in listeCouleurs]+[Carte(i,-1) for i in listeCouleurs]*2+[Carte("multi",1) for i in range(5)]+[Carte("last",1) for i in range(3)]+[Carte("last",2) for i in range(2)]+[Carte("multi",-1) for i in range(2)]

        await messAd.delete()
    except AssertionError as er:
        await ctx.send(embed=embedAssert(er))
        return
    except:
        await ctx.send(embed=await exeErrorExcept(ctx,bot,""))
        try:
            await message.unpin()
        except:
            pass
    try:
        await game.delEmotes()
    except:
        pass
    for i in game.ids:
        inGameTortues.remove(i)
    del gamesTortues[message.id]


async def startGameTortuesDuo(ctx,bot):
    try:
        assert ctx.author.id not in inGameTortues, "Terminez votre partie en cours avant de lancer ou rejoindre une partie."
        game=JeuTortuesDuo(ctx.guild,ctx.author.id)
        game.ids.append(ctx.author.id)
        inGameTortues.append(ctx.author.id)
        message=await ctx.send(embed=createEmbed("Course des tortues","Le jeu se joue avec 4 joueurs, en 2 contre 2.\nAu début de la partie, chaque binome (aléatoire) se voit attribuer deux couleurs secrètes, envoyées en message privé, qui est celle de ses tortues.\nSauf que vous ne connaissez pas le deuxième membre de votre binome, qui doit faire gagner les mêmes tortues que vous !\nLe but est de faire atteindre l'arrivée avant tout le monde aux deux tortues, en jouant avec des cartes qui font avancer les tortues.\nLes joueurs jouent chacun leur tour. Les réactions <:ot1:705766186909958185> à <:ot5:705766186713088042> permettent de choisir sa carte.\nSi vous choisissez une carte 'au choix', cliquez ensuite sur la réaction de la tortue que vous voulez déplacer <:OTTbleu:860119157491892255> <:OTTjaune:860119157688631316> <:OTTrouge:860119157495693343> <:OTTvert:860119157331853333> <:OTTviolet:860119157672247326>.\nLes cartes 'dernière tortue' font avancer la dernière tortue.\nEn dehors de la case départ, les tortues s'empilent et avancent en même temps !\nSi plusieurs tortues arrivent en même temps, celle qui est le plus bas gagne !\nBonne chance !\n\nAppuyez sur la réaction <:otVALIDER:772766033996021761> pour rejoindre la partie et <:otANNULER:811242376625782785> pour annuler votre participation.\nLa partie se lancera automatiquement quand assez de joueurs auront rejoint, sinon au bout de 1 minute elle sera annulée.",0xad917b,ctx.invoked_with.lower(),ctx.guild))
        gamesTortues[message.id]=game

        await message.add_reaction("<:otVALIDER:772766033996021761>")
        #await message.add_reaction("<:pepoG:825979653876482048>")
        await message.add_reaction("<:otANNULER:811242376625782785>")

        for i in range(60):
            if not game.playing:
                await asyncio.sleep(1)
            else:
                break
        
        game.playing=True
        await message.clear_reactions()
        if len(game.ids)<4:
            await message.edit(embed=createEmbed("Course des tortues","Une minute s'est écoulée et pas assez de personnes n'ont répondu à l'invitation. ({0}/4)".format(len(game.ids)),0xad917b,ctx.invoked_with.lower(),ctx.guild))
            for i in game.ids:
                inGameTortues.remove(i)
            return
        else:
            listeDel=[]
            for i in game.ids:
                user=ctx.guild.get_member(i)
                try:
                    await user.send("<:otVERT:868535645897912330> Vous m'avez bel et bien autorisé à vous envoyer des messages privés, vous êtes dans la partie !")
                    game.addPlayer(user)
                except discord.Forbidden:
                    await ctx.send("<:otROUGE:868535622237818910> <@{0}> n'a pas activé ses messages privés, je ne peux pas lui communiquer sa tortue et ne jouera donc pas la partie.".format(i))
                    inGameTortues.remove(i)
                    listeDel.append(i)
            for i in listeDel:
                game.ids.remove(i)
            
            if len(game.ids)<4:
                await message.edit(embed=createEmbed("Course des tortues","Sur les joueurs qui ont voulu rejoindre la partie, pas assez ont activé leurs messages privés pour recevoir leur couleur. La partie est annulée.",0xad917b,ctx.invoked_with.lower(),ctx.guild))
                for i in game.ids:
                    inGameTortues.remove(i)
                return

            await game.emotesUser(bot)
            descip="<:otVERT:868535645897912330> La partie commence "
            for i in game.joueurs:
                team=randint(1,2)
                if len(game.equipe[team])!=2:
                    game.equipe[team].append(i)
                    i.setEquipe(team)
                else:
                    if team==1:
                        game.equipe[2].append(i)
                        i.setEquipe(2)
                    else:
                        game.equipe[1].append(i)
                        i.setEquipe(1)
            for i in game.joueurs:
                descip+="<@{0}> ".format(i.userid)
                await i.user.send(embed=createEmbed("Course des tortues","Vos deux tortues à faire gagner sont : {0} {1} et {2} {3}".format(game.equipe[i.equipe][0].couleur,dictEmote[game.equipe[i.equipe][0].couleur],game.equipe[i.equipe][1].couleur,dictEmote[game.equipe[i.equipe][1].couleur]),dictColor[i.couleur],ctx.invoked_with.lower(),i.user))
            await message.channel.send(descip)
            message=await message.channel.send(embed=discord.Embed(title="Votre couleur vous a été envoyée par MP..."))
            gamesTortues[message.id]=game
            try:
                await message.pin()
            except:
                pass
            for i in emotes:
                await message.add_reaction(i)
            messAd=await bot.get_channel(870598360296488980).send("{0} - {1} : partie OT!tortuesduo débutée\n{2} joueurs".format(ctx.guild.name,ctx.guild.id,len(game.joueurs)))

        game.giveCards()
        turn=randint(0,len(game.joueurs)-1)
        while game.playing:
            await message.edit(embed=game.embedGame(game.joueurs[turn].user))
            game.action={game.joueurs[turn].userid:None}
            await attente(game,40,None)
            if game.action[game.joueurs[turn].userid] in (None,"bleue","jaune","rouge","verte","violette"):
                carte=game.joueurs[turn].jeu[randint(0,4)]
                couleur,valeur=carte.couleur,carte.valeur
                if couleur=="multi":
                    couleur=choice(listeCouleurs)
            elif game.joueurs[turn].jeu[game.action[game.joueurs[turn].userid]].couleur=="multi":
                carte=game.joueurs[turn].jeu[game.action[game.joueurs[turn].userid]]
                valeur=carte.valeur
                game.action={game.joueurs[turn].userid:None}
                eff=await message.channel.send("<@{0}>, choisissez une tortue avec les réactions <:OTTbleu:860119157491892255> <:OTTjaune:860119157688631316> <:OTTrouge:860119157495693343> <:OTTvert:860119157331853333> <:OTTviolet:860119157672247326>.".format(game.joueurs[turn].userid))
                await attente(game,20,"multi")
                await eff.delete()
                if game.action[game.joueurs[turn].userid]==None:
                    couleur=choice(listeCouleurs)
                else:
                    couleur=game.action[game.joueurs[turn].userid]
            else:
                carte=game.joueurs[turn].jeu[game.action[game.joueurs[turn].userid]]
                couleur,valeur=carte.couleur,carte.valeur

            game.historique[game.joueurs[turn].userid]=carte

            if game.mouvement(couleur,valeur):
                for i in range(len(game.plateau[9])):
                    win=game.getWinner()
                    if win!=None:
                        await message.channel.send("La tortue {0} {1} est arrivée ! Elle gagne le droit de se reposer, et de ne plus jamais bouger... :zzz:".format(win.couleur,dictEmote[win.couleur]))
                        if win.equipe!=0:
                            game.score[win.equipe]+=1
                            print("score",game.score[win.equipe])
                            if game.score[win.equipe]==2:
                                game.playing=False
                                await message.edit(embed=game.embedGame(game.joueurs[turn].user))
                                embed=game.embedWin()
                                await message.channel.send(embed=embed)
                                await message.clear_reactions()
                                await message.unpin()
                                game.stats(win.equipe)
                                break
                
            game.joueurs[turn].jeu.remove(carte)
            game.joueurs[turn].pioche(game.cartes)
            turn+=1
            if turn==len(game.joueurs):
                turn=0
            if len(game.cartes)==0:
                game.cartes=[Carte(i,1) for i in listeCouleurs]*5+[Carte(i,2) for i in listeCouleurs]+[Carte(i,-1) for i in listeCouleurs]*2+[Carte("multi",1) for i in range(5)]+[Carte("last",1) for i in range(3)]+[Carte("last",2) for i in range(2)]+[Carte("multi",-1) for i in range(2)]

        await messAd.delete()
    except AssertionError as er:
        await ctx.send(embed=embedAssert(er))
        return
    except:
        await ctx.send(embed=await exeErrorExcept(ctx,bot,""))
        try:
            await message.unpin()
        except:
            pass
    try:
        await game.delEmotes()
    except:
        pass
    for i in game.ids:
        inGameTortues.remove(i)
    del gamesTortues[message.id]


async def joinTortues(message,user,reaction):
    try:
        assert message.id in gamesTortues
        if user.bot:
            return
        game=gamesTortues[message.id]
        if user.id==game.invoke and user.id in game.ids and type(game)==JeuTortues:
            game.playing=True
            return
        assert user.id not in game.ids
        assert user.id not in inGameTortues
        game.ids.append(user.id)
        inGameTortues.append(user.id)
        if type(game)==JeuTortues:
            if len(game.ids)==5:
                game.playing=True
        elif type(game)==JeuTortuesDuo:
            if len(game.ids)==4:
                game.playing=True
        await message.channel.send("<:otVERT:868535645897912330> <@{0}> rejoint la partie !".format(user.id))
        await reaction.remove(user)
    except:
        pass


async def cancelGameTortues(message,user,reaction):
    if message.id in gamesTortues:
        game=gamesTortues[message.id]
        if user.id not in game.ids:
            if not user.bot:
                await reaction.remove(user)
            return
        inGameTortues.remove(user.id)
        game.ids.remove(user.id)
        await message.channel.send("<:otROUGE:868535622237818910> <@{0}> ne souhaite plus jouer.".format(user.id))
        await reaction.remove(user)


async def tortuesReact(message,client,emoji,user,guild,reaction):
    choix={705766186909958185:0,705766186989912154:1,705766186930929685:2,705766186947706934:3,705766186713088042:4,860119157491892255:"bleue",860119157688631316:"jaune",860119157495693343:"rouge",860119157331853333:"verte",860119157672247326:"violette"}
    if message.id in gamesTortues:
        game=gamesTortues[message.id]
        if user.id in game.action:
            game.action[user.id]=choix[emoji.id]
        if not user.bot:
            await reaction.remove(user)


async def attente(game,temps,event):
    time,done=0,False
    while time!=temps and not done:
        await asyncio.sleep(0.5)
        done=True
        for j in game.action:
            if event==None:
                if game.action[j] in (None,"bleue","jaune","rouge","verte","violette"):
                    done=False
            else:
                if game.action[j] in (None,0,1,2,3,4):
                    done=False
        time+=0.5

async def checkReactTortues(message,reaction):
    if message.id in gamesTortues:
        await message.add_reaction(str(reaction))