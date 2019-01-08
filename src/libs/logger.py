class Logger(object):

    def __init__(self, fp):
        super(Logger, self).__init__()
        self.fp = fp

    def log(self, l):
        with open(self.fp, 'a') as f:
            f.write(l)
