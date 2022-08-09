import os
import aiohttp
import disnake
import asyncio
from disnake.ext import commands

bot = commands.Bot(command_prefix=commands.when_mentioned, owner_id=790675967982436363, activity=disnake.Game(name='Starting...'), status=disnake.Status.dnd)
bot.remove_command('help')

cogs = ['info', 'listen_msgs']

@bot.event
async def on_ready():
    
    bot.load_extension("jishaku")

    print("Waiting for RASA servers...")

    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5)) as session:
        while True:
            try:
                async with session.get('http://localhost:5005/') as resp:
                    if resp.status == 200:
                        async with session.get(f'http://localhost:5055?token={os.getenv("RASA_TOKEN")}') as resp2:
                            if resp2.status == 404:
                                await bot.change_presence(activity=disnake.Game(name='Mention me to chat!'), status=disnake.Status.online)
                                break
                            else:
                                raise Exception("Action server not ready")
                    else:
                        raise Exception("Rasa server not ready")
            except:
                await asyncio.sleep(5)

    for cog in cogs:
        bot.load_extension(f"cogs.{cog}")
        
    print(f"Logged in as {bot.user}")

#@bot.slash_command(description="Get bot latency.")
async def ping(self, inter):
    await inter.response.send_message(f"Pong! `{round(self.bot.latency*1000,2)}ms`", ephemeral=True)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        return
    raise error

bot.run(os.environ['BOT_TOKEN'])
