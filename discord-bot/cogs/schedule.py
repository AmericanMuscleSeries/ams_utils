import discord
import logging
import utils

from datetime import datetime
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
    

    @app_commands.command(description='Get the next race.')
    async def next_race(self, interaction: discord.Interaction) -> None:
        schedule = utils.read_json_file(_schedule)
        output = str()

        for race in schedule:
            race_dt = datetime.strptime(schedule[race]['date'])
            
            if datetime.today() <= race_dt:
                output = f'Next race is {schedule[race]["track"]} on {schedule[race]["date"]}'
                break
        
        if len(output) == 0:
            output = 'The season is over. There are no more races. :face_holding_back_tears:'
        
        await interaction.response.send_message(output, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Schedule(bot))
