import constants as const
import discord
import json
import logging

from discord.ext import commands


log = logging.getLogger('discord')


class RegistrationMod(commands.Cog):
    def __init__(self, bot):
        log.info(f'{__name__} initializing')
        self.bot = bot


async def setup(bot):
    await bot.add_cog(RegistrationMod(bot))
