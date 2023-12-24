import constants as const
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
    

    @app_commands.command(description='Displays registration info for user.')
    @app_commands.describe(member='The member for whom to fetch registration info.')
    @commands.is_owner()
    async def reginfo(self, interaction: discord.Interaction, member: discord.Member):
        with open(_users, 'r') as file:
            users = json.load(file)
        
        if str(member.id) in users:
            user = users[str(member.id)]
            embed = discord.Embed(
                title=f'{member.display_name} Registration Info',
                color=discord.Color.red()
            )
            embed.add_field(name='iRacing ID', value=user['iracing_id'], inline=False)
            embed.add_field(name='Preferred Name', value=user['pref_name'], inline=False)
            embed.add_field(name='Team', value=user['team'], inline=False)
            embed.add_field(name='Location', value=user['loc'], inline=False)
            embed.add_field(name='Division', value=user['div'], inline=False)
            await interaction.response.send_message(embed=embed, ephemeral=True)
        else:
            await interaction.response.send_message(f'{member.display_name} not found in registered users.', ephemeral=True)
    

    @reginfo.error
    async def reginfo_error(self, ctx, error):
        if isinstance(error, commands.CheckFailure):
            log.warn(f'{ctx.message.author.display_name} attempted `{ctx.message.content}` but lacks permissions.')
        else:
            log.error(f'{ctx.message.author.display_name} attempted `{ctx.message.content}` but something went wrong.\n{error}')


async def setup(bot):
    await bot.add_cog(RegistrationMod(bot))
