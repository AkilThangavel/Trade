import discord
import chat_exporter
from discord.ext import commands

bot = commands.Bot(command_prefix="!")


@bot.event
async def on_ready():
    print("Live: " + bot.user.name)
    chat_exporter.init_exporter(bot)