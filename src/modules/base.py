from os.path import isfile

from ConfigParser import ConfigParser


class Base(object):

    def __init__(self):

        self.optionsfp = 'options.ini'
        if not isfile(self.optionsfp):
            self.options = ConfigParser()

            language = -1
            while not language in [0, 1]:
                print('English[0] / Deutsch[1]')
                language = int(input())
                if language == 0:
                    self.options['Miscellaneous'] = {'language': 'en'}
                elif language == 1:
                    self.options['Miscellaneous'] = {'language': 'de'}
                else:
                    print('Bad input..')


            self.load_language(self.options['Miscellaneous']['language'])

            print(self.language['modules.base.selected_language'])

            clientid = str()
            while not clientid.isdecimal():
                print(self.language['modules.base.clientid'])
                if clientid.isdecimal():
                    self.options['Miscellaneous']['ClientID'] = clientid
                else:
                    print(self.language['modules.base.badinput'])

            clientsecret = str()
            while not clientsecret == '':
                print(self.language['modules.base.clientsecret'])
                if clientsecret == '':
                    self.options['Miscellaneous']['ClientSecret'] = clientsecret
                else:
                    print(self.language['modules.base.badinput'])






    def load_language(self, language):

        with open('lang/' + language + '.lang', 'r') as languagefile:
            lines = languagefile.readlines()

        self.language = dict()

        for l in lines:
            a, b = l.rstrip('\n').split('=')
            self.language[a] = b
