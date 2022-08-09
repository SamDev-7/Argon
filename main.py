import subprocess

def background_execute(command):
    subprocess.Popen(command,shell=True,stdout=True)

background_execute(['rasa run actions'])
background_execute([f'&& rasa run -m models'])

import bot
