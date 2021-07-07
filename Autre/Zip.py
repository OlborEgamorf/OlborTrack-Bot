### OBSOLETE, A METTRE A JOUR JE PENSE

import zipfile
import discord
import os

async def exeZip(ctx,bot):
    """Cette fonction regroupe les stats du serveur dans un fichier .zip et l'envoie, pour pouvoir les consulter.
    
    La commande a un cooldown élevé."""
    ziph = zipfile.ZipFile("_"+str(ctx.guild.id)+".zip", 'w', zipfile.ZIP_DEFLATED)
    embedF=discord.Embed(title="<:otVERT:718396570638483538> Demande en cours d'exécution.", description="Vous allez recevoir vos données par message privé dans quelques instants.", color=0x339966)
    embedF.set_footer(text="OT!zip")
    await ctx.send(embed=embedF)
    for root, dirs, files in os.walk("SQL/"+str(ctx.guild.id)):
        for file in files:
            ziph.write(os.path.join(root, file))
    ziph.close()
    embedF=discord.Embed(title="<:otVERT:718396570638483538> Voici les données de votre serveur.", description="Vous pouvez en refaire la demande quand vous le souhaitez.", color=0x339966)
    embedF.set_footer(text="OT!zip")
    await ctx.author.send(embed=embedF,file=discord.File("_"+str(ctx.guild.id)+".zip"))
    return