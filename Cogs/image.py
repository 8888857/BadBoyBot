import discord
from discord.ext import commands
import config
import os
from io import BytesIO
import aiohttp
import json

class Images(commands.Cog, name = "Изображения"):
    """команды с картинками:"""
    def __init__(self, client):
        self.client = client
        self.some_random_api = "https://some-random-api.ml"

    @commands.command(
        name = 'пёс',
        aliases = ['собака', 'пес', 'dog'],
        usage = "пёс",
        brief = "Показывает случайное изображение собаки",
        description="• пёс"
    )
    async def _dog(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"{self.some_random_api}/img/dog") as r:
                data = await r.text()
                await ctx.reply(json.loads(data)['link'].replace('"', ''))

    @commands.command(
        name = 'кот',
        aliases = ['кошка', 'cat'],
        usage = "кот",
        brief = "Показывает случайное изображение кота",
        description = "• кот"
    )
    async def _cat(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"{self.some_random_api}/img/cat") as r:
                data = await r.text()
                await ctx.reply(json.loads(data)['link'].replace('"', ''))

    @commands.command(
        name = 'птица',
        aliases = ['bird'],
        usage = "птица",
        brief = "Показывает случайное изображение птицы",
        description="• птица"
    )
    async def _bird(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"{self.some_random_api}/img/birb") as r:
                data = await r.text()
                await ctx.reply(json.loads(data)['link'].replace('"', ''))

    @commands.command(
        name = 'лиса',
        aliases = ['fox'],
        usage = "лиса",
        brief = "Показывает случайное изображение лисы",
        description="• лиса"
    )
    async def _bird(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"{self.some_random_api}/img/fox") as r:
                data = await r.text()
                await ctx.reply(json.loads(data)['link'].replace('"', ''))

    @commands.command(
        name = 'панда',
        aliases = ['panda'],
        usage = "панда",
        brief = "Показывает случайное изображение панды",
        description="• панда"
    )
    async def _panda(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"{self.some_random_api}/img/panda") as r:
                data = await r.text()
                await ctx.reply(json.loads(data)['link'].replace('"', ''))

    @commands.command(
        name = 'коала',
        aliases = ['coala', 'koala'],
        usage = "коала",
        brief = "Показывает случайное изображение коалы",
        description="• коала"
    )
    async def _koala(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"{self.some_random_api}/img/koala") as r:
                data = await r.text()
                await ctx.reply(json.loads(data)['link'].replace('"', ''))


def setup(client):
    client.add_cog(Images(client))
