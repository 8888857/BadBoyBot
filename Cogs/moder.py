import discord
from discord.ext import commands
from discord.ext.commands import has_permissions
import config
import re
import typing
import datetime
from config import timeformMSK
from config import deltaMSK
from utils import DATABASE as DB

class moder(commands.Cog, name = "Модерация"):
    """Модерационные комманды:"""
    def __init__(self, client):
        self.client = client

    @commands.command(
        name = "префикс",
        brief = "Установка префикса бота на сервере",
        aliases = ['prefix'],
        usage = "префикс (новый префикс)",
        description="• префикс\n• префикс -_-"
    )
    @commands.guild_only()
    @commands.has_permissions(administrator = True)
    async def _prefix(Self, ctx, *, new_prefix = None):
        if new_prefix is None:
            current_prefix = DB.Get(ctx).prefix(None, ctx.message)
            return await ctx.reply(embed = discord.Embed(title = "Настройка префикса", description = f"Текущий префикс бота на сервере - `{current_prefix}` Чтобы изменить его, воспользуйтесь командой {current_prefix}префикс <новый префикс>", colour = config.COLORS['BASE']))
        else:
            if ctx.prefix == new_prefix:
                return await ctx.reply(embed=discord.Embed(title="ошибка",description="префикс не должен совпадать с нынешним префиксом.",colour=config.COLORS['ERROR']))
            if ' ' in new_prefix:
                return await ctx.reply(embed = discord.Embed(title = "Ошибка при обновлении префикса", description = "Префикс не должен содержать пробелы", colour = config.COLORS['ERROR']))
            if len(new_prefix) > 5:
                return await ctx.reply(embed = discord.Embed(title = "Ошибка при обновлении префикса", description = "Префикс не должен быть длиннее 4 символов", colour = config.COLORS['ERROR']))
            if DB.Set(ctx).prefix(new_prefix):
                return await ctx.reply(embed = discord.Embed(title = "Префикс успешно изменён", description = f"Теперь префикс бота на этом сервере - `{new_prefix}`", colour = config.COLORS['SUCCESS']))
            else:
                return await ctx.reply(embed = discord.Embed(title = "Ошибка при обновлении префикса", description = "Произошла непредвиденная ошибка при обновлении префикса. Повторите попытку позже", colour = config.COLORS['ERROR']))

    @commands.command(
        name = "очистить",
        brief = "Очистка чата",
        aliases = ['clear','чистка','отчистка','отчистить'],
        usage = "очистить [количество сообщений] (канал)",
        description="• очистить 100\n• очистить 100 #новости"
    )
    @commands.guild_only()
    async def _clear(self, ctx, amount: int, channel: discord.TextChannel = None):
        print(channel)
        if channel is None: channel = ctx.channel
        if (ctx.author in self.client.owners
        or channel.permissions_for(ctx.author).manage_messages):
            if ctx.author in self.client.owners:
                if amount > 9999999999999999999:
                    return await ctx.reply(embed = discord.Embed(title = "Ошибка очистки чата", description = "ты даун что ли? куда тебе столько", colour = config.COLORS['ERROR']))
            if ctx.author.id in self.client.premium_u:
                if amount > 5000:
                    return await ctx.reply(embed = discord.Embed(title = "Ошибка очистки чата", description = "имея **DEFAULT PREMIUM**\nНельзя очистить больше 5000 сообщений за раз", colour = config.COLORS['ERROR']))
            else:
                if amount > 500:
                    return await ctx.reply(embed = discord.Embed(title = "Ошибка очистки чата", description = "не имея premium\nНельзя очистить больше 500 сообщений за раз", colour = config.COLORS['ERROR']))
            if amount <= 0:
                return await ctx.reply(embed = discord.Embed(title = "Ошибка очистки чата", description = "Очищать чат на неположительное количество сообщений? Плохая идея...", colour = config.COLORS['ERROR']))
            cleared = await channel.purge(limit = (amount + 1) if channel == ctx.channel else amount)
            await ctx.send(embed = discord.Embed(title = "Успешно", colour = config.COLORS['SUCCESS']).add_field(name="Очищено:",value=f"{len(cleared) - 1} сообщение(ий)").add_field(name="Модератором:",value=f"{ctx.author.mention}"),delete_after = 15)
        else:
            raise discord.ext.commands.errors.CheckFailure
    
    @commands.command(
        name="сет_ник",
        usage="сет_ник (юзер) (новый ник)",
        brief="смена ника",
        aliases=["сетник","сэтник","сэт_ник","setnick","set_nick","nick","ник"],
        description="• сет_ник\n• сет_ник @BadBoyBot#2997 БэДБойБоТиК"
        )
    async def _set_nick(self, ctx, member:discord.Member=None, * , new_nick=None):
        if member == None:
            member = ctx.author
        if new_nick == None:
            return await ctx.reply(embed=discord.Embed(title="Ник:",description=f"**`{member.name}`**",colour=config.COLORS['BASE']))
        if (ctx.author in self.client.owners
        or ctx.author.guild_permissions.manage_nicknames):
            await member.edit(nick=new_nick)
            await ctx.message.add_reaction('✅')
        else:
            raise discord.ext.commands.errors.CheckFailure
    
    @commands.command(
        name = "кик",
        brief = "Кик пользователя",
        aliases = ['kick'],
        usage = "кик [юзер] (причина)",
        description="• кик @BadBoyBot#2997\n• кик @BadBoyBot#2997 веская причина"
    )
    @commands.guild_only()
    async def _kick(self, ctx, member: discord.Member, *, reason = None):
        if (ctx.author in self.client.owners
        or ctx.author.guild_permissions.kick_members):
            if member.id == ctx.author.id:
                return await ctx.reply(embed = discord.Embed(title = "Вы не можете кикнуть себя", description = "Нет, я конечно всё понимаю, но кикать себя - это уже чересчур", colour = config.COLORS['ERROR']))
            if member.top_role.position >= ctx.author.top_role.position:
                return await ctx.reply(embed = discord.Embed(title = "Вы не можете кикнуть этого пользователя", description = f"Пользователь {member.mention} обладает ролью, {'равной' if member.top_role.position == ctx.author.top_role.position else 'выше'} вашей.", colour = config.COLORS['ERROR']))
            await member.kick(reason = f"Кик от пользователя {ctx.author}{'. Причина не указана' if reason is None else ' по причине «' + reason + '»'}")
            await ctx.reply(embed = discord.Embed(title = "Успешно", description = f"Пользователь {member} успешно кикнут{'! Причина не указана' if reason is None else ' по причине «' + reason + '»'}", colour = config.COLORS['SUCCESS']))
            await member.send(embed = discord.Embed(description = f"Вы были кикнуты с сервера {ctx.guild.name}{'. Причина кика не указана' if reason is None else ' по причине «' + reason + '»'}", colour = config.COLORS['BASE']))
        else:
            raise discord.ext.commands.errors.CheckFailure
    
    @commands.command(
        name = "бан",
        brief = "Бан пользователя",
        aliases = ['ban'],
        usage = "бан [юзер] (причина)",
        description="• бан @BadBoyBot#2997\n• бан @BadBoyBot#2997 веская причина"
    )
    @commands.guild_only()
    async def _ban(self, ctx, member: discord.Member, *, reason = None):
        if (ctx.author in self.client.owners
        or ctx.author.guild_permissions.ban_members):
            if member.id == ctx.author.id:
                return await ctx.reply(embed = discord.Embed(title = "Вы не можете забанить себя", description = "Нет, я конечно всё понимаю, но банить себя - это уже чересчур", colour = config.COLORS['ERROR']))
            if member.top_role.position >= ctx.author.top_role.position:
                return await ctx.reply(embed = discord.Embed(title = "Вы не можете забанить этого пользователя", description = f"Пользователь {member.mention} обладает ролью, {'равной' if member.top_role.position == ctx.author.top_role.position else 'выше'} вашей.", colour = config.COLORS['ERROR']))
            await member.ban(reason = f"Бан от пользователя {ctx.author}{'. Причина не указана' if reason is None else ' по причине «' + reason + '»'}")    
            await ctx.reply(embed = discord.Embed(title = "Успешно", description = f"Пользователь {member} успешно забанен{'! Причина не указана' if reason is None else ' по причине «' + reason + '»'}", colour = config.COLORS['SUCCESS']))
            await member.send(embed = discord.Embed(description = f"Вы были забанены на сервере {ctx.guild.name}{'. Причина бана не указана' if reason is None else ' по причине «' + reason + '»'}", colour = config.COLORS['BASE']))
        else:
            raise discord.ext.commands.errors.CheckFailure
    
    @commands.command(
        name = "разбан",
        brief = "Разбан пользователя",
        aliases = ['unban'],
        usage = "разбан [юзер] (причина)",
        description="• разбан @BadBoyBot#2997\n• разбан @BadBoyBot#2997 веская причина"
    )
    @commands.guild_only()
    async def _unban(self, ctx, member: discord.User, *, reason = None):
        if (ctx.author in self.client.owners
        or ctx.author.guild_permissions.ban_members):
            if member.id == ctx.author.id:
                return await ctx.reply(embed = discord.Embed(title = "Вы не можете разбанить себя", description = "Нет, я конечно всё понимаю, но разбанивать себя - очень странно...", colour = config.COLORS['ERROR']))
            if ctx.guild.get_member(member.id) is not None:
                return await ctx.reply(embed = discord.Embed(title = "Пользователь не забанен", description = "По-моему нельзя разбанить незабаненного пользователя... Или я что-то путаю?", colour = config.COLORS['ERROR']))
            await ctx.guild.unban(member, reason = f"Разбан от пользователя {ctx.author}{'. Причина не указана' if reason is None else ' по причине «' + reason + '»'}")
            await ctx.reply(embed = discord.Embed(title = "Успешно", description = f"Пользователь {member} успешно разбанен{'! Причина не указана' if reason is None else ' по причине «' + reason + '»'}", colour = config.COLORS['SUCCESS']))
        else:
            raise discord.ext.commands.errors.CheckFailure
    
    @commands.command(
        name="роль",
        usage="роль [юзер] [+/-|добавить/удалить] [роль] (причина)",
        brief="добавление/удаление ролей",
        aliases=['role','роли','roles'],
        description="• роль @BadBoyBot#2997 + @супер_пупер_роль\n• роль @BadBoyBot#2997 - @супер_пупер_роль\n• роль @BadBoyBot#2997 добавить @супер_пупер_роль супер причина :>"
        )
    async def _role(self, ctx, member:discord.Member, act, role:discord.Role, * ,reason=None):
        if act in ['+','-','удалить','добавить','delete','add']:
            if (ctx.author in self.client.owners
            or ctx.author.guild_permissions.manage_roles):
                if member.top_role.position > ctx.author.top_role.position:
                    return await ctx.reply(embed = discord.Embed(title = "Вы не можете изменять роли этого пользователя", description = f"Пользователь {member.mention} обладает ролью выше вашей.", colour = config.COLORS['ERROR']))
                if role == None:
                    return await ctx.reply(embed=discord.Embed(title='ошибка',description="пожалуйста введите роль которую нужно добавить/удалить",colour=config.COLORS['ERROR']))
                else:
                    if reason == None:
                        reas=f"неуказана\n{ctx.author.name} изменил роли юзеру {member.name}"
                    if reason != None:
                        reas=f"«{reason}»\n{ctx.author.name} изменил роли юзеру {member.name}"
                    if act in ['+','добавить','add']:
                        await member.add_roles(role,reason=reas)
                        await ctx.message.add_reaction('✅')
                        await ctx.reply(embed=discord.Embed(description=f"роли {member.mention} были изменены.\n{role.mention} была добавлена.",colour=config.COLORS['SUCCESS']))
                    if act in ['-','удалить','delete']:
                        await member.remove_roles(role,reason=reas)
                        await ctx.message.add_reaction('✅')
                        await ctx.reply(embed=discord.Embed(description=f"роли {member.mention} были изменены.\n{role.mention} была удалена.",colour=config.COLORS['SUCCESS']))
            else:
                raise discord.ext.commands.errors.CheckFailure
        else:
            raise discord.ext.commands.errors.MissingRequiredArgument
    
def setup(client):
    client.add_cog(moder(client))
