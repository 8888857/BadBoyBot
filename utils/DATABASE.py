import pymongo
import config
import discord
from discord.ext import commands



client = pymongo.MongoClient(f"mongodb://{config.DB['user']}:{config.DB['password']}@{config.DB['host']}:{config.DB['port']}/{config.DB['database']}")
db = client[config.DB['database']]

#user_prefix = db['user']
guild_prefix = db['guild']
user_premium = db['user']
guild_premium = db['guild']
access_lvl = db['user']





class Get:
    def __init__(self, ctx = None):
        self.ctx = ctx
        
    def prefix(self, bot: commands.Bot, message: discord.Message):
        if message.guild is not None:
            prefixes = guild_prefix

            prefix = prefixes.find_one({"guild_id": message.guild.id})
            
            if prefix is None:
                prefixes.insert_one({"guild_id": message.guild.id, "prefix": ","})
                prefix = ","
            else:
                prefix = prefix['prefix']


            if bot is not None:
                return commands.when_mentioned_or(prefix,"Бэд", "Бэд ", "бэд ", "бед ", "бед ", "бэд","бед","bad ","Bad","Bad ","bad")(bot, message)
            else:
                return prefix
        else:
            if bot is not None:
                return commands.when_mentioned_or(",",", ","Бэд", "Бэд ", "бэд ", "бед ", "бед ", "бэд","бед","bad ","Bad","Bad ","bad")(bot, message)
            else:
                return ","


class Set:
    def __init__(self, ctx = None):
        self.ctx = ctx
        
    def prefix(self, prefix: str):
        try:
            prefixes = guild_prefix
            prefixes.update_one({"guild_id": self.ctx.guild.id}, {"$set": {"prefix": prefix}})
            return True
        except Exception as e:
            print(e)
            return False
        
class Delete:
    def __init__(self, ctx):
        self.ctx = ctx