from modules.base import Base
from modules.setup import Setup
from modules.bot import Bot
from modules.io import IO
from modules.server import Server
from modules.channel import Channel
from modules.user import User
from modules.role import Role
from modules.features import Features
from modules.config import Config
from modules.exceptions import MissingServer

from libs.logger import Logger

from discord import Client, Color
from logging import basicConfig, getLogger, FileHandler, Formatter, CRITICAL, ERROR, WARNING, INFO, DEBUG
from datetime import datetime

logger = getLogger('discord')
logger.setLevel(DEBUG)
log_path = 'logs/discord.log'
handler = FileHandler(filename=log_path, encoding='utf-8', mode='w')
handler.setFormatter(Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


class CXBot(Client, Setup, Bot, IO, Server, Channel, User, Role, Features, Base):

    def __init__(self):
        super(CXBot, self).__init__()

        self.c = Config()

        self.max_messages = 20000
        self.ready = False

        self.logger = Logger('logs/%s.log' % datetime.now().date().isoformat())

        self.busy = False

    @Base.excep
    async def on_ready(self):

        if not self.ready:
            self.ready = True

            print('Logged on as %s!' % self.user)

            if len(self.servers) == 0:
                print('You have to connect me to a server. Open https://discordapp.com/oauth2/authorize?client_id=%s\
                    &scope=bot&permissions=0' % self.c.clientID)
                await self.logout()
                await self.close()

            elif len(self.servers) > 1:
                print('Connected to the following servers:\n\t%s' % '\n\t'.join(self._server_names()))
                print('You connected me to multiple servers. Note that you may want to use multiple instances of this \
                    bot because otherwise all settings will be the same for all connected servers and some functions \
                    may could interfere in this state of development.')
            else:
                print('Connected to the server %s' % self._server_names()[0])

            if self.c.firstStart:
                self.busy = True
                await self.setup()
                self.busy = False

    async def on_resumed(self):
        pass

    async def on_error(self, event, *args, **kwargs):
        print(event)

    @Base.excep
    async def on_message(self, message):

        if self.c.logMessages:
            self.logger.log_message(message)

        if self.busy:
            return

        if not message.author == self.user:
            print(message.content)
            e = await self.create_embed("Github CeroProgramming", "https://github.com/CeroProgramming", "GitHub Profile URL", Color.dark_purple(), "CeroProgramming", "https://github.com/CeroProgramming/", "https://avatars3.githubusercontent.com/u/22818389?s=460&v=4", "https://proxy.duckduckgo.com/iu/?u=https%3A%2F%2Fimage.freepik.com%2Ffree-icon%2Fgithub-logo_318-53553.jpg&f=1")
            await self.io_embed(message.channel, e)

        if message.content == "shutdown":
            await self.shutdown()

    async def on_message_delete(self, message):
        pass  # Increase Clients max_messages for more cached messages

    async def on_message_edit(self, before, after):

        if self.c.logMessages:
            if before.content != after.content or before.embeds != after.embeds or before.attachments != after.attachments:
                self.logger.log_message_change(before, after)

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
        pass  # Includes banned, kicked, left, really removed

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

    async def on_server_available(self, server):
        pass

    async def on_server_unavailable(self, server):
        pass

    async def on_voice_state_update(self, before, after):
        pass  # leave join mute deaf

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

    async def shutdown(self):  # TODO Test
        await self.logout()
        await self.close()
