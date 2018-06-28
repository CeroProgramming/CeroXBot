from modules.base import Base
from modules.admin import Admin
from modules.channel import Channel
from modules.info import Info
from modules.misc import Misc
from modules.user import User


class Bot(Admin, Channel, Info, Misc, User, Base):

    def __init__(self):
        super().__init__()
