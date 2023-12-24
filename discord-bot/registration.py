import constants as const
import discord
import json
import logging

from discord import utils


log = logging.getLogger('discord')
_users = 'static/data/users.json'
_divs = ['PRO', 'AM']


class RegistrationModal(discord.ui.Modal, title='AMS Registration'):
    _ir_id_ = discord.ui.TextInput(label='iRacing ID', placeholder='123456', required=True, style=discord.TextStyle.short)
    _pref_name_ = discord.ui.TextInput(label='What is your preferred full name?', placeholder='Marty McFly', required=True, style=discord.TextStyle.short)
    _team_ = discord.ui.TextInput(label='What team will you race for? (optional)', placeholder='Privateer', required=False, style=discord.TextStyle.short)
    _loc_ = discord.ui.TextInput(label='Where are you located? (optional)', placeholder='Parts Unknown', required=False, style=discord.TextStyle.short)
    _div_ = discord.ui.TextInput(label='Which division are you entering? (PRO or AM)', placeholder='PRO or AM, IR > 2500 must be PRO', required=True,
                                 style=discord.TextStyle.short)


    def read_users(self):
        log.debug('reading users')

        with open(_users, 'r') as file:
            return json.load(file)


    def write_users(self, users):
        log.debug('writing users')

        with open(_users, 'w') as file:
            json.dump(users, file, indent=4)


    async def on_submit(self, interaction: discord.Interaction):
        users = self.read_users()
        user_ = str(interaction.user.id)

        if user_ in users:
            log.info(f'{interaction.user.display_name} attempted to register, but is already registered ({user_})')
            await interaction.response.send_message('You are already registered.', ephemeral=True)
        else:
            users[user_] = {}
            users[user_]['iracing_id'] = str(self._ir_id_)
            users[user_]['pref_name'] = str(self._pref_name_)
            users[user_]['team'] = str(self._team_)
            users[user_]['loc'] = str(self._loc_)
            users[user_]['div'] = str(self._div_).upper()
            users[user_]['num'] = '0'
            log.info(f'registration received: {users[user_]}')
            self.write_users(users)
            await self.verify_div(str(self._div_), interaction)
            await interaction.response.send_message('You are now registered.', ephemeral=True)
    

    async def verify_div(self, div: str, interaction: discord.Interaction):
        if div.upper() not in _divs:
            admin_ch = utils.get(interaction.guild.channels, name=const.ADMIN_CH)
            await admin_ch.send(f'Invalid division entered for {interaction.user.id} ({interaction.user.display_name}): {div.upper()}')
