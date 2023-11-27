import discord
from discord.ext import commands

from db_commands import create_or_get_user
from db_commands import update_user_info

class AddRank(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot

    #add rank to user
    @commands.command()
    async def add_rank(self, ctx: commands.Context, discord_user: discord.User, amount: int) -> None:

        if not discord_user:
            await ctx.send('User was not found')
            return

        person = create_or_get_user(discord_user, ctx.guild)
        new_rank = (person.exp + int(amount))

        if new_rank > 900000:
            await ctx.send('The number is too large')
            return

        update_user_info(person, new_rank)

        await ctx.message.add_reaction('✅')

async def setup(bot):
    await bot.add_cog(AddRank(bot))
