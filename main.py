from jinja2 import Template
import os
import discord
import json


def load_json(root, folder):
    values = dict()
    db_path = os.path.join(root, folder)
    paths = [os.path.join(db_path, fn) for fn in os.listdir(db_path)]
    for path in paths:
        with open(path) as fp:
            data = json.load(fp)
        slug = data["slug"]
        assert slug not in values
        values[slug] = data
    return values

# config
token = ""
data_root = "/home/ltheden/Tuxemon-development/"
monster_template = "monster_template.json"
monster_command = "=monster"

# global objects
monsters = load_json(data_root, "mods/tuxemon/db/monster")
techniques = load_json(data_root, "mods/tuxemon/db/technique")
images = data_root + "mods/tuxemon/gfx/sprites/battle/"
client = discord.Client()


@client.event
async def on_message(message):
    # for now we only check for monsters,
    # but in future we can add techniques, npcs, etc.
    if message.content.startswith(monster_command):
        m = message.content.strip()
        try:
            command, slug = m.split()
        except:
            pass
        else:
            if slug in monsters:
                # open template each time so it can be edited live
                with open(monster_template) as fp:
                    message_template = Template(fp.read())
                data = monsters[slug]
                content = message_template.render(
                    name=slug,
                    slug=slug,
                    category=data["category"],
                    moveset=data["moveset"],
                    weight=data["weight"],
                    catch_rate=data["catch_rate"],
                    types=data["types"],
                )
                imagefront = discord.File(images + slug + "-front.png")
                imageback = discord.File(images + slug + "-back.png")
                await message.channel.send(
                    content=content,
                    files=[imagefront, imageback],
                )


if __name__ == "__main__":
    client.run(token)
