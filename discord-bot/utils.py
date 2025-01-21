import constants as const
import discord
import json
import logging


log = logging.getLogger('discord')
_users = 'static/data/users.json'


def read_json_file(file_path: str) -> dict:
    log.debug(f'reading json from {file_path}')

    with open(file_path, 'r') as file:
        return json.load(file)


def write_json_file(json_: dict, file_path: str) -> None:
    log.debug(f'writing json to file {file_path}')

    with open(file_path, 'w') as file:
        json.dump(json_, file, indent=4)


async def set_nick(interaction: discord.Interaction, nick: str):
    try:
        await interaction.user.edit(nick=nick[0:32])
    except Exception as e:
        admin_ch = discord.utils.get(interaction.guild.channels, name=const.ADMIN_CH)
        await admin_ch.send(f'Invalid nick entered for {interaction.user.id} ({interaction.user.display_name}): {nick}')
        log.error(f'Invalid nick entered for {interaction.user.id} ({interaction.user.display_name}): {nick}', e)


async def admin_log(guild: discord.Guild, message: str) -> None:
    channel = discord.utils.get(guild.channels, name=const.ADMIN_CH)
    await channel.send(message)


async def update_roster(guild: discord.Guild) -> None:
    channel = discord.utils.get(guild.channels, name=const.INFO_CH)
    msg_id = const.ROSTER_MSG_ID
    drivers = read_json_file(_users)

    if not int(msg_id):
        log.info('initializing roster')
        prompt = await channel.send('roster loading...')
        log.info(f'roster initialized, message {prompt.id}')
        msg_id = prompt.id

    roster = [f'{drivers[d]["num"]} - {drivers[d]["pref_name"]} ({drivers[d]["div"]})' for d in drivers]
    roster.sort(key=lambda d: int(d.split()[0]))
    output = 'Season 8 roster:\n' + ''.join(f'> {entry}\n' for entry in roster) + _get_stats(drivers)
    roster_message = await channel.fetch_message(msg_id)
    await roster_message.edit(content=f'{output}')


def _get_stats(drivers: list) -> str:
    am_div = [drivers[d] for d in drivers if drivers[d]['div'] == 'AM']
    ch_div = [drivers[d] for d in drivers if drivers[d]['div'] == 'CH']
    pro_div = [drivers[d] for d in drivers if drivers[d]['div'] == 'PRO']
    stats = (f'\n**Registration stats:**\n{len(drivers)} drivers registered\n{len(pro_div)} PRO\n'
             f'{len(ch_div)} CH\n{len(am_div)} AM')
    
    return stats
