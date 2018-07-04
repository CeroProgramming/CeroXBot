from bot import Bot

cxbot = Bot()

try:
    cxbot.loop.run_until_complete(cxbot.start(cxbot.c.token))
except KeyboardInterrupt:
    cxbot.loop.run_until_complete(cxbot.logout())
    # cancel all tasks lingering
except MissingServer:
    cxbot.loop.run_until_complete(cxbot.logout())
finally:
    cxbot.loop.close()
