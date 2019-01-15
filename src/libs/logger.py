from datetime import datetime

class Logger(object):

    def __init__(self, fp):
        super(Logger, self).__init__()
        self.fp = fp

    def log(self, l):
        l = l.replace('\n', '\\n')
        l = l.replace('\t', '\\t') # TODO Need more?
        with open(self.fp, 'a+') as f:
            f.write('%s\n' % (l))

    def log_message(self, message):
        m = '[%s, %s] %s' % (datetime.now().time().isoformat(), message.id)
        m += '%s [%s (%s), ' % (message.content, message.author.name, message.author.id)
        m += '%s' % ("private channel" if message.channel.is_private else "%s (%s) at %s (%s))" % (message.channel.name, message.channel.id, message.channel.server.name, message.channel.server.id))
        if message.embeds != []:
            m += ', embeds:'
            for e in message.embeds:
                m += ' %s' % (e)
        if message.attachments != []:
            m += ', attachments:'
            for a in message.attachments:
                m += ' %s' % (a)
        m += ']'
        self.log(m)

    def log_message_change(self, before, after):
        m = '[%s, %s] ' % (datetime.now().time().isoformat(), after.id)
        m += '%s [%s (%s), ' % (before.content, before.author.name, before.author.id)
        m += '%s' % ("private channel" if before.channel.is_private else "%s (%s) at %s (%s))" % (before.channel.name, before.channel.id, before.channel.server.name, before.channel.server.id))
        if before.embeds != []:
            m += ', embeds:'
            for e in before.embeds:
                m += ' %s' % (e)
        if before.attachments != []:
            m += ', attachments:'
            for a in before.attachments:
                m += ' %s' % (a)
        m += ']'
        m += 'to %s, [' % (after.content)
        if after.embeds != []:
            m += ', embeds:'
            for e in after.embeds:
                m += ' %s' % (e)
        if after.attachments != []:
            m += ', attachments:'
            for a in after.attachments:
                m += ' %s' % (a)
        m += ']'

        self.log(m)
