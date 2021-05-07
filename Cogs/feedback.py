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
        brief="Написать идею",
        aliases=["idea"],
        description="• идея сделать кулдаун на команду идея меньше"
        )
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def _idea(self, ctx, * , idea):
        prefix = config.prefix
        if ctx.author.id in self.client.black_list:
            return await ctx.reply(embed=discord.Embed(description=f"**{ctx.author.mention}**,\n эта команда для вас заблокирована.", colour=config.COLORS['ERROR']))
        else:
            emb = discord.Embed(title= f"команду {prefix}идея", description= f"**использовал:\n{ctx.author}**\n`(id-{ctx.author.id})`\nтекст:\n```\n{idea}\n```", colour=config.COLORS['BASE'])
            emb.set_footer(text = f"{ctx.guild.name}\nid-{ctx.guild.id}" if ctx.guild is not None else "~~ЛС", icon_url = ctx.guild.icon_url_as(static_format = "jpg") if ctx.guild is not None else ctx.author.avatar_url_as(static_format = "jpg"))
            msg = await self.client.CHANNELS["idea"].send(embed=emb)
            await msg.add_reaction('✅')
            await msg.add_reaction('⚪')
            await msg.add_reaction('❌')
            await ctx.reply(embed = discord.Embed(description=f"**{ctx.message.author.mention}**,\n спасибо за ваш вклад в развитие бота", colour=config.COLORS['BASE']))
            await ctx.message.add_reaction(client.EMOJIS['SUCCESS'])
    
    @commands.command(
        name="баг",
        usage="баг [баг]",
        brief="Репорт бага",
        aliases=["bug","багулина"],
        description="• баг можно пинговать через say"
        )
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def _bug(self, ctx, * , bug):
        prefix = config.prefix
        if ctx.author.id in self.client.black_list:
            return await ctx.reply(embed=discord.Embed(description=f"**{ctx.author.mention}**,\n эта команда для вас заблокирована.", colour=config.COLORS['ERROR']))
        else:
            emb = discord.Embed(title= f"команду {prefix}баг", description= f"**использовал:\n{ctx.author}**\n`(id-{ctx.author.id})`\nтекст:\n```\n{bug}\n```", colour=config.COLORS['BASE'])
            emb.set_footer(text = f"{ctx.guild.name}\nid-{ctx.guild.id}" if ctx.guild is not None else "~~ЛС", icon_url = ctx.guild.icon_url_as(static_format = "jpg") if ctx.guild is not None else ctx.author.avatar_url_as(static_format = "jpg"))
            msg = await self.client.CHANNELS['bug'].send(embed=emb)
            await msg.add_reaction('✅')
            await msg.add_reaction('⚪')
            await msg.add_reaction('❌')
            await ctx.reply(embed = discord.Embed(description=f"**{ctx.message.author.mention}**,\n спасибо за ваш вклад в развитие бота", colour=config.COLORS['BASE']))
            await ctx.message.add_reaction(client.EMOJIS['SUCCESS'])
            
    @commands.command(
        name="отзыв",
        usage="отзыв [отзыв]",
        brief="отзыв о боте",
        aliases=["review"],
        description="• отзыв хороший бот 100500/10"
        )
    @commands.cooldown(1, 120, commands.BucketType.user)
    async def _rewiew(self, ctx, * , review):
        prefix = config.prefix
        if ctx.author.id in self.client.black_list:
            return await ctx.reply(embed=discord.Embed(description=f"**{ctx.author.mention}**,\n эта команда для вас заблокирована.", colour=config.COLORS['ERROR']))
        else:
            emb = discord.Embed(title= f"команду {prefix}отзыв", description= f"**использовал:\n{ctx.author}**\n`(id-{ctx.author.id})`\nтекст:\n```\n{review}\n```", colour=config.COLORS['BASE'])
            emb.set_footer(text = f"{ctx.guild.name}\nid-{ctx.guild.id}" if ctx.guild is not None else "~~ЛС", icon_url = ctx.guild.icon_url_as(static_format = "jpg") if ctx.guild is not None else ctx.author.avatar_url_as(static_format = "jpg"))
            msg = await self.client.CHANNELS['review'].send(embed=emb)
            await msg.add_reaction('✅')
            await msg.add_reaction('⚪')
            await msg.add_reaction('❌')
            await ctx.reply(embed = discord.Embed(description=f"**{ctx.message.author.mention}**,\n спасибо за ваш вклад в развитие бота", colour=config.COLORS['BASE']))
            await ctx.message.add_reaction(client.EMOJIS['SUCCESS'])
    
def setup(client):
    client.add_cog(FeedBack(client))
