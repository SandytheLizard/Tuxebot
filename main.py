# bot.py
from os import listdir
from os.path import isfile, join

import discord, json

load_dotenv()
TOKEN = ''
GUILD = '8'
onlyfiles = [f for f in listdir(mypath) if isfile(join(mypath, f))]
client = discord.Client()
@client.event
async def on_message(message):
    if "=" in message.content:
        for i in enumerate(onlyfiles):
            if str(onlyfiles[i]) in  message.content:
                curfile = open(onlyfiles[i])
                data = json.load(curfile)
                

client.run(TOKEN)
