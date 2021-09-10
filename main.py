# bot.py
from os import listdir
from os.path import isfile, join

import discord, json

# Load configuration
try:
    with open("config.json") as config_file:
        config = json.loads(config_file.read())
except:
    example_config = {"token":"", "monfiles":"", "techfiles":"","images":""}
    with open("config.json", "w") as config_file:
        config_file.write(json.dumps(example_config, indent=4))

    print("Empty config.json file created")
    exit(1)

# Verify if keys are not empty
for key in config:
    if not eval(f"len(config['{key}']) > 0"):
        print(f"Key {key} seems to be empty")
        exit(2)

# Apply configuration
TOKEN = config["token"]
monfiles = listdir(config["monfiles"])
techfiles = listdir(config["techfiles"])
images = config["images"]

client = discord.Client()
@client.event
async def on_message(message):
    if "=" in message.content:
        m = message.content
        if '.json' in m:
            m = m.replace('.json', '')
        for i in range(len(monfiles)):
            f =  str(monfiles[i])
            if '.json in f':
                f = f.replace('.json', '')
            if f in  m:
                curfile = open(config["monfiles"] + "/" + monfiles[i])
                data = json.load(curfile)
                slug = data['slug']
                category = data['category']
                moveset = data['moveset']
                weight = data['weight']
                catchrate = data['catch_rate']
                types = data['types']
                text = str(slug + ', the ' + category +' Tuxemon')
                await message.channel.send(text)
                text = str("Types:" + str(types))
                await message.channel.send(text)
                text = str("Weight: " + str(weight))
                await message.channel.send(text)
                text = str("Catch Rate: "+ str(catchrate) + '%')
                await message.channel.send(text)
                imagefrontstr = images + slug + '-front.png'
                imagebackstr = images + slug + '-back.png'
                imagefront = discord.File(imagefrontstr)
                imageback = discord.File(imagebackstr)
                await message.channel.send(file=imagefront)
                await message.channel.send(file=imageback)
                text = str('Learnable Moves: ')
                await message.channel.send(text)
                for j in range(len(moveset)):
                    text = str(moveset[j])
                    await message.channel.send(text)
client.run(TOKEN)
