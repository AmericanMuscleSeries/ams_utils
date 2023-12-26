import constants as const
import discord
import json
import logging


log = logging.getLogger('discord')


def read_json_file(file_path: str) -> dict:
    log.debug(f'reading json from {file_path}')

    with open(file_path, 'r') as file:
        return json.load(file)


def write_json_file(json_: dict, file_path: str) -> None:
    log.debug(f'writing json to file {file_path}')

    with open(file_path, 'w') as file:
        json.dump(json_, file, indent=4)


async def set_nick(self, interaction: discord.Interaction, nick: str):
    try:
        await interaction.user.edit(nick=nick)
    except Exception as e:
        admin_ch = discord.utils.get(interaction.guild.channels, name=const.ADMIN_CH)
        await admin_ch.send(f'Invalid nick entered for {interaction.user.id} ({interaction.user.display_name}): {nick}')
        log.error(f'Invalid nick entered for {interaction.user.id} ({interaction.user.display_name}): {nick}', e)
