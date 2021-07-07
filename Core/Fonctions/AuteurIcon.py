### Ligne auteur des embeds
def auteur(id,nom,avatar,embed,option):
    if option=="olbor":
        embed.set_author(name="Olbor Track Bot",icon_url=id.avatar_url)
        # https://media.discordapp.net/attachments/726034739550486618/768453640943042580/logoBldsqdeuddf.png
    elif option=="mal":
        embed.set_author(name="My Anime List",icon_url="https://cdn.discordapp.com/attachments/726034739550486618/755124985282166905/index.jpg")
    elif option=="wp":
        embed.set_author(name="Wikipédia",icon_url="https://cdn.discordapp.com/attachments/726034739550486618/757641659285635142/Wikipedia-logo-v2.png",url=id)
    elif option=="spo":
        embed.set_author(name="Spotify",icon_url="https://media.discordapp.net/attachments/726034739550486618/763482063319203950/Spotify_Icon_RGB_Green.png?width=676&height=676",url=id)
    elif option=="nasa":
        embed.set_author(name="NASA",icon_url="https://media.discordapp.net/attachments/726034739550486618/769603075282305044/nasa-vector-logo-small.png",url=id)
    elif option=="map":
        embed.set_author(name="Géographie",icon_url="https://media.discordapp.net/attachments/726034739550486618/769615020568608848/1f30d.png")
    elif option=="emote":
        if avatar.animated==True:
            embed.set_author(name=nom,icon_url="https://cdn.discordapp.com/emojis/"+str(id)+".gif")
        else:
            embed.set_author(name=nom,icon_url="https://cdn.discordapp.com/emojis/"+str(id)+".png")
    elif avatar==None and option=="guild":
        embed.set_author(name=nom, icon_url='https://cdn.discordapp.com/icons/'+str(id))
    elif avatar==None and option=="user":
        embed.set_author(name=nom, icon_url=('https://cdn.discordapp.com/avatars/'+str(id)))
    else:
        if avatar[1]=="_":
            sufx=".gif"
        else:
            sufx=".png"
        if option=="user":
            embed.set_author(name=nom, icon_url=('https://cdn.discordapp.com/avatars/'+str(id)+"/"+avatar+sufx))
        elif option=="guild":
            embed.set_author(name=nom, icon_url=('https://cdn.discordapp.com/icons/'+str(id)+"/"+avatar+sufx))
    return embed
#####


### Icon pour affichage log
def icon(id,avatar,option):
    if option=="emote":
        if avatar==None:
            link="https://cdn.discordapp.com/emojis/"+str(id)+".png"
        elif avatar.animated==True:
            link="https://cdn.discordapp.com/emojis/"+str(id)+".gif"
        else:
            link="https://cdn.discordapp.com/emojis/"+str(id)+".png"
    elif avatar==None:
        link=('https://cdn.discordapp.com/avatars/'+str(id))
    else:
        if avatar[1]=="_":
            sufx=".gif"
        else:
            sufx=".png"
        if option=="guild":
            link=('https://cdn.discordapp.com/icons/'+str(id)+"/"+avatar+sufx)
        else:
            link=('https://cdn.discordapp.com/avatars/'+str(id)+"/"+avatar+sufx)
    return link
#####