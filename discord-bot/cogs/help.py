import discord
import logging

from discord import app_commands
from discord.ext import commands


log = logging.getLogger('discord')


class Help(commands.Cog):
    def __init__(self, bot):
        log.info(f'{__name__} initializing')
        self.bot = bot
    

    @app_commands.command(description='Displays the available commands and their uses.')
    async def help(self, interaction: discord.Interaction):
        file = discord.File('static/img/bot-avatar.png', filename='bot-avatar.png')
        embed = discord.Embed(
            title='Jessica Rabbot Commands',
            description='List of usable commands',
            color=discord.Color.red()
        )
        embed.set_thumbnail(url='attachment://bot-avatar.png')
        embed.add_field(name='/help', value='Shows this message', inline=False)
        embed.add_field(name='/register', value='Register for current or upcoming AMS season', inline=False)
        embed.add_field(name='/myinfo', value='Displays your registration info', inline=False)
        embed.add_field(name='/name', value='Alter your preferred name', inline=False)
        embed.add_field(name='/number', value='Claim a number if it is available', inline=False)
        await interaction.response.send_message(embed=embed, file=file, ephemeral=True)


async def setup(bot):
    await bot.add_cog(Help(bot))
