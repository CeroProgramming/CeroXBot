from .base import Base


class Server(Base):

    def __init__(self):
        super(Server, self).__init__()

    def server_name(self, **kwargs):
        if kwargs['x'] in ['get']:
            return kwargs['server'].name
        elif kwargs['x'] in ['set']:
            pass


    def server_members(self, **kwargs):
        if kwargs['x'] in ['get']:
            cache = list()
            for member in kwargs['server'].members:
                cache.append((member.name, member.id, member.discriminator, member.avatar_url, member.display_name, member.bot, member.created_at))
            return cache
