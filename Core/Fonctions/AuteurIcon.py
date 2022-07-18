from Stats.SQL.EmoteDetector import emoteDetector

def auteur(nom,avatar,embed,option):
    if avatar==None and option=="guild":
        embed.set_author(name=nom)
    elif avatar==None and option=="user":
        embed.set_author(name=nom)
    else:
        if option=="user":
            embed.set_author(name=nom, icon_url=avatar.url)
        elif option=="guild":
            embed.set_author(name=nom, icon_url=avatar.url)
    return embed

def auteurJeux(user,embed):
    if user.emote!=None:
        embed.set_author(name=user.titre,icon_url="https://cdn.discordapp.com/emojis/{0}.png".format(emoteDetector(user.emote)[0]))
    else:
        embed.set_author(name=user.titre)