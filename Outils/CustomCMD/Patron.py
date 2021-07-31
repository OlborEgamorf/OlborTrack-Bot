### PAS ENCORE INTÉGRÉ

import discord

def CCMDpatron():
    """Patron d'aide"""
    embedT=discord.Embed(title="OT!customcmd titre [commande] ['del'/contenu autre]", description="OT!customcmd description [commande] [contenu]\n<--- OT!customcmd couleur [commande] ['blue'/'yellow'/'orange'/'green'/'pink'/'black'/'white'/'violet'/'cyan'/'red'/'turquoise'/'dblue'/'dgreen'/'user'/'olbor']")
    embedT.set_footer(text="OT!customcmd bas [commande] ['del'/contenu autre]")
    embedT.set_image(url="https://media.discordapp.net/attachments/752150155276451993/869951060784066600/fgsdfgqsdfgqsfdg.PNG")
    embedT.set_thumbnail(url="https://media.discordapp.net/attachments/752150155276451993/869951062323380274/dsfgqsdfqsdfg.PNG")
    embedT.set_author(name="OT!customcmd auteur [commande] ['user'/'guild'/'del'/mention d'un membre/texte autre]")
    return embedT