import discord
import chat_exporter
from discord.ext import commands

intents = discord.Intents.default()
intents.members = True

bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print("Live: " + bot.user.name)
    
@client.command()
async def test(ctx):
    filename = f"{ctx.channel.name}.txt"
    with open(filename, "w") as file:
        async for msg in ctx.channel.history(limit=None):
            file.write(f"{msg.created_at} - {msg.author.display_name}: {msg.clean_content}\n")

@bot.command()
async def save(ctx: commands.Context):
    await chat_exporter.quick_export(ctx.channel)

if __name__ == "__main__":
    bot.run("MTA1NDM2MzM0MjA3ODIyMjQzNw.GpYq14.YpA0lBAgR5fXjt7Z4RWVHexgtk6CL-CEKiBmvM")