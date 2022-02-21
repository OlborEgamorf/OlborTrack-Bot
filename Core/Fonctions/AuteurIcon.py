### Ligne auteur des embeds
def auteur(id,nom,avatar,embed,option):
    if option=="olbor":
        embed.set_author(name="Olbor Track Bot",icon_url=id.avatar_url)
        # https://media.discordapp.net/attachments/726034739550486618/768453640943042580/logoBldsqdeuddf.png
    elif option=="wp":
        embed.set_author(name="Wikipédia",icon_url="https://cdn.discordapp.com/attachments/726034739550486618/757641659285635142/Wikipedia-logo-v2.png",url=id)
    elif option=="nasa":
        embed.set_author(name="NASA",icon_url="https://media.discordapp.net/attachments/726034739550486618/769603075282305044/nasa-vector-logo-small.png",url=id)
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
#####