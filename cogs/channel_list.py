import discord
from discord.ext import commands
from discord.ui import Button, View

from models import *

import math


class ChannelList(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot
        self.color = 0xFF5733

    @commands.command()
    async def channel_list(self, ctx: commands.Context) -> None:
        page = 1

        embed = self.update_embed(ctx, page)

        async def button_left(interaction: discord.Interaction, page: int):
            if page > 1:
                page = page - 1

            embed = self.update_embed(ctx, page)

            await interaction.response.edit_message(embed=embed)

        async def button_right(interaction: discord.Interaction, page: int):
            channel_list = self.get_channel_list(ctx)
            max_pages = math.ceil(len(channel_list)/5)

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
        channel_list = self.get_channel_list(ctx)
        max_pages = math.ceil(len(channel_list)/10)

        embed = discord.Embed(title=f'**Page {page} of {max_pages}**', description=':closed_book: List of channels where you can get EXP:', color=self.color)

        start_index = (page-1)*10
        end_index = page * 10

        current_page_channels = channel_list[start_index:end_index]

        for channel in current_page_channels:
            embed.add_field(name=channel['name'],value='\n', inline=False)

        return embed

    def get_channel_list(self, ctx: commands.Context) -> list:
        channel_list = list(Channel.select().dicts().where(Channel.guild_id==ctx.guild.id))
        return channel_list
    
async def setup(bot):
    await bot.add_cog(ChannelList(bot))
