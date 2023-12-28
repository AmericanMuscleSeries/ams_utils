import discord
import logging
import utils

from discord import app_commands
from discord.ext import commands


log = logging.getLogger('discord')
_users = 'static/data/users.json'


class RegistrationMod(commands.Cog):
    def __init__(self, bot):
        log.info(f'{__name__} initializing')
        self.bot = bot

    
    def get_user_info(self, member: discord.Member) -> dict:
        users = utils.read_json_file(_users)
        
        if str(member.id) in users:
            return users[str(member.id)]
    

    def get_user_info_embed(self, member: discord.Member) -> discord.Embed:
        user = self.get_user_info(member)
        
        if user:
            embed = discord.Embed(
                title=f'{member.display_name} Registration Info',
                color=discord.Color.red()
            )
            embed.add_field(name='iRacing ID', value=user['iracing_id'], inline=False)
            embed.add_field(name='Preferred Name', value=user['pref_name'], inline=False)
            embed.add_field(name='Team', value=user['team'], inline=False)
            embed.add_field(name='Location', value=user['loc'], inline=False)
            embed.add_field(name='Division', value=user['div'], inline=False)
            embed.add_field(name='Number', value=user['num'], inline=False)
            
            return embed
    

    @app_commands.command(description='Displays your registration info.')
    async def myinfo(self, interaction: discord.Interaction):
        embed = self.get_user_info_embed(interaction.user)

        if embed:
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(f'You are not currently registered. Please use `/register` to register.', ephemeral=True)
    

    @app_commands.command(description='Displays registration info for user. (requires permissions)')
    @app_commands.describe(member='The member for whom to fetch registration info.')
    @app_commands.default_permissions()
    @commands.is_owner()
    async def reginfo(self, interaction: discord.Interaction, member: discord.Member):
        embed = self.get_user_info_embed(member)

        if embed:
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(f'{member.display_name} not found in registered users.', ephemeral=True)
    

    @reginfo.error
    async def reginfo_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            log.warn(f'{ctx.message.author.display_name} attempted `{ctx.message.content}` but lacks permissions.')
        else:
            log.error(f'{ctx.message.author.display_name} attempted `{ctx.message.content}` but something went wrong.\n{error}')
    

    @app_commands.command(description='Set a driver\'s division.  (requires permissions)')
    @app_commands.describe(driver='The driver whose division is to be changed.', division='The division in which to place the driver.')
    @app_commands.default_permissions()
    @commands.is_owner()
    async def division(self, interaction: discord.Interaction, driver: discord.Member, division: str):
        users = utils.read_json_file(_users)
        user = str(driver.id)

        if user in users:
            current_role = discord.utils.get(interaction.guild.roles, name=users[user]['div'])
            new_role = discord.utils.get(interaction.guild.roles, name=division.upper())
            await driver.remove_roles(current_role)
            await driver.add_roles(new_role)
            users[user]['div'] = division.upper()
            utils.write_json_file(users, _users)
            await interaction.response.send_message(f'{driver.display_name} division updated to {division}', ephemeral=True)
        else:
            await interaction.response.send_message(f'{driver.display_name} not registered.', ephemeral=True)

    
    @app_commands.command(description='Alter a driver\'s preferred name. (requires permissions)')
    @app_commands.describe(driver='The driver whose name is to be edited.', name='The driver\'s updated name.')
    @app_commands.default_permissions()
    @commands.is_owner()
    async def alter_name(self, interaction: discord.Interaction, driver: discord.Member, name: str):
        users = utils.read_json_file(_users)
        user_ = str(driver.id)

        if user_ in users:
            users[user_]['pref_name'] = name
            await driver.edit(nick=name)
            utils.write_json_file(users, _users)
            await interaction.response.send_message(f'Driver {driver.id} preferred name updated to {name}.', ephemeral=True)
        else:
            await interaction.response.send_message(f'{driver.display_name} is not registered.', ephemeral=True)
    

    @app_commands.command(description='Alter your preferred name.')
    @app_commands.describe(name='The new preferred name you wish to use.')
    async def name(self, interaction: discord.Interaction, name: str):
        users = utils.read_json_file(_users)
        user_ = str(interaction.user.id)

        if user_ in users:
            users[user_]['pref_name'] = name
            await utils.set_nick(interaction, name)
            utils.write_json_file(users, _users)
            await interaction.response.send_message(f'Your preferred name updated to {name}.', ephemeral=True)
        else:
            await interaction.response.send_message('You are not registered. Use the /register command if you wish to drive in the league.', ephemeral=True)
    

    @app_commands.command(description='Claim a number if it is available.')
    @app_commands.describe(number='The number you wish to claim. PRO numbers run from 2-99 (leading 0s are OK). AM numbers run from 100-199.')
    async def number(self, interaction: discord.Interaction, number: str):
        try:
            int(number)
        except ValueError as e:
            interaction.response.send_message(f'{number} is not a valid number. Please run the command again with a number. '
                                              f'PRO numbers run from 2-99 (leading 0s are OK). AM numbers run from 100-199.',
                                              ephemeral=True)
        
        driver = self.get_user_info(interaction.user)

        if driver:
            if driver['div'] == 'PRO' and not 1 < int(number) < 100:
                await interaction.response.send_message(f'{number} is not valid for you. PRO numbers run from 2-99. Leading 0s are ok.', ephemeral=True)
            elif driver['div'] == 'AM' and not 100 <= int(number) < 200:
                await interaction.response.send_message(f'{number} is not valid for you. AM numbers run from 100-199.', ephemeral=True)
            else:
                users = utils.read_json_file(_users)

                for id in users:
                    user = users[str(id)]

                    if int(id) == interaction.user.id and user['num'] == number:
                        await interaction.response.send_message('You already have that number.', ephemeral= True)
                        return
                    else:
                        leading_zero_change = True
                    
                    if int(user['num']) == int(number) and not leading_zero_change:
                        await interaction.response.send_message(f'Sorry, that number is already taken. Please run the command again with another number.',ephemeral=True)
                        return
                
                users[str(interaction.user.id)]['num'] = number[-2:] if users[str(interaction.user.id)]['div'] == 'PRO' else number[-3:]
                
                utils.write_json_file(users, _users)

                await interaction.response.send_message(f'Your number has been set to {number}.', ephemeral=True)
    

    @app_commands.command(description='Process a driver\'s payment. (requires permissions)')
    @app_commands.describe(driver='The driver whose pamyent is to be processed.')
    @app_commands.default_permissions()
    @commands.is_owner()
    async def payment(self, interaction: discord.Interaction, driver: discord.Member):
        unpaid = discord.utils.get(interaction.guild.roles, name='unpaid')
        await driver.remove_roles(unpaid)
        await interaction.response.send_message(f'Payment processed for {driver.display_name}.', ephemeral=True)
    

    @app_commands.command(description='Download registered drivers. (requires permissions)')
    @app_commands.default_permissions()
    @commands.is_owner()
    async def registrations(self, interaction: discord.Interaction):
        file = discord.File(_users, filename='registrations.json')
        await interaction.response.send_message(file=file, ephemeral=True)
    

    @app_commands.command(description='Change the team for which you are driving.')
    @app_commands.describe(team='The team to which you want to change.')
    async def team(self, interaction: discord.Interaction, team: str):
        users = utils.read_json_file(_users)
        user_ = str(interaction.user.id)

        if user_ in users:
            users[user_]['team'] = team
            utils.write_json_file(users, _users)
            await interaction.response.send_message(f'Your team name has been changed to {team}.', ephemeral=True)
        else:
            await interaction.response.send_message(f'You are not currently registered. Please use the `/register` command to register if you wish to drive.',
                                                    ephemeral=True)
    

    @app_commands.command(description='Change the team of a driver. (requires permission)')
    @app_commands.describe(driver='The driver whose team to change.', team='The team to assign to the driver.')
    @app_commands.default_permissions()
    @commands.is_owner()
    async def alter_team(self, interaction: discord.Interaction, driver: discord.Member, team: str):
        users = utils.read_json_file(_users)
        user_ = str(driver.id)

        if user_ in users:
            users[user_]['team'] = team
            utils.write_json_file(users, _users)
            await interaction.response.send_message(f'{driver.display_name}\'s team changed to {team}.', ephemeral=True, delete_after=5)
        else:
            await interaction.response.send_message(f'{driver.display_name} ({driver.id}) is not registered.', ephemeral=True, delete_after=5)


async def setup(bot):
    await bot.add_cog(RegistrationMod(bot))
