from .base import Base

class Setup(Base):

    def __init__(self):
        super(Setup, self).__init__()

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
