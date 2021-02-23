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

client = commands.Bot(command_prefix = config.prefix, intents = discord.Intents.all())

@client.event
async def on_ready():
    print('------------------')
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------------------')
    while True:
          await client.change_presence(status=discord.Status.online, activity=discord.Game(",help"))
          await sleep(30)
          await client.change_presence(status=discord.Status.online, activity=discord.Game("Просмотр своих брутальных фоток"))
          await sleep(15)

def insert_returns(body):
    # insert return stmt if the last expression is a expression statement
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

@client.command(aliases=["юзер","юзеринфо","userinfo","пользователь","я","i"])
async def user(ctx,member:discord.Member= None):
    if member == None:
        emb = discord.Embed(title='Информация о пользователе',color = ctx.author.color)
        emb.add_field(name="Имя:",value=ctx.author.display_name,inline=False)
        emb.add_field(name="Статус:",value=ctx.author.status)
        emb.add_field(name="В discord с:", value=ctx.author.created_at.strftime("%d.%m.%Y, %H:%M:%S"))
        emb.add_field(name="На сервере с:",value=ctx.author.joined_at.strftime("%d.%m.%Y, %H:%M:%S"),inline=False)
        emb.add_field(name="`id:`", value=ctx.author.id,inline=False)
        emb.set_thumbnail(url=ctx.author.avatar_url)
        emb.set_footer(text=f"Использовано пользователем:\n {ctx.message.author}" ,icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed = emb)
    else:
        emb = discord.Embed(title='Информация о пользователе',color = member.color)
        emb.add_field(name="Имя:",value=member.display_name,inline=False)
        emb.add_field(name="Статус:",value=member.status)
        emb.add_field(name="В discord с:", value=member.created_at.strftime("%d.%m.%Y, %H:%M:%S"))
        emb.add_field(name="На сервере с:",value=member.joined_at.strftime("%d.%m.%Y, %H:%M:%S"),inline=False)
        emb.add_field(name="`id:`", value=member.id,inline=False)
        emb.set_thumbnail(url=member.avatar_url)
        emb.set_footer(text=f"Использовано пользователем:\n {ctx.message.author}" ,icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed = emb)
    
@client.command(pass_context=True, aliases=["очистить"])
@has_permissions(manage_messages=True)
async def clear(ctx, amount=1):
    cleared=await ctx.channel.purge(limit=int(amount) + 1)
    cleared_count=str(len(cleared))
    emb = discord.Embed(title="Очистка",description = "Удалено "+cleared_count+" сообщений", colour=discord.Colour.blue())
    emb.set_footer(text=f"Использовано пользователем:\n {ctx.message.author}",icon_url=ctx.message.author.avatar_url)
    message_bot= await ctx.send(embed = emb)
    
@client.command(aliases=["ава","аватар"])
async def avatar(ctx,member:discord.Member = None):
    if member == None:
        emb = discord.Embed(title=f"аватар пользователя: \n {ctx.message.author.display_name}",color=ctx.message.author.color)
        emb.set_image(url=ctx.message.author.avatar_url)
        emb.set_footer(text=f"Использовано пользователем: \n {ctx.message.author}", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed = emb)
    else:
        emb = discord.Embed(title=f"аватар пользователя: \n {member.display_name}", color=member.color)
        emb.set_image(url=member.avatar_url)
        emb.set_footer(text=f"Использовано пользователем: \n {ctx.message.author}", icon_url=ctx.message.author.avatar_url)
        await ctx.send(embed = emb)
        
@client.command(aliases=["server","infoserver","сервер","серв","серверинфо","serv"])
async def serverinfo(ctx):
  name = str(ctx.guild.name)
  description = str(ctx.guild.description)

  owner = str(ctx.guild.owner)
  id = str(ctx.guild.id)
  region = str(ctx.guild.region)
  memberCount = str(ctx.guild.member_count)

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
  emb.add_field(name="Регион:",value=name,inline=True)
  emb.add_field(name="`id:`", value=id,inline=True)
  emb.set_footer(text=f"Использовано пользователем:\n{ctx.message.author}", icon_url=ctx.message.author.avatar_url)
  await ctx.send(embed=emb)
  
@client.command(aliases=["сказать","озв"])
@has_permissions(administrator=True)
async def say(ctx, *,text):
    await ctx.message.delete()
    await ctx.send(text)

#client.run(config.TOKEN)
token = os.environ.get("BOT_TOKEN")     
client.run(str(token))
