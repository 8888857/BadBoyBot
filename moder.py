import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import config
import re
import typing
import datetime

class moder(commands.Cog, name = "Модерация"):
    """Модерационные комманды:"""
    def __init__(self, client):
        self.client = client

    @commands.command(
        name = "очистить",
        description = "Очистка чата",
        aliases = ['clear','чистка'],
        usage = "очистить [количество сообщений] (канал)"
    )
    @commands.guild_only()
    @has_permissions(manage_messages = True)
    async def _clear(self, ctx, amount: int, channel: discord.TextChannel = None):
        print(channel)
        if channel is None: channel = ctx.channel

        if channel.permissions_for(ctx.author).manage_messages:
            if amount > 100500:
                return await ctx.send(embed = discord.Embed(title = "Ошибка очистки чата", description = "Нельзя очистить больше 100500 сообщений за раз", colour = config.COLORS['ERROR']))
            if amount <= 0:
                return await ctx.send(embed = discord.Embed(title = "Ошибка очистки чата", description = "Очищать чат на неположительное количество сообщений? Плохая идея...", colour = config.COLORS['ERROR']))
            cleared = await channel.purge(limit = (amount + 1) if channel == ctx.channel else amount)
            await ctx.send(embed = discord.Embed(title = f"Чат успешно очищен на {len(cleared) - 1} сообщений модератором {ctx.author}", colour = config.COLORS['SUCCESS']), delete_after = 30)
        else:
            raise discord.ext.commands.errors.CheckFailure
    
    @commands.command(
        name="сказать",
        usage="сказать (1/2) [текст]",
        description="Писать от имени бота\n`( 1-просто сообщение, 2-сообщение в рамочке(ембед))`",
        aliases=["say","озв"]
        )
    @has_permissions(administrator=True)
    async def _say(self, ctx, typemsg, *, text):
        await ctx.message.delete()
        if typemsg == "1":
            await ctx.send(text)
        if typemsg == "2":
            await ctx.send(embed=discord.Embed(description=text, colour=ctx.author.color))
        if typemsg != "1":
            if typemsg != "2":
                await ctx.send(text)

def setup(client):
    client.add_cog(moder(client))