import asyncio

class IO(object):


    def __init__(self):
        pass


    async def io_message(self, dest, content):

        await self.send_typing(message)
        await asyncio.sleep(3)
        await self.send_message(dest, content)
