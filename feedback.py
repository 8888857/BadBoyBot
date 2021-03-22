import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import config
import re
import typing
import datetime

class FeedBack(commands.Cog):
    """Обратная связь:"""
    def __init__(self, client):
        self.client = client
        
    @commands.command(
        name="идея",
        usage="идея [идея]",
        description="Написать идею",
        aliases=["idea"]
        )
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def _idea(self, ctx, * , idea):
        prefix = config.prefix
        if ctx.message.author.id == config.black_list:
            await ctx.send(embed=discord.Embed(title="ОШИБКА", description=f"**{ctx.message.author}**,\n эта команда для вас заблокирована.", colour=discord.Colour.red()))
            return
        else:
            emb = discord.Embed(title= f"команду {prefix}идея", description= f"**использовал:\n{ctx.author}**\n`(id-{ctx.author.id})`\nтекст:\n```\n{idea}\n```", colour=config.COLORS['BASE'])
            emb.set_footer(text = f"{ctx.guild.name}\nid-{ctx.guild.id}" if ctx.guild is not None else "~~ЛС", icon_url = ctx.guild.icon_url_as(static_format = "jpg") if ctx.guild is not None else ctx.author.avatar_url_as(static_format = "jpg"))
            await self.client.idea_channel.send(embed=emb)
            await ctx.send(embed = discord.Embed(description=f"**{ctx.message.author.mention}**,\n спасибо за ваш вклад в развитие бота", color= ctx.message.author.color))
    
    @commands.command(
        name="баг",
        usage="баг [баг]",
        description="Репорт бага",
        aliases=["bug","багулина"]
        )
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def _bug(self, ctx, * , bug):
        prefix = config.prefix
        if ctx.message.author.id == config.black_list:
            await ctx.send(embed=discord.Embed(title="ОШИБКА", description=f"**{ctx.message.author}**,\n эта команда для вас заблокирована.", colour=discord.Colour.red()))
            return
        else:
            emb = discord.Embed(title= f"команду {prefix}баг", description= f"**использовал:\n{ctx.author}**\n`(id-{ctx.author.id})`\nтекст:\n```\n{bug}\n```", colour=config.COLORS['BASE'])
            emb.set_footer(text = f"{ctx.guild.name}\nid-{ctx.guild.id}" if ctx.guild is not None else "~~ЛС", icon_url = ctx.guild.icon_url_as(static_format = "jpg") if ctx.guild is not None else ctx.author.avatar_url_as(static_format = "jpg"))
            await self.client.bug_channel.send(embed=emb)
            await ctx.send(embed = discord.Embed(description=f"**{ctx.message.author.mention}**,\n спасибо за ваш вклад в развитие бота", color= ctx.message.author.color))
            
def setup(client):
    client.add_cog(FeedBack(client))