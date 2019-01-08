from os.path import isfile

from configparser import ConfigParser

class Config(object):

    def __init__(self):
        super(Config, self).__init__()

        self.yes_alternatives = ['yes', 'Yes', 'y', 'Y', 'ja', 'Ja', 'j', 'J']
        self.no_alternatives = ['no', 'No', 'n', 'N', 'nein', 'Nein']

        self.optionsfp = 'config/options.cfg'
        if not isfile(self.optionsfp):
            self.options = ConfigParser()
            self.options.add_section('Miscellaneous')
            self.options.add_section('Properties')
            self.options.add_section('Logging')
            self.options.add_section('Games')
            self.options.add_section('Permissions')
            language = -1
            while not language in [0, 1]:
                print('English[0] / Deutsch[1]')
                language = int(input())
                if language == 0:
                    self.language = 'en'
                elif language == 1:
                    self.language = 'de'
                else:
                    print('Bad input..')
            self.load_language(self.language)
            print(self.glossary['modules.base.selected_language'])

            clientid = str()
            while not clientid.isdecimal():
                print(self.glossary['modules.base.clientid'])
                clientid = input()
                if clientid.isdecimal():
                    self.clientID = clientid
                else:
                    print(self.glossary['modules.base.badinput'])

            token = str()
            while token == '':
                print(self.glossary['modules.base.token'])
                token = input()
                if token != '':
                    self.token = token
                else:
                    print(self.glossary['modules.base.badinput'])

            ownerid = str()
            while not ownerid.isdecimal():
                print(self.glossary['modules.base.ownerid'])
                ownerid = input()
                if ownerid.isdecimal():
                    self.ownerID = ownerid
                else:
                    print(self.glossary['modules.base.badinput'])

            self.firstStart = True

            #print('Open https://discordapp.com/oauth2/authorize?client_id=%s&scope=bot&permissions=0 to add the bot to a server.' % self.clientID)

            self.__write()


        else:
            self.options = ConfigParser()
            self.__read()


    def __read(self):
        self.options.read(self.optionsfp)

    def __write(self):
        with open(self.optionsfp, 'w') as f:
            self.options.write(f)


    def load_language(self, language):
        with open('lang/' + language + '.lang', 'r') as languagefile:
            lines = languagefile.readlines()
        self.glossary = dict()
        for l in lines:
            a, b = l.rstrip('\n').split('=')
            self.glossary[a] = b


    @property
    def language(self):
        self.__read()
        return self.options.get('Miscellaneous', 'language')

    @language.setter
    def language(self, n):
        self.options.set('Miscellaneous', 'language', n)
        self.__write()

    @property
    def clientID(self):
        self.__read()
        return self.options.get('Miscellaneous', 'clientID')

    @clientID.setter
    def clientID(self, n):
        self.options.set('Miscellaneous', 'clientID', n)
        self.__write()

    @property
    def clientSecret(self):
        self.__read()
        return self.options.get('Miscellaneous', 'clientSecret')

    @clientSecret.setter
    def clientSecret(self, n):
        self.options.set('Miscellaneous', 'clientSecret', n)
        self.__write()

    @property
    def token(self):
        self.__read()
        return self.options.get('Miscellaneous', 'token')

    @token.setter
    def token(self, n):
        self.options.set('Miscellaneous', 'token', n)
        self.__write()

    @property
    def ownerID(self):
        self.__read()
        return self.options.get('Miscellaneous', 'ownerID')

    @ownerID.setter
    def ownerID(self, n):
        self.options.set('Miscellaneous', 'ownerID', n)
        self.__write()

    @property
    def firstStart(self):
        self.__read()
        r = self.options.get('Miscellaneous', 'firstStart')
        if r == 'True':
            return True
        else:
            return False

    @firstStart.setter
    def firstStart(self, n):
        if n:
            self.options.set('Miscellaneous', 'firstStart', 'True')
        else:
            self.options.set('Miscellaneous', 'firstStart', 'False')
        self.__write()

    @property
    def nickname(self):
        self.__read()
        return self.options.get('Properties', 'nickname')

    @nickname.setter
    def nickname(self, n):
        self.options.set('Properties', 'nickname', n)
        self.__write()

    @property
    def autoSetNickname(self):
        self.__read()
        return self.options.get('Properties', 'autoSetNickname')

    @autoSetNickname.setter
    def autoSetNickname(self, n):
        if n == '0':
            self.options.set('Properties', 'autoSetNickname', 'never')
        elif n == '1':
            self.options.set('Properties', 'autoSetNickname', 'always')
        elif n == '2':
            self.options.set('Properties', 'autoSetNickname', 'once')
        self.__write()

    @property
    def prefix(self):
        self.__read()
        return self.options.get('Properties', 'prefix')

    @prefix.setter
    def prefix(self, n):
        self.options.set('Properties', 'prefix', n)
        self.__write()

    @property
    def logging(self):
        self.__read()
        return self.options.get('Logging', 'logging')

    @autoSetNickname.setter
    def logging(self, n):
        if n:
            self.options.set('Logging', 'logging', 'True')
        else:
            self.options.set('Logging', 'logging', 'False')
        self.__write()

    @property
    def logMessages(self):
        self.__read()
        return self.options.get('Logging', 'logMessages')

    @logMessages.setter
    def logMessages(self, n):
        if n:
            self.options.set('Logging', 'logMessages', 'True')
        else:
            self.options.set('Logging', 'logMessages', 'False')
        self.__write()

    @property
    def logBotActivities(self):
        self.__read()
        return self.options.get('Logging', 'logBotActivities')

    @logBotActivities.setter
    def logBotActivities(self, n):
        if n:
            self.options.set('Logging', 'logBotActivities', 'True')
        else:
            self.options.set('Logging', 'logBotActivities', 'False')
        self.__write()

    @property
    def logUserActivities(self):
        self.__read()
        return self.options.get('Logging', 'logUserActivities')

    @logUserActivities.setter
    def logUserActivities(self, n):
        if n:
            self.options.set('Logging', 'logUserActivities', 'True')
        else:
            self.options.set('Logging', 'logUserActivities', 'False')
        self.__write()

    @property
    def trackGameHistory(self):
        self.__read()
        return self.options.get('Games', 'trackGameHistory')

    @trackGameHistory.setter
    def trackGameHistory(self, n):
        if n:
            self.options.set('Games', 'trackGameHistory', 'True')
        else:
            self.options.set('Games', 'trackGameHistory', 'False')
        self.__write()

    @property
    def trackGameStatistics(self):
        self.__read()
        return self.options.get('Games', 'trackGameStatistics')

    @trackGameStatistics.setter
    def trackGameStatistics(self, n):
        if n:
            self.options.set('Games', 'trackGameStatistics', 'True')
        else:
            self.options.set('Games', 'trackGameStatistics', 'False')
        self.__write()

    @property
    def autoCreateGameRoles(self):
        self.__read()
        return self.options.get('Games', 'autoCreateGameRoles')

    @autoCreateGameRoles.setter
    def autoCreateGameRoles(self, n):
        if n:
            self.options.set('Games', 'autoCreateGameRoles', 'True')
        else:
            self.options.set('Games', 'autoCreateGameRoles', 'False')
        self.__write()

    @property
    def autoCreateTemporaryGameRoles(self):
        self.__read()
        return self.options.get('Games', 'autoCreateTemporaryGameRoles')

    @autoCreateTemporaryGameRoles.setter
    def autoCreateTemporaryGameRoles(self, n):
        if n:
            self.options.set('Games', 'autoCreateTemporaryGameRoles', 'True')
        else:
            self.options.set('Games', 'autoCreateTemporaryGameRoles', 'False')
        self.__write()

    @property
    def autoAddGames(self):
        self.__read()
        return self.options.get('Games', 'autoAddGames')

    @autoAddGames.setter
    def autoAddGames(self, n):
        if n:
            self.options.set('Games', 'autoAddGames', 'True')
        else:
            self.options.set('Games', 'autoAddGames', 'False')
        self.__write()

    @property
    def autoGiveGameRoles(self):
        self.__read()
        return self.options.get('Games', 'autoGiveGameRoles')

    @autoGiveGameRoles.setter
    def autoGiveGameRoles(self, n):
        if n:
            self.options.set('Games', 'autoGiveGameRoles', 'True')
        else:
            self.options.set('Games', 'autoGiveGameRoles', 'False')
        self.__write()

    @property
    def defaultCommandPermissions(self):
        self.__read()
        return self.options.get('Permissions', 'defaultCommandPermissions')

    @defaultCommandPermissions.setter
    def defaultCommandPermissions(self, n):
        if n:
            self.options.set('Permissions', 'defaultCommandPermissions', 'True')
        else:
            self.options.set('Permissions', 'defaultCommandPermissions', 'False')
        self.__write()



if __name__ == '__main__':
    b = Base()
