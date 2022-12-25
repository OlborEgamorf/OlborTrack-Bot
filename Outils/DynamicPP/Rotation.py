from random import choice

import discord
from colorthief import ColorThief
from Stats.SQL.ConnectSQL import connectSQL


async def rotation(guild,channel):
    connexion,curseur=connectSQL(guild.id)
    icons=curseur.execute("SELECT * FROM icons WHERE Rotation=0").fetchall()
    if len(icons)==0:
        curseur.execute("UPDATE icons SET Rotation=0")
        icons=curseur.execute("SELECT * FROM icons WHERE Rotation=0").fetchall()
        if len(icons)==0:
            return

    img=choice(icons)
    with open(img["Path"],"rb") as image:
        i=image.read()
    color=ColorThief(img["Path"]).get_color(quality=1)
    hexcolor=int('%02x%02x%02x' % color, base=16)

    try:
        await guild.edit(icon=i)
        embed=discord.Embed(title="Icone du serveur du jour !",color=hexcolor)
        if img["Description"]!="None":
            embed.description=img["Description"]
        else:
            embed.description="*Cette icone n'a pas encore de description !*"
        embed.set_image(url="https://cdn.discordapp.com/icons/{0}/{1}.png?size=600".format(guild.id,guild.icon.url))
        embed.set_author(icon_url="https://cdn.discordapp.com/icons/{0}/{1}.png".format(guild.id,guild.icon.url),name=guild.name)
        embed.set_footer(text="OT!dynicon")
        embed.add_field(name="Ajouté par",value="<@{0}>".format(img["Auteur"]),inline=True)
        if img["Membres"]!="None":
            members=img["Membres"].split(";")
            descip=""
            for i in members:
                descip+="<@{0}> ".format(i)
            embed.add_field(name="Membres présents",value=descip,inline=True)
        embed.add_field(name="N°",value="`{0}`".format(img["Nombre"]))
        if channel!=0:
            await guild.get_channel(channel).send(embed=embed)
    except:
        pass

    curseur.execute("UPDATE icons SET Rotation=1 WHERE Nombre={0}".format(img["Nombre"]))
    connexion.commit()
