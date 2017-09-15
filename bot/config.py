import os
import shutil
import traceback
import configparser
import fileinput

from .exceptions import HelpfulError


class Config:
    def __init__(self, config_file):
        self.config_file = config_file
        config = configparser.ConfigParser()

        if not config.read(config_file, encoding='utf-8'):
            print('[config] Config file not found, copying example_options.ini')

            try:
                shutil.copy('config/example_options.ini', config_file)

                # load the config again and check to see if the user edited that one
                c = configparser.ConfigParser()
                c.read(config_file, encoding='utf-8')

                if not int(c.get('Permissions', 'OwnerID', fallback=0)):
                    print("\nPlease configure config/options.ini and restart the bot.", flush=True)
                    os._exit(1)

            except FileNotFoundError as e:
                raise HelpfulError(
                    "Your config files are missing.  Neither options.ini nor example_options.ini were found.",
                    "Grab the files back from the archive or remake them yourself and copy paste the content "
                    "from the repo.  Stop removing important files!"
                )

            except ValueError: # Config id value was changed but its not valid
                print("\nInvalid value for OwnerID, config cannot be loaded.")
                # TODO: HelpfulError
                os._exit(4)

            except Exception as e:
                print(e)
                print("\nUnable to copy config/example_options.ini to %s" % config_file, flush=True)
                os._exit(2)

        config = configparser.ConfigParser(interpolation=None)
        config.read(config_file, encoding='utf-8')

        confsections = {"Credentials", "Permissions", "Chat"}.difference(config.sections())
        if confsections:
            raise HelpfulError(
                "One or more required config sections are missing.",
                "Fix your config.  Each [Section] should be on its own line with "
                "nothing else on it.  The following sections are missing: {}".format(
                    ', '.join(['[%s]' % s for s in confsections])
                ),
                preface="An error has occured parsing the config:\n"
            )

        self._login_token = config.get('Credentials', 'Token', fallback=ConfigDefaults.token)

        self.auth = None
        self.logger = config.get('Debugging', 'Logger', fallback=ConfigDefaults.logger)
        self.logtofile = config.get('Debugging', 'LogToFile', fallback=ConfigDefaults.logtofile)
        self.owner_id = config.get('Permissions', 'OwnerID', fallback=ConfigDefaults.owner_id)
        self.command_prefix = config.get('Chat', 'CommandPrefix', fallback=ConfigDefaults.command_prefix)

        self.blacklist_file = config.get('Files', 'BlacklistFile', fallback=ConfigDefaults.blacklist_file)



        self.run_checks()



    def run_checks(self):
        """
        Validation logic for bot settings.
        """
        confpreface = "An error has occured reading the config:\n"



        if not self._login_token:
            raise HelpfulError(
                "No login credentials were specified in the config.",

                "Please fill in either the Email and Password fields, or "
                "the Token field.  The Token field is for Bot accounts only.",
                preface=confpreface
            )

        else:
            self.auth = (self._login_token,)

        if self.owner_id and self.owner_id.isdigit():
            if int(self.owner_id) < 10000:
                raise HelpfulError(
                    "OwnerID was not set.",

                    "Please set the OwnerID in the config.  If you "
                    "don't know what that is, use the %sid command" % self.command_prefix,
                    preface=confpreface)

        else:
            raise HelpfulError(
                "An invalid OwnerID was set.",

                "Correct your OwnerID.  The ID should be just a number, approximately "
                "18 characters long.  If you don't know what your ID is, "
                "use the %sid command.  Current invalid OwnerID: %s" % (self.command_prefix, self.owner_id),
                preface=confpreface)


    # TODO: Add save function for future editing of options with commands

    def write_default_config(self, location):
        pass


class ConfigDefaults:
    token = None    #This is not where you put your login info, go away.

    owner_id = None
    command_prefix = '!'

    delete_messages = True
    delete_invoking = False
    logtofile = None
    logger = "NOTSET"

    options_file = 'config/options.ini'
    blacklist_file = 'config/blacklist.txt'

# These two are going to be wrappers for the id lists, with add/remove/load/save functions
# and id/object conversion so types aren't an issue
class Blacklist:
    pass

class Whitelist:
    pass

class Games:
    pass
