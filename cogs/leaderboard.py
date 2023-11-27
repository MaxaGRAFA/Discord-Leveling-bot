import discord
from discord.ext import commands
from discord.ui import Button, View

from models import *

import math


class Leaderboard(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot
        self.color = 0xFF5733

    #Show leaderboard
    @commands.command()
    async def leaderboard(self, ctx: commands.Context) -> None:
        page = 1

        embed = self.update_embed(ctx, page)

        async def button_left(interaction: discord.Interaction, page: int):
            if page > 1:
                page = page - 1

            embed = self.update_embed(ctx, page)

            await interaction.response.edit_message(embed=embed)

        async def button_right(interaction: discord.Interaction, page: int):
            user_list = self.get_user_list(ctx)
            max_pages = math.ceil(len(user_list)/5)

            if page < max_pages:
                page = page + 1
        
            embed = self.update_embed(ctx, page)

            await interaction.response.edit_message(embed=embed)

        left = Button(style=discord.ButtonStyle.secondary, emoji='⬅️')
        right = Button(style=discord.ButtonStyle.secondary, emoji='➡️')

        left.callback = lambda i: button_left(i, page)
        right.callback = lambda i: button_right(i, page)

        view = View()
        view.add_item(left)
        view.add_item(right)

        await ctx.send(embed=embed, view=view)

    def update_embed(self, ctx: commands.Context, page: int) -> discord.Embed:
        user_list = self.get_user_list(ctx)
        max_pages = math.ceil(len(user_list)/10)

        embed = discord.Embed(title=f'**Page {page} of {max_pages}**', description=':trophy: Leaderboard', color=self.color)

        start_index = (page-1)*10
        end_index = page * 10

        current_page_users = user_list[start_index:end_index]

        for user in current_page_users:
            embed.add_field(name=f"#{user_list.index(user)+1} {user['name']}", value=f"**Exp:** {user['exp']}| **Level:** {user['level']}", inline=False)

        return embed
    
    def get_user_list(self, ctx: commands.Context) -> list:
        user_list = list(User.select().dicts().where(User.guild_id==ctx.guild.id))
        sorted_list = sorted(user_list, key=lambda x: x['exp'], reverse=True)

        return sorted_list

async def setup(bot):
    await bot.add_cog(Leaderboard(bot))