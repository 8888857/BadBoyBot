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
    async def _pressure(self, ctx, systo:int, diast:int, puls:int, * , time=None):
        
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

    @commands.command(
        name="сет_ник",
        usage="сет_ник [юзер] [новый ник]",
        description="смена ника",
        aliases=["сетник","сэтник","сэт_ник","setnick","set_nick","nick","ник"]
        )
    async def _set_nick(self, ctx, member:discord.Member, * , new_nick):
        if ctx.author.guild_permissions.manage_nicknames:
            await member.edit(nick=new_nick)
            await ctx.message.add_reaction('✅')
    
    @commands.command(
        name = "кик",
        description = "Кик пользователя",
        aliases = ['kick'],
        usage = "кик [юзер] (причина)"
    )
    @commands.guild_only()
    @commands.has_permissions(kick_members = True)
    async def _kick(self, ctx, member: discord.Member, *, reason = None):
        if member.id == ctx.author.id:
            return await ctx.send(embed = discord.Embed(title = "Вы не можете кикнуть себя", description = "Нет, я конечно всё понимаю, но кикать себя - это уже чересчур", colour = config.COLORS['ERROR']))
        if member.top_role.position >= ctx.author.top_role.position:
            return await ctx.send(embed = discord.Embed(title = "Вы не можете кикнуть этого пользователя", description = f"Пользователь {member.mention} обладает ролью, {'равной' if member.top_role.position == ctx.author.top_role.position else 'выше'} вашей.", colour = config.COLORS['ERROR']))
        await member.kick(reason = f"Кик от пользователя {ctx.author}{'. Причина не указана' if reason is None else ' по причине «' + reason + '»'}")
        await ctx.send(embed = discord.Embed(title = "Успешно", description = f"Пользователь {member} успешно кикнут{'! Причина не указана' if reason is None else ' по причине «' + reason + '»'}", colour = config.COLORS['SUCCESS']))
        await member.send(embed = discord.Embed(description = f"Вы были кикнуты с сервера {ctx.guild.name}{'. Причина кика не указана' if reason is None else ' по причине «' + reason + '»'}", colour = config.COLORS['BASE']))
    
    @commands.command(
        name = "бан",
        description = "Бан пользователя",
        aliases = ['ban'],
        usage = "бан [юзер] (причина)"
    )
    @commands.guild_only()
    @commands.has_permissions(ban_members = True)
    async def _ban(self, ctx, member: discord.Member, *, reason = None):
        if member.id == ctx.author.id:
            return await ctx.send(embed = discord.Embed(title = "Вы не можете забанить себя", description = "Нет, я конечно всё понимаю, но банить себя - это уже чересчур", colour = config.COLORS['ERROR']))
        if member.top_role.position >= ctx.author.top_role.position:
            return await ctx.send(embed = discord.Embed(title = "Вы не можете забанить этого пользователя", description = f"Пользователь {member.mention} обладает ролью, {'равной' if member.top_role.position == ctx.author.top_role.position else 'выше'} вашей.", colour = config.COLORS['ERROR']))
        await member.ban(reason = f"Бан от пользователя {ctx.author}{'. Причина не указана' if reason is None else ' по причине «' + reason + '»'}")    
        await ctx.send(embed = discord.Embed(title = "Успешно", description = f"Пользователь {member} успешно забанен{'! Причина не указана' if reason is None else ' по причине «' + reason + '»'}", colour = config.COLORS['SUCCESS']))
        await member.send(embed = discord.Embed(description = f"Вы были забанены на сервере {ctx.guild.name}{'. Причина бана не указана' if reason is None else ' по причине «' + reason + '»'}", colour = config.COLORS['BASE']))
    
    @commands.command(
        name = "разбан",
        description = "Разбан пользователя",
        aliases = ['unban'],
        usage = "разбан [юзер] (причина)"
    )
    @commands.guild_only()
    @commands.has_permissions(ban_members = True)
    async def _unban(self, ctx, member: discord.User, *, reason = None):
        if member.id == ctx.author.id:
            return await ctx.send(embed = discord.Embed(title = "Вы не можете разбанить себя", description = "Нет, я конечно всё понимаю, но разбанивать себя - очень странно...", colour = config.COLORS['ERROR']))
        if ctx.guild.get_member(member.id) is not None:
            return await ctx.send(embed = discord.Embed(title = "Пользователь не забанен", description = "По-моему нельзя разбанить незабаненного пользователя... Или я что-то путаю?", colour = config.COLORS['ERROR']))
        await ctx.guild.unban(member, reason = f"Разбан от пользователя {ctx.author}{'. Причина не указана' if reason is None else ' по причине «' + reason + '»'}")
        await ctx.send(embed = discord.Embed(title = "Успешно", description = f"Пользователь {member} успешно разбанен{'! Причина не указана' if reason is None else ' по причине «' + reason + '»'}", colour = config.COLORS['SUCCESS']))
    
def setup(client):
    client.add_cog(moder(client))
