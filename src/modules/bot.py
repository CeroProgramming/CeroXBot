from .base import Base

class Bot(Base):

    def __init__(self):
        super(Bot, self).__init__()

    async def name(self, **kwargs):
        if kwargs['x'] in ['get']:
            return self.user.name

    async def id(self, **kwargs):
        if kwargs['x'] in ['get']:
            return self.user.id

    async def discriminator(self, **kwargs):
        if kwargs['x'] in ['get']:
            return str(self.user.discriminator)

    async def avatar(self, **kwargs):
        if kwargs['x'] in ['get']:
            return self.user.avatar_url

    async def mention(self, **kwargs):
        if kwargs['x'] in ['get']:
            return self.user.mention

    async def displayname(self, **kwargs):
        if kwargs['x'] in ['get']:
            return self.user.display_name
