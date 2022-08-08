from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import aiohttp 

class GetJoke(Action):

    def name(self) -> Text:
        return "action_get_joke"

    async def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5)) as session:
                try:
                    async with session.get('https://v2.jokeapi.dev/joke/Miscellaneous,Pun?blacklistFlags=nsfw,religious,political,racist,sexist,explicit') as resp:
                        if resp.status == 200:
                            data = await resp.json() 
                            if data['type'] == 'single':
                                dispatcher.utter_message(text=data['joke'])
                            else:
                                dispatcher.utter_message(text=f"{data['setup']}\n||{data['delivery']}||")
                        else:
                            dispatcher.utter_message(text="Uh oh! There was an error connecting to external sevices, try again later! Error Code: `JKNOK`")
                except aiohttp.client_exceptions.ClientConnectorError:
                    dispatcher.utter_message(text="Uh oh! There was an error connecting to external sevices, try again later! Error Code: `JKNCN`")
        
            return []
