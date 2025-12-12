import discord
import logging
import utils

from discord import app_commands
from discord.ext import commands


log = logging.getLogger('discord')


class Help(commands.Cog):
    def __init__(self, bot):
        log.info(f'{__name__} initializing')
        self.bot = bot

    
    def get_avatar(self) -> discord.File:
        return discord.File('static/img/bot-avatar.png', filename='bot-avatar.png')
    

    def get_help_embed(self, for_admin: bool = False) -> discord.Embed:
        embed = discord.Embed(
            title='Jessica Rabbot Commands',
            description='List of usable commands',
            color=discord.Color.red()
        )
        embed.set_thumbnail(url='attachment://bot-avatar.png')
        embed.add_field(name='/help', value='Shows this message', inline=False)
        embed.add_field(name='/register', value='Register for current AMS season', inline=False)
        embed.add_field(name='/myinfo', value='Displays your registration info', inline=False)
        embed.add_field(name='/name', value='Alter your preferred name', inline=False)
        embed.add_field(name='/number', value='Claim a number if it is available', inline=False)
        embed.add_field(name='/team', value='Alter your team', inline=False)
        embed.add_field(name='/schedule', value='Display the season schedule', inline=False)
        embed.add_field(name='/next_race', value='Display the track and date of the next race', inline=False)

        if for_admin:
            embed.add_field(name='/helpp', value='Shows help message publicly.', inline=False)
            embed.add_field(name='/help_admin', value='Display message showing admin commands', inline=False)

        return embed
    

    def get_help_admin_embed(self) -> discord.Embed:
        embed = discord.Embed(
            title='Jessica Rabbot Commands',
            description='List of usable commands',
            color=discord.Color.red()
        )
        embed.set_thumbnail(url='attachment://bot-avatar.png')
        embed.add_field(name='/alter_name', value='Alter a driver\'s preferred name', inline=False)
        embed.add_field(name='/alter_team', value='Alter a driver\'s team', inline=False)
        embed.add_field(name='/division', value='Alter a driver\'s division', inline=False)
        embed.add_field(name='/invite', value='Alerts a driver of pending league invite (direct message)', inline=False)
        embed.add_field(name='/payment', value='Marks a driver as paid', inline=False)
        embed.add_field(name='/reginfo', value='Shows a driver\'s registration info', inline=False)
        embed.add_field(name='/registrations', value='Produces all registered drivers\' info (JSON)', inline=False)
        embed.add_field(name='/set_number', value='Sets a driver\'s number', inline=False)


    @app_commands.command(description='Displays the available commands and their uses.')
    async def help(self, interaction: discord.Interaction):
        embed = self.get_help_embed(utils.is_admin(interaction.user.id))
        file = self.get_avatar()
        await interaction.response.send_message(embed=embed, file=file, ephemeral=True)
    

    @app_commands.command(description='Displays the available commands and their uses publicly. (requires permissions)')
    async def helpp(self, interaction: discord.Interaction):
        if not utils.is_admin(interaction.user.id):
            await utils.admonish(interaction)
        else:
            embed = self.get_help_embed(False)
            file = self.get_avatar()
            await interaction.response.send_message(embed=embed, file=file)
    

    @app_commands.command(description='Displays the available admin commands and their uses. (requires permissions)')
    async def help_admin(self, interaction: discord.Interaction):
        if not utils.is_admin(interaction.user.id):
            await utils.admonish(interaction)
        else:
            embed = self.get_help_admin_embed()
            file = self.get_avatar
            await interaction.response.send_message(embed=embed, file=file)


async def setup(bot):
    await bot.add_cog(Help(bot))
