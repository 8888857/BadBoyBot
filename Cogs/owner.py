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
from config import timeformMSK
from config import deltaMSK

class owner(commands.Cog):
    
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
        description="исполнение кусков кода"
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
#            'DB': DB,
            'os': os,
        }
        exec(compile(parsed, filename="<ast>", mode="exec"), env)

        result = (await eval(f"{fn_name}()", env))
        await ctx.message.add_reaction("✅")

    @commands.command(
        name = "ливай",
        aliases = ['leave'],
        usage="ливай (сервер)",
        description = "бот ливнет с сервера"
        )
    @commands.is_owner()
    async def _leave(self, ctx):
        await ctx.guild.leave()
        await ctx.send(embed = discord.Embed(description = "я ливнул",colour= config.COLORS['SUCCESS']))
    
    @commands.command(
        name="рестарт",
        usage="рестарт",
        description="перезагружает бота",
        aliases=["reload","restart"]
        )
    @commands.is_owner()
    async def _restart(self, ctx):
        await ctx.message.add_reaction("✅")
        os.system("pm2 restart 2")
        
    @commands.command(
        name="ког",
        usage="ког [name/all] [r/l/u]",
        description="работа с когами",
        aliases=["cog","коги"]
        )
    @commands.is_owner()
    async def _cog(self, ctx, name, act):
        if act in ['перезагрузить','перезагрузка','релоад','reload','r','р']:
            if name in ['all','все']:
                for cog in os.listdir('./Cogs'):
                    if cog not in config.COGS_IGNORE:
                        if cog.endswith('.py'):
                            self.client.reload_extension(f'Cogs.{cog.replace(".py", "")}')
                await ctx.message.add_reaction('✅')
            else:
                self.client.reload_extension(f"Cogs.{name}")
                await ctx.message.add_reaction('✅')
            print("-----------------------------------")
            print(f'ког имя="{name}" - перезагружен')
            print("-----------------------------------")
            
        if act in ['вкл','включить','загрузить','загрузка','load','лоад','l','л']:
            if name in ['all','все']:
                for cog in os.listdir('./Cogs'):
                    if cog not in config.COGS_IGNORE:
                        if cog.endswith('.py'):
                            self.client.load_extension(f'Cogs.{cog.replace(".py", "")}')
                await ctx.message.add_reaction('✅')
            else:
                self.client.load_extension(f"Cogs.{name}")
                await ctx.message.add_reaction('✅')
            print("-----------------------------------")
            print(f'ког имя="{name}" - загружен')
            print("-----------------------------------")
        if act in ['выкл','выключить','отгрузка','анлоад','unload','u','а']:
            if name in ['all','все']:
                for cog in os.listdir('./Cogs'):
                    if cog not in config.COGS_IGNORE:
                        if cog.endswith('.py'):
                            self.client.unload_extension(f'Cogs.{cog.replace(".py", "")}')
                await ctx.message.add_reaction('✅')
            else:
                self.client.unload_extension(f"Cogs.{name}")
                await ctx.message.add_reaction('✅')
            print("-----------------------------------")
            print(f'ког имя="{name}" - отгружен')
            print("-----------------------------------")
        
        
    @commands.command(
        name="гинв",
        usage="гинв [guild_id]",
        description="генерирует ссылку на сервер",
        aliases=["ginv","guild-invite"]
        )
    @commands.is_owner()
    async def _ginv(self, ctx, guild_id:int):
        guild = self.client.get_guild(guild_id)
        channel = guild.channels[0]
        invitelink = await channel.create_invite()
        await ctx.send(invitelink)
            
def setup(client):
    client.add_cog(owner(client))