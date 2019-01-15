#!/usr/bin/python3

venv_file='venv/ceroxbot/bin/activate_this.py'
execfile(venv_file, dict(__file__=venv_file))

from cxbot import CXBot
from modules.exceptions import MissingServer

cxbot = CXBot()

try:
    cxbot.loop.run_until_complete(cxbot.start(cxbot.c.token))
except KeyboardInterrupt:
    cxbot.loop.run_until_complete(cxbot.logout())
    # cancel all tasks lingering
except MissingServer:
    cxbot.loop.run_until_complete(cxbot.logout())
finally:
    cxbot.loop.close()
