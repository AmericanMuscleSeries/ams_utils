import constants as const
import discord
import logging
import os
import utils

from discord import app_commands
from discord.ext import commands


log = logging.getLogger('discord')
_users = 'static/data/users.json'
_overlay = 'static/data/overlay_roster.csv'
_number = 'static/data/number_roster.csv'


class Broadcast(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        log.info(f'{__name__} initializing')
        self.bot = bot

    
    @app_commands.command(description='Generates a roster for with driver divs, names, and numbers.')
    @commands.has_role(1192260514466762833)
    async def number_roster(self, interaction: discord.Interaction) -> None:
        users = utils.read_json_file(_users)
        roster = [f'({users[user]["div"]}) {users[user]["pref_name"]},{users[user]["num"]}' for user in users]
        roster.sort(key=lambda x: x.split()[1])
        output = ''.join(f'{driver}\n' for driver in roster)[:-1]

        with open(_number, 'w') as file:
            file.write(output)
        
        with open(_number, 'rb') as file:
            await interaction.response.send_message(file=discord.File(file, filename='number_roster.csv'), ephemeral=True)

            if os.path.exists(_number):
                os.remove(_number)
    

    @app_commands.command(description='Generates a roster for loading overlays.')
    @commands.has_role(1192260514466762833)
    async def overlay_roster(self, interaction: discord.Interaction) -> None:
        users = utils.read_json_file(_users)
        output = 'iRacing name,iRacing ID,Multicar team background color,Multicar team text color,Multicar team logo url,iRacing car color override,iRacing car number color override,First name override,Last name override,Suffix override,Initials override,iRacing team name override,Multicar team name,Highlight,Club name override,Photo URL,Number URL,Car Url,Class 1,Class 2,Class 3,Birth date,Home town,Driver header,Driver information\n'

        for user in users:
            user_ = users[user]
            line = ''
            line = line + f'{user_["pref_name"]},{user_["iracing_id"]}'
            line = line + ',Transparent,Transparent,,Transparent,Transparent,'
            tokens = user_['pref_name'].split(maxsplit=2)
            num_tokens = len(tokens)
            line = line + f'{tokens[0]},{tokens[1]},{tokens[2] if num_tokens > 2 else ""}'
            line = line + ',,,,None,None,None,,,'
            line = line + f'{user_["div"]}'
            line = line + ',None,None,,,None,None'
            output = output + line + '\n'
        
        with open(_overlay, 'w') as file:
            file.write(output)
        
        with open(_overlay, 'rb') as file:
            await interaction.response.send_message(file=discord.File(file, filename='ams-driver-overrides.csv'), ephemeral=True)
            
            if os.path.exists(_overlay):
                os.remove(_overlay)
    

    @app_commands.command(description='Generates help menu for broadcast roles.')
    @commands.has_role(1192260514466762833)
    async def help_broadcast(self, interaction: discord.Interaction) -> None:
        file = discord.File('static/img/bot-avatar.png', filename='bot-avatar.png')
        embed = discord.Embed(
            title='Jessica Rabbot Broadcast Commands',
            description='List of usable broadcast commands',
            color=discord.Color.red()
        )
        embed.set_thumbnail(url='attachment://bot-avatar.png')
        embed.add_field(name='/help_broadcast', value='Shows this message', inline=False)
        embed.add_field(name='/number_roster', value='Generates a roster in SDK points format without the points values', inline=False)
        embed.add_field(name='/overlay_roster', value='Generates an overlay roster in SDK format', inline=False)
        await interaction.response.send_message(embed=embed, file=file, ephemeral=True)

    

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Broadcast(bot))
