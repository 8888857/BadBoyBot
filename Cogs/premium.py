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
        description="проверка статуса премиума у юзера"
        )
    async def _ups(self, ctx, member:discord.Member=None):
        if member != None:
            if member in self.client.owners:
                return await ctx.send(embed=discord.Embed(description=f"премиум статус \n{member.mention}:\n**OWNER PREMIUM**",colour=config.COLORS['BASE']))
            if member.id in self.client.premium_u:
                return await ctx.send(embed=discord.Embed(description=f"премиум статус \n{member.mention}:\n**DEFAULT PREMIUM**",colour=config.COLORS['BASE']))
            else:
                await ctx.send(embed=discord.Embed(description=f"премиум статус \n{member.mention}:\n**NO PREMIUM**",colour=config.COLORS['BASE']))
        else:
            if ctx.author in self.client.owners:
                return await ctx.send(embed=discord.Embed(description=f"{ctx.author.mention},\nваш премиум статус:\n**OWNER PREMIUM**",colour=config.COLORS['BASE']))
            if ctx.author.id in self.client.premium_u:
                return await ctx.send(embed=discord.Embed(description=f"{ctx.author.mention},\nваш премиум статус:\n**DEFAULT PREMIUM**",colour=config.COLORS['BASE']))
            else:
                await ctx.send(embed=discord.Embed(description=f"{ctx.author.mention},\nваш премиум статус:\n**NO PREMIUM**",colour=config.COLORS['BASE']))
    
    @commands.command(
        name="сервер_премиум_статус",
        usage="сервер_премиум_статус",
        description="проверка статуса премиума у сервера",
        aliases=["server_premuim_status","sps","спс"]
        )
    async def _sps(self, ctx, guild_id:int=None):
        if guild_id == None: 
            if ctx.guild.id in self.client.owner_g:
                return await ctx.send(embed=discord.Embed(description=f"Премиум статус сервера \n{ ctx.guild.name}:\n**OWNER GUILD PREMIUM**", colour = config.COLORS['BASE']))
            if ctx.guild.id in self.client.premium_g:
                return await ctx.send(embed=discord.Embed(description=f"Премиум статус сервера \n{ ctx.guild.name}:\n**DEFAULT GUILD PREMIUM**", colour = config.COLORS['BASE']))
            else:
                await ctx.send(embed=discord.Embed(description=f"Премиум статус сервера \n{ ctx.guild.name}:\n**NO GUILD PREMIUM**", colour = config.COLORS['BASE']))
        else:
            if ctx.author in self.client.owners:
                guild = self.client.get_guild(guild_id)
                if guild_id in self.client.owner_g:
                    return await ctx.send(embed=discord.Embed(description=f"Премиум статус сервера \n{guild.name}:\n**OWNER GUILD PREMIUM**", colour = config.COLORS['BASE']))
                if guild_id in self.client.premium_g:
                    return await ctx.send(embed=discord.Embed(description=f"Премиум статус сервера \n{guild.name}:\n**DEFAULT GUILD PREMIUM**", colour = config.COLORS['BASE']))
                else:
                    await ctx.send(embed=discord.Embed(description=f"Премиум статус сервера \n{guild.name}:\n**NO GUILD PREMIUM**", colour = config.COLORS['BASE']))
            else:
                ctx.send(embed=discord.Embed(title="ошибка",description="смотреть премиум статус определенного сервера может только овнер бота.", colour=config.COLORS['ERROR']))


def setup(client):
    client.add_cog(premium(client))
