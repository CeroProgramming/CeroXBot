from datetime import datetime

class Logger(object):

    def __init__(self, fp):
        super(Logger, self).__init__()
        self.fp = fp

    async def log(self, l):
        l = l.replace('\n', '\\n')
        l = l.replace('\t', '\\t') # TODO Need more?
        with open(self.fp, 'a+') as f:
            f.write('%s\n' % (l))

    async def log_message(self, message):
        m = '[%s, created message] ' % (datetime.now().time().isoformat())
        m += '%s ' % (message.content)
        if message.embeds != []:
            m += '(embeds: %s) ' % (' '.join(message.embeds))
        if message.attachments != []:
            m += '(attachments: %s) ' % (' '.join(message.attachments))
        m += '[%s, by %s, in %s]' % (message.id, message.author.id, "private channel" if message.channel.is_private else "%s at %s" % (message.channel.id, message.channel.server.id))
        await self.log(m)

    async def log_message_change(self, before, after):
        m = '[%s, changed message] ' % (datetime.now().time().isoformat())
        m += 'from %s ' % (before.content)
        if before.embeds != []:
            m += '(embeds: %s) ' % (' '.join(before.embeds))
        if before.attachments != []:
            m += '(attachments: %s) ' % (' '.join(before.attachments))
        m += 'to %s ' % (after.content)
        if after.embeds != []:
            m += '(embeds: %s) ' % (' '.join(after.embeds))
        if after.attachments != []:
            m += '(attachments: %s) ' % (' '.join(after.attachments))
        m += '[%s, by %s, in %s]' % (after.id, after.author.id, "private channel" if after.channel.is_private else "%s at %s" % (after.channel.id, after.channel.server.id))
        await self.log(m)

    async def log_message_delete(self, message):
        m = '[%s, deleted message] ' % (datetime.now().time().isoformat())
        m += '%s ' % (message.content)
        if message.embeds != []:
            m += '(embeds: %s) ' % (' '.join(message.embeds))
        if message.attachments != []:
            m += '(attachments: %s) ' % (' '.join(message.attachments))
        m += '[%s, by %s, in %s]' % (message.id, message.author.id, "private channel" if message.channel.is_private else "%s at %s" % (message.channel.id, message.channel.server.id))
        await self.log(m)

    async def log_server_join(self, member):
        m = '[%s, joined server] ' % (datetime.now().time().isoformat())
        m += '%s (%s), ' % (member.name, member.id)
        m += 'server: %s (%s)' % (member.server.name, member.server.id)
        await self.log(m)

    async def log_server_leave(self, member):
        m = '[%s, leaved server] ' % (datetime.now().time().isoformat())
        m += '%s (%s), ' % (member.name, member.id)
        m += 'server: %s (%s)' % (member.server.name, member.server.id)
        await self.log(m)
