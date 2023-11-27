import discord
from discord.ext import commands

from models import *

from db_commands import create_or_get_user
from db_commands import reset_user

class ResetRank(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot

    @commands.command()
    async def reset_rank(self, ctx: commands.Context, discord_user: discord.User = None) -> None:
        if discord_user is None:
            await ctx.send('User was not found')
            return    
        
        person = create_or_get_user(discord_user, ctx.guild)

        reset_user(person)

        await ctx.message.add_reaction('✅')

    

async def setup(bot):
    await bot.add_cog(ResetRank(bot))