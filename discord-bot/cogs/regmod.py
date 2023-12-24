import discord
import json
import logging

from discord import app_commands
from discord.ext import commands


log = logging.getLogger('discord')
_users = 'static/data/users.json'


class RegistrationMod(commands.Cog):
    def __init__(self, bot):
        log.info(f'{__name__} initializing')
        self.bot = bot

    
    def get_user_info(self, member: discord.Member) -> dict:
        with open(_users, 'r') as file:
            users = json.load(file)
        
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
    

    @app_commands.command(description='Claim a number if it is available.')
    @app_commands.describe(number='The number you wish to claim. PRO numbers run from 2-99 (leading 0s are OK). AM numbers run from 100-199.')
    async def number(self, interaction: discord.Interaction, number: int):
        try:
            int(number)
        except ValueError as e:
            interaction.response.send_message(f'{number} is not a valid number. Please run the command again with a number. '
                                              f'PRO numbers run from 2-99 (leading 0s are OK). AM numbers run from 100-199.',
                                              ephemeral=True)
        
        user = self.get_user_info(interaction.user)

        if user:
            if user['div'] == 'PRO' and not 1 < int(number) < 100:
                await interaction.response.send_message(f'{number} is not valid for you. PRO numbers run from 2-99. Leading 0s are ok.', ephemeral=True)
            elif user['div'] == 'AM' and not 100 <= int(number) < 200:
                await interaction.response.send_message(f'{number} is not valid for you. AM numbers run from 100-199.', ephemeral=True)
            else:
                with open(_users, 'r') as file:
                    users = json.load(file)

                for id in users:
                    u = users[str(id)]

                    if int(u['num']) == int(number):
                        if int(id) == interaction.user.id:
                            await interaction.response.send_message('You already have that number.', ephemeral= True)
                        else:
                            await interaction.response.send_message(f'Sorry, that number is already taken. Please run the command again with another number.',
                                                                    ephemeral=True)
                        
                        return
                
                users[str(interaction.user.id)]['num'] = str(number)[-2:] if users[str(interaction.user.id)]['div'] == 'PRO' else str(number)[-3:]
                
                with open(_users, 'w') as file:
                    json.dump(users, file, indent=4)
                
                await interaction.response.send_message(f'Your number has been set to {number}.', ephemeral=True)



async def setup(bot):
    await bot.add_cog(RegistrationMod(bot))
