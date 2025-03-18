import constants as const
import discord
import logging
import os
import standings
import utils

from discord import app_commands
from discord.ext import commands


log = logging.getLogger('discord')
_users = 'static/data/users.json'
_overlay = 'static/data/overlay_roster.csv'
_number = 'static/data/number_roster.csv'
_am_points = 'static/data/ams_am_points.csv'
_ch_points = 'static/data/ams_ch_points.csv'
_pro_points = 'static/data/ams_pro_points.csv'


class Broadcast(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        log.info(f'{__name__} initializing')
        self.bot = bot
    

    async def handle_check_failure(self, interaction: discord.Interaction, 
                                   error: discord.app_commands.AppCommandError) -> None:
        if isinstance(error, app_commands.CheckFailure):
            await interaction.response.send_message('You must be part of the broadcast team to access '
                                                    'this command.', ephemeral=True, delete_after=5)

    
    @app_commands.command(description='Generates a roster for with driver divs, names, and numbers.')    
    @app_commands.checks.has_any_role('broadcast team', 'officials', 'Inner Circle')
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
    

    @number_roster.error
    async def number_roster_error(self, interaction: discord.Interaction, 
                                  error: discord.app_commands.AppCommandError) -> None:
        await self.handle_check_failure(interaction, error)
    

    @app_commands.command(description='Generates a roster for loading overlays.')    
    @app_commands.checks.has_any_role('broadcast team', 'officials', 'Inner Circle')
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
    

    @overlay_roster.error
    async def overlay_roster_error(self, interaction: discord.Interaction, 
                                  error: discord.app_commands.AppCommandError) -> None:
        await self.handle_check_failure(interaction, error)
    

    @app_commands.command(description='Generates a points sheet for each division.')    
    @app_commands.checks.has_any_role('broadcast team', 'officials', 'Inner Circle')
    async def points_roster(self, interaction: discord.Interaction) -> None:
        drivers = utils.read_json_file(_users)
        points = standings.get_points(const.INCLUDE_DROPS)
        headers = 'First name,Last name,Suffix,Multicar team name,Club name,iRacing ID,Car number,Multicar team background color,iRacing car color,iRacing car number color,iRacing car number color 2,iRacing car number color 3,iRacing car number font ID,iRacing car number style,Points before weekend,Points earned,Bonus points,Points after weekend\n'
        lines = []
        
        for driver in drivers:
            driver_ = drivers[driver]
            iracing_id = driver_['iracing_id']
            current_points = points[iracing_id] if iracing_id in points else 0
            line = ''
            tokens = driver_['pref_name'].split(maxsplit=2)
            num_tokens = len(tokens)
            line = line + f'{tokens[0]},{tokens[1]},{tokens[2] if num_tokens > 2 else ""}'
            line = line + f',{driver_["team"]},,{iracing_id},{driver_["num"]}'
            line = line + ',Transparent,Transparent,Transparent,Transparent,Transparent,0,0,0,0,0'
            line = line + f',{current_points}'
            lines.append(line)
        
        lines.sort(key=lambda x: int(x.split(',')[6]))
        pro_points = headers + '\n'.join(line for line in lines if int(line.split(',')[6]) < 100)
        ch_points = headers + '\n'.join(line for line in lines if 100 <= int(line.split(',')[6]) < 200)
        am_points = headers + '\n'.join(line for line in lines if int(line.split(',')[6]) >= 200)

        with open(_am_points, 'w') as file:
            file.write(am_points)
        with open(_ch_points, 'w') as file:
            file.write(ch_points)
        with open(_pro_points, 'w') as file:
            file.write(pro_points)

        points_files_to_read: list[str] = [_am_points, _ch_points, _pro_points]
        files_to_send: list[discord.File] = []

        for filename in points_files_to_read:
            with open(filename, 'rb') as file:
                files_to_send.append(discord.File(file, filename=os.path.basename(file.name)))

        await interaction.response.send_message(files=files_to_send, ephemeral=True)

        if os.path.exists(_am_points):
            os.remove(_am_points)
        if os.path.exists(_ch_points):
            os.remove(_ch_points)
        if os.path.exists(_pro_points):
            os.remove(_pro_points)
    

    @points_roster.error
    async def points_roster_error(self, interaction: discord.Interaction, 
                                  error: discord.app_commands.AppCommandError) -> None:
        await self.handle_check_failure(interaction, error)
    

    @app_commands.command(description='Generates help menu for broadcast roles.')
    @app_commands.checks.has_any_role('broadcast team', 'officials', 'Inner Circle')
    async def help_broadcast(self, interaction: discord.Interaction) -> None:
        file = discord.File('static/img/bot-avatar.png', filename='bot-avatar.png')
        embed = discord.Embed(
            title='Jessica Rabbot Broadcast Commands',
            description='List of usable broadcast commands',
            color=discord.Color.red()
        )
        embed.set_thumbnail(url='attachment://bot-avatar.png')
        embed.add_field(name='/help_broadcast', value='Shows this message', inline=False)
        embed.add_field(name='/number_roster', value='Generates a number roster', inline=False)
        embed.add_field(name='/overlay_roster', value='Generates an overlay roster in SDK format', inline=False)
        embed.add_field(name='/points_roster', value='Generates point sheet in the SDK format for each division', inline=False)
        await interaction.response.send_message(embed=embed, file=file, ephemeral=True)
    

    @help_broadcast.error
    async def help_broadcast_error(self, interaction: discord.Interaction, 
                                  error: discord.app_commands.AppCommandError) -> None:
        await self.handle_check_failure(interaction, error)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Broadcast(bot))
