import discord
from random import choice
import asyncio
from Fonctions.EcritureRecherche3 import rechercheCsv

async def changepres(active,client):
    '''Changement de statut toutes les 150secondes'''
    pres=rechercheCsv("pres",0,0,0,0,0)[0]
    while active:
        i=choice(pres)
        await client.change_presence(status=discord.Status.dnd, activity=discord.Game(name=i["Statut"]))
        # await client.change_presence(status=discord.Status.idle, activity=discord.Game(name="OT!"+commands[i]+" : "+pres[i]+" | OT!help"))
        if i["Statut"]=="J'aime Zey.":
            await asyncio.sleep(5)
        else:
            await asyncio.sleep(150)