import constants as const
import discord
import logging

from discord import app_commands
from registration import RegistrationModal


TOKEN = const.TOKEN
GUILD = const.GUILD
log = logging.getLogger('discord')
intents = discord.Intents.all()
client = discord.Client(command_prefix='!', intents=intents)
tree = app_commands.CommandTree(client)


@client.event
async def on_ready():
    tree.copy_global_to(guild=discord.Object(id=GUILD))
    await tree.sync(guild=discord.Object(id=GUILD))
    log.info(f'{client.user} is now running!')


@tree.command(description='Register for current or upcoming AMS season.')
async def register(interaction: discord.Interaction):
    await interaction.response.send_modal(RegistrationModal())


client.run(TOKEN)
