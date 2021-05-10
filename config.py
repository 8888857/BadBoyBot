import datetime
import discord

prefix = ","

COGS_IGNORE = ['cog.py','narabotki.py']

COLORS = {
    'BASE': 0xFF8000,
    'SUCCESS': 0x80FF00,
    'ERROR': 0xFF0700
}

timeformMSK = " %H:%M %d.%m.%Y ||`UTC(+3:00)`||"

deltaMSK = datetime.timedelta(hours=3)

webhooks = {
    'bot_on': discord.Webhook.partial(823524857118457908,"WLGIkThKQ89Xqcczs7soJt3C9iQu8stCfeL6k88npB2S9N_eKheejLHL4eJ_ZVHt5U57", adapter = discord.RequestsWebhookAdapter()),
    'shard_on': discord.Webhook.partial(823524881139892264, "-qckgNwCgOlqCrZjCQJTNTatH_XTqWT_Ulw0zH1rep-ymDzM0nAG8jemTjGp8NLlXKP5", adapter = discord.RequestsWebhookAdapter()),
    'bot_off': discord.Webhook.partial(823524874513416252,"eLGwHh4OLdjGeDTTvxd9WvPZ2DqEQLfZRXG2TFhBy_P_LWrEzUQ6JYix1IfHZ6lT-3fR", adapter = discord.RequestsWebhookAdapter()),
    'shard_off': discord.Webhook.partial(823524888945098812, "Kg4oKTQSzxrq7foJ0-E1NMrTJH69esLbOl1EWSnOzI-7LDTIZhQMSxzhsKwwBjq_kMsS", adapter = discord.RequestsWebhookAdapter())
}
