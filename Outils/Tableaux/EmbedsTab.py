from Core.Fonctions.Embeds import createEmbed


def embedStarBoard(user,content,channel,image,id,link):
    embedS=createEmbed("",content,user.color.value,"tableau",user)
    if image!=[]:
        embedS.set_image(url=image[0].url)
    embedS.add_field(name="Salon",value="<#{0}>".format(channel),inline=True)
    embedS.add_field(name="Contexte",value="[Lien vers le message !]({1})".format(channel,link),inline=True)
    return embedS
