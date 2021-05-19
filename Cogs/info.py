import discord
from discord import utils
from discord.utils import get
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord_slash import cog_ext, SlashContext
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
import random

class info(commands.Cog, name="Информация"):
    """Инфо комманды:"""
    def __init__(self, client):
        self.client = client
    
    @commands.command(
        name="хелп",
        aliases=["help","помощь"],
        usage="хелп (команда)",
        brief="Помощь по командам",
        description=f"• хелп\n• хелп юзеринфо"
    )
    async def _help(self, ctx: commands.Context, input_name = None):
        prefix = config.prefix
        if ctx.author.id in [owner.id for owner in self.client.owners]:
            if input_name in ["no_owner","noowner","noown","no","не_овнер","неовнер","неовн","но"]:
                bcklist = ["events", "Овнер"]
            else:
                bcklist = ["events"]
        elif ctx.author.id not in [owner.id for owner in self.client.owners]:
            bcklist = ["events", "Овнер"]
        if input_name is None:
            embed = discord.Embed(
                description=f"Мой префикс - `{prefix}`\nПомощь по коммандам - `{prefix}хелп [команда]`\nсервер поддержки - **[[зайти]](https://discord.gg/X3VcB5mrTG)**",
                colour=self.client.COLORS['BASE'])
            for cog in self.client.cogs:
                cog = self.client.cogs[cog]
                if cog.qualified_name in bcklist:
                    continue
                help_commands = ''
                for command in cog.get_commands():
                    help_commands += command.qualified_name + ', '
                embed.add_field(name='\n' + cog.qualified_name.capitalize(), value=f"*`{cog.description}`*\n{re.sub(r', $', '', help_commands)}\n",inline=False)
            embed.set_thumbnail(url=self.client.user.avatar_url)
            embed.set_footer(icon_url=self.client.user.avatar_url,text="аргументы в [] обязательны к указыванию, а в () нет.")
            await ctx.reply(embed=embed)
        else:
            command = self.client.get_command(input_name)
            if command is None:
                embed = discord.Embed(title="Помощь по командам",
                    description=f"Мой префикс - `{prefix}`\nПомощь по коммандам - `{prefix}хелп [команда]`\nсервер поддержки - **[[зайти]](https://discord.gg/X3VcB5mrTG)**",
                    colour=self.client.COLORS['BASE'])
                for cog in self.client.cogs:
                    cog = self.client.cogs[cog]
                    if cog.qualified_name in bcklist:
                        continue
                    help_commands = ''
                    for command in cog.get_commands():
                        help_commands += command.qualified_name + ', '
                    embed.add_field(name='\n' + cog.qualified_name.capitalize(), value=f"{cog.description}\n{re.sub(r', $', '', help_commands)}\n",inline=False)
                embed.set_footer(icon_url=self.client.user.avatar_url,text="аргументы в [] обязательны к указыванию, а в () нет.")
                embed.set_thumbnail(url=self.client.user.avatar_url)
                await ctx.reply(embed=embed)
            else:
                emb = discord.Embed(title = f"Команда: **`{command.name}`**", description = f"`{command.brief}`\nсервер поддержки - **[[зайти]](https://discord.gg/X3VcB5mrTG)**", colour = self.client.COLORS['BASE'])
                emb.add_field(name='Алиасы:', value=f"{re.sub(r', $', '', ', '.join(command.aliases))}",inline=False)
                emb.add_field(name="Использование:",value=f"{prefix}{command.usage}",inline=False)
                emb.add_field(name="Примеры:",value=f"```\n{command.description}\n```",inline=False)
                emb.set_footer(icon_url=self.client.user.avatar_url,text="аргументы в [] обязательны к указыванию, а в () нет.")
                emb.set_thumbnail(url=self.client.user.avatar_url)
                await ctx.reply(embed = emb)
        await ctx.message.add_reaction(self.client.EMOJIS['SUCCESS'])
                
    @commands.command(
        aliases=["user","юзеринфо","userinfo","пользователь"],
        name="юзер",
        usage="юзер (юзер)",
        brief="Информация о юзере",
        description="• юзер\n• юзер @BadBoyBot#2997"
        )
    async def _user(self, ctx,member:discord.Member= None,guild: discord.Guild = None):
        if member == None:
            member = ctx.author
        emb = discord.Embed(title='Информация о пользователе',colour = self.client.COLORS['BASE'])
        if  member.name != member.display_name:
            emb.add_field(name="Имя:",value=member.name,inline=False)
            emb.add_field(name="Имя на сервере:",value=member.mention)
        else:
            emb.add_field(name="Имя:",value=member.mention,inline=False)
        emb.add_field(name="Статус:", value=member.activity,inline=False)
        t = member.status
        if t == discord.Status.online:
            d = f"{self.client.EMOJIS['online']} В сети"
        if t == discord.Status.offline:
            d = f"{self.client.EMOJIS['offline']} Не в сети"
        if t == discord.Status.idle:
            d = f"{self.client.EMOJIS['idle']} Не активен"
        if t == discord.Status.dnd:
            d = f"{self.client.EMOJIS['dnd']} Не беспокоить"
        emb.add_field(name="Активность:", value=d,inline=False)
        emojis_str = ''
        for flag in member.public_flags.all():
            emojis_str += f'{self.client.EMOJIS[flag.name]}' + ' '
        emb.add_field(name = "Значки:", value =emojis_str if emojis_str != '' else "Нету", inline = False)
        if member in self.client.owners:
            emb.add_field(name="премиум статус:",value="**OWNER PREMIUM**",inline=False)
        if member.id in self.client.premium_u:
            emb.add_field(name="премиум статус:",value="**DEFAULT PREMIUM**",inline=False)
        if member not in self.client.owners:
            if member.id not in self.client.premium_u:
                emb.add_field(name="премиум статус:",value="**NO PREMIUM**",inline=False)
        emb.add_field(name="В discord с:", value=(member.created_at + deltaMSK).strftime(timeformMSK))
        emb.add_field(name="На сервере с:",value=(member.joined_at + deltaMSK).strftime(timeformMSK),inline=False)
        emb.add_field(name="Высшая роль на сервере:", value=f"{member.top_role.mention}",inline=False)
        emb.set_thumbnail(url=member.avatar_url)
        emb.set_footer(text=f"id: {member.id}")
        await ctx.reply(embed = emb)
        await ctx.message.add_reaction(self.client.EMOJIS['SUCCESS'])
            
    @commands.command(
        name="аватар",
        usage="аватар (юзер) (формат) (размер)",
        brief="Аватар пользователя",
        aliases=["ava","ава","avatar"],
        description="• аватар\n• аватар @BadBoyBot#2997\n• аватар @BadBoyBot#2997 png\n• аватар @BadBoyBot#2997 png 1024"
        )
    async def _avatar(self, ctx,member:discord.Member = None, pformat=None, psize = None):
        if psize == None:
            psize="1024"
        if pformat == None:
            pformat="png"
        if member == None:
            member = ctx.author
        if psize not in ["16","32","64","128","256","512","1024","2048","4096"]:
            return await ctx.reply(embed=discord.Embed(title='ошибка', description='значение размера не валидно.\nможно использовать только:\n16, 32, 64, 128, 256, 512, 1024, 2048, 4096.',colour=self.client.COLORS['ERROR']))
        if pformat not in ["webp","jpeg","jpg","png","gif"]:
            return await ctx.reply(embed=discord.Embed(title='ошибка', description='значение формата не валидно.\nможно использовать только:\nwebp, jpeg, jpg, png, gif.',colour=self.client.COLORS['ERROR']))
        emb = discord.Embed(title=f"аватар пользователя:",description=member.mention, colour=self.client.COLORS['BASE'])
        emb.set_image(url=member.avatar_url_as(format=pformat,size=int(psize)))
        await ctx.reply(embed = emb)
        await ctx.message.add_reaction(self.client.EMOJIS['SUCCESS'])
    
    @commands.command(
        name="сервер",
        usage="сервер",
        brief="Информация о сервере",
        aliases=["server","infoserver","serverinfo","серв","серверинфо","serv"],
        description="• сервер"
        )
    @commands.guild_only()
    async def _serverinfo(self, ctx):
      name = str(ctx.guild.name)
      description = str(ctx.guild.description)
      owner = str(ctx.guild.owner)
      id = str(ctx.guild.id)
      region = str(ctx.guild.region)
      memberCount = str(ctx.guild.member_count)
      create_at = str((ctx.guild.created_at + deltaMSK).strftime(timeformMSK))
    
      icon = str(ctx.guild.icon_url)
       
      emb = discord.Embed(
          title="Информация о сервере:",
          colour=self.client.COLORS['BASE']
        )
      emb.set_thumbnail(url=icon)
      emb.add_field(name="Название:", value=name,inline=True)
      emb.add_field(name="Владелец:", value=owner, inline=True)
      emb.add_field(name="Участников:", value=memberCount, inline=True)
      emb.add_field(name="Регион:",value=region,inline=True)
      emb.add_field(name="создан:",value=create_at,inline=True)
      emb.add_field(name = "Пользователей", value = len([member for member in ctx.guild.members if not member.bot]), inline = False)
      emb.add_field(name = "Ботов", value = len([member for member in ctx.guild.members if member.bot]), inline = False)
      emb.add_field(name = "Ролей", value = len(ctx.guild.roles))
      emb.add_field(name = "Текстовых каналов", value = len(ctx.guild.text_channels), inline = False)
      emb.add_field(name = "Голосовых каналов", value = len(ctx.guild.voice_channels), inline = False)
      emb.add_field(name = "Эмодзи", value = len(ctx.guild.emojis), inline = False)
      if ctx.guild.me.guild_permissions.ban_members:
        bans = await ctx.guild.bans()
        emb.add_field(name = "Банов", value = len(bans))
      if ctx.guild.afk_channel is not None:
        emb.add_field(name = "АФК канал", value = ctx.guild.afk_channel.name)
        emb.add_field(name = "Время до перемещения в АФК канал", value = f"{ctx.guild.afk_timeout} секунд")
      if ctx.guild.premium_subscription_count > 0:
        emb.add_field(name = "**Бусты**", value = "‌‌‍‍", inline = False)
        emb.add_field(name = "Уровень буста", value = ctx.guild.premium_tier)
        emb.add_field(name = "Бустеров", value = len(ctx.guild.premium_subscribers))
        emb.add_field(name = "Количество бустов", value = ctx.guild.premium_subscription_count)
      emb.set_footer(text=f"id: {ctx.guild.id}")
      await ctx.reply(embed=emb)
      await ctx.message.add_reaction(self.client.EMOJIS['SUCCESS'])

    @commands.command(
        name="эмоджи",
        usage="эмоджи [эмоджи]",
        brief="Информация о эмоджи",
        aliases=["emoji","емоджи","имоджи","емодзи","amogi","эмодзи"],
        description="• эмоджи 😎"
        )
    async def _emoji(self, ctx,emoji: discord.Emoji):
        emb = discord.Embed(title = f"Информация об эмоджи:\n :{emoji.name}:", colour=self.client.COLORS['BASE'])
        emb.add_field(name = "Анимированное", value = "Да" if emoji.animated else "Нет", inline = False)
        emb.add_field(name = "Сервер эмоджи", value = emoji.guild.name)
        emb.add_field(name = "Время создания", value = (emoji.created_at+deltaMSK).strftime(timeformMSK), inline = False)
        emb.add_field(name = "URL", value = emoji.url, inline = False)
        emb.set_image(url = emoji.url)
        emb.set_footer(text = f"ID {emoji.id}")
        await ctx.reply(embed = emb)
        await ctx.message.add_reaction(self.client.EMOJIS['SUCCESS'])
        
    @commands.command(
        name = "бот",
        usage="бот",
        aliases = ["bot", "ботинок","ботинфо","botinfo"],
        brief = "Информация о боте",
        description="• бот"
        )
    async def _bot(self, ctx):
        servers=len(self.client.guilds)
        users=len(self.client.users)
        commands=len(self.client.commands)
        channels=len(list(self.client.get_all_channels()))
        time = datetime.datetime.now()
        msg = await ctx.reply(embed=discord.Embed(title="bot", description="загрузка...",colour=self.client.COLORS['SUCCESS']))
        emb= discord.Embed(title="Информация о боте",description= f"Я - Discord бот {self.client.user.mention}.\n Сейчас я умею делать немного вещей, но мой создатель постоянно меня улучшает и добавляет в меня новые функции.",colour=self.client.COLORS['BASE'])
        emb.add_field(name="Создатель:",value=self.client.owners[1].mention)
        emb.add_field(name="Разработчик(и):",
        value=f"{self.client.owners[0].mention}")
        emb.add_field(name="Был выкован гномами(создан):",value=(self.client.user.created_at+deltaMSK).strftime(timeformMSK))
        emb.add_field(name="Запущен:",value=self.client.start_time.strftime(timeformMSK))
        emb.add_field(name="Ping WebSocket:",value=f"{round(self.client.latency, 3)} сек")
        emb.add_field(name="Ping Discord API:",value=f"{str(round((datetime.datetime.now() - time).total_seconds(), 3))} сек")
        emb.add_field(name="Серверов:",value=servers,inline=False)
        emb.add_field(name="Каналов:",value=channels,inline=False)
        emb.add_field(name="Пользователей:",value=users,inline=False)
        emb.add_field(name="Команд:",value=commands,inline=False)
        emb.add_field(name="Полезные ссылки:",value=f"сервер - **[[волшебная кнопка]](https://discord.gg/X3VcB5mrTG)**\nпригласить бота - **[[волшебная кнопка]](https://discord.com/api/oauth2/authorize?client_id={self.client.user.id}&permissions=8&scope=bot)**",inline=False)
        emb.set_thumbnail(url=self.client.user.avatar_url)
        await msg.edit(embed=emb)
        await ctx.message.add_reaction(self.client.EMOJIS['SUCCESS'])
        
    @commands.command(
        name="пинг",
        usage="пинг",
        brief="узнать пинг бота",
        aliases=["ping"],
        description="• пинг"
        )
    async def _ping(self, ctx):
        time = datetime.datetime.now()
        msg = await ctx.reply(embed=discord.Embed(title="ping", description="загрузка...",colour=self.client.COLORS['SUCCESS']))
        await msg.edit(embed=discord.Embed(colour=self.client.COLORS['BASE']).add_field(name="ping WebSocket:",value=f"{round(self.client.latency, 3)} сек").add_field(name="ping Discord API:",value=f"{str(round((datetime.datetime.now() - time).total_seconds(), 3))} сек"))
        await ctx.message.add_reaction(self.client.EMOJIS['SUCCESS'])
    
    @commands.command(
        name = "канал",
        brief = "Информация о канале",
        aliases = ['channel', 'channelinfo'],
        usage = "канал (канал)",
        description="• канал\n• канал #новости"
    )
    async def _channel(self, ctx, channel: typing.Union[discord.TextChannel, discord.VoiceChannel] = None):
        if channel is None: 
            channel = ctx.channel
        if type(channel) == discord.DMChannel:
            raise discord.ext.commands.errors.NoPrivateMessage
        embed = discord.Embed(title = f"Информация о канале {channel.name}", colour = self.client.COLORS['BASE'])
        if type(channel) == discord.TextChannel:
            embed.add_field(name = "Тип канала", value = "Текстовый", inline = False)
            embed.add_field(name = "Описание канала", value = channel.topic if channel.topic is not None else "Отсутствует", inline = False)
            embed.add_field(name = "Канал создан", value = (channel.created_at+deltaMSK).strftime(timeformMSK), inline = False)
            embed.add_field(name = "Задержка(слоумод)", value = f"{channel.slowmode_delay} секунд", inline = False)
            embed.add_field(name = "NSFW канал", value = "Да" if channel.is_nsfw() else "Нет", inline = False)
            embed.add_field(name = "Новостной канал", value = "Да" if channel.is_news() else "Нет", inline = False)
            embed.add_field(name = "Количество пользователей, которые могут видеть этот канал", value = len(channel.members), inline = False)
            if ctx.channel.permissions_for(ctx.guild.me).manage_channels:
                invites = await channel.invites()
                embed.add_field(name = "Приглашений", value = len(invites), inline = False)
            pins = await channel.pins()
            embed.add_field(name = "Закреплённых сообщений", value = len(pins), inline = False)
            
        elif type(channel) == discord.VoiceChannel:
            embed.add_field(name = "Тип канала", value = "Голосовой", inline = False)
            embed.add_field(name = "Канал создан", value = (channel.created_at+deltaMSK).strftime(timeformMSK), inline = False)
            embed.add_field(name = "Битрейт", value = f"{channel.bitrate} бит в секунду", inline = False)
            embed.add_field(name = "Лимит пользователей", value = channel.user_limit if channel.user_limit != 0 else "Отсутствует", inline = False)
            embed.add_field(name = "Пользователей в голосовом канале", value = len(channel.members), inline = False)
            if ctx.channel.permissions_for(ctx.guild.me).manage_channels:
                invites = await channel.invites()
                embed.add_field(name = "Приглашений", value = len(invites), inline = False)

        embed.set_footer(text = f"ID {channel.id}")
        await ctx.reply(embed = embed)
        await ctx.message.add_reaction(self.client.EMOJIS['SUCCESS'])

    @commands.command(
        name = "инфо-роль",
        brief = "Информация о роли",
        aliases = ['roleinfo','role-info','инфороль'],
        usage = "инфо-роль [роль]",
        description="• инфо роль @супер_пупер_роль"
    )
    async def _role(self, ctx, * ,role: discord.Role):
        embed = discord.Embed(title = f"Информация о роли {role.name}", colour = self.client.COLORS['BASE'])
        embed.add_field(name = "Цвет роли", value = role.color, inline = False)
        embed.add_field(name = "Роль создана", value = (role.created_at + deltaMSK).strftime(timeformMSK), inline = False)
        embed.add_field(name = "Позиция(с конца)", value = f"{role.position + 1}/{len(role.guild.roles)}", inline = False)
        embed.add_field(name = "Отображение отдельно", value = "Да" if role.hoist else "Нет", inline = False)
        embed.add_field(name = "Упоминаемая", value = "Да" if role.mentionable else "Нет", inline = False)
        embed.add_field(name = "Количество пользователей с этой ролью", value = len(role.members), inline = False)

        embed.set_footer(text = f"ID {role.id}")
        await ctx.reply(embed = embed)
        await ctx.message.add_reaction(self.client.EMOJIS['SUCCESS'])

def setup(client):
    client.add_cog(info(client))
