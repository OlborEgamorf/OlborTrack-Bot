### PAS ENCORE INTÉGRÉ

import discord

def CCMDpatron():
    """Patron d'aide"""
    embedT=discord.Embed(title="OT!customcmd titre [commande]", description="OT!customcmd description [commande]\n<--- OT!customcmd couleur [commande]")
    embedT.set_footer(text="OT!customcmd bas [commande]")
    embedT.set_image(url="https://media.discordapp.net/attachments/752150155276451993/869951060784066600/fgsdfgqsdfgqsfdg.PNG")
    embedT.set_thumbnail(url="https://media.discordapp.net/attachments/752150155276451993/869951062323380274/dsfgqsdfqsdfg.PNG")
    embedT.set_author(name="OT!customcmd auteur [commande]")
    return embedT