from .config import Config
from .exceptions import MissingServer

class Base(object):

    def __init__(self):

        super(Base, self).__init__()

        self.c = Config()

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

    async def _wait_for_picture_url(self, author):
        message = await self.wait_for_message(timeout=None, author=author)
        while not message.attachments:
            await self.send_typing(author)
            await self.send_message(author, content='No picture send..')
            message = await self.wait_for_message(timeout=None, author=author)
        return message.attachments[0]['url']
