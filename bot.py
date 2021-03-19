import discord
from discord import utils
from discord.ext import commands
from discord.ext.commands import has_permissions
from discord.utils import get
import os
import asyncio
from asyncio import sleep
import ast
import config
import datetime

client = commands.Bot(command_prefix = config.prefix, intents = discord.Intents.all())

delta = datetime.timedelta(hours=3)
timeform1 = " %H:%M %d.%m.%Y ||`UTC(+3:00)`||"

@client.event
async def on_ready():
    client.start_time = datetime.datetime.now()
    ai = await client.application_info()
    client.owners = ai.team.members
    client.idea_channel = client.get_channel(813511569795055634)
    client.bug_channel = client.get_channel(813511569795055635)
    client.eval_fn_channel = client.get_channel(816209752249597952)
    print("---------------------")
    print(f'{client.user}')
    print(f'{len(client.guilds)} сервера')
    print(f'Пинг: {round(client.latency, 3)} секунд')
    print('Я готов к работе')
    print("---------------------")
    while True:
          await client.change_presence(status=discord.Status.online, activity=discord.Game(",help"))
          await sleep(30)
          await client.change_presence(status=discord.Status.online, activity=discord.Streaming(name="свои брутальные фотки", url="https://discord.com/"))
          await sleep(15)

def insert_returns(body):
    # insert return stmt if the la9st expression is a expression statement
    if isinstance(body[-1], ast.Expr):
        body[-1] = ast.Return(body[-1].value)
        ast.fix_missing_locations(body[-1])

    # for if statements, we insert returns into the body and the orelse
    if isinstance(body[-1], ast.If):
        insert_returns(body[-1].body)
        insert_returns(body[-1].orelse)

    # for with blocks, again we insert returns into the body
    if isinstance(body[-1], ast.With):
        insert_returns(body[-1].body)


@client.command(aliases=["eval"])
@commands.is_owner()
async def eval_fn(ctx, *, cmd):
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

    insert_returns(body)

    env = {
        'client': ctx.bot,
        'discord': discord,
        'commands': commands,
        'ctx': ctx,
        '__import__': __import__
    }
    exec(compile(parsed, filename="<ast>", mode="exec"), env)
    result = (await eval(f"{fn_name}()", env))
    await client.eval_fn_channel.send(embed=discord.Embed(title="использована команда eval",color=ctx.message.author.color).add_field(name="кем:",value=f"{ctx.message.author}").add_field(name="код:", value=f"```py\n{cmd}\n```"))
    await ctx.message.add_reaction("✅")

@client.command(aliases=["идея"])
async def idea(ctx, * , idea = None):
    if ctx.message.author.id == config.black_list:
        await ctx.send(embed=discord.Embed(title="ОШИБКА", description=f"**{ctx.message.author}**,\n эта команда для вас заблокирована.", colour=discord.Colour.red()))
        return
    if idea == None:
        await ctx.send(embed=discord.Embed(title="ОШИБКА",description="напишите идею.\nнельзя отправить пустое сообщение о идее",colour=discord.Colour.red()))
    else:
        emb = discord.Embed(title= "идея", description= idea, color = ctx.message.author.color)
        emb.set_footer( text=f"Использовано пользователем:\n{ctx.message.author}", icon_url=ctx.message.author.avatar_url)
        await client.idea_channel.send(embed=emb)
        await ctx.send(embed = discord.Embed(description=f"**{ctx.message.author}** ,\n спасибо за ваш вклад в развитие бота", color= ctx.message.author.color))

@client.command(aliases=["баг","багулина"])
async def bug(ctx, * , bug = None):
    
    if ctx.message.author.id == config.black_list:
        await ctx.send(embed=discord.Embed(title="ОШИБКА", description=f"**{ctx.message.author}**,\n эта команда для вас заблокирована.", colour=discord.Colour.red()))
        return
    if bug == None:
        await ctx.send(embed=discord.Embed(title="ОШИБКА",description="напишите баг.\nнельзя отправить пустое сообщение о баге",colour=discord.Colour.red()))
    else:
        emb = discord.Embed(title= "баг", description= bug, color = ctx.message.author.color)
        emb.set_footer( text=f"Использовано пользователем:\n{ctx.message.author}", icon_url=ctx.message.author.avatar_url)
        await client.bug_channel.send(embed=emb)
        await ctx.send(embed = discord.Embed(description=f"**{ctx.message.author}** ,\n спасибо за ваш вклад в развитие бота", color= ctx.message.author.color))

@client.command(aliases=["юзер","юзеринфо","userinfo","пользователь","я","i"])
async def user(ctx,member:discord.Member= None,guild: discord.Guild = None):
    if member == None:
        emb = discord.Embed(title='Информация о пользователе',color = ctx.author.color)
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
        emb.add_field(name="В discord с:", value=(ctx.author.created_at + delta).strftime(timeform1))
        emb.add_field(name="На сервере с:",value=(ctx.author.joined_at + delta).strftime(timeform1),inline=False)
        emb.add_field(name="Высшая роль на сервере:", value=f"{ctx.message.author.top_role.mention}",inline=False)
        emb.set_thumbnail(url=ctx.author.avatar_url)
        emb.set_footer(text=f"id: {ctx.message.author.id}")
        await ctx.send(embed = emb)
    else:
        emb = discord.Embed(title='Информация о пользователе',color = member.color)
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
        emb.add_field(name="В discord с:", value=(member.created_at + delta).strftime(timeform1))
        emb.add_field(name="На сервере с:",value=(member.joined_at + delta).strftime(timeform1),inline=False)
        emb.add_field(name="Высшая роль на сервере:", value=f"{member.top_role.mention}",inline=False)
        emb.set_thumbnail(url=member.avatar_url)
        emb.set_footer(text=f"id: {member.id}")
        await ctx.send(embed = emb)
    
@client.command(pass_context=True, aliases=["очистить"])
@has_permissions(manage_messages=True)
async def clear(ctx, amount=1):
    cleared=await ctx.channel.purge(limit=int(amount) + 1)
    cleared_count=str(len(cleared))
    emb = discord.Embed(title="Очистка",description = "Удалено "+cleared_count+" сообщений", colour=discord.Colour.blue())
    message_bot= await ctx.send(embed = emb)
    
@client.command(aliases=["ava","ава","аватар"])
async def avatar(ctx,member:discord.Member = None):
    if member == None:
        emb = discord.Embed(title=f"аватар пользователя:",description=ctx.message.author.mention,color=ctx.message.author.color)
        emb.set_image(url=ctx.message.author.avatar_url)
        await ctx.send(embed = emb)
    else:
        emb = discord.Embed(title=f"аватар пользователя:",description=member.mention, color=member.color)
        emb.set_image(url=member.avatar_url)
        await ctx.send(embed = emb)
        
@client.command(aliases=["server","infoserver","сервер","серв","серверинфо","serv"])
async def serverinfo(ctx):
  name = str(ctx.guild.name)
  description = str(ctx.guild.description)

  owner = str(ctx.guild.owner)
  id = str(ctx.guild.id)
  region = str(ctx.guild.region)
  memberCount = str(ctx.guild.member_count)
  create_at = str((ctx.guild.created_at + delta).strftime(timeform1))

  icon = str(ctx.guild.icon_url)
   
  emb = discord.Embed(
      title="Информация о сервере:",
      color=ctx.message.author.color
    )
  emb.set_thumbnail(url=icon)
  emb.add_field(name="Название:", value=name,inline=True)
  emb.add_field(name="Описание:",value=description,inline=True)
  emb.add_field(name="Владелец:", value=owner, inline=True)
  emb.add_field(name="Участников:", value=memberCount, inline=True)
  emb.add_field(name="Регион:",value=region,inline=True)
  emb.add_field(name="создан:",value=create_at,inline=True)
  emb.set_footer(text=f"id: {ctx.guild.id}")
  await ctx.send(embed=emb)
  
@client.command(aliases=["сказать","озв"])
@has_permissions(administrator=True)
async def say(ctx, *,text):
    await ctx.message.delete()
    await ctx.send(text)
        
@client.command(aliases=["эмоджи","емоджи","имоджи","емодзи","amogi"])
async def emoji(ctx,emoji: discord.Emoji= None):
    if emoji == None:
        await ctx.send(embed=discord.Embed(title="ОШИБКА",description=f"**{ctx.message.author}**,\nпожалуйста укажите emoji", colour=discord.Colour.red()))
    else:
        embed = discord.Embed(title = f"Информация об эмоджи:\n :{emoji.name}:", color = ctx.message.author.color)
        embed.add_field(name = "Анимированное", value = "Да" if emoji.animated else "Нет", inline = False)
        embed.add_field(name = "Сервер эмоджи", value = emoji.guild.name)
        embed.add_field(name = "Время создания", value = (emoji.created_at+delta).strftime(timeform1), inline = False)
        embed.add_field(name = "URL", value = emoji.url, inline = False)
        embed.set_image(url = emoji.url)
        embed.set_footer(text = f"ID {emoji.id}")

        await ctx.send(embed = embed)
   
@client.command(aliases = ['ливай'])
async def leave(ctx):
    if ctx.message.author.id == 690496049361584159:
        await ctx.send(embed = discord.Embed(description = "Всем бай-бай",color= ctx.message.author.color))
        await ctx.guild.leave()
    else: 
        await ctx.send(embed=discord.Embed(title="ОШИБКА",description=f"**{ctx.message.author}**,\n эта команда только для владельца бота", colour=discord.Colour.red()))

client.run(config.TOKEN)
