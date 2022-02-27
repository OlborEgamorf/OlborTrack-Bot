import asyncio

import discord
from Core.Decorator import OTCommand
from Core.Fonctions.Embeds import createEmbed, embedAssert
from Core.Fonctions.GetNom import getTitre
from Core.Fonctions.Phrase import createPhrase
from Core.Fonctions.WebRequest import getAvatar, getImage
from PIL import Image, ImageDraw, ImageFont
from Stats.SQL.ConnectSQL import connectSQL

from Outils.Bienvenue.Manipulation import squaretoround
from Titres.Listes import commandeTMP
from Titres.Outils import createAccount


async def sendCarte(user,jeu,wins,option,chan):
    await newCarte(user,jeu,wins,option)
    await chan.send(file=discord.File("Images/ExFond/{0}.png".format(user.id)))

class Badge:
    def __init__(self,path,x,y):
        self.path=path
        self.x=x
        self.y=y

async def newCarte(user,jeu,wins,option):
    connexionUser,curseurUser=connectSQL("OT",user.id,"Titres",None,None)
    connexion,curseur=connectSQL("OT","Titres","Titres",None,None)

    fond=curseur.execute("SELECT * FROM cartes WHERE ID={0}".format(user.id)).fetchone()
    if fond==None or fond["Fond"]=="defaut":
        color=curseur.execute("SELECT * FROM couleurs WHERE ID={0}".format(user.id)).fetchone()
        if color==None:
            color=(110,200,250)
        else:
            color=(color["R"],color["G"],color["B"])
        im = Image.new("RGBA", (1280,720), color)
    else:
        im=Image.open("Images/Fonds/{0}.png".format(fond["Fond"]))

    if fond==None or fond["Texte"]=="None":
        texte=None
    else:
        texte=fond["Texte"]
    
    if option=="cross":
        nom=getTitre(curseur,user.id)
        emote=curseur.execute("SELECT * FROM emotes WHERE ID={0}".format(user.id)).fetchone()
        if emote==None:
            imPP=Image.open("Images/ot256.png")
        else:
            await getImage(emote["IDEmote"])
            squaretoround(emote["IDEmote"])
            imPP=Image.open("PNG/Round{0}.png".format(emote["IDEmote"]))
    else:
        await getAvatar(user)
        squaretoround(user.id)
        nom=user.name
        imPP=Image.open("PNG/Round{0}.png".format(user.id))
    
    im.paste(imPP, ((im.size[0]-imPP.size[0])//2,(im.size[1]-imPP.size[1])//2), mask = imPP)

    if curseurUser.execute("SELECT * FROM badges WHERE Période='VIP'").fetchone()!=None:
        imVIP=Image.open("Images/Badges/400/VipmotifCrop400.png")
    else:
        imVIP=Image.open("Images/Badges/400/VIPBlank.png")
    imVIP=imVIP.resize((46,80))
    im.paste(imVIP, ((im.size[0]-imVIP.size[0])//2+120,490),mask=imVIP)
    if curseurUser.execute("SELECT * FROM badges WHERE Période='Testeur'").fetchone()!=None:
        imTest=Image.open("Images/Badges/400/TesteursmotifCrop400.png")
    else:
        imTest=Image.open("Images/Badges/400/TesteurBlank.png")
    imTest=imTest.resize((43,80))
    im.paste(imTest, ((im.size[0]-imTest.size[0])//2-120,490),mask=imTest)
        
    liste=[]
    top3=False
    dictPath={101:"Images/Badges/400/SaphirGlobalCrop400.png",102:"Images/Badges/400/RubisGlobalRec400.png",103:"Images/Badges/400/DiamantGlobalRect400.png",13:"Images/Badges/400/BadgeOrAnneeCrop400.png",12:"Images/Badges/400/BadgeArgentAnneeCrop400.png",11:"Images/Badges/400/BadgeBronzeAnneeCrop400.png",3:"Images/Badges/400/OrBase2Crop400.png",2:"Images/Badges/400/ArgentBase2Crop400.png",1:"Images/Badges/400/BronzeBase2Crop400.png"}
    for i,badge in enumerate(curseurUser.execute("SELECT * FROM badges WHERE Type='{0}' ORDER BY Valeur DESC".format(jeu)).fetchall()):
        if i==3 and not top3:
            for j in liste:
                j.y-=25
        if badge["Valeur"] in (101,102,103):
            imBadge=Image.open(dictPath[badge["Valeur"]])
            imBadge=imBadge.resize((157,148))
            im.paste(imBadge, ((im.size[0]-imBadge.size[0])//2,460),mask=imBadge)
            top3=True
        else:
            if top3:
                x,y,start,stop=(im.size[0]-25)//2+25*(len(liste)),600,0,len(liste)
            else:
                if i>2:
                    x,y,start,stop=(im.size[0]-25)//2+25*(len(liste)-2),550,3,i+1
                else:
                    x,y,start,stop=(im.size[0]-25)//2+25*(len(liste)+1),525,0,i+1
            
            liste.append(Badge(dictPath[badge["Valeur"]],x,y))
            for j in range(start,stop):
                liste[j].x-=25

    for i in liste:
        imBadge=Image.open(i.path)
        imBadge=imBadge.resize((25,35))
        im.paste(imBadge, (i.x,i.y),mask=imBadge)

    font1 = ImageFont.truetype("Font/RobotoCondensed-Regular.ttf", 25)
    font2 = ImageFont.truetype("Font/RobotoCondensed-Regular.ttf", 37)
    draw=ImageDraw.Draw(im)
    draw.text((im.size[0]//2,700),"{0}e victoire pour {1} !".format(wins,nom),(255,255,255),font=font1,anchor="mm",align="center")
    if texte!=None:
        if top3:
            draw.text((im.size[0]//2,665),'"{0}"'.format(texte),(255,255,255),font=font2,anchor="mm",align="center")
        else:
            draw.text((im.size[0]//2,635),'"{0}"'.format(texte),(255,255,255),font=font2,anchor="mm",align="center")

    im.save("Images/ExFond/{0}.png".format(user.id))

class User:
    def __init__(self,id,name):
        self.id=id
        self.name=name
#asyncio.run(newCarte(User(309032693499297802,"OlborEgamorf"),"P4",69,"classic"))

@OTCommand
async def fondsUser(ctx,bot,args):
    if len(args)==0:
        await commandeTMP(ctx,None,False,None,"fonds")
        return
    
    connexion,curseur=connectSQL("OT","Titres","Titres",None,None)
    connexionUser,curseurUser=connectSQL("OT",ctx.author.id,"Titres",None,None)
    try:
        fond=curseur.execute("SELECT * FROM fonds WHERE (Guild=0 OR Guild={0}) AND ID={1}".format(ctx.guild.id,args[0])).fetchone()
        assert fond!=None
        user=curseur.execute("SELECT * FROM cartes WHERE ID={0}".format(ctx.author.id)).fetchone()
        if user!=None:
            assert user["Fond"]!=fond["Path"]
    except:
        raise AssertionError("Le fond que vous cherchez n'existe pas, ou alors vous l'avez déjà équipé.")
    
    createAccount(connexionUser,curseurUser)
    coins=curseurUser.execute("SELECT * FROM coins").fetchone()["Coins"]
    assert coins>=250, "Vous n'avez pas assez d'OT Coins !"

    embed=createEmbed("Changement de fond","Vous êtes sur le point d'acheter le fond **{0}** pour *250 <:otCOINS:873226814527520809>*.\nVous possèdez {1} <:otCOINS:873226814527520809> au total et en aurez {2} <:otCOINS:873226814527520809> après la transaction.\nAppuyez sur <:otVALIDER:772766033996021761> pour confirmer l'achat.".format(fond["Nom"],int(coins),int(coins-250)),0xf58d1d,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.author)

    message=await ctx.reply(embed=embed)
    await message.add_reaction("<:otVALIDER:772766033996021761>")

    connexion.close()
    connexionUser.close()

    def check(reaction,user):
        if type(reaction.emoji)==str:
            return False
        return reaction.emoji.id==772766033996021761 and reaction.message.id==message.id and user.id==ctx.author.id

    reaction,user=await bot.wait_for('reaction_add', check=check, timeout=60)
    await message.clear_reactions()

    connexion,curseur=connectSQL("OT","Titres","Titres",None,None)
    connexionUser,curseurUser=connectSQL("OT",ctx.author.id,"Titres",None,None)
    coins=curseurUser.execute("SELECT * FROM coins").fetchone()["Coins"]
    assert coins>=250, "Vous n'avez pas assez d'OT Coins !"
    curseurUser.execute("UPDATE coins SET Coins=Coins-250")

    if curseur.execute("SELECT * FROM cartes WHERE ID={0}".format(ctx.author.id)).fetchone()==None:
        curseur.execute("INSERT INTO cartes VALUES({0},'{1}','None')".format(ctx.author.id,fond["Path"]))
    else:
        curseur.execute("UPDATE cartes SET Fond='{0}' WHERE ID={1}".format(fond["Path"],ctx.author.id))

    connexion.commit()
    connexionUser.commit()

    embed=createEmbed("Fond équipé","Fond équipé avec succès !\nVotre nouveau fond est maintenant : **{0}**.".format(fond["Nom"]),0xf58d1d,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.author)
    await ctx.reply(embed=embed)

@OTCommand
async def texteFond(ctx,bot,args):
    assert len(args)!=0, "Vous devez me donner la phrase que vous voulez équiper !"
    clean=createPhrase(args)[:-1]
    assert len(clean)<35, "Votre phrase ne doit pas dépasser les 35 caractères !"

    connexionUser,curseurUser=connectSQL("OT",ctx.author.id,"Titres",None,None)
    createAccount(connexionUser,curseurUser)
    coins=curseurUser.execute("SELECT * FROM coins").fetchone()["Coins"]
    assert coins>=50, "Vous n'avez pas assez d'OT Coins !"
    curseurUser.execute("UPDATE coins SET Coins=Coins-50")
    curseurUser.commit()

    connexion,curseur=connectSQL("OT","Titres","Titres",None,None)
    assert curseur.execute("SELECT * FROM custombans WHERE ID={0}".format(ctx.author.id)).fetchone()==None, "Vous êtes banni des outils de personnalisation."
    if curseur.execute("SELECT * FROM cartes WHERE ID={0}".format(ctx.author.id)).fetchone()==None:
        curseur.execute("INSERT INTO cartes VALUES({0},'defaut','{1}')".format(ctx.author.id,clean))
    else:
        curseur.execute("UPDATE cartes SET Texte='{0}' WHERE ID={1}".format(clean,ctx.author.id))
    connexion.commit()
    embed=createEmbed("Modification texte carte","Votre nouvelle phrase de carte est {0} !".format(clean),0xf58d1d,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.author)
    await ctx.send(embed=embed)
    await bot.get_channel(750803643820802100).send("Phrase : {0} - {1}".format(ctx.author.id,clean))


@OTCommand
async def submitFond(ctx,bot):
    try:
        connexion,curseur=connectSQL("OT","Titres","Titres",None,None)
        if curseur.execute("SELECT * FROM custombans WHERE ID={0}".format(ctx.guild.id)).fetchone()!=None:
            await ctx.reply(embed=embedAssert("Votre serveur est banni de cette procédure."))
            return

        embed=createEmbed("Proposition de fond","Pour augmenter la boutique de fond, vous pouvez proposer des fonds personnalisés pour votre serveur, et qui seront proposés uniquement aux membres de votre serveur.\n\nLa vérification et la validation des fonds et soumis à plusieurs critères : \n- La taille de l'image doit être 1280x720\n- Votre serveur doit avoir un certain nombre de membres\n- Votre serveur doit être connu comme utilisant souvent le bot\n- Aucune publicité explicite n'est acceptée, exemple : lien d'invitation du serveur affiché\n- Aucune image choquante ou provocante ne sera validée, et pourra même venir à un bannissement de votre serveur pour cette procédure.\n\nSi tout est bon, envoyez l'image que vous souhaitez.",0xf58d1d,ctx.invoked_with.lower(),ctx.guild)
        await ctx.reply(embed=embed)

        def check(mess):
            return mess.author.id==ctx.author.id and mess.channel.id==ctx.message.channel.id and mess.attachments!=[]
        
        message=await bot.wait_for("message",check=check,timeout=60)

        await bot.get_channel(886911788938035260).send("{0} - {1}\n{2} - {3}\n{4}".format(ctx.guild.name,ctx.guild.id,ctx.author.name,ctx.author.id,message.attachments[0].url))

        embed=createEmbed("Proposition de fond","Votre image a été envoyée ! Vous receverez un message privé lorsqu'elle sera revue.",0xf58d1d,ctx.invoked_with.lower(),ctx.guild)
        await ctx.reply(embed=embed)
    except asyncio.exceptions.TimeoutError:
        await embedAssert(ctx,"Une minute s'est écoulée et vous n'avez pas envoyé d'image. L'opération a été annulée",True)
        await message.clear_reactions()



async def profil(user):
    connexionUser,curseurUser=connectSQL("OT",user.id,"Titres",None,None)
    connexion,curseur=connectSQL("OT","Titres","Titres",None,None)

    color=curseur.execute("SELECT * FROM couleurs WHERE ID={0}".format(user.id)).fetchone()
    if color==None:
        color=(110,200,250)
    else:
        color=(color["R"],color["G"],color["B"])

    fond=curseur.execute("SELECT * FROM cartes WHERE ID={0}".format(user.id)).fetchone()
    if fond!=None:
        fond=Image.open("Images/Fonds/{0}.png".format(fond["Fond"]))
    else:
        fond=Image.new("RGBA", (1280,720), color)

    if fond==None or fond["Texte"]=="None":
        texte=None
    else:
        texte=fond["Texte"]

    nom=getTitre(curseur,user.id)
    emote=curseur.execute("SELECT * FROM emotes WHERE ID={0}".format(user.id)).fetchone()
    if emote==None:
        imPP=Image.open("Images/ot256.png")
    else:
        await getImage(emote["IDEmote"])
        squaretoround(emote["IDEmote"])
        imPP=Image.open("PNG/Round{0}.png".format(emote["IDEmote"]))
    await getAvatar(user)
    squaretoround(user.id)
    nom=user.name
    imPP=Image.open("PNG/Round{0}.png".format(user.id))


