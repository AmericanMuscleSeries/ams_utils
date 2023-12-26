import constants as const
import discord
import logging
import os

from datetime import datetime
from discord.ext import commands
from registration import RegistrationModal
from typing import Optional


GUILD = const.GUILD
log = logging.getLogger('discord')
intents = discord.Intents.all()
client = commands.Bot(command_prefix='!', intents=intents)


@client.event
async def on_ready():
    await load()
    log.info(f'{client.user} is now running!')


async def load():
    for filename in os.listdir('./cogs'):
        if filename.endswith('.py'):
            await client.load_extension(f'cogs.{filename[:-3]}')


@client.tree.command()
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
async def sync(ctx):
    ctx.bot.tree.copy_global_to(guild=ctx.guild)
    synced = await ctx.bot.tree.sync(guild=ctx.guild)
    log.info(f'{len(synced)} commands synced')


@client.tree.command(description='Register for current or upcoming AMS season.')
async def register(interaction: discord.Interaction):
    await interaction.response.send_modal(RegistrationModal())


@client.tree.command(description='Clear messages from this channel.')
@commands.is_owner()
async def clear(interaction: discord.Interaction, amount: str, month: int = None, day: int = None, year: int = None):
    limit = int(amount) + 1 if amount.isdigit() else None
    has_date = month is not None and day is not None and year is not None
    date = datetime(year, month, day) if has_date else None
    await interaction.channel.purge(limit=limit, after=date)
    await interaction.response.send_message('Clear done.', ephemeral=True, delete_after=5)


client.remove_command('help')
client.run(const.TOKEN)
