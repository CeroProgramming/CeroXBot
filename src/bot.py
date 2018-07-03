from modules.base import Base
from modules.admin import Admin
from modules.channel import Channel
from modules.info import Info
from modules.misc import Misc
from modules.user import User


from discord import Client
from logging import basicConfig, getLogger, FileHandler, Formatter, CRITICAL, ERROR, WARNING, INFO, DEBUG



logger = getLogger('discord')
logger.setLevel(INFO)
logpath = 'logs/discord.log'
handler = FileHandler(filename=logpath, encoding='utf-8', mode='w')
handler.setFormatter(Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)



class Bot(Client, Admin, Channel, Info, Misc, User, Base):

    def __init__(self):
        super().__init__()
        self.max_messages = 20000


    async def on_ready(self):
        pass #Likely not called once

    async def on_resumed(self):
        pass

    async def on_message(self, message):
        pass

    async def on_message_delete(self, message):
        pass #Increase Clients max_messages for more cached messages

    async def on_message_edit(self, before, after):
        pass

    async def on_reaction_add(self, reaction, user):
        pass

    async def on_reaction_remove(self, reaction, user):
        pass

    async def on_reaction_clear(self, message, reactions):
        pass

    async def on_channel_create(self, channel):
        pass

    async def on_channel_delete(self, channel):
        pass

    async def on_channel_update(self, before, after):
        pass

    async def on_member_join(self, member):
        pass

    async def on_member_remove(self, member):
        pass

    async def on_member_update(self, before, after):
        pass

    async def on_server_join(self, server):
        pass

    async def on_server_remove(self, server):
        pass #Includes banned, kicked, left, really removed

    async def on_server_update(self, before, after):
        pass

    async def on_server_role_create(self, role):
        pass

    async def on_server_role_delete(self, role):
        pass

    async def on_server_role_update(self, before, after):
        pass

    async def on_server_emojis_update(self, before, after):
        pass

    async def on_server_avaiable(self, server):
        pass

    async def on_server_unavaiable(self, server):
        pass

    async def on_voice_state_update(self, before, after):
        pass #leave join mute deaf

    async def on_member_ban(self, member):
        pass

    async def on_member_unban(self, server, user):
        pass

    async def on_typing(self, channel, user, when):
        pass

    async def on_group_join(self, channel, user):
        pass

    async def on_group_remove(self, channel, user):
        pass
