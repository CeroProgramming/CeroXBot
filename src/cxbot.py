from modules.base import Base
from modules.setup import Setup
from modules.bot import Bot
from modules.server import Server
from modules.channel import Channel
from modules.user import User
from modules.role import Role
from modules.features import Features
from modules.config import Config
from modules.exceptions import MissingServer

from discord import Client
from logging import basicConfig, getLogger, FileHandler, Formatter, CRITICAL, ERROR, WARNING, INFO, DEBUG



logger = getLogger('discord')
logger.setLevel(INFO)
logpath = 'logs/discord.log'
handler = FileHandler(filename=logpath, encoding='utf-8', mode='w')
handler.setFormatter(Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)



class CXBot(Client, Setup, Bot, Server, Channel, User, Role, Features, Base):

    def __init__(self):
        super(CXBot, self).__init__()

        self.c = Config()

        self.max_messages = 20000
        self.ready = False

    async def on_ready(self):

        if not self.ready:
            self.ready = True

            print('Logged on as %s!' % self.user)

            if len(self.servers) == 0:
                print('You have to connect me to a server. Open https://discordapp.com/oauth2/authorize?client_id=%s&scope=bot&permissions=0' % self.c.clientID)
                await self.logout()
                await self.close()

            elif len(self.servers) > 1:
                print('Connected to the following servers:\n\t%s' % '\n\t'.join(self._server_names()))
                print('You connected me to multiple servers. Note that you may want to use multiple instances of this bot because otherwise all settings will be the same for all connected servers.')
            else:
                print('Connected to the server %s' % self._server_names()[0])

            if self.c.firstStart:
                await self.setup()










    async def on_resumed(self):
        pass

    async def on_error(self, event, *args, **kwargs):
        print(event)

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




    async def shutdown(self): #TODO Test
        await self.logout()
        await self.close()
