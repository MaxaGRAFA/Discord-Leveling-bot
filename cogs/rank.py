import discord
from discord.ext import commands

from easy_pil import Canvas, Editor, Font, load_image

from models import *

from db_commands import create_or_get_user
from db_commands import exp_for_level_up

class rank(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        super().__init__()
        self.bot = bot

   #Show information about user
    @commands.command()
    async def rank(self, ctx: commands.Context, user: discord.User = None) -> None:

        discord_user=ctx.author

        if user is not None:
            discord_user = user

        background = self.rank_card(ctx, discord_user)
        file = discord.File(fp=background.image_bytes, filename='card.png')

        await ctx.send(file=file)

    def rank_card(self, ctx: commands.Context, user: discord.User = None) -> Editor:
        person = create_or_get_user(user, ctx.guild)

        next_level_exp = exp_for_level_up(person.level)

        user_data = {
            'name': user.name,
            'xp': person.exp,
            'next_level_xp': next_level_exp,
            'level': person.level,
            'percentage': ((person.exp/next_level_exp)*100)
        }

        background = Editor(Canvas((900,300), color='#23272A'))

        profile_image= load_image(str(user.avatar.url))
        profile = Editor(profile_image).resize((150, 150)).circle_image()

        poppins = Font.poppins(size=40)
        poppins_small = Font.poppins(size=30)

        card_shape = [(600,0),(750,300),(900,300),(900,0)]

        background.polygon(card_shape, '#2C2F33')
        background.paste(profile, (30,30))

        background.rectangle((30, 220), width=650, height=60, fill='#111111',radius=20)
        background.bar(
            (30,220),
            max_width=650,
            height=60,
            percentage=user_data['percentage'],
            fill='#3db374',
            radius=20)

        background.text((200, 40), user_data['name'], font=poppins, color='white')

        background.rectangle((200,100), width=350,height=2,fill='#17F3F6')
        background.text((200,130),
            f'Level: {user_data["level"]} ' + 
            f'EXP: {user_data["xp"]} / {user_data["next_level_xp"]}',
            font=poppins_small,
            color='white')
        
        return background


async def setup(bot):
    await bot.add_cog(rank(bot))