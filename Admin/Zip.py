### OBSOLETE, A METTRE A JOUR JE PENSE

import zipfile
import discord
import os
from Core.Fonctions.Embeds import createEmbed

async def exeZip(ctx,bot):
    """Cette fonction regroupe les stats du serveur dans un fichier .zip et l'envoie, pour pouvoir les consulter.
    
    La commande a un cooldown élevé."""
    try:
        ziph = zipfile.ZipFile("SQL/{0}/{0}.zip".format(ctx.guild.id), 'w', zipfile.ZIP_DEFLATED)
        embed=createEmbed("Le fichier .zip se génère.","Quand ce sera terminé, il vous sera envoyé par message privé.",0x220cc9,ctx.invoked_with.lower(),ctx.guild)
        await ctx.send(embed=embed)
        for root, dirs, files in os.walk("SQL/{0}".format(ctx.guild.id)):
            for file in files:
                ziph.write(os.path.join(root, file))
        ziph.close()
        embedF=discord.Embed(title="<:otVERT:718396570638483538> Voici les données de votre serveur.", description="Vous pouvez en refaire la demande quand vous le souhaitez.", color=0x339966)
        embedF.set_footer(text="OT!zip")
        await ctx.author.send(embed=embedF,file=discord.File("SQL/{0}/{0}.zip".format(ctx.guild.id)))
    except:
        await ctx.send("Je n'ai pas réussi à envoyer le fichier. Soit vos DMs sont désactivés, soit le fichier est trop lourd pour être envoyé.")
    os.remove("SQL/{0}/{0}.zip".format(ctx.guild.id))
    return