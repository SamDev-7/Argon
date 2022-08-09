import os
import disnake
from disnake.ext import commands

bot = commands.Bot(command_prefix=disnake.ext.commands.when_mentioned, owner_id=790675967982436363, activity=disnake.Game(name='Mention me to chat!'))
bot.remove_command('help')

cogs = ['info', 'listen_msgs']

@bot.event
async def on_ready():
    
    bot.load_extension("jishaku")

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
