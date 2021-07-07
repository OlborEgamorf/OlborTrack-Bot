### Embed des tableaux
import discord
from Core.Fonctions.AuteurIcon import auteur

def embedStarBoard(user,content,channel,image,id,link):
    embedS=discord.Embed(description=content+"\n<#{0}> - [Contexte]({1})".format(channel,link),color=user.color.value)
    if user.nick!=None:
        embedS=auteur(user.id,user.nick,user.avatar,embedS,"user")
    else:
        embedS=auteur(user.id,user.name,user.avatar,embedS,"user")
    if id!=0:
        embedS.set_footer(icon_url="https://cdn.discordapp.com/emojis/"+str(id)+".png",text="OT!tableau")
    else:
        embedS.set_footer(text="OT!tableau")
    if image!=[]:
        embedS.set_image(url=image[0].url)
    return embedS
#####

def embedSB(guildOT):
    pass