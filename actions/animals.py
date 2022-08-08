# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import random
import aiohttp 

async def get_cat(dispatcher: CollectingDispatcher):
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5)) as session:
        try:
            async with session.get('https://api.thecatapi.com/v1/images/search') as resp:
                if resp.status == 200:
                    data = await resp.json() 
                    dispatcher.utter_message(image=data[0]['url'])
                else:
                    dispatcher.utter_message(text="Uh oh! There was an error connecting to external sevices, try again later! Error Code: `CANOK`")
        except aiohttp.client_exceptions.ClientConnectorError:
            dispatcher.utter_message(text="Uh oh! There was an error connecting to external sevices, try again later! Error Code: `CANCN`")

    return []

async def get_dog(dispatcher: CollectingDispatcher):
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5)) as session:
        try:
            async with session.get('https://api.thedogapi.com/v1/images/search') as resp:
                if resp.status == 200:
                    data = await resp.json() 
                    dispatcher.utter_message(image=data[0]['url'])
                else:
                    dispatcher.utter_message(text="Uh oh! There was an error connecting to external sevices, try again later! Error Code: `DONOK`")
        except aiohttp.client_exceptions.ClientConnectorError:
            dispatcher.utter_message(text="Uh oh! There was an error connecting to external sevices, try again later! Error Code: `DONCN`")

    return []

async def get_duck(dispatcher: CollectingDispatcher):
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5)) as session:
        try:
            async with session.get('https://random-d.uk/api/v2/random') as resp:
                if resp.status == 200:
                    data = await resp.json() 
                    dispatcher.utter_message(image=data['url'])
                else:
                    dispatcher.utter_message(text="Uh oh! There was an error connecting to external sevices, try again later! Error Code: `DUNOK`")
        except aiohttp.client_exceptions.ClientConnectorError:
            dispatcher.utter_message(text="Uh oh! There was an error connecting to external sevices, try again later! Error Code: `DUNCN`")

    return []

async def get_fox(dispatcher: CollectingDispatcher):
    async with aiohttp.ClientSession(timeout=aiohttp.ClientTimeout(total=5)) as session:
        try:
            async with session.get('https://randomfox.ca/floof/') as resp:
                if resp.status == 200:
                    data = await resp.json() 
                    dispatcher.utter_message(image=data['image'])
                else:
                    dispatcher.utter_message(text="Uh oh! There was an error connecting to external sevices, try again later! Error Code: `FXNOK`")
        except aiohttp.client_exceptions.ClientConnectorError:
            dispatcher.utter_message(text="Uh oh! There was an error connecting to external sevices, try again later! Error Code: `FXNCN`")

    return []

class ImageAnimal(Action):

    def name(self) -> Text:
        return "action_image_animal"

    async def run(self, dispatcher: CollectingDispatcher,
        tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            animal = next(tracker.get_latest_entity_values("animal"), None)
            animals = ['dog', 'cat', 'duck', 'fox']
            if not animal:
                animal = random.choice(animals)

            if animal == 'dog':
                return await get_dog(dispatcher)
            elif animal == 'cat':
                return await get_cat(dispatcher)
            elif animal == 'duck':
                return await get_duck(dispatcher)
            elif animal == 'fox': 
                return await get_fox(dispatcher)

        