# bot.py
from os import listdir
from os.path import isfile, join

import discord, json

TOKEN = ''
monfiles = listdir('/home/pi/Desktop/bot/Tuxemon-development/mods/tuxemon/db/monster')
techfiles = listdir('/home/pi/Desktop/bot/Tuxemon-development/mods/tuxemon/db/technique')
images = '/home/pi/Desktop/bot/Tuxemon-development/mods/tuxemon/gfx/sprites/battle/'
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
                curfile = open(monfiles[i])
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
