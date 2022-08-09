import io
import os
import aiohttp
import disnake
import traceback
from aiohttp_retry import RetryClient, ExponentialRetry
from disnake.ext import commands

# Cog class
class ListenMsgs(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.allowed_mentions = disnake.AllowedMentions.none()

    async def fetch_rasa(self, message: str, usrid: str, already_tried=False):
        data = {
            "message": message,
            'sender': usrid
        }
            
        async with RetryClient(timeout=aiohttp.ClientTimeout(total=5), retry_options=ExponentialRetry(attempts=3)) as session:
            try:
                async with session.post(f'http://localhost:5005/webhooks/restauth/webhook?token={os.getenv("RASA_TOKEN")}', json=data) as r:
                    if r.status == 200:
                        data = await r.json()
                        if len(data) <= 0:
                            if already_tried == True:
                                raise Exception("Empty response from Rasa")
                            return await self.fetch_rasa(message, usrid, True)
                        text = []
                        images = []
                        urls = []
                        for entry in data:
                            if 'image' in entry:
                                urls.append(entry['image'])
                            if 'text' in entry:
                                text.append(entry['text'])
                        for i, image in enumerate(urls):
                            async with session.get(image) as r2:
                                buffer = io.BytesIO(await r2.read())
                                images.append(disnake.File(buffer, filename = f'{i}.jpg'))
                        if len(images) == 0:
                            images = None
                        return ' '.join(text), images
                    else:
                        raise Exception(f"Rasa: Not OK: {r.status}")
            except Exception:
                traceback.print_exc()
                return 'Uh oh! There was an error connecting to our servers, try again later! Error Code: `RW`', None

    async def parse_vars(self, text: str, member: disnake.Member):
        text = text.replace("[NAME]", member.display_name)

        return text
    
    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return
        if not message.content:
            return

        # Mentioned bot
        if message.content.startswith('<@1004936113384869968>'):
            message.content = message.content.replace('<@1004936113384869968>', '', 1).strip()

        if len(message.content) == 0:
            message.content = "who are you?"

        async with message.channel.typing():
            text, images = await self.fetch_rasa(message.content, str(message.author.id))
            text = await self.parse_vars(text, message.author)
            try:
                await message.reply(text, mention_author=False, files=images, allowed_mentions=self.allowed_mentions)
            except Exception:
                traceback.print_exc()
                await message.reply("Uh oh! Our servers are having some issues processing your message, try again later! Error Code: `SMCNS`", mention_author=False)

    @commands.slash_command()
    async def chat(self, inter, message: str):
        """
        Chat with the bot privately
    
        Parameters
        ----------
        message: The message to send the bot
        """
        text, images = await self.fetch_rasa(message, str(inter.author.id))
        text = await self.parse_vars(text, inter.author)
        try:
            if images:
                await inter.response.send_message(text, ephemeral=True, files=images)
            else:
                await inter.response.send_message(text, ephemeral=True)
        except Exception:
            traceback.print_exc()
            await inter.response.send_message("Uh oh! Our servers are having some issues processing your message, try again later! Error Code: `SMCNS`", ephemeral=True)

    @commands.slash_command()
    async def help(self, inter):
        """
        Some useful information about me!
        """
        text, images = await self.fetch_rasa('who are you?', str(inter.author.id))
        text = await self.parse_vars(text, inter.author)
        try:
            await inter.response.send_message(text, ephemeral=True)
        except Exception:
            traceback.print_exc()
            await inter.response.send_message("Uh oh! Our servers are having some issues processing your message, try again later! Error Code: `SMCNS`", ephemeral=True)
        
# Setup
def setup(bot):
	bot.add_cog(ListenMsgs(bot))