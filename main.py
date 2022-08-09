import os
from threading import Thread

def background_execute(command):
    
    def run():
        print(f"Running {command}")
        os.system(command)
        
    Thread(target=run).start()

background_execute(f'rasa run actions --auth-token {os.getenv("RASA_TOKEN")}')
background_execute('export PYTHONPATH=/home/runner/Command-RASA/ && rasa run --response-timeout 20')

import bot
