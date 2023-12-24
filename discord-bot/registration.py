import discord
import json
import logging


log = logging.getLogger('discord')
_users = 'static/data/users.json'


class RegistrationModal(discord.ui.Modal, title='AMS Registration'):
    _ir_id_ = discord.ui.TextInput(label='iRacing ID', placeholder='123456', required=True, style=discord.TextStyle.short)
    _pref_name_ = discord.ui.TextInput(label='What name will you race under? (Preferred Full Name)', placeholder='Marty McFly', required=True, style=discord.TextStyle.short)
    _team_ = discord.ui.TextInput(label='What team will you race for? (optional)', placeholder='Privateer', required=False, style=discord.TextStyle.short)
    _loc_ = discord.ui.TextInput(label='Where are you located? (optional)', placeholder='Parts Unknown', required=False, style=discord.TextStyle.short)


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
            log.info(f'registration received: {users[user_]}')
            self.write_users(users)
            await interaction.response.send_message('You are now registered.', ephemeral=True)
