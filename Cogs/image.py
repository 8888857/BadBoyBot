import discord
from discord.ext import commands
import config
import os
from io import BytesIO
import aiohttp
import json

class Images(commands.Cog, name = "Изображения"):
    """Всё связанное с изображениями"""
    def __init__(self, client):
        self.client = client
        self.some_random_api = "https://some-random-api.ml"

    @commands.command(
        name = 'пёс',
        aliases = ['собака', 'пес', 'dog'],
        usage = "пёс",
        description = "Показывает случайное изображение собаки"
    )
    async def _dog(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"{self.some_random_api}/img/dog") as r:
                data = await r.text()
                await ctx.send(json.loads(data)['link'].replace('"', ''))

    @commands.command(
        name = 'кот',
        aliases = ['кошка', 'cat'],
        usage = "кот",
        description = "Показывает случайное изображение кота"
    )
    async def _cat(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"{self.some_random_api}/img/cat") as r:
                data = await r.text()
                await ctx.send(json.loads(data)['link'].replace('"', ''))

    @commands.command(
        name = 'птица',
        aliases = ['bird'],
        usage = "птица",
        description = "Показывает случайное изображение птицы"
    )
    async def _bird(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"{self.some_random_api}/img/birb") as r:
                data = await r.text()
                await ctx.send(json.loads(data)['link'].replace('"', ''))

    @commands.command(
        name = 'лиса',
        aliases = ['fox'],
        usage = "лиса",
        description = "Показывает случайное изображение лисы"
    )
    async def _bird(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"{self.some_random_api}/img/fox") as r:
                data = await r.text()
                await ctx.send(json.loads(data)['link'].replace('"', ''))

    @commands.command(
        name = 'панда',
        aliases = ['panda'],
        usage = "панда",
        description = "Показывает случайное изображение панды"
    )
    async def _panda(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"{self.some_random_api}/img/panda") as r:
                data = await r.text()
                await ctx.send(json.loads(data)['link'].replace('"', ''))

    @commands.command(
        name = 'коала',
        aliases = ['coala', 'koala'],
        usage = "коала",
        description = "Показывает случайное изображение коалы"
    )
    async def _koala(self, ctx):
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"{self.some_random_api}/img/koala") as r:
                data = await r.text()
                await ctx.send(json.loads(data)['link'].replace('"', ''))


def setup(client):
    client.add_cog(Images(client))
