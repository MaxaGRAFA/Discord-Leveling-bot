import discord
from discord.ext import commands

from db_commands import delete_channel

class RemoveChannel(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot

    @commands.command()
    async def remove_channel(self, ctx: commands.Context, channel: discord.TextChannel) -> None:
        delete_channel(channel.guild, channel)
        await ctx.message.add_reaction('✅')

async def setup(bot):
    await bot.add_cog(RemoveChannel(bot))
