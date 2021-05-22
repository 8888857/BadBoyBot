import discord
from discord.ext import commands
import config
import asyncio
import json
import ast
import requests
import os
import typing
import subprocess
import datetime
import random
from config import timeformMSK
from config import deltaMSK

class owner(commands.Cog, name="Овнер"):
    """команды только для овнеров бота:"""
    
    def __init__(self, client):
        self.client = client
        
    def insert_returns(self, body):
        # insert return stmt if the last expression is a expression statement
        if isinstance(body[-1], ast.Expr):
            body[-1] = ast.Return(body[-1].value)
            ast.fix_missing_locations(body[-1])

        # for if statements, we insert returns into the body and the orelse
        if isinstance(body[-1], ast.If):
            self.insert_returns(body[-1].body)
            self.insert_returns(body[-1].orelse)

        # for with blocks, again we insert returns into the body
        if isinstance(body[-1], ast.With):
            self.insert_returns(body[-1].body)

    
    @commands.command(
        name="евал",
        aliases = ['eval'],
        usage="евал [код]",
        brief="исполнение кусков кода",
        description="• АЛОООО ты и сам знать должен😎👌"
        )
    @commands.is_owner()
    async def eval_fn(self, ctx, *, cmd):
        """Evaluates input.
        Input is interpreted as newline seperated statements.
        If the last statement is an expression, that is the return value.
        Usable globals:
        - `bot`: the bot instance
        - `discord`: the discord module
        - `commands`: the discord.ext.commands module
        - `ctx`: the invokation context
        - `__import__`: the builtin `__import__` function
        Such that `>eval 1 + 1` gives `2` as the result.
        The following invokation will cause the bot to send the text '9'
        to the channel of invokation and return '3' as the result of evaluating
        >eval ```
        a = 1 + 2
        b = a * 2
        await ctx.send(a + b)
        a
        ```
        """
        fn_name = "_eval_expr"

        cmd = cmd.strip("` ")

        # add a layer of indentation
        cmd = "\n".join(f"    {i}" for i in cmd.splitlines())

        # wrap in async def body
        body = f"async def {fn_name}():\n{cmd}"

        parsed = ast.parse(body)
        body = parsed.body[0].body

        self.insert_returns(body)

        env = {
            'client': ctx.bot,
            'bot': ctx.bot,
            'discord': discord,
            'commands': commands,
            'ctx': ctx,
            '__import__': __import__,
            'os': os,
            'random': random
        }
        exec(compile(parsed, filename="<ast>", mode="exec"), env)

        result = (await eval(f"{fn_name}()", env))
        await ctx.message.add_reaction(self.client.EMOJIS['SUCCESS'])

    @commands.command(
        name = "ливай",
        aliases = ['leave'],
        usage="ливай (сервер)",
        brief = "бот ливнет с сервера",
        description="• АЛОООО ты и сам знать должен😎👌"
        )
    @commands.is_owner()
    async def _leave(self, ctx, guild_id:int=None):
        if guild_id == None:
            guild = ctx.guild
        else:
            guild = self.client.get_guild(guild_id)
        await guild.leave()
        await ctx.reply(embed = discord.Embed(description = f"я успешно ливнул с сервер:\n{guild.name}",colour= self.client.COLORS['SUCCESS']))
        await ctx.message.add_reaction(self.client.EMOJIS['SUCCESS'])
    
    @commands.command(
        name="рестарт",
        usage="рестарт",
        brief="перезагружает бота",
        aliases=["reload","restart"],
        description="• АЛОООО ты и сам знать должен😎👌"
        )
    @commands.is_owner()
    async def _restart(self, ctx, id=None):
        if id == None:
            id = "BadBoyBot"
        await ctx.message.add_reaction(self.client.EMOJIS['SUCCESS'])
        os.system(f"pm2 restart {id}")
        
    @commands.command(
        name="ког",
        usage="ког [name/all] [r/l/u]",
        brief="работа с когами",
        aliases=["cog","коги"],
        description="• АЛОООО ты и сам знать должен😎👌"
        )
    @commands.is_owner()
    async def _cog(self, ctx, name, act):
        if name in ['all','все']:
            i = 'и '
            i2 = "ы"
            active = "все"
        else:
            i = ' '
            i2 = ''
            active = "один"
        if act in ['перезагрузить','перезагрузка','релоад','reload','r','р']:
                act2 = "перезагружен"
                act3 = self.client.reload_extension
                emb_color = self.client.COLORS['BASE']
        if act in ['вкл','включить','загрузить','загрузка','load','лоад','l','л']:
                act2 = "загружен"
                act3 = self.client.load_extension
                emb_color = self.client.COLORS['SUCCESS']
        if act in ['выкл','выключить','отгрузка','анлоад','unload','u','а']:
                act2 = "отгружен"
                act3 = self.client.unload_extension
                emb_color = self.client.COLORS['ERROR']
        if active == "все":
            for cog in os.listdir('./Cogs'):
                if cog not in config.COGS_IGNORE:
                    if cog.endswith('.py'):
                        act3(f'Cogs.{cog.replace(".py", "")}')
        if active == "один":
            act3(f'Cogs.{name}')
        print(f'-----------------------------------\nког{i}{name} - {act2}{i2}\n-----------------------------------')
        await self.client.CHANNELS['on_off'].send(embed=discord.Embed(title=f"{act2}{i2}",description=f"ког{i} {name} успешно {act2}{i2}",colour=emb_color))
        await ctx.send(embed=discord.Embed(title=f"{act2}{i2}",description=f"ког{i} {name} успешно {act2}{i2}",colour=emb_color))
        await ctx.message.add_reaction(self.client.EMOJIS['SUCCESS'])
        
    @commands.command(
        name="гинв",
        usage="гинв (guild_id)",
        brief="генерирует ссылку на сервер",
        aliases=["ginv","guild-invite"],
        description="• АЛОООО ты и сам знать должен😎👌"
        )
    @commands.is_owner()
    async def _ginv(self, ctx, guild_id:int=None):
        if guild_id == None:
            channel=ctx.channel
        else:
            guild = self.client.get_guild(guild_id)
            channel = random.choice(guild.text_channels)
        invitelink = await channel.create_invite()
        await ctx.reply(invitelink)
        await ctx.message.add_reaction(self.client.EMOJIS['SUCCESS'])
        
    @commands.command(
        name="пуш",
        usage="пуш (бот/ког) (айди/имя)",
        brief="загружает обнову с гитхаба",
        aliases=["push"],
        description="• АЛОООО ты и сам знать должен😎👌"
        )
    @commands.is_owner()
    async def _push(self, ctx, targ=None, pm2_id_or_cog_name=None):
        os.chdir("/root/badboybot")
        os.system("git pull")
        emb = discord.Embed(description="файлы с гитхаба успешно добавлены",colour=self.client.COLORS['BASE'])
        if targ in ["cog","ког","к","c"]:
            if pm2_id_or_cog_name in ["все","all"]:
                i = "и "
                i2 = "ы"
                for cog in os.listdir('./Cogs'):
                    if cog not in config.COGS_IGNORE:
                        if cog.endswith('.py'):
                            self.client.reload_extension(f'Cogs.{cog.replace(".py", "")}')
            else:
                i = " "
                i2 = ""
                self.client.reload_extension(f'Cogs.{pm2_id_or_cog_name}')
            print(f'-----------------------------------\nког{i}{name} - перезагружен{i2}\n-----------------------------------')
            await self.client.CHANNELS['on_off'].send(embed=discord.Embed(title=f"перезагружен{i2}",description=f"ког{i} {pm2_id_or_cog_name} успешно перезагружен{i2}",colour=self.client.COLORS['BASE']))
            emb.add_field(name=f"перезагружен{i2}",value=f"ког{i} {pm2_id_or_cog_name} успешно перезагружен{i2}")
        if targ in ["bot","бот","б","b"]:
            if pm2_id_or_cog_name == None:
                pm2_id_or_cog_name = "BadBoyBot"
            emb.add_field(name="перезагружен",value="весь бот")
            os.system(f"pm2 reload {pm2_id_or_cog_name}")
        await ctx.reply(embed=emb)
        await ctx.message.add_reaction(self.client.EMOJIS['SUCCESS'])
            
def setup(client):
    client.add_cog(owner(client))
