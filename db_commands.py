import discord

from models import *

#
#this is a file with commands that interact with the database
#


def get_channel(guild: discord.Guild, channel: discord.TextChannel) -> Channel:
    return Channel.get_or_none((Channel.id==channel.id) & (Channel.guild_id == guild.id))

def create_channel(guild: discord.Guild, channel: discord.TextChannel) -> None:
    Channel.create(id=channel.id, guild_id=guild.id, name=channel.name)

def delete_channel(guild: discord.Guild, channel: discord.TextChannel) -> None:
    channel = get_channel(guild, channel)
    if channel != None:
        channel.delete_instance()

def in_right_channel(guild: discord.Guild, channel: discord.TextChannel) -> bool:
    if get_channel(guild, channel) is None:
        return False


#create a new user or get an existing one
def create_or_get_user(user: discord.User = None, guild: discord.Guild = None) -> User:

    if user is None or guild is None:
        return
    
    person, _ = User.get_or_create(
        guild_id=guild.id,
        id=user.id,
        defaults={'name':user.name, 'exp':0, 'level':0}
    )        

    return person

#delete user from db
def delete_user(user: discord.User, guild: discord.Guild) -> None:
    person = create_or_get_user(user, guild)
    person.delete_instance()

#updating information in the database
def update_user_info(person: User , rank:int) -> None:

    level = level_up(rank, person.level)
    
    (User.update({User.exp: rank, User.level: level}).where((User.id==person.id) & (User.guild_id==person.guild_id))).execute()

#Level up if necessary
def level_up(exp: int, level: int) -> int:
    while ((level*220) + 5) - exp <= 0:
        level += 1
    return level

#reset user info
def reset_user(person: User) -> None:
    (User.update({User.exp: 0, User.level: 0}).where((User.id==person.id) & (User.guild_id==person.guild_id))).execute()

#Calculation of how much exp is needed for the next level
def exp_for_level_up(level:int) -> int:
    return ((level*220) + 5)