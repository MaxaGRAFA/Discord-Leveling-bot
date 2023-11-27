from discord.ext import commands
import discord 

import asyncio
import os

import yaml


with open('Configs\config.yml', 'r') as file:
    config = yaml.safe_load(file)



intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.messages = True


bot = commands.Bot(command_prefix=config['Prefix'], intents=intents, help_command=None)


async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await bot.load_extension(f'cogs.{filename[:-3]}')

async def main():
    await load()
    await bot.start(config['Bot_Token'])
    
asyncio.run(main()) 