import discord
from discord.ext import commands

from models import *

import random

from db_commands import create_or_get_user
from db_commands import update_user_info
from db_commands import delete_user
from db_commands import delete_channel
from db_commands import in_right_channel

class RankingSystem(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot
    
    #adds exp for each message
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message) -> None:
        if message.author.bot:
            return
        
        #checks whether this channel can give XP
        if in_right_channel(message.guild, message.channel) == False:
            return

        person = create_or_get_user(message.author, message.guild)
        new_rank = person.exp

        #25% chance
        if random.randint(1,4)==2:
            new_rank += 1

        update_user_info(person, new_rank)

    #add a person to the db when he join in
    @commands.Cog.listener()
    async def on_member_join(self, member: discord.Member) -> None:
        if not member.bot:
            user = await self.bot.fetch_user(member.id)
            create_or_get_user(user, member.guild)

    #add all users to the database
    @commands.Cog.listener()
    async def on_guild_join(self, guild: discord.Guild) -> None:
        for member in guild.members:
            if not member.bot:
                user = await self.bot.fetch_user(member.id)
                create_or_get_user(user, guild)

    #delete all users and channels from the database if the bot exits
    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild) -> None:
        for member in guild.members:
            user = await self.bot.fetch_user(member.id)
            delete_user(user, member.guild)

        for channel in guild.channels:
            delete_channel(guild, channel)


    #remove a user from the database if he has left the server
    @commands.Cog.listener()
    async def on_member_remove(self, member: discord.Member) -> None:
        user = await self.bot.fetch_user(member.id)
        delete_user(user, member.guild)
        
async def setup(bot):
    await bot.add_cog(RankingSystem(bot))