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
import urllib

class utils(commands.Cog, name="Утилиты"):
    """утилит комманды:"""

    def __init__(self, client):
        self.client = client
        
    @commands.command(
        name="сказать",
        usage="сказать (1/2) [текст]",
        description="Писать от имени бота\n`( 1-просто сообщение, 2-сообщение в рамочке(ембед))`",
        aliases=["say","озв"]
        )
    @has_permissions(administrator = True)
    async def _say(self, ctx, typemsg, *, text=None):
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

    @commands.command(
        name="давление",
        usage="давление [систолическое] [диастолическое] [пульс] (время)",
        description="выводит показания вашего давления",
        aliases=["давл","pressure"]
        )
    @has_permissions(administrator=True)
    async def _pressure(self, ctx, systo:int, diast:int, puls:int, * , time=None):
        
        min_systo = 110
        max_systo = 130
        
        min_diast = 70
        max_diast = 90
        
        min_puls = 80
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
        emb.add_field(name="Время",value=time)
        await ctx.send(embed=emb)
        
    @commands.command(
        name="калькулятор",
        aliases=['посчитать', 'калк', 'calculator', 'calc', 'math'],
        usage="калькулятор <выражение>",
        description="Простейший математический калькулятор прямо в дискорде"
    )
    async def _calculator(self, ctx, *, expression = None):
        mathjs = "http://api.mathjs.org/v4"
        if not expression:
            return await ctx.send(embed = discord.Embed(description = "Укажите выражение, которое необходимо вычислить", colour = config.COLORS['ERROR']))
        async with aiohttp.ClientSession() as cs:
            async with cs.get(f"{mathjs}?expr={expression.replace(' ', '').replace('+', '%2B').replace('/', '%2F2')}") as r:
                r = await r.read()
                r = r.decode('utf-8')
                if 'Error: Undefined symbol' in r:
                    return await ctx.send(embed = discord.Embed(description = "Неопознанный символ", colour = config.COLORS['ERROR']))
                elif 'Error' in r:
                    return await ctx.send(embed = discord.Embed(description = "Произошла непредвиденная ошибка. Повторите попытку позже.", colour = config.COLORS['ERROR']))
                await ctx.send(f"Результат: {r}", allowed_mentions = discord.AllowedMentions(everyone = False, roles = False, users = False))
    
def setup(client):
    client.add_cog(utils(client))