from Stats.SQL.EmoteDetector import emoteDetector

def auteur(id,nom,avatar,embed,option):
    if option=="olbor":
        embed.set_author(name="Olbor Track Bot",icon_url=id.avatar_url)
        # https://media.discordapp.net/attachments/726034739550486618/768453640943042580/logoBldsqdeuddf.png
    elif avatar==None and option=="guild":
        embed.set_author(name=nom)
    elif avatar==None and option=="user":
        embed.set_author(name=nom)
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

def auteurJeux(user,embed):
    if user.emote!=None:
        embed.set_author(name=user.titre,icon_url="https://cdn.discordapp.com/emojis/{0}.png".format(emoteDetector(user.emote)[0]))
    else:
        embed.set_author(name=user.titre)