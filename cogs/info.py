from disnake.ext import commands

# Cog class
class Info(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    # Ping command
    @commands.slash_command(description="Get the bot's latency")
    async def ping(self, inter):
        await inter.response.send_message(f"Pong! `{round(self.bot.latency*1000,2)}ms`", ephemeral=True)
    
# Setup
def setup(bot):
	bot.add_cog(Info(bot))