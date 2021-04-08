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
            await ctx.reply(embed = discord.Embed(title = f"Чат успешно очищен на {len(cleared) - 1} сообщений модератором {ctx.author}", colour = config.COLORS['SUCCESS']), delete_after = 30)
        else:
            raise discord.ext.commands.errors.CheckFailure
    
    @commands.command(
        name="сет_ник",
        usage="сет_ник (юзер) (новый ник)",
        description="смена ника",
        aliases=["сетник","сэтник","сэт_ник","setnick","set_nick","nick","ник"]
        )
    async def _set_nick(self, ctx, member:discord.Member=None, * , new_nick=None):
        if member == None:
            member = ctx.author
        if new_nick == None:
<<<<<<< HEAD
            return await ctx.reply(embed=discord.Embed(title="Ник:",description=f"**`{member.name}`**",colour=config.COLORS['BASE']))
=======
            return await ctx.send(embed=discord.Embed(title="Ник:",description=f"**`{member.name}`**",colour=config.COLORS['BASE']))
>>>>>>> 59ae30c0b283ff47516f1471a1dc457782f027e9
        if (ctx.author in self.client.owners
        or ctx.author.guild_permissions.manage_nicknames):
            await member.edit(nick=new_nick)
            await ctx.message.add_reaction('✅')
        else:
            raise discord.ext.commands.errors.CheckFailure
    
    @commands.command(
        name = "кик",
        description = "Кик пользователя",
        aliases = ['kick'],
        usage = "кик [юзер] (причина)"
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
        description = "Бан пользователя",
        aliases = ['ban'],
        usage = "бан [юзер] (причина)"
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
        description = "Разбан пользователя",
        aliases = ['unban'],
        usage = "разбан [юзер] (причина)"
    )
    @commands.guild_only()
    @commands.has_permissions(ban_members = True)
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
        description="добавление/удаление ролей",
        aliases=['role','роли','roles']
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
