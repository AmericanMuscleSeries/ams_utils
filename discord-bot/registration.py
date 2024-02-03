import constants as const
import discord
import logging
import utils


log = logging.getLogger('discord')
_users = 'static/data/users.json'
_divs = ['PRO', 'AM']


class RegistrationModal(discord.ui.Modal, title='AMS Registration'):
    _ir_id_ = discord.ui.TextInput(label='iRacing ID', placeholder='123456', required=True, style=discord.TextStyle.short)
    _pref_name_ = discord.ui.TextInput(label='What is your preferred full name?', placeholder='Marty McFly', required=True, style=discord.TextStyle.short)
    _div_ = discord.ui.TextInput(label='Which division are you entering? (PRO or AM)', placeholder='PRO or AM, IR > 2500 must be PRO', required=True,
                                 style=discord.TextStyle.short)
    _team_ = discord.ui.TextInput(label='What team will you race for? (optional)', placeholder='Privateer', required=False, style=discord.TextStyle.short)
    _loc_ = discord.ui.TextInput(label='Where are you located? (optional)', placeholder='Parts Unknown', required=False, style=discord.TextStyle.short)


    async def on_submit(self, interaction: discord.Interaction):
        users = utils.read_json_file(_users)
        user_ = str(interaction.user.id)
        users[user_] = {}
        users[user_]['iracing_id'] = str(self._ir_id_)
        users[user_]['pref_name'] = str(self._pref_name_)
        users[user_]['team'] = str(self._team_)
        users[user_]['loc'] = str(self._loc_)
        users[user_]['div'] = str(self._div_).upper()
        users[user_]['num'] = '0'
        log.info(f'registration received: {users[user_]}')
        await self.verify_div(str(self._div_), interaction)
        await self.set_role(str(self._div_), interaction.user, interaction)
        await utils.set_nick(interaction, str(self._pref_name_))
        utils.write_json_file(users,_users)
        await utils.admin_log(interaction.guild, f'/register called by {interaction.user.name}')
        await interaction.response.send_message(f'You are now registered. Please read the rules in #links-and-info. '
                                                f'You can send your {const.ENTRY_FEE} entry fee to https://paypal.me/finnimcfinger?country.x=US&locale.x=en_US '
                                                f'(friends and family preferred). You can modify your registration details via commands. '
                                                f'Use /help to see available commands.', ephemeral=True)
    

    async def verify_div(self, div: str, interaction: discord.Interaction):
        if div.upper() not in _divs:
            admin_ch = discord.utils.get(interaction.guild.channels, name=const.ADMIN_CH)
            await admin_ch.send(f'Invalid division entered for {interaction.user.id} ({interaction.user.display_name}): {div.upper()}')
    
    
    async def set_role(self, div: str, member: discord.Member, interaction: discord.Interaction):
        for _div in _divs:
            if div.upper() == _div:
                div_role = discord.utils.get(interaction.guild.roles, name=_div)
                await member.add_roles(div_role)
        
        driver_role = discord.utils.get(interaction.guild.roles, name='drivers')
        unpaid_role = discord.utils.get(interaction.guild.roles, name='unpaid')
        await member.add_roles(driver_role, unpaid_role)
