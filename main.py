import discord
from discord import utils
from discord.ext import commands
from discord.ext.commands import has_permissions
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

client.remove_command('help')

@client.event
async def on_ready():
    client.start_time = datetime.datetime.now()
    ai = await client.application_info()
    client.owners = ai.team.members
    client.premium = [714383981952630875,361156000155172865,683308136169603123,693151663321645098]
    client.black_list = []
    client.idea_channel = client.get_channel(813511569795055634)
    client.bug_channel = client.get_channel(813511569795055635)
    client.eval_fn_channel = client.get_channel(816209752249597952)
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
    discord.Webhook.partial(823524857118457908,"WLGIkThKQ89Xqcczs7soJt3C9iQu8stCfeL6k88npB2S9N_eKheejLHL4eJ_ZVHt5U57", adapter = discord.RequestsWebhookAdapter()).send(embed=discord.Embed(description=f"**------------------------------------**\n{client.user}\n{len(client.guilds)} серверов\nПинг: {round(client.latency, 3)} секунд\n**запущен**\n**------------------------------------**",colour=config.COLORS['SUCCESS']))
    while True:
          await client.change_presence(status=discord.Status.online, activity=discord.Game(f"{config.prefix}help"))
          await asyncio.sleep(30)
          await client.change_presence(status=discord.Status.online, activity=discord.Streaming(name="свои брутальные фотки", url="https://discord.com/"))
          await asyncio.sleep(30)

@client.event
async def on_disconnect():
    discord.Webhook.partial(823524874513416252,"eLGwHh4OLdjGeDTTvxd9WvPZ2DqEQLfZRXG2TFhBy_P_LWrEzUQ6JYix1IfHZ6lT-3fR", adapter = discord.RequestsWebhookAdapter()).send(embed=discord.Embed(description=f"**------------------------------------**\n{client.user}\n{len(client.guilds)} серверов\n**выключен**\n**------------------------------------**",colour=config.COLORS['ERROR']))

@client.event
async def on_shard_connect(shard_id):
    discord.Webhook.partial(823524881139892264, "-qckgNwCgOlqCrZjCQJTNTatH_XTqWT_Ulw0zH1rep-ymDzM0nAG8jemTjGp8NLlXKP5", adapter = discord.RequestsWebhookAdapter()).send(embed=discord.Embed(description=f"Шард с ID {shard_id} успешно запущен",colour=config.COLORS['SUCCESS']))

@client.event
async def on_shard_disconnect(shard_id):
    discord.Webhook.partial(823524888945098812, "Kg4oKTQSzxrq7foJ0-E1NMrTJH69esLbOl1EWSnOzI-7LDTIZhQMSxzhsKwwBjq_kMsS", adapter = discord.RequestsWebhookAdapter()).send(embed=discord.Embed(description=f"Шард с ID {shard_id} отключён",colour=config.COLORS['ERROR']))

if __name__ == '__main__':
    client.run(config.TOKEN)
