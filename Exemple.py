import discord
from discord.ext import commands

intent=discord.Intents(messages=True,guilds=True,members=True,bans=False,emojis=False,integrations=False,webhooks=False,invites=False,voice_states=True, reactions=True)
bot=commands.Bot(command_prefix=(commands.when_mentioned_or('OT?')), case_insensitive=True, intents=intent,chunk_guilds_at_startup=True)
token=""

@bot.event 
async def on_ready():
    pass

@bot.listen()
async def on_message(message):
    pass

@bot.listen()
async def on_message_delete(message):
    pass

@bot.listen()
async def on_reaction_add(reaction,user):
    pass

@bot.listen()
async def on_raw_message_edit(payload):
    pass

@bot.event
async def on_command(ctx):
    pass

class Test(commands.Cog):
    @commands.command()
    async def test1(self,ctx,*args):
        pass
    @commands.command()
    async def test2(self,ctx,*args):
        pass
    @commands.command()
    async def test2(self,ctx,*args):
        pass

bot.add_cog(Test)
bot.run(token)