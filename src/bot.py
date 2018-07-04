from modules.base import Base
from modules.admin import Admin
from modules.channel import Channel
from modules.info import Info
from modules.misc import Misc
from modules.user import User
from modules.exceptions import MissingServer

from discord import Client
from logging import basicConfig, getLogger, FileHandler, Formatter, CRITICAL, ERROR, WARNING, INFO, DEBUG



logger = getLogger('discord')
logger.setLevel(DEBUG)
logpath = 'logs/discord.log'
handler = FileHandler(filename=logpath, encoding='utf-8', mode='w')
handler.setFormatter(Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)



class Bot(Client, Admin, Channel, Info, Misc, User):

    def __init__(self):
        super(Bot, self).__init__()

        self.c = Base()
        self.max_messages = 20000
        self.ready = False

    def _server_names(self):
        return [s.name for s in self.servers]

    async def _get_owner_by_id(self):
        return await self.get_user_info(self.c.ownerID)

    async def _wait_for_bool(self, author):
        message = await self.wait_for_message(timeout=None, author=author)
        while message.content not in self.c.yes_alternatives and message.content not in self.c.no_alternatives:
            await self.send_typing(author)
            await self.send_message(author, content='No valid message..')
            message = await self.wait_for_message(timeout=None, author=author)
        if message.content in self.c.yes_alternatives:
            return True
        elif message.content in self.c.no_alternatives:
            return False

    async def _wait_for_list(self, author, whitelist):
        message = await self.wait_for_message(timeout=None, author=author)
        while message.content not in whitelist:
            await self.send_typing(author)
            await self.send_message(author, content='No valid message..')
            message = await self.wait_for_message(timeout=None, author=author)
        return message.content


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

    async def setup(self):
        owner = await self._get_owner_by_id()

        await self.send_typing(owner)
        await self.send_message(owner, content='Welcome. I am the CeroXBot aka CXBot. You or someone who knows your ID has set you as my owner. Can we start with the setup? If yes type \'start\'.')
        await self.wait_for_message(timeout=None, author=owner, content='start')
        await self.send_typing(owner)
        await self.send_message(owner, content='All settings will be applied for all connected servers.')
        await self.send_typing(owner)
        await self.send_message(owner, content='Do you like to give me a nickname? (No/Yes)')
        b = await self._wait_for_bool(owner)
        if b:
            await self.send_typing(owner)
            await self.send_message(owner, content='Okay, which one?')
            message = await self.wait_for_message(timeout=None, author=owner)
            self.c.nickname = message.content
            await self.send_typing(owner)
            await self.send_message(owner, content='Shall I try to set my nickname? (Never[0]/Always[1]/Only when added to a new server[2]')
            self.c.autoSetNickname = await self._wait_for_list(owner, ['0', '1', '2'])


    async def shutdown(self): #TODO Test
        await self.logout()
        await self.close()
