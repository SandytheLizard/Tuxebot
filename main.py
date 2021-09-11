# bot.py
from os import listdir

import discord
import json

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
mon_files = listdir(config["monfiles"])
tech_files = listdir(config["techfiles"])
images = config["images"]

client = discord.Client()


@client.event
async def on_message(message):
    # for now we only check for monsters,
    # but in future we can add techniques, npcs, etc.
    if message.content.startswith("/monster"):
        m = message.content
        if '.json' in m:
            m = m.replace('.json', '')
        for i in range(len(mon_files)):
            f = str(mon_files[i])
            if '.json in f':
                f = f.replace('.json', '')
            if f in m:
                curfile = open(mon_files[i])
                data = json.load(curfile)
                slug = data['slug']
                category = data['category']
                move_set = data['moveset']
                weight = data['weight']
                catch_rate = data['catch_rate']
                types = data['types']
                text = str(slug + ', the ' + category + ' Tuxemon\n')\
                    .join(str("Types:" + str(types)))\
                    .join(str("Weight: " + str(weight)))\
                    .join(str("Catch Rate: " + str(catch_rate) + '%'))\
                    .join(str('Learnable Moves: '))
                for j in range(len(move_set)):
                    text.join(str(move_set[j]))

                imagefront = discord.File(images + slug + '-front.png')
                imageback = discord.File(images + slug + '-back.png')

                await message.channel.send(content=text, files=[imagefront, imageback])


client.run(TOKEN)
