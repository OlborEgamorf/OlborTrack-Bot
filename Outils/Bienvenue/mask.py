from PIL import Image, ImageDraw, ImageFont, ImageOps
from Core.Fonctions.Embeds import createEmbed, embedAssert
from Core.Fonctions.Phrase import createPhrase
from Stats.SQL.ConnectSQL import connectSQL
from Core.Fonctions.WebRequest import getAttachment, getAvatar
import discord
from colorthief import ColorThief
import asyncio
from time import strftime


def fusionAdieu(back,user,text,guild):
    
    img1 = Image.open(back)
    assert img1.size[0]>255 and img1.size[1]>255, "La taille de votre image doit être supérieure à 256 pixels, que ce soit en largeur ou en hauteur."
    
    img2 = Image.open("PNG/Round{0}.png".format(user.id))
    img3 = Image.open("Images/Cross.png")

    img1.paste(img2, ((img1.size[0]-img2.size[0])//2,(img1.size[1]-img2.size[1])//2), mask = img2)
    img1.convert('L')
    img1.paste(img3, ((img1.size[0]-img2.size[0])//2,(img1.size[1]-img2.size[1])//2), mask = img3)

    if text!=None:
        setText(img1,img2,back,user,text,guild)

    img1.save("Temp/AD{0}.png".format(user.id))