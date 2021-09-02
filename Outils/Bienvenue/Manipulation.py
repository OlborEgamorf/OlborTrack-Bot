from colorthief import ColorThief
from PIL import ImageDraw, ImageFont, ImageOps, Image


def squaretoround(user):
    
    mask = Image.open('Images/mask.png').convert('L')
    im = Image.open('PNG/{0}.png'.format(user))

    output = ImageOps.fit(im, mask.size, centering=(0.5, 0.5))
    output.putalpha(mask)

    output.save('PNG/Round{0}.png'.format(user))


def fusion(back,user,text,couleur,taille,guild):
    
    img1 = Image.open(back)
    assert img1.size[0]>255 and img1.size[1]>255, "La taille de votre image doit être supérieure à 256 pixels, que ce soit en largeur ou en hauteur."
    
    img2 = Image.open("PNG/Round{0}.png".format(user.id))
    
    img1.paste(img2, ((img1.size[0]-img2.size[0])//2,(img1.size[1]-img2.size[1])//2), mask = img2)

    if text not in (None,"None"):
        setText(img1,img2,back,user,text,couleur,taille,guild)

    img1.save("Temp/BV{0}.png".format(user.id))


def formatage(alerte,user,guild):
    new=""
    mention=alerte.split("{user}")
    longMention=len(mention)
    for i in range(longMention):
        new+=mention[i]
        if i!=longMention-1:
            new+="<@{0}>".format(user.id)
    
    newN=""
    name=new.split("{name}")
    longName=len(name)
    for i in range(longName):
        newN+=name[i]
        if i!=longName-1:
            newN+="{0}".format(user.name)

    newG=""
    guildName=newN.split("{guild}")
    longGuild=len(guildName)
    for i in range(longGuild):
        newG+=guildName[i]
        if i!=longGuild-1:
            newG+="{0}".format(guild.name)

    newN=""
    number=newG.split("{number}")
    longNumb=len(number)
    for i in range(longNumb):
        newN+=number[i]
        if i!=longNumb-1:
            newN+="{0}".format(guild.member_count)
    
    return newN


def setText(img1,img2,back,user,text,couleur,taille,guild):
    if couleur=="default":
        color=ColorThief(back).get_color(quality=1)
        if color[0]*0.21+color[1]*0.72+color[2]*0.07<50:
            color=(255,255,255)
        else:
            color=(0,0,0)
    else:
        dictColor={"blanc":(255,255,255),"noir":(0,0,0),"rouge":(255,0,0),"vert":(0,255,0),"bleu":(0,0,255),"jaune":(221,255,0),"cyan":(0,251,255)}
        color=dictColor[couleur]
    font = ImageFont.truetype("Font/RobotoCondensed-Regular.ttf", taille)
    text=formatage(text,user,guild)
    textAlign=""
    maxi=img1.size[0]-img1.size[0]//10
    nb=0
    pix=taille*30/50
    for i in text.split(" "):
        if len(i)*pix>maxi:
            cut=0
            textAlign+=" "
            for j in i:
                if cut>maxi:
                    textAlign+="\n"
                    cut=0
                textAlign+=j
                cut+=pix
            textAlign+=" "
            nb=cut
            continue
        elif len(i)*pix+nb>maxi:
            textAlign+="\n"
            nb=0
        else:
            textAlign+=" "
        textAlign+=i
        nb+=len(i)*pix

    draw=ImageDraw.Draw(img1)
    draw.text((img1.size[0]//2,(img1.size[1]-img2.size[1])//2+img1.size[1]//2),textAlign[1:],color,font=font,anchor="mm",align="center")
