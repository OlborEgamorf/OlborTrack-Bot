import discord

def embedSV(table,page,pagemax):
    descip=""
    stop=15*page if 15*page<len(table) else len(table)
    for i in range(15*(page-1),stop):
        if table[i]["Image"]!="None":
            image="**+ Image**"
        else:
            image=""
        if len(table[i]["Texte"])>110:
            descip+="`{0}` : {1}... {2}\n".format(table[i]["Count"],table[i]["Texte"][0:110],image)
        else:
            descip+="`{0}` : {1} {2}\n".format(table[i]["Count"],table[i]["Texte"],image)
    embed=discord.Embed(title="Phrases OT!savezvous",description=descip,color=0x00ffd0)
    embed.set_footer(text="Page {0}/{1}".format(page,pagemax))
    return embed