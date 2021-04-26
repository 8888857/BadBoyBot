import discord
from discord import utils
from discord.utils import get
from discord.ext import commands
from discord.ext.commands import has_permissions
import datetime
import config
from config import timeformMSK
from config import deltaMSK
import aiohttp
import os
import re
import asyncio
from asyncio import sleep
import ast
import typing
import json
import requests
from bs4 import BeautifulSoup
import requests
import random
import urllib
import pyowm
from pyowm.utils.config import get_default_config

class utils(commands.Cog, name="Утилиты"):
    """утилит комманды:"""

    def __init__(self, client):
        self.client = client
        
    @commands.command(
        name="сказать",
        usage="сказать (1/2) [текст]",
        brief="Писать от имени бота\n`( 1-просто сообщение, 2-сообщение в рамочке(ембед))`",
        aliases=["say","озв"],
        description="• сказать я бот\n• сказать 1 я бот\n• сказать 2 я бот"
        )
    async def _say(self, ctx, typemsg, *, text=None):
        if (ctx.author in self.client.owners
        or ctx.author.guild_permissions.administrator):
            await ctx.message.delete()
            if text == None:
                return await ctx.send(f"{typemsg}")
            if typemsg in ["1","2","emb","емб"]:
                if typemsg == "1":
                    await ctx.send(text)
                else:
                    await ctx.send(embed=discord.Embed(description=text, colour=ctx.author.color))
            else:
                await ctx.send(f"{typemsg} {text}")
        else:
            raise discord.ext.commands.errors.CheckFailure

    @commands.command(
        name="давление",
        usage="давление [систолическое] [диастолическое] [пульс] (delete/удалить) (время)",
        brief="выводит показания вашего давления",
        aliases=["давл","pressure"],
        description="• давление 120 80 90\n• давление 120 80 90 delete\n• давление 120 80 90 delete 12:40\n• давление 120 80 90 12:40"
        )
    async def _pressure(self, ctx, systo:int, diast:int, puls:int, delete=None, * , time=None):
        if delete != None:
            if delete in ["d","delete","удалить","у","-"]:
                await ctx.message.delete()
            else:
                time=delete
        
        min_systo = 110
        max_systo = 130
        
        min_diast = 70
        max_diast = 90
        
        min_puls = 70
        max_puls = 100
        
        colors = {
            'min':0x8BD1FF,
            'norm':0x80FF00,
            'max':0xFF0700
        }
        
        if time == None:
            time = datetime.datetime.now().strftime(timeformMSK)
        
        if (systo < min_systo
        or diast < min_diast
        or puls < min_puls):
            emb=discord.Embed(colour=colors['min'])
        if (systo > max_systo
        or diast > max_diast
        or puls > max_puls):
            emb=discord.Embed(colour=colors['max'])
        if min_systo <= systo <= max_systo:
            if min_diast <= diast <= max_diast:
                if min_puls <= puls <= max_puls:
                    emb=discord.Embed(colour=colors['norm'])
            
        emb.add_field(name="Давление",value=f"систолическое: **{systo}**\nдиастолическое: **{diast}**\nпульс: **{puls}**")
        emb.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
        emb.add_field(name="Время",value=time)
        await ctx.send(embed=emb)
        
    @commands.command(
        name="калькулятор",
        aliases=['посчитать', 'калк', 'calculator', 'calc', 'math'],
        usage="калькулятор <выражение>",
        brief="Простейший математический калькулятор прямо в дискорде",
        description="• калькулятор 1+1"
    )
    async def _calculator(self, ctx, *, expression = None):
        mathjs = "http://api.mathjs.org/v4"
        if not expression:
            return await ctx.reply(embed = discord.Embed(description = "Укажите выражение, которое необходимо вычислить", colour = config.COLORS['ERROR']))
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"{mathjs}?expr={expression.replace(' ', '').replace('+', '%2B').replace('/', '%2F2')}") as r:
                r = await r.read()
                r = r.decode('utf-8')
                if 'Error: Undefined symbol' in r:
                    return await ctx.reply(embed = discord.Embed(description = "Неопознанный символ", colour = config.COLORS['ERROR']))
                elif 'Error' in r:
                    return await ctx.reply(embed = discord.Embed(description = "Произошла непредвиденная ошибка. Повторите попытку позже.", colour = config.COLORS['ERROR']))
                await ctx.reply(f"Результат: {r}", allowed_mentions = discord.AllowedMentions(everyone = False, roles = False, users = False))

    @commands.command(
        name="голосование",
        usage="голосование [кол-во реакций] [тема]",
        brief="создает голосование",
        aliases=["vote"],
        description="• голосование 2 я крутой?\n1- да\n2- нет"
        )
    async def _vote(self, ctx, quantity:int, * ,topic):
        if (quantity <= 0
        or 10 < quantity):
            return await ctx.send(embed=discord.Embed(title="ошибка",description="кол-во реакций не должно быть меньше 1 и больше 10",colour=config.COLORS['ERROR']))
        await ctx.message.delete()
        emb = discord.Embed(description=topic,colour=ctx.author.color)
        emb.set_author(name=ctx.author.name,icon_url=ctx.author.avatar_url)
        vote = await ctx.send(embed=emb)
        if quantity >= 1:
            await vote.add_reaction("1️⃣")
        if quantity >= 2:
            await vote.add_reaction("2️⃣")
        if quantity >= 3:
            await vote.add_reaction("3️⃣")
        if quantity >= 4:
            await vote.add_reaction("4️⃣")
        if quantity >= 5:
            await vote.add_reaction("5️⃣")
        if quantity >= 6:
            await vote.add_reaction("6️⃣")
        if quantity >= 7:
            await vote.add_reaction("7️⃣")
        if quantity >= 8:
            await vote.add_reaction("8️⃣")
        if quantity >= 9:
            await vote.add_reaction("9️⃣")
        if quantity == 10:
            await vote.add_reaction("🔟")
        await ctx.author.send(f"{ctx.author.mention},\nвы создали голосование\nНа сервере:\n```\n{ctx.guild.name}\n```\nЕго текст:\n```\n{topic}\n```")

    @commands.command(
        name="погода",
        usage="погода [город]",
        brief="узнать погоду в определенном городе",
        aliases=["weather"],
        description="• погода Москва"
        )
    async def _weather(self, ctx, * ,city):
        config_dict = get_default_config()
        config_dict['language'] = 'ru'
        owm = pyowm.OWM('290ad7a9c0c0a979294080fa2dbf5bd4', config_dict)
        mgr = owm.weather_manager()
        observation = mgr.weather_at_place(city)
        w = observation.weather
        temp = w.temperature('celsius')['temp']
        tempfeellike = w.temperature('celsius')['feels_like']
        icon = w.weather_icon_url(size='2x')
        wind = w.wind()['speed']
        emb=discord.Embed(title=f"в городе __**{city}**__",colour=config.COLORS['BASE'])
        emb.add_field(name="Температура:",value=f"{temp}°C")
        if tempfeellike != temp:
            emb.add_field(name="Температура ощущается как:",value=f"{tempfeellike}°C")
        emb.add_field(name="Скорость ветра:",value=f"{wind}м/с")
        emb.add_field(name="Погода:",value=f"{w.detailed_status}")
        emb.set_thumbnail(url=icon)
        
        await ctx.reply(embed=emb)

    @commands.command(
        name="рандом",
        usage="рандом (от) (до)",
        brief="генератор рандомных чисел",
        aliases=["random"],
        description="• рандом\n• рандом 20\n• рандом 20 40"
        )
    async def _random(self, ctx, start:int=None, finish:int=None):
        if start == None:
            rnumber = random.randint(-99999999, 999999999999999999999999999999999999)
        else:
            if finish == None:
                rnumber = random.randint(start, 999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999999)
            else:
                if start >= finish:
                    rnumber = random.randint(finish, start)
                else:
                    rnumber = random.randint(start, finish)
        await ctx.reply(embed=discord.Embed(title="выпало число:", description=f"**{rnumber}**",colour=discord.Colour.random()))

def setup(client):
    client.add_cog(utils(client))
