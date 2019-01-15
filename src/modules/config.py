from os.path import isfile

from configparser import ConfigParser

import sys
sys.path.append('../')

from libs.cxjson import load, dump

class Config(object):

    def __init__(self):
        super(Config, self).__init__()

        self.yes_alternatives = ['yes', 'Yes', 'y', 'Y', 'ja', 'Ja', 'j', 'J']
        self.no_alternatives = ['no', 'No', 'n', 'N', 'nein', 'Nein']

        self.permissionsfp = 'config/permissions.json'
        if not isfile(self.permissionsfp):
            self.permissions = {
                'spectator': {
                    'bot': {
                        'help': True,
                        'setup': False,
                        'restart': False,
                        'shutdown': False,
                        'transfer': False,
                        'create_server': False,
                        'credits': True,
                        'get_name': False,
                        'set_name': False,
                        'get_avatar': False,
                        'set_avatar': False,
                        'get_nickname': False,
                        'set_nickname': False,
                        'get_game': False,
                        'set_game': False,
                        'get_prefix': True,
                        'set_prefix': False,
                        'del_prefix': False,
                        'get_owner': True,
                        'set_owner': False,
                        'get_token': False,
                        'set_token': False,
                        'get_loggermode': False,
                        'set_loggermode': False,
                        'toggle_logtofile': False,
                        'get_log': False,
                        'set_log': False,
                        'get_logoptions': False,
                        'set_logoptions': False,
                        'toggle_autoaddgamerole': False,
                        'toggle_autogiverole': False
                    },
                    'server': {
                        'get_name': False,
                        'set_name': False,
                        'get_icon': False,
                        'set_icon': False,
                        'get_splash': False,
                        'set_splash': False,
                        'get_region': False,
                        'set_region': False,
                        'get_afkchannel': False,
                        'set_afkchannel': False,
                        'del_afkchannel': False,
                        'get_afktimeout': False,
                        'set_afktimeout': False,
                        'del_timeout': False,
                        'get_verificationlevel': False,
                        'set_verificationlevel': False,
                        'kick': False,
                        'ban': False,
                        'unban': False,
                        'get_bans': False,
                        'get_reprimand': False,
                        'add_reprimand': False,
                        'del_reprimand': False,
                        'get_invites': False,
                        'add_invites': False,
                        'del_invites': False,
                        'clear': False,
                        'info': False,
                        'get_members': False,
                        'get_ids': False,
                        'get_users': False,
                        'get_channels': False
                    },
                    'role': {
                        'create': False,
                        'remove': False,
                        'apply': False,
                        'take': False,
                        'move': False,
                        'allow': False,
                        'deny': False
                    },
                    'user': {
                        'make_admin': False,
                        'make_silentadmin': False,
                        'unmake_admin': False,
                        'apply': False,
                        'take': False,
                        'allow': False,
                        'deny': False,
                        'get_info': False,
                        'get_id': False,
                        'permissions': False,
                        'clear': False
                    },
                    'channel': {
                        'voice_edit': False,
                        'text_edit': False,
                        'gather': False,
                        'pin': False,
                        'reactions_clear': False,
                        'rections_add': False,
                        'allow_role': False,
                        'allow_user': False,
                        'allow_all': False,
                        'deny_role': False,
                        'deny_user': False,
                        'deny_all': False,
                        'create_text': False,
                        'create_text_temporary': False,
                        'create_voice': False,
                        'voice_temmporary': False,
                        'remove_text': False,
                        'remove_voice': False,
                        'options_text': False,
                        'options_voice': False,
                        'count_own': False,
                        'count_all': False
                    },
                    'games': {
                        'add_game': False,
                        'add_alternative': False,
                        'add_member': False,
                        'remove_game': False,
                        'remove_alternatives': False,
                        'remove_member': False,
                        'list': False,
                        'history': False,
                        'statistics': False
                    },
                    'features': {
                        'toggle_personalprotocol': False,
                        'get_personalprotocol': False,
                        'del_personalprotocol': False,
                        'sleep': False,
                        'start_watch': False,
                        'stop_watch': False,
                        'state_watch': False,
                        'add_survey': False,
                        'del_survey': False,
                        'get_survey': False,
                        'evaluate_survey': False,
                        'set_remind': False,
                        'get_remind': False,
                        'del_remind': False,
                        'get_birthday': False,
                        'set_birthday': False,
                        'del_birthday': False,
                        'toggle_spam': False,
                        'get_spamfilter': False,
                        'set_spamfilter': False,
                        'toggle_censoring': False,
                        'get_censorfilters': False,
                        'set_censorfilters': False,
                        'add_executionoption': False,
                        'get_excutionoption': False,
                        'del_excutionoption': False
                    }
                },
                'user': {
                    'bot': {
                        'help': True,
                        'setup': True,
                        'restart': False,
                        'shutdown': False,
                        'transfer': False,
                        'create_server': False,
                        'credits': True,
                        'get_name': False,
                        'set_name': False,
                        'get_avatar': False,
                        'set_avatar': False,
                        'get_nickname': False,
                        'set_nickname': False,
                        'get_game': False,
                        'set_game': False,
                        'get_prefix': True,
                        'set_prefix': False,
                        'del_prefix': False,
                        'get_owner': True,
                        'set_owner': False,
                        'get_token': False,
                        'set_token': False,
                        'get_loggermode': False,
                        'set_loggermode': False,
                        'toggle_logtofile': False,
                        'get_log': False,
                        'set_log': False,
                        'get_logoptions': False,
                        'set_logoptions': False,
                        'toggle_autoaddgamerole': False,
                        'toggle_autogiverole': False
                    },
                    'server': {
                        'get_name': False,
                        'set_name': False,
                        'get_icon': False,
                        'set_icon': False,
                        'get_splash': False,
                        'set_splash': False,
                        'get_region': False,
                        'set_region': False,
                        'get_afkchannel': False,
                        'set_afkchannel': False,
                        'del_afkchannel': False,
                        'get_afktimeout': False,
                        'set_afktimeout': False,
                        'del_afktimeout': False,
                        'get_verificationlevel': False,
                        'set_verificationlevel': False,
                        'kick': False,
                        'ban': False,
                        'unban': False,
                        'get_bans': False,
                        'get_reprimand': False,
                        'add_reprimand': False,
                        'del_reprimand': False,
                        'get_invites': False,
                        'add_invites': False,
                        'del_invites': False,
                        'clear': False,
                        'info': False,
                        'get_members': False,
                        'get_ids': False,
                        'get_users': False,
                        'get_channels': False
                    },
                    'role': {
                        'create': False,
                        'remove': False,
                        'apply': False,
                        'take': False,
                        'move': False,
                        'allow': False,
                        'deny': False
                    },
                    'user': {
                        'make_admin': False,
                        'make_silentadmin': False,
                        'unmake_admin': False,
                        'apply': False,
                        'take': False,
                        'allow': False,
                        'deny': False,
                        'get_info': False,
                        'get_id': False,
                        'permissions': False,
                        'clear': False
                    },
                    'channel': {
                        'voice_edit': False,
                        'text_edit': False,
                        'gather': False,
                        'pin': False,
                        'reactions_clear': False,
                        'rections_add': False,
                        'allow_role': False,
                        'allow_user': False,
                        'allow_all': False,
                        'deny_role': False,
                        'deny_user': False,
                        'deny_all': False,
                        'create_text': False,
                        'create_text_temporary': False,
                        'create_voice': False,
                        'create_voice_temmporary': False,
                        'remove_text': False,
                        'remove_voice': False,
                        'options_text': False,
                        'options_voice': False,
                        'count_own': False,
                        'count_all': False
                    },
                    'games': {
                        'add_game': False,
                        'add_alternative': False,
                        'add_member': False,
                        'remove_game': False,
                        'remove_alternatives': False,
                        'remove_member': False,
                        'list': True,
                        'history': True,
                        'statistics': True
                    },
                    'features': {
                        'toggle_personalprotocol': True,
                        'get_personalprotocol': True,
                        'del_personalprotocol': True,
                        'sleep': True,
                        'start_watch': True,
                        'stop_watch': True,
                        'state_watch': True,
                        'add_survey': False,
                        'del_survey': False,
                        'get_survey': False,
                        'evaluate_survey': False,
                        'set_remind': True,
                        'get_remind': True,
                        'del_remind': True,
                        'get_birthday': True,
                        'set_birthday': True,
                        'del_birthday': True,
                        'toggle_spam': False,
                        'get_spamfilter': False,
                        'set_spamfilter': False,
                        'toggle_censoring': False,
                        'get_censorfilters': False,
                        'set_censorfilters': False,
                        'add_executionoption': False,
                        'get_excutionoption': False,
                        'del_excutionoption': False
                    }
                },
                'friend': {
                    'bot': {
                        'help': True,
                        'setup': True,
                        'restart': False,
                        'shutdown': False,
                        'transfer': False,
                        'create_server': False,
                        'credits': True,
                        'get_name': True,
                        'set_name': False,
                        'get_avatar': True,
                        'set_avatar': False,
                        'get_nickname': True,
                        'set_nickname': False,
                        'get_game': False,
                        'set_game': False,
                        'get_prefix': True,
                        'set_prefix': False,
                        'del_prefix': False,
                        'get_owner': True,
                        'set_owner': False,
                        'get_token': False,
                        'set_token': False,
                        'get_loggermode': False,
                        'set_loggermode': False,
                        'toggle_logtofile': False,
                        'get_log': False,
                        'set_log': False,
                        'get_logoptions': False,
                        'set_logoptions': False,
                        'toggle_autoaddgamerole': False,
                        'toggle_autogiverole': False
                    },
                    'server': {
                        'get_name': True,
                        'set_name': False,
                        'get_icon': True,
                        'set_icon': False,
                        'get_splash': True,
                        'set_splash': False,
                        'get_region': False,
                        'set_region': False,
                        'get_afkchannel': False,
                        'set_afkchannel': False,
                        'del_afkchannel': False,
                        'get_afktimeout': False,
                        'set_afktimeout': False,
                        'del_afktimeout': False,
                        'get_verificationlevel': False,
                        'set_verificationlevel': False,
                        'kick': False,
                        'ban': False,
                        'unban': False,
                        'get_bans': False,
                        'get_reprimand': False,
                        'add_reprimand': False,
                        'del_reprimand': False,
                        'get_invites': False,
                        'add_invites': False,
                        'del_invites': False,
                        'clear': False,
                        'info': True,
                        'get_members': True,
                        'get_ids': True,
                        'get_users': True,
                        'get_channels': True
                    },
                    'role': {
                        'create': False,
                        'remove': False,
                        'apply': False,
                        'take': False,
                        'move': False,
                        'allow': False,
                        'deny': False
                    },
                    'user': {
                        'make_admin': False,
                        'make_silentadmin': False,
                        'unmake_admin': False,
                        'apply': False,
                        'take': False,
                        'allow': False,
                        'deny': False,
                        'get_info': True,
                        'get_id': True,
                        'permissions': False,
                        'clear': False
                    },
                    'channel': {
                        'voice_edit': False,
                        'text_edit': False,
                        'gather': False,
                        'pin': False,
                        'reactions_clear': False,
                        'rections_add': False,
                        'allow_role': False,
                        'allow_user': False,
                        'allow_all': False,
                        'deny_role': False,
                        'deny_user': False,
                        'deny_all': False,
                        'create_text': False,
                        'create_text_temporary': True,
                        'create_voice': False,
                        'create_voice_temmporary': True,
                        'remove_text': False,
                        'remove_voice': False,
                        'options_text': False,
                        'options_voice': False,
                        'count_own': True,
                        'count_all': True
                    },
                    'games': {
                        'add_game': False,
                        'add_alternative': False,
                        'add_member': False,
                        'remove_game': False,
                        'remove_alternatives': False,
                        'remove_member': False,
                        'list': True,
                        'history': True,
                        'statistics': True
                    },
                    'features': {
                        'toggle_personalprotocol': True,
                        'get_personalprotocol': True,
                        'del_personalprotocol': True,
                        'sleep': True,
                        'start_watch': True,
                        'stop_watch': True,
                        'state_watch': True,
                        'add_survey': True,
                        'del_survey': True,
                        'get_survey': True,
                        'evaluate_survey': True,
                        'set_remind': True,
                        'get_remind': True,
                        'del_remind': True,
                        'get_birthday': True,
                        'set_birthday': True,
                        'del_birthday': True,
                        'toggle_spam': False,
                        'get_spamfilter': False,
                        'set_spamfilter': False,
                        'toggle_censoring': False,
                        'get_censorfilters': False,
                        'set_censorfilters': False,
                        'add_executionoption': False,
                        'get_excutionoption': False,
                        'del_excutionoption': False
                    }
                },
                'admin': {
                    'bot': {
                        'help': True,
                        'setup': True,
                        'restart': True,
                        'shutdown': True,
                        'transfer': True,
                        'create_server': True,
                        'credits': True,
                        'get_name': True,
                        'set_name': True,
                        'get_avatar': True,
                        'set_avatar': True,
                        'get_nickname': True,
                        'set_nickname': True,
                        'get_game': True,
                        'set_game': True,
                        'get_prefix': True,
                        'set_prefix': True,
                        'del_prefix': True,
                        'get_owner': True,
                        'set_owner': True,
                        'get_token': True,
                        'set_token': True,
                        'get_loggermode': True,
                        'set_loggermode': True,
                        'toggle_logtofile': True,
                        'get_log': True,
                        'set_log': True,
                        'get_logoptions': True,
                        'set_logoptions': True,
                        'toggle_autoaddgamerole': True,
                        'toggle_autogiverole': True
                    },
                    'server': {
                        'get_name': True,
                        'set_name': False,
                        'get_icon': True,
                        'set_icon': False,
                        'get_splash': True,
                        'set_splash': False,
                        'get_region': True,
                        'set_region': True,
                        'get_afkchannel': True,
                        'set_afkchannel': True,
                        'del_afkchannel': True,
                        'get_afktimeout': True,
                        'set_afktimeout': True,
                        'del_timeout': True,
                        'get_verificationlevel': True,
                        'set_verificationlevel': True,
                        'kick': True,
                        'ban': True,
                        'unban': True,
                        'get_bans': True,
                        'get_reprimand': True,
                        'add_reprimand': True,
                        'del_reprimand': True,
                        'get_invites': True,
                        'add_invites': True,
                        'del_invites': True,
                        'clear': True,
                        'info': True,
                        'get_members': True,
                        'get_ids': True,
                        'get_users': True,
                        'get_channels': True
                    },
                    'role': {
                        'create': True,
                        'remove': True,
                        'apply': True,
                        'take': True,
                        'move': True,
                        'allow': True,
                        'deny': True
                    },
                    'user': {
                        'make_admin': True,
                        'make_silentadmin': True,
                        'unmake_admin': True,
                        'apply': True,
                        'take': True,
                        'allow': True,
                        'deny': True,
                        'get_info': True,
                        'get_id': True,
                        'permissions': True,
                        'clear': True
                    },
                    'channel': {
                        'voice_edit': True,
                        'text_edit': True,
                        'gather': True,
                        'pin': True,
                        'reactions_clear': True,
                        'rections_add': True,
                        'allow_role': True,
                        'allow_user': True,
                        'allow_all': True,
                        'deny_role': True,
                        'deny_user': True,
                        'deny_all': True,
                        'create_text': True,
                        'create_text_temporary': True,
                        'create_voice': True,
                        'voice_temmporary': True,
                        'remove_text': True,
                        'remove_voice': True,
                        'options_text': True,
                        'options_voice': True,
                        'count_own': True,
                        'count_all': True
                    },
                    'games': {
                        'add_game': True,
                        'add_alternative': True,
                        'add_member': True,
                        'remove_game': True,
                        'remove_alternatives': True,
                        'remove_member': True,
                        'list': True,
                        'history': True,
                        'statistics': True
                    },
                    'features': {
                        'toggle_personalprotocol': True,
                        'get_personalprotocol': True,
                        'del_personalprotocol': True,
                        'sleep': True,
                        'start_watch': True,
                        'stop_watch': True,
                        'state_watch': True,
                        'add_survey': True,
                        'del_survey': True,
                        'get_survey': True,
                        'evaluate_survey': True,
                        'set_remind': True,
                        'get_remind': True,
                        'del_remind': True,
                        'get_birthday': True,
                        'set_birthday': True,
                        'del_birthday': True,
                        'toggle_spam': True,
                        'get_spamfilter': True,
                        'set_spamfilter': True,
                        'toggle_censoring': True,
                        'get_censorfilters': True,
                        'set_censorfilters': True,
                        'add_executionoption': True,
                        'get_excutionoption': True,
                        'del_excutionoption': True
                    }
                },
                'owner': {
                    'bot': {
                        'help': True,
                        'setup': True,
                        'restart': True,
                        'shutdown': True,
                        'transfer': True,
                        'create_server': True,
                        'credits': True,
                        'get_name': True,
                        'set_name': True,
                        'get_avatar': True,
                        'set_avatar': True,
                        'get_nickname': True,
                        'set_nickname': True,
                        'get_game': True,
                        'set_game': True,
                        'get_prefix': True,
                        'set_prefix': True,
                        'del_prefix': True,
                        'get_owner': True,
                        'set_owner': True,
                        'get_token': True,
                        'set_token': True,
                        'get_loggermode': True,
                        'set_loggermode': True,
                        'toggle_logtofile': True,
                        'get_log': True,
                        'set_log': True,
                        'get_logoptions': True,
                        'set_logoptions': True,
                        'toggle_autoaddgamerole': True,
                        'toggle_autogiverole': True
                    },
                    'server': {
                        'get_name': True,
                        'set_name': True,
                        'get_icon': True,
                        'set_icon': True,
                        'get_splash': True,
                        'set_splash': True,
                        'get_region': True,
                        'set_region': True,
                        'get_afkchannel': True,
                        'set_afkchannel': True,
                        'del_afkchannel': True,
                        'get_afktimeout': True,
                        'set_afktimeout': True,
                        'del_timeout': True,
                        'get_verificationlevel': True,
                        'set_verificationlevel': True,
                        'kick': True,
                        'ban': True,
                        'unban': True,
                        'get_bans': True,
                        'get_reprimand': True,
                        'add_reprimand': True,
                        'del_reprimand': True,
                        'get_invites': True,
                        'add_invites': True,
                        'del_invites': True,
                        'clear': True,
                        'info': True,
                        'get_members': True,
                        'get_ids': True,
                        'get_users': True,
                        'get_channels': True
                    },
                    'role': {
                        'create': True,
                        'remove': True,
                        'apply': True,
                        'take': True,
                        'move': True,
                        'allow': True,
                        'deny': True
                    },
                    'user': {
                        'make_admin': True,
                        'make_silentadmin': True,
                        'unmake_admin': True,
                        'apply': True,
                        'take': True,
                        'allow': True,
                        'deny': True,
                        'get_info': True,
                        'get_id': True,
                        'permissions': True,
                        'clear': True
                    },
                    'channel': {
                        'voice_edit': True,
                        'text_edit': True,
                        'gather': True,
                        'pin': True,
                        'reactions_clear': True,
                        'rections_add': True,
                        'allow_role': True,
                        'allow_user': True,
                        'allow_all': True,
                        'deny_role': True,
                        'deny_user': True,
                        'deny_all': True,
                        'create_text': True,
                        'create_text_temporary': True,
                        'create_voice': True,
                        'voice_temmporary': True,
                        'remove_text': True,
                        'remove_voice': True,
                        'options_text': True,
                        'options_voice': True,
                        'count_own': True,
                        'count_all': True
                    },
                    'games': {
                        'add_game': True,
                        'add_alternative': True,
                        'add_member': True,
                        'remove_game': True,
                        'remove_alternatives': True,
                        'remove_member': True,
                        'list': True,
                        'history': True,
                        'statistics': True
                    },
                    'features': {
                        'toggle_personalprotocol': True,
                        'get_personalprotocol': True,
                        'del_personalprotocol': True,
                        'sleep': True,
                        'start_watch': True,
                        'stop_watch': True,
                        'state_watch': True,
                        'add_survey': True,
                        'del_survey': True,
                        'get_survey': True,
                        'evaluate_survey': True,
                        'set_remind': True,
                        'get_remind': True,
                        'del_remind': True,
                        'get_birthday': True,
                        'set_birthday': True,
                        'del_birthday': True,
                        'toggle_spam': True,
                        'get_spamfilter': True,
                        'set_spamfilter': True,
                        'toggle_censoring': True,
                        'get_censorfilters': True,
                        'set_censorfilters': True,
                        'add_executionoption': True,
                        'get_excutionoption': True,
                        'del_excutionoption': True
                    }
                }
            }
            dump(self.permissions, self.permissionsfp)
        else:
            self.permissions = load(self.permissionsfp)


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
        return True if self.options.get('Miscellaneous', 'firstStart') == 'True' else False

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
        return self.options.get('Properties', 'nickname') if self.options.get('Properties', 'nickname') != 'None' else None

    @nickname.setter
    def nickname(self, n):
        self.options.set('Properties', 'nickname', n)
        self.__write()

    @nickname.deleter
    def nickname(self):
        self.options.set('Properties', 'nickname', 'None')
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
        return self.options.get('Properties', 'prefix') if self.options.get('Properties', 'prefix') != 'None' else None

    @prefix.setter
    def prefix(self, n):
        self.options.set('Properties', 'prefix', n)
        self.__write()

    @prefix.deleter
    def prefix(self):
        self.options.set('Properties', 'prefix', 'None')
        self.__write()

    @property
    def logging(self):
        self.__read()
        return True if self.options.get('Logging', 'logging') == 'True' else False

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
        return True if self.options.get('Logging', 'logMessages') == 'True' else False

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
        return True if self.options.get('Logging', 'logBotActivities') == 'True' else False

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
        return True if self.options.get('Logging', 'logUserActivities') == 'True' else False

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
        return True if self.options.get('Games', 'trackGameHistory') == 'True' else False

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
        return True if self.options.get('Games', 'trackGameStatistics') == 'True' else False

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
        return True if self.options.get('Games', 'autoCreateGameRoles') == 'True' else False

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
        return True if self.options.get('Games', 'autoCreateTemporaryGameRoles') == 'True' else False

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
        return True if self.options.get('Games', 'autoAddGames') == 'True' else False

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
        return True if self.options.get('Games', 'autoGiveGameRoles') == 'True' else False

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
        if n == 0:
            self.options.set('Permissions', 'defaultCommandPermissions', 'spectator')
        elif n == 1:
            self.options.set('Permissions', 'defaultCommandPermissions', 'user')
        elif n == 2:
            self.options.set('Permissions', 'defaultCommandPermissions', 'friend')
        elif n == 3:
            self.options.set('Permissions', 'defaultCommandPermissions', 'admin')
        self.__write()

    @staticmethod
    def list2string(l):
        return ", ".join(l)

    @staticmethod
    def string2list(s):
        return s.split(", ")

if __name__ == '__main__':
    b = Base()
