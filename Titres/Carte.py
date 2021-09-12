import discord
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
    imVIP=imVIP.resize((58,100))
    im.paste(imVIP, ((im.size[0]-imVIP.size[0])//2+170,490),mask=imVIP)
    if curseurUser.execute("SELECT * FROM badges WHERE Période='Testeur'").fetchone()!=None:
        imTest=Image.open("Images/Badges/400/TesteursmotifCrop400.png")
    else:
        imTest=Image.open("Images/Badges/400/TesteurBlank.png")
    imTest=imTest.resize((54,100))
    im.paste(imTest, ((im.size[0]-imTest.size[0])//2-170,490),mask=imTest)
        
    listeAll=[1,2,3,11,12,13]
    liste=[]
    for i in curseurUser.execute("SELECT * FROM badges WHERE Type='{0}'".format(jeu)).fetchall():
        if i["Valeur"] in (101,102,103):
            if i["Valeur"]==101:
                imBadge=Image.open("Images/Badges/400/SaphirGlobalCrop400.png")
            elif i["Valeur"]==102:
                imBadge=Image.open("Images/Badges/400/RubisGlobalRec400.png")
            else:
                imBadge=Image.open("Images/Badges/400/DiamantGlobalRect400.png")
            imBadge=imBadge.resize((175,165))
            im.paste(imBadge, ((im.size[0]-imBadge.size[0])//2,460),mask=imBadge)
        elif i["Valeur"]==13:
            imOr=Image.open("Images/Badges/400/BadgeOrAnneeCrop400.png")
            imOr=imOr.resize((25,35))
            im.paste(imOr, ((im.size[0]-imOr.size[0])//2+120,485),mask=imOr)
        elif i["Valeur"]==12:
            imOr=Image.open("Images/Badges/400/BadgeArgentAnneeCrop400.png")
            imOr=imOr.resize((25,35))
            im.paste(imOr, ((im.size[0]-imOr.size[0])//2+120,525),mask=imOr)
        elif i["Valeur"]==11:
            imOr=Image.open("Images/Badges/400/BadgeBronzeAnneeCrop400.png")
            imOr=imOr.resize((25,35))
            im.paste(imOr, ((im.size[0]-imOr.size[0])//2+120,565),mask=imOr)
        elif i["Valeur"]==3:
            imOr=Image.open("Images/Badges/400/OrBase2Crop400.png")
            imOr=imOr.resize((25,35))
            im.paste(imOr, ((im.size[0]-imOr.size[0])//2-120,485),mask=imOr)
        elif i["Valeur"]==2:
            imOr=Image.open("Images/Badges/400/ArgentBase2Crop400.png")
            imOr=imOr.resize((25,35))
            im.paste(imOr, ((im.size[0]-imOr.size[0])//2-120,525),mask=imOr)
        elif i["Valeur"]==1:
            imOr=Image.open("Images/Badges/400/BronzeBase2Crop400.png")
            imOr=imOr.resize((25,35))
            im.paste(imOr, ((im.size[0]-imOr.size[0])//2-120,565),mask=imOr)
        liste.append(i["Valeur"])
    
    imOr=Image.open("Images/Badges/400/Blank.png")
    imOr=imOr.resize((25,35))
    dictCoord={13:((im.size[0]-imOr.size[0])//2+120,485),12:((im.size[0]-imOr.size[0])//2+120,525),11:((im.size[0]-imOr.size[0])//2+120,565),3:((im.size[0]-imOr.size[0])//2-120,485),2:((im.size[0]-imOr.size[0])//2-120,525),1:((im.size[0]-imOr.size[0])//2-120,565)}
    for i in listeAll:
        if i not in liste:
            im.paste(imOr, dictCoord[i],mask=imOr)

    font1 = ImageFont.truetype("Font/RobotoCondensed-Regular.ttf", 25)
    font2 = ImageFont.truetype("Font/RobotoCondensed-Regular.ttf", 40)
    draw=ImageDraw.Draw(im)
    draw.text((im.size[0]//2,700),"{0}e victoire pour {1} !".format(wins,nom),(255,255,255),font=font1,anchor="mm",align="center")
    if texte!=None:
        draw.text((im.size[0]//2,650),'"{0}"'.format(texte),(255,255,255),font=font2,anchor="mm",align="center")

    im.save("Images/ExFond/{0}.png".format(user.id))


async def fondsUser(ctx,bot,args):
    try:
        if len(args)==0:
            await commandeTMP(ctx,None,False,None,"fonds")
            return
        
        connexion,curseur=connectSQL("OT","Titres","Titres",None,None)
        connexionUser,curseurUser=connectSQL("OT",ctx.author.id,"Titres",None,None)
        try:
            fond=curseur.execute("SELECT * FROM fonds WHERE (Guild=0 OR Guild={0}) AND ID={1}".format(ctx.guild.id,args[0])).fetchone()
            assert fond!=None
        except:
            raise AssertionError("Le fond que vous cherchez n'existe pas.")
        
        createAccount(connexionUser,curseurUser)
        coins=curseurUser.execute("SELECT * FROM coins").fetchone()["Coins"]
        assert coins>=fond["Prix"], "Vous n'avez pas assez d'OT Coins !"

        embed=createEmbed("Changement de fond","Vous êtes sur le point d'acheter le fond **{0}** pour *{1} <:otCOINS:873226814527520809>*.\nVous possèdez {2} <:otCOINS:873226814527520809> au total et en aurez {3} <:otCOINS:873226814527520809> après la transaction.\nAppuyez sur <:otVALIDER:772766033996021761> pour confirmer l'achat.".format(fond["Nom"],fond["Prix"],int(coins),int(coins-fond["Prix"])),0xf58d1d,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.author)

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
        assert coins>=fond["Prix"], "Vous n'avez pas assez d'OT Coins !"
        curseurUser.execute("UPDATE coins SET Coins=Coins-{0}".format(fond["Prix"]))

        if curseur.execute("SELECT * FROM cartes WHERE ID={0}".format(ctx.author.id)).fetchone()==None:
            curseur.execute("INSERT INTO cartes VALUES({0},'{1}','None')".format(ctx.author.id,fond["Path"]))
        else:
            curseur.execute("UPDATE cartes SET Fond='{0}' WHERE ID={1}".format(fond["Path"],ctx.author.id))

        connexion.commit()
        connexionUser.commit()

        embed=createEmbed("Fond équipé","Fond équipé avec succès !\nVotre nouveau fond est maintenant : **{0}**.".format(fond["Nom"]),0xf58d1d,"{0} {1}".format(ctx.invoked_parents[0],ctx.invoked_with.lower()),ctx.author)
        await ctx.reply(embed=embed)
    except AssertionError as er:
        await ctx.reply(embed=embedAssert(er))


async def texteFond(ctx,bot,args):
    try:
        assert len(args)!=0, "Vous devez me donner l'emote que vous voulez équiper !"
        clean=createPhrase(args)
        assert len(clean)<35, "Votre phrase ne doit pas dépasser les 35 caractères !"

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
    except AssertionError as er:
        await ctx.send(embed=embedAssert(er))
