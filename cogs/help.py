import discord
from discord.ext import commands


class help(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot
        self.color = 0xFF5733

    @commands.command()
    async def help(self, ctx: commands.Context) -> None:
        embed = discord.Embed(title='Available commands',description='Here is the list of commands: \n **help \n rank \n reset_rank {user}\n add_rank {user} {amount} \n leaderboard \n add_channel {channel} \n remove_channel {channel} \n channel_list**', color=self.color)
        await ctx.send(embed=embed)

async def setup(bot):
    await bot.add_cog(help(bot))