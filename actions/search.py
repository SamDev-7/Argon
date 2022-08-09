import json
from typing import Any, Text, Dict, List, Tuple
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import aiohttp 
import traceback
import disnake
import urllib.parse
from actions import wolfram

class Search(Action):

    def name(self) -> Text:
        return "action_search"

    def truncate(self, string, max_length):
        if len(string) > max_length:
            return string[:(max_length-1)] + '…'
        return string

    async def get_duck_duck_go(self, dispatcher: CollectingDispatcher, question: str) -> bool:
        async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=10)) as session:
            try:
                async with session.get(f"https://api.duckduckgo.com/?q={urllib.parse.quote(question, safe='')}&format=json&t=argon") as resp:
                    if resp.status == 200:
                        data = await resp.json(content_type=None) 
                        
                        if data['AbstractText']:
                            embed = disnake.Embed(title=self.truncate(question, 256), color=0x5865F2)
                            embed.url = f"https://duckduckgo.com/?q={urllib.parse.quote(question, safe='')}&t=argon"
                            embed.set_author(name=f"Results from {data['AbstractSource']}", url=data['AbstractURL'])
                            embed.description = self.truncate(data['AbstractText'], 4096)
                            embed.url = data['AbstractURL']
                            if data['Image']:
                                embed.set_thumbnail(url=f"https://api.duckduckgo.com{data['Image']}")
                            embed.set_footer(text="Powered by DuckDuckGo", icon_url="https://duckduckgo.com/assets/logo_header.v108.png")
                            
                            dispatcher.utter_message(json_message={"embed": embed.to_dict()})
                            return True
                        else:
                            return None

                    else:
                        dispatcher.utter_message(text="Uh oh! There was an error connecting to external sevices, try again later! Error Code: `DGNOK`")
                        return False
            except:
                traceback.print_exc()
                dispatcher.utter_message(text="Uh oh! There was an error connecting to external sevices, try again later! Error Code: `DGNCN`")
                return False

    async def get_wolfram_alpha(self, dispatcher: CollectingDispatcher, question: str) -> bool:
        w = wolfram.Wolfram()
        try:
            result = await w.request(question)
        except:
            traceback.print_exc()
            dispatcher.utter_message(text="Uh oh! There was an error connecting to external sevices, try again later! Error Code: `WAFERR`")
            return False
        if result['queryresult']['error']:
            #dispatcher.utter_message(text="Uh oh! There was an error connecting to external sevices, try again later! Error Code: `WAFQER`")
            #print(f"Error from wolfram: {result['queryresult']['error']['msg']}")
            return None
        if result['queryresult']['numpods'] == 0:
            return None

        embed = disnake.Embed(title=self.truncate(question, 256), color=0x5865F2, url=f"https://www.wolframalpha.com/input/?i={urllib.parse.quote(question, safe='')}")
        image_set = False
        for pod in result['queryresult']['pods'][:25]:
            if pod['id'] == 'Input':
                continue
            if not pod['subpods']:
                continue
            subpod = pod['subpods'][0]
            if subpod['plaintext']:
                embed.add_field(name=pod['title'], value=self.truncate(subpod['plaintext'], 4096), inline=False)
            elif subpod['img']:
                if not image_set:
                    embed.set_image(url=subpod['img']['src'])
                    image_set = True
        embed.set_footer(text="Powered by Wolfram|Alpha", icon_url="https://is3-ssl.mzstatic.com/image/thumb/Purple126/v4/f5/0c/96/f50c968c-28e1-e783-549e-b8f5d7571619/WolframAlpha-AppIcon-1x_U007emarketing-0-5-0-85-220.png/230x0w.webp")
        dispatcher.utter_message(json_message={"embed": embed.to_dict()})
        return True

    async def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        question = tracker.latest_message['text']
        if await self.get_duck_duck_go(dispatcher, question) == None:
            if await self.get_wolfram_alpha(dispatcher, question) == None:
                embed = disnake.Embed(title=self.truncate(question, 256), color=0xf84444, description="No results found.", url=f"https://duckduckgo.com/?q={urllib.parse.quote(question, safe='')}&t=argon")
                embed.set_footer(text="Click on the link to search on DuckDuckGo.", icon_url="https://duckduckgo.com/assets/logo_header.v108.png")
                dispatcher.utter_message(json_message={"embed": embed.to_dict()})
        return []