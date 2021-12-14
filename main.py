import io

from discord import Embed
from jinja2 import Template
from PIL import Image
from table2ascii import PresetStyle, table2ascii
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
monster_template = "monster_template.j2"
monster_command = "=monster"

# global objects
monsters = load_json(data_root, "mods/tuxemon/db/monster")
techniques = load_json(data_root, "mods/tuxemon/db/technique")
images = data_root + "mods/tuxemon/gfx/sprites/battle/"
client = discord.Client()


def slug2title(text):
    return text.replace("_", " ").title()


def monster_embed(slug):
    # open template each time so it can be edited live
    with open(monster_template) as fp:
        message_template = Template(fp.read())
    data = monsters[slug]
    moves_table = table2ascii(
        style=PresetStyle.markdown,
        header=["Name", "Level Learned"],
        body=[
            [slug2title(i["technique"]), str(i["level_learned"])]
            for i in data["moveset"]
        ],
    )
    description = message_template.render(
        catch_rate=data["catch_rate"],
        category=data["category"],
        moves_table=moves_table,
        moveset=data["moveset"],
        name=slug,
        slug=slug,
        types=data["types"],
        weight=data["weight"],
    )
    embed = Embed(
        color=discord.Color.red(),
        description=description,
        image="attachment://image.png",
        title=f'{slug2title(slug)} the {slug2title(data["category"])} Tuxemon',
        type="rich",
    )
    buf = io.BytesIO()
    front = Image.open(images + slug + "-front.png")
    front = front.resize((128, 128), resample=Image.NEAREST)
    back = Image.open(images + slug + "-back.png")
    back = back.resize((128, 128), resample=Image.NEAREST)
    menu01 = Image.open(images + slug + "-menu01.png")
    menu01 = menu01.resize((48, 48), resample=Image.NEAREST)
    menu02 = Image.open(images + slug + "-menu02.png")
    menu02 = menu02.resize((48, 48), resample=Image.NEAREST)
    comp = Image.new("RGBA", (314, 128))
    comp.paste(menu01, (0, 0))
    comp.paste(menu02, (0, 56))
    comp.paste(back, (58, 0))
    comp.paste(front, (186, 0))
    comp.save(buf, "png")
    buf.seek(0)
    files = [
        discord.File(fp=buf, filename="image.png"),
        # discord.File(images + slug + "-back.png", filename="back.png"),
    ]
    return embed, files


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
                embed, files = monster_embed(slug)
                await message.channel.send(embed=embed, files=files)


if __name__ == "__main__":
    client.run(token)
