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

class premium(commands.Cog, name="Премиум"):
    """Премиум комманды:"""

    def __init__(self, client):
        self.client = client
        
    @commands.command(
        name="юзер_премиум_статус",
        usage="юзер_премиум_статус (юзер)",
        aliases=["user_premium_status","ups","юпс"],
        brief="проверка статуса премиума у юзера",
        description="• юзер_премиум_статус\n• юзер_премиум_статус @BadBoyBot#2997"
        )
    async def _ups(self, ctx, member:discord.Member=None):
        if member != None:
            if member in self.client.owners:
                await ctx.message.add_reaction(self.client.EMOJIS['SUCCESS'])
                return await ctx.reply(embed=discord.Embed(description=f"премиум статус \n{member.mention}:\n**OWNER PREMIUM**",colour=self.client.COLORS['BASE']))
            if member.id in self.client.premium_u:
                await ctx.message.add_reaction(self.client.EMOJIS['SUCCESS'])
                return await ctx.reply(embed=discord.Embed(description=f"премиум статус \n{member.mention};\n**DEFAULT PREMIUM**",colour=self.client.COLORS['BASE']))
            else:
                await ctx.reply(embed=discord.Embed(description=f"премиум статус \n{member.mention}:\n**NO PREMIUM**",colour=self.client.COLORS['BASE']))
                await ctx.message.add_reaction(self.client.EMOJIS['SUCCESS'])
        else:
            if ctx.author in self.client.owners:
                await ctx.message.add_reaction(self.client.EMOJIS['SUCCESS'])
                return await ctx.reply(embed=discord.Embed(description=f"{ctx.author.mention},\nваш премиум статус:\n**OWNER PREMIUM**",colour=self.client.COLORS['BASE']))
            if ctx.author.id in self.client.premium_u:
                await ctx.message.add_reaction(self.client.EMOJIS['SUCCESS'])
                return await ctx.reply(embed=discord.Embed(description=f"{ctx.author.mention},\nваш премиум статус:\n**DEFAULT PREMIUM**",colour=self.client.COLORS['BASE']))
            else:
                await ctx.reply(embed=discord.Embed(description=f"{ctx.author.mention},\nваш премиум статус:\n**NO PREMIUM**",colour=self.client.COLORS['BASE']))
                await ctx.message.add_reaction(self.client.EMOJIS['SUCCESS'])
    
    @commands.command(
        name="гуилд_премиум_статус",
        usage="guild_премиум_статус",
        brief="проверка статуса премиума у сервера",
        aliases=["server_premuim_status","gps","гпс"],
        description="• гуилд_премиум_статус"
        )
    async def _sps(self, ctx, guild_id:int=None):
        if guild_id == None: 
            if ctx.guild.id in self.client.owner_g:
                await ctx.message.add_reaction(self.client.EMOJIS['SUCCESS'])
                return await ctx.reply(embed=discord.Embed(description=f"Премиум статус сервера \n{ ctx.guild.name}:\n**OWNER GUILD PREMIUM**", colour = self.client.COLORS['BASE']))
            if ctx.guild.id in self.client.premium_g:
                await ctx.message.add_reaction(self.client.EMOJIS['SUCCESS'])
                return await ctx.reply(embed=discord.Embed(description=f"Премиум статус сервера \n{ ctx.guild.name}:\n**DEFAULT GUILD PREMIUM**", colour = self.client.COLORS['BASE']))
            else:
                await ctx.message.add_reaction(self.client.EMOJIS['SUCCESS'])
                await ctx.reply(embed=discord.Embed(description=f"Премиум статус сервера \n{ ctx.guild.name}:\n**NO GUILD PREMIUM**", colour = self.client.COLORS['BASE']))
        else:
            if ctx.author in self.client.owners:
                guild = self.client.get_guild(guild_id)
                if guild_id in self.client.owner_g:
                    await ctx.message.add_reaction(self.client.EMOJIS['SUCCESS'])
                    return await ctx.reply(embed=discord.Embed(description=f"Премиум статус сервера \n{guild.name}:\n**OWNER GUILD PREMIUM**", colour = self.client.COLORS['BASE']))
                if guild.id in self.client.premium_g:
                    await ctx.message.add_reaction(self.client.EMOJIS['SUCCESS'])
                    return await ctx.reply(embed=discord.Embed(description=f"Премиум статус сервера \n{guild.name}:\n**DEFAULT GUILD PREMIUM**", colour = self.client.COLORS['BASE']))
                else:
                    await ctx.message.add_reaction(self.client.EMOJIS['SUCCESS'])
                    await ctx.reply(embed=discord.Embed(description=f"Премиум статус сервера \n{guild.name}:\n**NO GUILD PREMIUM**", colour = self.client.COLORS['BASE']))
            else:
                await ctx.reply(embed=discord.Embed(title="ошибка",description="смотреть премиум статус определенного сервера может только овнер бота.", colour=self.client.COLORS['ERROR']))
                await ctx.message.add_reaction(self.client.EMOJIS['ERROR'])


def setup(client):
    client.add_cog(premium(client))
