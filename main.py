import discord
from discord import utils
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord_slash import SlashCommand
from utils import DATABASE as DB
from discord.utils import get
import os
import asyncio
from asyncio import sleep
import ast
import datetime
import config
from config import timeformMSK
from config import deltaMSK


client = commands.AutoShardedBot(shard_count=1, command_prefix = config.prefix,  intents = discord.Intents.all(), case_insensitive = True)
slash = SlashCommand(client, sync_commands=True)

client.remove_command('help')

@client.event
async def on_ready():
    client.start_time = datetime.datetime.now()
    ai = await client.application_info()
    client.owners = ai.team.members
    client.owner = {
        'id': [owner.id for owner in client.owners],
        'name': [owner.name for owner in client.owners]
    }
    client.premium_u = [511508551492173836,711826939224260618,714383981952630875,361156000155172865,683308136169603123,693151663321645098,768896954331430956]
    client.owner_g = [813511569521639474]
    client.premium_g = [828067961934839861,759796323569500160,707187238127009862]
    client.black_list = []
    client.guilds_id = [guild.id for guild in client.guilds]
    client.CHANNELS = {
        'idea': client.get_channel(813511569795055634),
        'bug': client.get_channel(813511569795055635),
        'review': client.get_channel(827809033188278292),
        'on_off': client.get_channel(813511570529320961),
        'guilds': client.get_channel(839649855839404043),
        'members': client.get_channel(839650083893149716)
    }
    client.COLORS = {
        'BASE': 0xFF8000,
        'SUCCESS': 0x80FF00,
        'ERROR': 0xFF0700,
        
        'red': 0xff1a1a,
        'dark_red': 0x992d22,
        'blue': 0x00ccff,
        'dark_blue': 0x206694,
        'orange': 0xff9100,
        'dark_orange': 0xa84300,
        'purple': 0x9b00ff,
        'dark_purple': 0x71368a,
        'green': 0x22ff00,
        'dark_green': 0x1f8b4c,
        'teel': 0x1abc9c,
        'dark_teel': 0x11806a,
        'grey': 0x979c9f,
        'dark_grey': 0x607d8b,
        'magenta': 0xe91e63, 
        'dark_magenta': 0xad1457,
        'gold': 0xf1c40f,
        'dark_gold': 0xc27c0e
    }
    client.EMOJIS = {
        'SUCCESS': client.get_emoji(835420636490235905),
        'ERROR': client.get_emoji(835420703029329931),
        
        "staff": client.get_emoji(815972657001660436),
        "partner": client.get_emoji(815972654326480906),
        "bug_hunter": client.get_emoji(815972668440182815),
        "hypesquad_bravery": client.get_emoji(815972658843484191),
        "hypesquad_brilliance": client.get_emoji(815972665763954689),
        "hypesquad_balance": client.get_emoji(815972662773809213),
        "early_supporter": client.get_emoji(815972640014598164),
        "system": client.get_emoji(815972642103361537),
        "bug_hunter_level_2": client.get_emoji(815972668440182815),
        "verified_bot": client.get_emoji(815972644884185128),
        "verified_bot_developer": client.get_emoji(815972649154641920),
        
        "dnd": client.get_emoji(813698546657787914),
        "idle": client.get_emoji(813698687913295894),
        "online": client.get_emoji(813698625569947680),
        "offline": client.get_emoji(813698775125983272),
    }
    await client.CHANNELS['guilds'].edit(name=f"серверов: {len(client.guilds)}")
    await client.CHANNELS['members'].edit(name=f"пользователей: {len(client.users)}")
    for cog in os.listdir('./Cogs'):
        if cog not in config.COGS_IGNORE:
            if cog.endswith('.py'):
                client.load_extension(f'Cogs.{cog.replace(".py", "")}')
    print("---------------------")
    print(f'{client.user}')
    print(f'{len(client.guilds)} сервера')
    print(f'Пинг: {round(client.latency, 3)} секунд')
    print('Я готов к работе')
    print("---------------------")
    discord.Webhook.partial(823524857118457908,"WLGIkThKQ89Xqcczs7soJt3C9iQu8stCfeL6k88npB2S9N_eKheejLHL4eJ_ZVHt5U57", adapter = discord.RequestsWebhookAdapter()).send(embed=discord.Embed(description=f"**------------------------------------**\n{client.user.mention}\n{len(client.guilds)} серверов\nПинг: {round(client.latency, 3)} секунд\n**запущен**\n**------------------------------------**",colour=config.COLORS['SUCCESS']))
    while True:
          await client.change_presence(status=discord.Status.online, activity=discord.Game(f"{config.prefix}help"))
          await sleep(30)
          await client.change_presence(status=discord.Status.online, activity=discord.Streaming(name="свои брутальные фотки", url="https://discord.com/"))
          await sleep(30)

@client.event
async def on_disconnect():
    print("---------------------")
    print(f'{client.user}')
    print(f'{len(client.guilds)} сервера')
    print('выключен.')
    print("---------------------")
    discord.Webhook.partial(823524874513416252,"eLGwHh4OLdjGeDTTvxd9WvPZ2DqEQLfZRXG2TFhBy_P_LWrEzUQ6JYix1IfHZ6lT-3fR", adapter = discord.RequestsWebhookAdapter()).send(embed=discord.Embed(description=f"**------------------------------------**\n{client.user.mention}\n{len(client.guilds)} серверов\n**выключен**\n**------------------------------------**",colour=config.COLORS['ERROR']))

@client.event
async def on_shard_connect(shard_id):
    print("---------------------")
    print(f"Шард\nбота {client.user}\n№ {int(shard_id) + 1}\nID {shard_id} \nуспешно запущен")
    print("---------------------")
    discord.Webhook.partial(823524881139892264, "-qckgNwCgOlqCrZjCQJTNTatH_XTqWT_Ulw0zH1rep-ymDzM0nAG8jemTjGp8NLlXKP5", adapter = discord.RequestsWebhookAdapter()).send(embed=discord.Embed(description=f"**------------------------------------**\nШард\nбота {client.user.mention}\n№ {int(shard_id) + 1}\nID {shard_id} \nуспешно запущен\n**------------------------------------**",colour=config.COLORS['SUCCESS']))

@client.event
async def on_shard_disconnect(shard_id):
    print("---------------------")
    print(f"Шард\nбота {client.user}\n№ {int(shard_id) + 1}\nID {shard_id} \nотключён")
    print("---------------------")
    discord.Webhook.partial(823524888945098812, "Kg4oKTQSzxrq7foJ0-E1NMrTJH69esLbOl1EWSnOzI-7LDTIZhQMSxzhsKwwBjq_kMsS", adapter = discord.RequestsWebhookAdapter()).send(embed=discord.Embed(description=f"**------------------------------------**\nШард\nбота {client.user.mention}\n№ {int(shard_id) + 1}\nID {shard_id} \nотключён\n**------------------------------------**",colour=config.COLORS['ERROR']))

if __name__ == '__main__':
    client.run(config.TOKEN)
