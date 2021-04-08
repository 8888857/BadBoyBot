import discord
from discord.ext import commands
import config

class events(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_error(self, error):
        for owner in self.client.owners:
            await ctx.message.add_reaction("❌")
            await self.client.get_user(owner.id).send(embed=discord.Embed(title="ОШИБКА",description=f"`{type(error)}`\n{error}", colour=config.COLORS['ERROR']))
        raise error

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if type(error) == discord.ext.commands.errors.MissingRequiredArgument:
            await ctx.message.add_reaction("❌")
            return await ctx.send(embed = discord.Embed(title = "Неверно указаны аргументы команды", description = f"Использование команды: {ctx.prefix}{ctx.command.usage}", colour = config.COLORS['ERROR']))
        elif type(error) == discord.ext.commands.errors.CommandInvokeError:
            await ctx.message.add_reaction("❌")
            return await ctx.send(embed = discord.Embed(title = "Неверно указаны аргументы команды", description = f"Использование команды: {ctx.prefix}{ctx.command.usage}", colour = config.COLORS['ERROR']))
        elif type(error) == discord.ext.commands.errors.NotOwner:
            await ctx.message.add_reaction("❌")
            return await ctx.send(embed=discord.Embed(title="ошибка",description=f"{ctx.author.mention}, вы не являетесь овнером бота.\nЭта команда доступна только им",colour=config.COLORS['ERROR']))
        elif type(error) == discord.ext.commands.errors.BadUnionArgument:
            await ctx.message.add_reaction("❌")
            return await ctx.send(embed = discord.Embed(title = "Неверно указаны аргументы команды", description = f"Использование команды: {ctx.prefix}{ctx.command.usage}", colour = config.COLORS['ERROR']))
        elif type(error) == discord.ext.commands.errors.BadArgument:
            await ctx.message.add_reaction("❌")
            return await ctx.send(embed = discord.Embed(title = "Неверно указаны аргументы команды", description = f"Использование команды: {ctx.prefix}{ctx.command.usage}", colour = config.COLORS['ERROR']))
        elif type(error) == discord.ext.commands.errors.CheckFailure:
            await ctx.message.add_reaction("❌")
            return await ctx.send(embed = discord.Embed(title = "Произошла ошибка", description = "У вас недостаточно прав для выполнения данной команды", colour = config.COLORS['ERROR']))
        elif type(error) == discord.ext.commands.errors.CommandOnCooldown:
            await ctx.message.add_reaction("⏳")
            return await ctx.send(embed = discord.Embed(title = "У вас кулдаун на эту команду", description = f"Подождите {round(error.retry_after)} секунд, до тех пор, когда вы сможете использовать команду", colour = config.COLORS['ERROR']))
        elif type(error) == discord.ext.commands.errors.NoPrivateMessage:
            await ctx.message.add_reaction("❌")
            return await ctx.send(embed = discord.Embed(title = "Произошла ошибка", description = "Эту команду можно использовать только на сервере", colour = config.COLORS['ERROR']))
        elif type(error) == discord.ext.commands.errors.MemberNotFound:
            await ctx.message.add_reaction("❌")
            return await ctx.send(embed = discord.Embed(title = "Указанный пользователь не найден", colour = config.COLORS['ERROR']))
        elif type(error) == discord.ext.commands.errors.ChannelNotFound:
            await ctx.message.add_reaction("❌")
            return await ctx.send(embed = discord.Embed(title = "Указанный канал не найден", colour = config.COLORS['ERROR']))
        elif type(error) == discord.ext.commands.errors.RoleNotFound:
            await ctx.message.add_reaction("❌")
            return await ctx.send(embed = discord.Embed(title = "Указанная роль не найдена", colour = config.COLORS['ERROR']))
        elif type(error) == discord.ext.commands.errors.EmojiNotFound:
            await ctx.message.add_reaction("❌")
            return await ctx.send(embed = discord.Embed(title = "Указанный эмоджи не найден", colour = config.COLORS['ERROR']))
        elif type(error) == discord.ext.commands.errors.CommandNotFound:
            return
        elif type(error) == discord.ext.commands.errors.CommandInvokeError and type(error.original) == discord.errors.Forbidden and error.original.text == "Missing Permissions":
            await ctx.message.add_reaction("❌")
            return await ctx.send(embed = discord.Embed(title = "У меня недостаточно прав для выполнения данной команды", description = "Рекомендуется выдать мне права администратора для использования всего функционала бота", colour = config.COLORS['ERROR']))
        elif type(error) == discord.ext.commands.errors.MissingPermissions:
            await ctx.message.add_reaction("❌")
            return await ctx.send(embed = discord.Embed(title = "У вас недостаточно прав для выполнения этой команды", colour = config.COLORS['ERROR']))
        else:
            if ctx.author.id not in [owner.id for owner in self.client.owners]:
                await ctx.message.add_reaction("❌")
                for owner in self.client.owners:
                    if ctx.command is not None:
                        await self.client.get_user(owner.id).send(embed=discord.Embed(description=f"Ошибка в команде `{ctx.command.name}`\n`{type(error)}`\n{error}\nКоманду выполнил {ctx.author}", colour=config.COLORS['ERROR']))
                await ctx.send(embed=discord.Embed(description="Произошла непредвиденная ошибка. Отчёт об ошибке уже отправлен разработчикам. Приносим свои извинения за доставленные неудобства.",colour=config.COLORS['ERROR']))
            else:
                await ctx.message.add_reaction("❌")
                await ctx.send(embed=discord.Embed(description=f"Произошла непредвиденная ошибка\n`{type(error)}`\n{error}",colour=config.COLORS['ERROR']))
            raise error

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        await self.client.get_channel(813511570529320962).send(embed = discord.Embed(title = "Новый сервер!", description = "Бот зашёл на новый сервер!", colour = config.COLORS['SUCCESS']).add_field(name = "Сервер", value = guild.name).add_field(name = "Количество участников", value = len(guild.members)).add_field(name = "Владелец", value = str(guild.owner)).add_field(name = "Шард", value = f"#{guild.shard_id}").set_footer(text=f"{guild.id}").set_thumbnail(url = guild.icon_url))
        servers=len(self.client.guilds)
        users=len(self.client.users)
        await self.client.get_channel(813511570529320962).send(embed=discord.Embed(colour=config.COLORS['BASE']).add_field(name="серверов:",value=servers,inline=False).add_field(name="пользователей:",value=users,inline=False))

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await self.client.get_channel(813511570529320962).send(embed = discord.Embed(title = "-сервер :(", description = "Бот покинул сервер :(", colour = config.COLORS['ERROR']).add_field(name = "Сервер", value = guild.name).add_field(name = "Количество участников", value = len(guild.members)).add_field(name = "Владелец", value = str(guild.owner)).add_field(name = "Шард", value = f"#{guild.shard_id}").set_footer(text=f"{guild.id}").set_thumbnail(url = guild.icon_url))
        servers=len(self.client.guilds)
        users=len(self.client.users)
        await self.client.get_channel(813511570529320962).send(embed=discord.Embed(colour=config.COLORS['BASE']).add_field(name="серверов:",value=servers,inline=False).add_field(name="пользователей:",value=users,inline=False))

def setup(client):
    client.add_cog(events(client))