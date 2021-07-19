import asyncio
from random import choice

import discord


async def changeStatut(bot):
    '''Changement de statut toutes les deux minutes'''
    listeStatut=[]
    for i in bot.commands:
        listeStatut.append("OT!help | OT!{0} : {1}".format(i.name, i.help))
    while True:
        await bot.change_presence(status=discord.Status.online, activity=discord.Game(name=choice(listeStatut)))
        await asyncio.sleep(120)