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

class info(commands.Cog, name="Информация"):
    """Инфо комманды:"""

    def __init__(self, client):
        self.client = client

    @commands.command(
        name="хелп",
        aliases=["help","помощь"],
        usage="хелп [команда]",
        description="Помощь по командам"
    )
    async def _help(self, ctx: commands.Context, input_name = None):
        prefix = config.prefix
        if input_name is None:
            embed = discord.Embed(
                description=f"помощь по коммандам - {prefix}хелп [команда]",
                colour=config.COLORS['BASE'])
            for cog in self.client.cogs:
                cog = self.client.cogs[cog]
                if cog.qualified_name in ["events", "owner","Премиум"]:
                    continue
                help_commands = ''
                for command in cog.get_commands():
                    help_commands += prefix + command.qualified_name + '  '
                embed.add_field(name='\n' + cog.qualified_name.capitalize(), value=f"{cog.description}\n{re.sub(r', $', '', help_commands)}\n")
            await ctx.send(embed=embed)
        else:
            command = self.client.get_command(input_name)
            if command is None:
                embed = discord.Embed(title="Помощь по командам",
                    description=f"Для подробной информации по команде используйте {prefix}хелп [команда]",
                    colour=config.COLORS['BASE'])
                for cog in self.client.cogs:
                    cog = self.client.cogs[cog]
                    if cog.qualified_name in ["events", "owner","Премиум"]:
                        continue
                    help_commands = ''
                    for command in cog.get_commands():
                        help_commands += command.qualified_name + ', '
                    embed.add_field(name='\n' + cog.qualified_name.capitalize(), value=f"{cog.description}\n{re.sub(r', $', '', help_commands)}\n")
                await ctx.send(embed=embed)
            else:
                await ctx.send(embed = discord.Embed(title = f"Помощь по команде {command.name}", description = f"{command.description}\nАлиасы: {re.sub(r', $', '', ', '.join(command.aliases))}\nИспользование: {prefix}{command.usage}", colour = config.COLORS['BASE']))
                
    @commands.command(
        aliases=["user","юзеринфо","userinfo","пользователь"],
        name="юзер",
        usage="юзер (юзер)",
        description="Информация о юзере"
        )
    async def _user(self, ctx,member:discord.Member= None,guild: discord.Guild = None):
        if member == None:
            emb = discord.Embed(title='Информация о пользователе',colour = config.COLORS['BASE'])
            if  ctx.author.name != ctx.author.display_name:
                emb.add_field(name="Имя:",value=ctx.author.name,inline=False)
                emb.add_field(name="Имя на сервере:",value=ctx.author.mention)
            else:
                emb.add_field(name="Имя:",value=ctx.author.mention,inline=False)
            emb.add_field(name="Статус:", value=ctx.message.author.activity,inline=False)
            t = ctx.message.author.status
            if t == discord.Status.online:
                d = "<:online:813698625569947680>  В сети"

            t = ctx.message.author.status
            if t == discord.Status.offline:
                d = "<:offline:813698775125983272>  Не в сети"

            t = ctx.message.author.status
            if t == discord.Status.idle:
                d = "<:idle:813698687913295894> Не активен"

            t = ctx.message.author.status
            if t == discord.Status.dnd:
                d = "<:dnd:813698546657787914> Не беспокоить"

            emb.add_field(name="Активность:", value=d,inline=False)
            emojis = {
                "staff": "<:discord_staff:777516108260704256>",
                "partner": "<:discord_partner:777513164912328706>",
                "bug_hunter": "<:bug_hunter:777543195483570197>",
                "hypesquad_bravery": "<:hypesquad_bravery:777540499858653195>",
                "hypesquad_brilliance": "<:hypesquad_brilliance:777540500035076127>",
                "hypesquad_balance": "<:hypesquad_balance:777540500026294272>",
                "early_supporter": "<:early_supporter:777504637094985758>",
                "system": "<:discord:777505535930007593>",
                "bug_hunter_level_2": "<:bug_hunter:777543195483570197>",
                "verified_bot": "<:verified_bot:777507474017615884>",
                "verified_bot_developer": "<:verified_bot_developer:777510397316956170>"
            }
            emojis_str = ''
            for flag in ctx.message.author.public_flags.all():
                emojis_str += emojis[flag.name] + ' '
            emb.add_field(name = "Значки:", value =emojis_str if emojis_str != '' else "Нету", inline = False)
            if ctx.author in self.client.owners:
                emb.add_field(name="премиум статус:",value="**OWNER PREMIUM**",inline=False)
            if ctx.author.id in self.client.premium_u:
                emb.add_field(name="премиум статус:",value="**DEFAULT PREMIUM**",inline=False)
            if ctx.author not in self.client.owners:
                if ctx.author.id not in self.client.premium_u:
                    emb.add_field(name="премиум статус:",value="**NO PREMIUM**",inline=False)
            emb.add_field(name="В discord с:", value=(ctx.author.created_at + deltaMSK).strftime(timeformMSK))
            emb.add_field(name="На сервере с:",value=(ctx.author.joined_at + deltaMSK).strftime(timeformMSK),inline=False)
            emb.add_field(name="Высшая роль на сервере:", value=f"{ctx.message.author.top_role.mention}",inline=False)
            emb.set_thumbnail(url=ctx.author.avatar_url)
            emb.set_footer(text=f"id: {ctx.message.author.id}")
            await ctx.send(embed = emb)
        else:
            emb = discord.Embed(title='Информация о пользователе',colour = config.COLORS['BASE'])
            if  member.name != member.display_name:
                emb.add_field(name="Имя:",value=member.name,inline=False)
                emb.add_field(name="Имя на сервере:",value=member.mention)
            else:
                emb.add_field(name="Имя:",value=member.mention,inline=False)
            emb.add_field(name="Статус:", value=member.activity,inline=False)
            t = member.status
            if t == discord.Status.online:
                d = "<:online:813698625569947680> В сети"

            t = member.status
            if t == discord.Status.offline:
                d = "<:offline:813698775125983272>  Не в сети"

            t = member.status
            if t == discord.Status.idle:
                d = "<:idle:813698687913295894> Не активен"

            t = member.status
            if t == discord.Status.dnd:
                d = "<:dnd:813698546657787914> Не беспокоить"
            emb.add_field(name="Активность:", value=d,inline=False)
            emojis = {
                "staff": "<:discord_staff:777516108260704256>",
                "partner": "<:discord_partner:777513164912328706>",
                "bug_hunter": "<:bug_hunter:777543195483570197>",
                "hypesquad_bravery": "<:hypesquad_bravery:777540499858653195>",
                "hypesquad_brilliance": "<:hypesquad_brilliance:777540500035076127>",
                "hypesquad_balance": "<:hypesquad_balance:777540500026294272>",
                "early_supporter": "<:early_supporter:777504637094985758>",
                "system": "<:discord:777505535930007593>",
                "bug_hunter_level_2": "<:bug_hunter:777543195483570197>",
                "verified_bot": "<:verified_bot:777507474017615884>",
                "verified_bot_developer": "<:verified_bot_developer:777510397316956170>"
            }
            emojis_str = ''
            for flag in member.public_flags.all():
                emojis_str += emojis[flag.name] + ' '
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
            await ctx.send(embed = emb)
            
    @commands.command(
        name="аватар",
        usage="аватар (юзер) (формат) (размер)",
        description="Аватар пользователя",
        aliases=["ava","ава","avatar"])
    async def _avatar(self, ctx,member:discord.Member = None, pformat=None, psize:int = None):
        if psize == None:
            psize=1024
        if psize < 1:
            psize=1024
        if pformat in ["webp","jpeg","jpg","png","gif",None]:
            if member == None:
                emb = discord.Embed(title=f"аватар пользователя:",description=ctx.message.author.mention,colour=config.COLORS['BASE'])
                emb.set_image(url=ctx.message.author.avatar_url_as(format=pformat,size=psize))
                await ctx.send(embed = emb)
            else:
                emb = discord.Embed(title=f"аватар пользователя:",description=member.mention, colour=config.COLORS['BASE'])
                emb.set_image(url=member.avatar_url_as(format=pformat,size=psize))
                await ctx.send(embed = emb)
            
    @commands.command(
        name="сервер",
        usage="сервер",
        description="Информация о сервере",
        aliases=["server","infoserver","serverinfo","серв","серверинфо","serv"])
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
          colour=config.COLORS['BASE']
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
      await ctx.send(embed=emb)

    @commands.command(
        name="эмоджи",
        usage="эмоджи [эмоджи]",
        description="Информация о эмоджи",
        aliases=["emoji","емоджи","имоджи","емодзи","amogi","эмодзи"])
    async def _emoji(self, ctx,emoji: discord.Emoji):
            emb = discord.Embed(title = f"Информация об эмоджи:\n :{emoji.name}:", colour=config.COLORS['BASE'])
            emb.add_field(name = "Анимированное", value = "Да" if emoji.animated else "Нет", inline = False)
            emb.add_field(name = "Сервер эмоджи", value = emoji.guild.name)
            emb.add_field(name = "Время создания", value = (emoji.created_at+deltaMSK).strftime(timeformMSK), inline = False)
            emb.add_field(name = "URL", value = emoji.url, inline = False)
            emb.set_image(url = emoji.url)
            emb.set_footer(text = f"ID {emoji.id}")
    
            await ctx.send(embed = emb)
        
    @commands.command(
        name = "бот",
        usage="бот",
        aliases = ["bot", "ботинок","ботинфо","botinfo"],
        description = "Информация о боте"
        )
    async def _bot(self, ctx):
        servers=len(self.client.guilds)
        users=len(self.client.users)
        commands=len(self.client.commands)
        time = datetime.datetime.now()
        msg = await ctx.send(embed=discord.Embed(colour=config.COLORS['SUCCESS']))
        emb= discord.Embed(title="Информация о боте",description= f"Я - Discord бот {self.client.user.mention}.\n Сейчас я умею делать немного вещей, но мой создатель постоянно меня улучшает и добавляет в меня новые функции.",colour=config.COLORS['BASE'])
        emb.add_field(name="запущен в:",value=self.client.start_time.strftime(timeformMSK))
        emb.add_field(name="ping WebSocket:",value=f"{round(self.client.latency, 3)} сек")
        emb.add_field(name="ping Discord API:",value=f"{str(round((datetime.datetime.now() - time).total_seconds(), 3))} сек")
        emb.add_field(name="серверов:",value=servers,inline=False)
        emb.add_field(name="пользователей:",value=users,inline=False)
        emb.add_field(name="команд:",value=commands,inline=False)
        emb.add_field(name="полезные ссылки:",value=f"сервер - **[[волшебная кнопка]](https://discord.gg/X3VcB5mrTG)**\nпригласить бота - **[[волшебная кнопка]](https://discord.com/api/oauth2/authorize?client_id={self.client.user.id}&permissions=8&scope=bot)**",inline=False)
        emb.set_thumbnail(url=self.client.user.avatar_url)
        await msg.edit(embed=emb)
        
    @commands.command(
        name="пинг",
        usage="пинг",
        description="узнать пинг бота",
        aliases=["ping"]
        )
    async def _ping(self, ctx):
        time = datetime.datetime.now()
        msg = await ctx.send(embed=discord.Embed(colour=config.COLORS['SUCCESS']))
        await msg.edit(embed=discord.Embed(colour=config.COLORS['BASE']).add_field(name="ping WebSocket:",value=f"{round(self.client.latency, 3)} сек").add_field(name="ping Discord API:",value=f"{str(round((datetime.datetime.now() - time).total_seconds(), 3))} сек"))
    
    @commands.command(
        name = "канал",
        description = "Информация о канале",
        aliases = ['channel', 'channelinfo'],
        usage = "канал (канал)"
    )
    async def _channel(self, ctx, channel: typing.Union[discord.TextChannel, discord.VoiceChannel] = None):
        if channel is None: 
            channel = ctx.channel
        if type(channel) == discord.DMChannel:
            raise discord.ext.commands.errors.NoPrivateMessage
        embed = discord.Embed(title = f"Информация о канале {channel.name}", colour = config.COLORS['BASE'])
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
        await ctx.send(embed = embed)

    @commands.command(
        name = "роль",
        description = "Информация о роли",
        aliases = ['role', 'roleinfo'],
        usage = "роль [Роль]"
    )
    async def _role(self, ctx, role: discord.Role):
        embed = discord.Embed(title = f"Информация о роли {role.name}", colour = config.COLORS['BASE'])
        embed.add_field(name = "Цвет роли", value = role.color, inline = False)
        embed.add_field(name = "Роль создана", value = (role.created_at + deltaMSK).strftime(timeformMSK), inline = False)
        embed.add_field(name = "Позиция(с конца)", value = f"{role.position + 1}/{len(role.guild.roles)}", inline = False)
        embed.add_field(name = "Отображение отдельно", value = "Да" if role.hoist else "Нет", inline = False)
        embed.add_field(name = "Упоминаемая", value = "Да" if role.mentionable else "Нет", inline = False)
        embed.add_field(name = "Количество пользователей с этой ролью", value = len(role.members), inline = False)

        embed.set_footer(text = f"ID {role.id}")
        await ctx.send(embed = embed)

def setup(client):
    client.add_cog(info(client))