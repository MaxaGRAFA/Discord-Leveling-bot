import discord
from discord.ext import commands

from db_commands import get_channel
from db_commands import create_channel

class AddChannel(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot

    @commands.command()
    async def add_channel(self, ctx: commands.Context, channel: discord.TextChannel) -> None:

        if get_channel(channel.guild, channel) == None:
            create_channel(channel.guild, channel)
        
        await ctx.message.add_reaction('✅')

async def setup(bot):
    await bot.add_cog(AddChannel(bot))
