import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import config
import re
import typing
import datetime
from config import timeformMSK
from config import deltaMSK

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
            if ctx.author in self.client.owners:
                if amount > 9999999999999999999:
                    return await ctx.send(embed = discord.Embed(title = "Ошибка очистки чата", description = "ты даун что ли? куда тебе столько", colour = config.COLORS['ERROR']))
            if ctx.author.id in self.client.premium_u:
                if amount > 5000:
                    return await ctx.send(embed = discord.Embed(title = "Ошибка очистки чата", description = "имея **DEFAULT PREMIUM**\nНельзя очистить больше 5000 сообщений за раз", colour = config.COLORS['ERROR']))
            else:
                if amount > 500:
                    return await ctx.send(embed = discord.Embed(title = "Ошибка очистки чата", description = "не имея premium\nНельзя очистить больше 500 сообщений за раз", colour = config.COLORS['ERROR']))
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
    async def _pressure(self, ctx, systo:int, diast:int, puls:int, time=None):
        
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

def setup(client):
    client.add_cog(moder(client))
