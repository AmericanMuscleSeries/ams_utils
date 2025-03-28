import constants as const
import discord
import logging
import os
import utils

from discord.ext import commands
from registration import RegistrationModal
from typing import Literal, Optional


GUILD = const.GUILD
log = logging.getLogger('discord')
intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)
_users = 'static/data/users.json'


@client.event
async def on_ready():
    await load()

    try:
        synced = await client.tree.sync()
        log.info(f'Synced {len(synced)} commands.')
    except Exception as e:
        log.error(e)

    log.info(f'{client.user} is now running!')
    log.info(f'*****CONFIG*****\nLogo: {const.LOGO}\nLog Dir: {const.LOG_DIR}\n'
             f'Admin Channel: {const.ADMIN_CH}\nBroadcaster Role: {const.BROADCAST_ROLE}\n'
             f'Entry Fee: {const.ENTRY_FEE}\nRegistration Open: {const.REG_OPEN}\n'
             f'Reg Open For: {const.REG_OPEN_FOR}\nInfo Channel: {const.INFO_CH}\n'
             f'Points File: {const.POINTS_FILE}\nInclude Drops: {const.INCLUDE_DROPS}')


async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')


@client.tree.command(description='Reload an extension by name. If a name isn\'t given, all extensions are reloaded.')
@commands.is_owner()
async def reload(interaction: discord.Interaction, extension: Optional[str] = '*'):
    if extension == '*':
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await client.reload_extension(f'cogs.{filename[:-3]}')
    else:
        await client.reload_extension(f'cogs.{extension}')
    
    await interaction.response.send_message('Reload complete.', ephemeral=True, delete_after=5)


@client.command()
@commands.guild_only()
@commands.is_owner()
async def sync(ctx: commands.Context, guilds: commands.Greedy[discord.Object], spec: Optional[Literal['~', '*', '^']] = None) -> None:
    if not guilds:
        if spec == '~':
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == '*':
            ctx.bot.tree.copy_global_to(guild=ctx.guild)
            synced = await ctx.bot.tree.sync(guild=ctx.guild)
        elif spec == '^':
            ctx.bot.tree.clear_commands(guild=ctx.guild)
            await ctx.bot.tree.sync(guild=ctx.guild)
            synced = []
        else:
            synced = await ctx.bot.tree.sync()
        
        log.info(f'Synced {len(synced)} commands {"globally" if spec is None else "to current guild."}')

        return
        
    count = 0

    for guild in guilds:
        try:
            await ctx.bot.tree.sync(guild=guild)
        except discord.HTTPException:
            pass
        else:
            count = count + 1
    
    log.info(f'Synced command tree to {count}/{len(guilds)}')
    # try:
    #     synced = await client.tree.sync()
    #     log.info(f'Synced {len(synced)} commands.')
    # except Exception as e:
    #     log.error(e)


@client.tree.command(description='Register for current or upcoming AMS season.')
async def register(interaction: discord.Interaction):
    users = utils.read_json_file(_users)
    user_ = str(interaction.user.id)
    log.info(f'registration attempt by {interaction.user.display_name}')

    if user_ in users:
        log.info(f'{interaction.user.display_name} attempted to register, but is already registered ({users[user_]})')
        await interaction.response.send_message('You are already registered.', ephemeral=True)
    elif const.REG_OPEN:
        if can_register_now(interaction.user):
            await interaction.response.send_modal(RegistrationModal())
        else:
            await interaction.response.send_message(f'Registration is currently only open for season 7 drivers. An announcement will be posted soon '
                                                    f'when registration opens for everyone else.', ephemeral=True)
    else:
        await interaction.response.send_message('I\'m sorry, but registration is currently closed. Please keep an eye out for next season\'s registration.', ephemeral=True)


def can_register_now(user: discord.User) -> bool:
    if const.REG_OPEN_FOR == 'all' or 'season 7' in [role.name for role in user.roles]:
        return True
    else:
        return False


client.remove_command('help')
client.run(const.TOKEN)
