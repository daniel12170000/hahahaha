import discord
import asyncio
import os
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv


load_dotenv()
token = os.getenv('TOKEN')

intents = discord.Intents.default()
intents.message_content = True 
intents.guild_messages = True

bot = commands.Bot(command_prefix='!', intents=intents)
async def load_extensions():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

@bot.command()
async def sync(ctx):
    bot.tree.copy_global_to(guild = ctx.guild)
    synced = await bot.tree.sync(guild = ctx.guild)
    await ctx.send("synced")

@bot.event
async def on_ready():
    print(f"{bot.user} logged in!")
    
async def main():
    async with bot:
        await load_extensions()
        await bot.start(token)

if __name__ == '__main__':
    asyncio.run(main())
