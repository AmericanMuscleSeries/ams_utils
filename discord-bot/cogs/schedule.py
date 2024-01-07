import discord
import logging
import utils

from discord import app_commands
from discord.ext import commands


log = logging.getLogger('discord')
_schedule = 'static/data/schedule.json'


class Schedule(commands.Cog):
    def __init__(self, bot):
        log.info(f'{__name__} initializing')
        self.bot = bot
    

    @app_commands.command(description='Get the season schedule.')
    async def schedule(self, interaction: discord.Interaction) -> None:
        schedule = utils.read_json_file(_schedule)
        output = ''.join(f'{schedule[x]["date"]} - {schedule[x]["track"]}\n' for x in schedule)
        await interaction.response.send_message(output[:-1], ephemeral=True)


async def setup(bot):
    await bot.add_cog(Schedule(bot))
