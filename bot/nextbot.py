#!/usr/bin/env python
# -*- coding: utf-8 -*-

import discord
import asyncio
import random
import logging
import aiohttp
import os
import sys
import time
import shlex
import shutil
import inspect
import traceback
import configparser


from discord import utils
from discord.object import Object
from discord.enums import ChannelType
from discord.voice_client import VoiceClient
from discord.ext import commands
from discord.ext.commands.bot import _get_variable

from io import BytesIO
from functools import wraps
from textwrap import dedent
from datetime import timedelta
from random import choice, shuffle
from collections import defaultdict


from bot.config import Config, ConfigDefaults
from bot.permissions import Permissions, PermissionsDefaults
from bot.utils import load_file, write_file, sane_round_int

from . import exceptions
from .constants import VERSION as BOTVERSION

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)


class Response:
    def __init__(self, content, reply=False, delete_after=0):
        self.content = content
        self.reply = reply
        self.delete_after = delete_after


class NextBot(discord.Client):
    def __init__(self, config_file=ConfigDefaults.options_file, perms_file=PermissionsDefaults.perms_file):
        self.players = {}
        self.locks = defaultdict(asyncio.Lock)
        self.end = False
        self.config = Config(config_file)
        self.permissions = Permissions(perms_file, grant_all=[self.config.owner_id])

        self.blacklist = set(load_file(self.config.blacklist_file))

        self.exit_signal = None
        self.init_ok = False
        self.cached_client_id = None


        ssd_defaults = {'last_np_msg': None, 'auto_paused': False}
        self.server_specific_data = defaultdict(lambda: dict(ssd_defaults))

        super().__init__()
        self.aiosession = aiohttp.ClientSession(loop=self.loop)
        self.http.user_agent += ' AdminBot/%s' % BOTVERSION
        self.statustimer = 0

        self.timer = 0


        #FIXME Logger level
        """
        if self.config.logtofile == True:

            logger = logging.getLogger('discord')


            if self.config.logger == "DEBUG":
                logger.setLevel(logging.DEBUG)
            elif self.config.logger == "INFO":
                logger.setLevel(logging.INFO)
            elif self.config.logger == "WARNING":
                logger.setLevel(logging.WARNING)
            elif self.config.logger == "ERROR":
                logger.setLevel(logging.ERROR)
            elif self.config.logger == "CRITICAL":
                logger.setLevel(logging.CRITICAL)
            else:
                logger.setLevel(logging.NOTSET)

                handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
                handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
                logger.addHandler(handler)
        #FIXME Output to console
        elif self.config.logtofile == False:
            if self.config.logger == "DEBUG":
                logging.basicConfig(level=logging.DEBUG)
            elif self.config.logger == "INFO":
                logging.basicConfig(level=logging.INFO)
            elif self.config.logger == "WARNING":
                logging.basicConfig(level=logging.WARNING)
            elif self.config.logger == "ERROR":
                logging.basicConfig(level=logging.ERROR)
            elif self.config.logger == "CRITICAL":
                logging.basicConfig(level=logging.CRITICAL)
            else:
                logging.basicConfig(level=logging.NOTSET)

        else:
            pass
    """

    # TODO: Add some sort of `denied` argument for a message to send when someone else tries to use it
    def owner_only(func):
        @wraps(func)
        async def wrapper(self, *args, **kwargs):
            # Only allow the owner to use these commands
            orig_msg = _get_variable('message')

            if not orig_msg or orig_msg.author.id == self.config.owner_id:
                return await func(self, *args, **kwargs)
            else:
                raise exceptions.PermissionsError("Only the owner can use this command..", expire_in=30)

        return wrapper


    @staticmethod
    def _fixg(x, dp=2):
        return ('{:.%sf}' % dp).format(x).rstrip('0').rstrip('.')


    def _get_owner(self, voice=False):
        if voice:
            for server in self.servers:
                for channel in server.channels:
                    for m in channel.voice_members:
                        if m.id == self.config.owner_id:
                            return m
        else:
            return discord.utils.find(lambda m: m.id == self.config.owner_id, self.get_all_members())


    async def _wait_delete_msg(self, message, after):
        await asyncio.sleep(after)
        await self.safe_delete_message(message)


    async def generate_invite_link(self, *, permissions=None, server=None):
        if not self.cached_client_id:
            appinfo = await self.application_info()
            self.cached_client_id = appinfo.id

        return discord.utils.oauth_url(self.cached_client_id, permissions=permissions, server=server)


    async def safe_send_message(self, dest, content, *, tts=False, expire_in=0, also_delete=None, quiet=False):
        msg = None
        try:
            msg = await self.send_message(dest, content, tts=tts)

            if msg and expire_in:
                asyncio.ensure_future(self._wait_delete_msg(msg, expire_in))

            if also_delete and isinstance(also_delete, discord.Message):
                asyncio.ensure_future(self._wait_delete_msg(also_delete, expire_in))

        except discord.Forbidden:
            if not quiet:
                self.safe_print("Warning: Cannot send message to %s, no permission" % dest.name)

        except discord.NotFound:
            if not quiet:
                self.safe_print("Warning: Cannot send message to %s, invalid channel?" % dest.name)

        return msg


    async def safe_delete_message(self, message, *, quiet=False):
        try:
            return await self.delete_message(message)

        except discord.Forbidden:
            if not quiet:
                self.safe_print("Warning: Cannot delete message \"%s\", no permission" % message.clean_content)

        except discord.NotFound:
            if not quiet:
                self.safe_print("Warning: Cannot delete message \"%s\", message not found" % message.clean_content)


    async def safe_edit_message(self, message, new, *, send_if_fail=False, quiet=False):
        try:
            return await self.edit_message(message, new)

        except discord.NotFound:
            if not quiet:
                self.safe_print("Warning: Cannot edit message \"%s\", message not found" % message.clean_content)
            if send_if_fail:
                if not quiet:
                    print("Sending instead")
                return await self.safe_send_message(message.channel, new)


    def safe_print(self, content, *, end='\n', flush=True):
        sys.stdout.buffer.write((content + end).encode('utf-8', 'replace'))
        if flush: sys.stdout.flush()


    async def send_typing(self, destination):
        try:
            return await super().send_typing(destination)
        except discord.Forbidden:
            if self.config.debug_mode:
                print("Could not send typing to %s, no permssion" % destination)


    async def edit_profile(self, **fields):
        if self.user.bot:
            return await super().edit_profile(**fields)
        else:
            return await super().edit_profile(self.config._password,**fields)


    def _cleanup(self):
        try:
            self.loop.run_until_complete(self.logout())
        except: # Can be ignored
            pass

        pending = asyncio.Task.all_tasks()
        gathered = asyncio.gather(*pending)

        try:
            gathered.cancel()
            self.loop.run_until_complete(gathered)
            gathered.exception()
        except: # Can be ignored
            pass


    # noinspection PyMethodOverriding
    def run(self):
        try:
            self.loop.run_until_complete(self.start(*self.config.auth))

        except discord.errors.LoginFailure:
            # Add if token, else
            raise exceptions.HelpfulError(
                "Bot cannot login, bad credentials.",
                "Fix your Token in the options file.  "
                "Remember that each field should be on their own line.")
        except KeyboardInterrupt:
            try:
                self._cleanup()
            except Exceptison as e:
                print("Error in cleanup:", e)
            self.loop.run_until_complete(self.logout())

        finally:
            try:
                self._cleanup()
            except Exception as e:
                print("Error in cleanup:", e)
            self.logout()
            self.loop.close()
            if self.exit_signal:
                raise self.exit_signal


    ####################################################API Methods############################################################


    async def on_ready(self):


        print('')
        print('-----------------------------------------------------\n')
        if self.config.owner_id == self.user.id:
            raise exceptions.HelpfulError(
                "Your OwnerID is incorrect or you've used the wrong credentials.",

                "The bot needs its own account to function.  "
                "The OwnerID is the id of the owner, not the bot.  "
                "Figure out which one is which and use the correct information.")

        self.init_ok = True

        self.safe_print("Logged in as %s/%s#%s" % (self.user.id, self.user.name, self.user.discriminator))

        owner = self._get_owner()
        if owner and self.servers:
            self.safe_print("Owner: %s/%s#%s\n" % (owner.id, owner.name, owner.discriminator))

            print('Server List:')
            [self.safe_print(' - ' + s.name) for s in self.servers]

        elif self.servers:
            print("Owner could not be found on any server (id: %s)\n" % self.config.owner_id)

            print('Server List:')
            [self.safe_print(' - ' + s.name) for s in self.servers]

        else:
            print("Owner unknown, bot is not on any servers.")
            if self.user.bot:
                print("\nTo make the bot join a server, paste this link in your browser.")
                print("Note: You should be logged into your main account and have \n"
                      "manage server permissions on the server you want the bot to join.\n")
                print("    " + await self.generate_invite_link())

        print()
        useragent = self.http.user_agent.replace("Pyt", "\nPyt").replace("aiohttp", "\naiohttp").replace("Admin", "\nNext")
        print(useragent)
        print()
        print('-----------------------------------------------------\n')

        #TODO Expand Options
        print("Options:")

        self.safe_print("  Command prefix: " + self.config.command_prefix)
        self.safe_print("  Logging Level: " + self.config.logger)
        self.safe_print("  Log to file: " + self.config.logtofile)

        print()
        print('-----------------------------------------------------\n')


        #Clear temporary channel sequenze:
        await self.dump()


    async def on_resumed(self):
        print("The last session was not ended clearly..")


    async def on_message(self, message):
        await self.wait_until_ready()

        message_content = message.content.strip()

        if not message_content.startswith(self.config.command_prefix):
            if (message.content).lower().replace("?","") == 'what is the prefix':
                command_prefix=self.config.command_prefix
                await self.send_message(message.channel, "The prefix is set to %s" % self.config.command_prefix)
                return
            elif (message.content).lower() == "hi" or (message.content).lower() == "hello" or (message.content).lower() == "hallo":
                await self.send_message(message.channel, 'Hello {0.author.mention}'.format(message))
                return
            elif (message.content).lower().replace("?","") == "what is the sense of life" or (message.content).lower().replace("?","") == "the answer to the question of life, the universe and everything":
                await self.send_message(message.channel, '42!')
                return
            else:
                return

        if message.author == self.user:
            return



        command, *args = message_content.split()  # Uh, doesn't this break prefixes with spaces in them (it doesn't, config parser already breaks them)
        command = command[len(self.config.command_prefix):].lower().strip()

        handler = getattr(self, 'cmd_%s' % command, None)
        if not handler:
            return

        if message.channel.is_private:
            if not (message.author.id == self.config.owner_id and command == 'joinserver'):
                await self.send_message(message.channel, 'You cannot use this bot in private messages.')
                return

        if message.author.id in self.blacklist and message.author.id != self.config.owner_id:
            self.safe_print("[User blacklisted] {0.id}/{0.name} ({1})".format(message.author, message_content))
            return

        else:
            self.safe_print("[Command] {0.id}/{0.name} ({1})".format(message.author, message_content))

        user_permissions = self.permissions.for_user(message.author)

        argspec = inspect.signature(handler)
        params = argspec.parameters.copy()

        # noinspection PyBroadException
        try:

            handler_kwargs = {}
            if params.pop('message', None):
                handler_kwargs['message'] = message

            if params.pop('channel', None):
                handler_kwargs['channel'] = message.channel

            if params.pop('author', None):
                handler_kwargs['author'] = message.author

            if params.pop('server', None):
                handler_kwargs['server'] = message.server

            if params.pop('permissions', None):
                handler_kwargs['permissions'] = user_permissions

            if params.pop('user_mentions', None):
                handler_kwargs['user_mentions'] = list(map(message.server.get_member, message.raw_mentions))

            if params.pop('channel_mentions', None):
                handler_kwargs['channel_mentions'] = list(map(message.server.get_channel, message.raw_channel_mentions))

            if params.pop('voice_channel', None):
                handler_kwargs['voice_channel'] = message.server.me.voice_channel

            if params.pop('leftover_args', None):
                handler_kwargs['leftover_args'] = args

            args_expected = []
            for key, param in list(params.items()):
                doc_key = '[%s=%s]' % (key, param.default) if param.default is not inspect.Parameter.empty else key
                args_expected.append(doc_key)

                if not args and param.default is not inspect.Parameter.empty:
                    params.pop(key)
                    continue

                if args:
                    arg_value = args.pop(0)
                    handler_kwargs[key] = arg_value
                    params.pop(key)

            if message.author.id != self.config.owner_id:
                if user_permissions.command_whitelist and command not in user_permissions.command_whitelist:
                    raise exceptions.PermissionsError(
                        "This command is not enabled for your group (%s)." % user_permissions.name,
                        expire_in=20)

                elif user_permissions.command_blacklist and command in user_permissions.command_blacklist:
                    raise exceptions.PermissionsError(
                        "This command is disabled for your group (%s)." % user_permissions.name,
                        expire_in=20)

            if params:
                docs = getattr(handler, '__doc__', None)
                if not docs:
                    docs = 'Usage: {}{} {}'.format(
                        self.config.command_prefix,
                        command,
                        ' '.join(args_expected)
                    )

                docs = '\n'.join(l.strip() for l in docs.split('\n'))
                await self.safe_send_message(
                    message.channel,
                    '```\n%s\n```' % docs.format(command_prefix=self.config.command_prefix),
                    expire_in=60
                )
                return

            response = await handler(**handler_kwargs)
            if response and isinstance(response, Response):
                content = response.content
                if response.reply:
                    content = '%s, %s' % (message.author.mention, content)

                sentmsg = await self.safe_send_message(
                    message.channel, content,
                    expire_in=response.delete_after,
                    also_delete=message
                )


        except (exceptions.CommandError, exceptions.HelpfulError, exceptions.ExtractionError) as e:
            print("{0.__class__}: {0.message}".format(e))

            expirein = e.expire_in if self.config.delete_messages else None
            alsodelete = message if self.config.delete_invoking else None

            await self.safe_send_message(
                message.channel,
                '```\n%s\n```' % e.message,
                expire_in=expirein,
                also_delete=alsodelete
            )

        except exceptions.Signal:
            raise

        except Exception:
            traceback.print_exc()


    async def on_error(self, event, *args, **kwargs):
        ex_type, ex, stack = sys.exc_info()

        if ex_type == exceptions.HelpfulError:
            print("Exception in", event)
            print(ex.message)

            await asyncio.sleep(2)  # don't ask
            await self.logout()

        elif issubclass(ex_type, exceptions.Signal):
            self.exit_signal = ex_type
            await self.logout()

        else:
            traceback.print_exc()


    async def on_message_edit(self, before, after):
        await self.on_message(after)


    async def on_member_update(self, before, after):

        #Check the game that is played
        if before.game != after.game and after.game != None and self.statustimer == 0:
            self.statustimer = 2
            config = configparser.ConfigParser(interpolation=None)
            config.read(self.config.game_file, encoding='utf-8')
            playedgame = None
            partof = False
            gameexist = False
            #Researches all registered games
            for game in self.config.allgamenames:
                #Check if members game is registered
                if after.game.name == game:
                    gameexist = True
                    #Researches all sections
                    for section in config.sections():
                        #Check to which game the name is depend on
                        namesraw = config.get(section, "names")
                        nameslist = namesraw.split(", ")
                        for name in nameslist:
                            if after.game.name == name:
                                membersraw = config.get(section, "members", fallback="")
                                memberslist = membersraw.split(", ")
                                for member in memberslist:
                                    if after.name == member:
                                        partof = True
                                        break
                                sectionsave = section

            if partof == False and gameexist == True:
                searchline = "[" + sectionsave + "]\n"
                gameconfig = open(self.config.game_file, "r")
                gamesfilecontent = gameconfig.readlines()
                line = False
                for i in range(len(gamesfilecontent)):
                    if searchline == gamesfilecontent[i]:
                        line = i+2
                        break
                gameconfig.close()
                gameconfig = open(self.config.game_file, "w")
                length = len(gamesfilecontent[line])
                if (gamesfilecontent[line])[length-3:length] == "= \n":
                    writecontent = gamesfilecontent[line] + after.name
                elif (gamesfilecontent[line])[length-2:length] == "=\n":
                    writecontent = gamesfilecontent[line] + " " + after.name
                else:
                    writecontent = gamesfilecontent[line] + ", " + after.name
                writecontent = writecontent.replace("\n", "")
                writecontent += "\n"
                gamesfilecontent[line] = writecontent

                gameconfig.writelines(gamesfilecontent)
                gameconfig.close()



        elif before.game != after.game and after.game != None and self.statustimer == 2:
            self.statustimer = 1

        elif before.game != after.game and after.game != None and self.statustimer == 1:
            self.statustimer = 0


    async def on_server_join(self, server):
        for server in self.servers:
            for member in server.members:
                if member.id == self.config.owner_id:
                    owner = member

        await self.send_message(owner, ("I has been added to "))

    ########################################################General#############################################################


    async def cmd_help(self, message, command=None):
        """
        Usage:
            {command_prefix}help [command]

        Prints a help message.
        If a command is specified, it prints a help message for that command.
        Otherwise, it lists the available commands.
        """
        if message.channel.name == "bot-control":
            return
        if command:
            cmd = getattr(self, 'cmd_' + command, None)
            if cmd:
                return Response(
                    "```\n{}```".format(
                        dedent(cmd.__doc__),
                        command_prefix=self.config.command_prefix
                    ),
                    delete_after=60
                )
            else:
                return Response("No such command", delete_after=10)

        else:
            helpmsg = "**Commands**\n```"
            commands = []

            for att in dir(self):
                delete = True
                cmds = ['cmd_help', 'cmd_helpstatic', 'cmd_ggt', 'cmd_ggtalternate', 'cmd_äqyptmultiplikation', 'cmd_shutdownsurrogate', 'cmd_helpstatic']
                for dummy in cmds:
                    if att == dummy:
                        delete = False
                if att.startswith('cmd_') and delete == True:
                    command_name = att.replace('cmd_', '').lower()
                    commands.append("{}{}".format(self.config.command_prefix, command_name))

            helpmsg += "\n".join(commands)
            helpmsg += "```"

            return Response(helpmsg, reply=True, delete_after=90)


    async def cmd_helpstatic(self, message, command=None):
        """
        Usage:
            {command_prefix}help [command]

        Prints a help message.
        If a command is specified, it prints a help message for that command.
        Otherwise, it lists the available commands.
        """
        if message.channel.name == "bot-control":
            return

        if command:
            cmd = getattr(self, 'cmd_' + command, None)
            if cmd:
                return Response(
                    "```\n{}```".format(
                        dedent(cmd.__doc__),
                        command_prefix=self.config.command_prefix
                    ),
                    delete_after=60
                )
            else:
                return Response("No such command", delete_after=10)

        else:
            helpmsg = "**Commands**\n```"
            commands = []

            for att in dir(self):
                delete = True
                cmds = ['cmd_help', 'cmd_helpstatic', 'cmd_ggt', 'cmd_ggtalternate', 'cmd_äqyptmultiplikation', 'cmd_shutdownsurrogate', 'cmd_helpstatic']
                for dummy in cmds:
                    if att == dummy:
                        delete = False
                if att.startswith('cmd_') and delete == True:
                    command_name = att.replace('cmd_', '').lower()
                    commands.append("{}{}".format(self.config.command_prefix, command_name))

            helpmsg += "\n".join(commands)
            helpmsg += "```"
            await self.clear(message, 1)
            return Response(helpmsg, reply=True)


    #TODO Repair restart/shutdown
    async def cmd_restart(self, message, channel):
        if message.channel.name == "bot-control":
            return
        #await self.safe_send_message(channel, "Wait a second :wink:")
        #raise exceptions.RestartSignal
        return Response("Not available now", delete_after=20)


    #FIXME Unclosed session Error
    async def cmd_shutdown(self, message, channel):
        if message.channel.name == "bot-control":
            return
        await self.safe_send_message(channel, "Good bye :wave:")
        raise exceptions.TerminateSignal



    ######################################################Bot Settings###########################################################


    @owner_only
    async def cmd_setname(self, message, leftover_args, name):
        """
        Usage:
            {command_prefix}setname name

        Changes the bot's username.
        Note: This operation is limited by discord to twice per hour.
        """
        if message.channel.name == "bot-control":
            return

        name = ' '.join([name, *leftover_args])

        try:
            await self.edit_profile(username=name)
        except Exception as e:
            raise exceptions.CommandError(e, expire_in=20)

        return Response(":ok_hand:", delete_after=20)


    @owner_only
    async def cmd_setavatar(self, message, url=None):
        """
        Usage:
            {command_prefix}setavatar [url]

        Changes the bot's avatar.
        Attaching a file and leaving the url parameter blank also works.
        """
        if message.channel.name == "bot-control":
            return

        if message.attachments:
            thing = message.attachments[0]['url']
        else:
            thing = url.strip('<>')

        try:
            with aiohttp.Timeout(10):
                async with self.aiosession.get(thing) as res:
                    await self.edit_profile(avatar=await res.read())

        except Exception as e:
            raise exceptions.CommandError("Unable to change avatar: %s" % e, expire_in=20)

        return Response(":ok_hand:", delete_after=20)


    async def cmd_setnick(self, message, server, channel, leftover_args, nick):
        """
        Usage:
            {command_prefix}setnick nick

        Changes the bot's nickname.
        """
        if message.channel.name == "bot-control":
            return

        if not channel.permissions_for(server.me).change_nickname:
            raise exceptions.CommandError("Unable to change nickname: no permission.")

        nick = ' '.join([nick, *leftover_args])

        try:
            await self.change_nickname(server.me, nick)
        except Exception as e:
            raise exceptions.CommandError(e, expire_in=20)

        return Response(":ok_hand:", delete_after=20)


    ##########################################################Tools##############################################################


    async def cmd_clear(self, message, leftover_args):
        """
        Usage:
            {command_prefix}clear number/all

        Clears the specified number of messages in the chat history.
        This can take time in cause of the server side rage limit.
        """
        mess = []
        if leftover_args[0] == "all":
            async for log in self.logs_from(message.channel, limit=300):
                mess.append(log)
            figure = len(mess) + 1
        else:
            try:
                figure = int(leftover_args[0]) +1
                async for log in self.logs_from(message.channel, limit=300):
                    mess.append(log)
            except TypeError:
                if message.channel.name == "bot-control":
                    return
                else:
                    return Response("Bad input. Please just take integers or 'all' as argument")
        for j in range(figure):
            try:
                await self.delete_message(mess[j])
            except IndexError:
                pass

        #NOBUG Warning in cause of impossibility to delete deleted messages
        return Response("I deleted %s messages" % leftover_args[0], delete_after=25)


    async def cmd_kick(self, message, name):
        """
        Usage:
            {command_prefix}kick member

        Kicks a member from the server.
        """
        for member in message.server.members:
            if member.name == name:
                await self.kick(member)
                return Response("Succesfully kicked %s" % name, delete_after=30)
        return Response("Couldn't find user..", delete_after=30)


    async def cmd_ban(self, message, name, leftover_args):
        """
        Usage:
            {command_prefix}ban member delete_days(optional)

        Bans a member from the server. You can delete all messages of this
        member up to 7 days by setting a value between 1 and 7 for
        delete_days (this is optional).
        """
        try:
            number = int(leftover_args[0])
        except:
            number = 0

        for member in message.server.members:
            if member.name == name:
                await self.ban(member, number)
                return Response("Succesfully banned %s" % name, delete_after=30)
        return Response("Couldn't find user..", delete_after=30)


    async def cmd_unban(self, message, server, name):
        """
        Usage:
            {command_prefix}unban user

        Unbans a user from the server.
        """
        bans = await self.get_bans(server)
        for member in bans:
            if member.name == name:
                await self.unban(server, member)
                return Response("Succesfully unbanned %s" % name, delete_after=30)
        return Response("Couldn't find banned user..", delete_after=30)


    async def cmd_getbans(self, server):
        """
        Usage:
            {command_prefix}listbans

        Shows a list of users banned at the current server.
        """
        bans = await self.get_bans(server)
        for member in bans:
            try:
                answer += "\n"
            except:
                answer = ""
            answer += member.name
        try:
            return Response(answer, delete_after=30)
        except UnboundLocalError:
            return Response("No banned users at this server.", delete_after=30)


    async def cmd_dump(self, server):
        channels = []
        for channel in server.channels:
            channels.append(channel)

        for channel in channels:
            if channel.type != discord.ChannelType.voice:
                pass
            else:
                length = len(channel.name)
                if channel.name[length-3:length] == "(t)":
                    await self.delete_channel(channel)


    async def cmd_gathering(self, server, group, leftover_args):
        #for member in server.members:
        #    if member.voice_channel != None:
        #        for group in member.
        for part in leftover_args:
            try:
                voiced += " "
                voiced += part
            except UnboundLocalError:
                voiced = part
        print(voiced)
        for channel in server.channels:
            if channel.name == voiced and channel.type == discord.ChannelType.voice:
                voice = channel
        print(voice)

        collect = ""
        for member in server.members:
            for role in member.roles:
                if role.name == group:
                    await self.move_member(member, voice)
        return Response("Moved members :thumbsup:", delete_after=5)

    async def cmd_sendlog(self, message, author):
        """
        Usage:
            {command_prefix}sendlog

        Sends you the log file into a private channel.
        """
        await self.send_file(author, 'discord.log')
        return Response(":mailbox_with_mail:", delete_after=5)


    async def cmd_pin(self, message):
        messages = []
        async for log in self.logs_from(message.channel, limit=2):
            messages.append(log)
        await self.pin_message(messages[1])
        return Response("Pinned message :thumbsup:", delete_after=5)


    #####################################################Right Management########################################################



    ####################################################Channel Management#######################################################


    async def cmd_crchannel(self, message, name):
        """
        Usage:
            {command_prefix}crchannel name

        Creates a channel
        Text-only
        """
        #TODO Add support for ä ö ü ß – fixed?

        kind = discord.ChannelType.text

        await self.create_channel(server=message.server, type=kind, name=name)
        return Response("Channel successful created!", delete_after=30)


    async def cmd_crpchannel(self, message, name):
        """
        Usage:
            {command_prefix}crpchannel name

        Creates a private channel
        WARNING: Private channel creation works not at the moment!
        Text-only
        """

        allowaccess = discord.PermissionOverwrite(read_messages=True)
        denyaccess = discord.PermissionOverwrite(read_messages=False)
        default = discord.ChannelPermissions(target=message.server.default_role, overwrite=denyaccess)
        creator = discord.ChannelPermissions(target=message.server.me, overwrite=allowaccess)

        kind = discord.ChannelType.text

        #BUG Syntax invalid
        """
        await self.create_channel(server=message.server, type=kind, name=name, default, creator)
        return Response("Private channel successful created!", delete_after=30)
        """
        return Response("Not usable in this version", delete_after=30)


    async def cmd_crvchannel(self, message, leftover_args):
        """
        Usage:
            {command_prefix}crvchannel name

        Creates a channel
        Voice-only
        """

        kind = discord.ChannelType.voice

        for part in leftover_args:
            try:
                name += " "
            except:
                name = ""
            name += part

        await self.create_channel(server=message.server, type=kind, name=name)
        return Response("Voice-channel successful created!", delete_after=30)


    async def cmd_crpvchannel(self, message, leftover_args):
        """
        Usage:
            {command_prefix}crpvchannel name

        Creates a private voice channel
        WARNING: Private channel creation works not at the moment!
        Voice-only
        """

        allowaccess = discord.PermissionOverwrite(read_messages=True)
        denyaccess = discord.PermissionOverwrite(read_messages=False)
        default = discord.ChannelPermissions(target=message.server.default_role, overwrite=denyaccess)
        creator = discord.ChannelPermissions(target=message.server.me, overwrite=allowaccess)

        kind = discord.ChannelType.voice

        for part in leftover_args:
            try:
                name += " "
            except:
                name = ""
            name += part

        #BUG Syntax invalid
        """
        await self.create_channel(server=message.server, type=kind, name=name, default, creator)
        return Response("Private voice-channel successful created!", delete_after=30)
        """
        return Response("Not usable in this version", delete_after=30)


    async def cmd_crtempchannel(self, message, leftover_args):
        """
        Usage:
            {command_prefix}crtempchannel name

        Creates a temporary voice channel. It will be deleted at the next restart
        or manually with {command_prefix}dump
        Voice-only
        """

        kind = discord.ChannelType.voice

        for part in leftover_args:
            try:
                name += " "
            except:
                name = ""
            name += part
        name += " (t)"
        await self.create_channel(server=message.server, type=kind, name=name)
        return Response("Temporary voice-channel successful created!", delete_after=30)


    async def cmd_rmchannel(self, message, name):
        """
        Usage:
            {command_prefix}rmchannel name

        Removes a text channel.
        Text-only
        """
        chan = message.server.channels
        deleted = False
        kind = discord.ChannelType.text

        for element in chan:
            if element.name == name and element.type == kind:
                await self.delete_channel(element)
                deleted = True
                break

        if deleted == True:
            return Response("Channel succesfully removed!", delete_after=30)
        else:
            return Response("Nothing happend..", delete_after=30)


    async def cmd_rmvchannel(self, message, leftover_args):
        """
        Usage:
            {command_prefix}rmvchannel name

        Removes a voice-channel.
        Voice-only
        """
        for part in leftover_args:
            try:
                name += " "
            except:
                name = ""
            name += part
        chan = message.server.channels
        deleted = False
        kind = discord.ChannelType.voice
        for element in chan:
            if element.name == name and element.type == kind:
                await self.delete_channel(element)
                deleted = True
                break

        if deleted == True:
            return Response("Voice-channel succesfully removed!", delete_after=30)
        else:
            return Response("Nothing happend..", delete_after=30)


    async def cmd_rmcchannel(self, message, channel):
        """
        Usage:
            {command_prefix}rmtchannel

        Removes the current channel.
        """
        await self.delete_channel(channel)

        return Response("Channel succesfully removed!", delete_after=30)


    async def cmd_edchannel(self, message, name, value, leftover_args):
        """
        Usage:
            {command_prefix}edchannel name valuetyp
            valuetypes:
                topic
                bitrate(voice-only)
                userlimit(voice-only)
                role # Not impementated now
                name

        Edits a channel
        Text-only
        All commands are also seperated and more easy accessable
        """
        chan = message.server.channels
        edited = False
        kind = discord.ChannelType.text

        for element in chan:
            if element.name == name and element.type == kind:
                if value == "topic":
                    dummy = ""
                    for i in leftover_args:
                        dummy += i + " "
                    await self.edit_channel(element, topic=dummy)
                    edited = True
                elif value == "name":
                    await self.edit_channel(element, name=leftover_args[0])
                    edited = True
                #TODO Implement role edit
                '''
                elif value == "role":
                    dummy = ""
                    for i in leftover_args:
                        dummy += i + " "
                    await self.edit_channel(element, topic=dummy)
                    edited = True
                    '''

        if edited == True:
            return Response("Channel succesfully edited!", delete_after=30)
        else:
            return Response("Nothing happend..", delete_after=30)


    async def cmd_edvchannel(self, message, name, value, leftover_args):
        """
        Usage:
            {command_prefix}edchannel name valuetyp
            valuetypes:
                name
                topic
                bitrate(voice-only)
                userlimit(voice-only)
                role # Not impementated now

        Edits a voice channel
        Voice-only
        All commands are also seperated and more easy accessable
        """
        chan = message.server.channels
        edited = False
        kind = discord.ChannelType.voice

        for element in chan:
            if element.name == name and element.type == kind:
                if value == "topic":
                    dummy = ""
                    for i in leftover_args:
                        dummy += i + " "
                    await self.edit_channel(element, topic=dummy)
                    edited = True
                elif value == "bitrate" and element.type == discord.ChannelType.voice:
                    await self.edit_channel(element, bitrate=int(leftover_args[0])*1000)
                    edited = True
                elif value == "userlimit" and element.type == discord.ChannelType.voice:
                    await self.edit_channel(element, user_limit=int(leftover_args[0]))
                    edited = True
                elif value == "name":
                    await self.edit_channel(element, name=leftover_args[0])
                    edited = True
                #TODO Implement role edit
                '''
                elif value == "role":
                    dummy = ""
                    for i in leftover_args:
                        dummy += i + " "
                    await self.edit_channel(element, topic=dummy)
                    edited = True
                    '''

        if edited == True:
            return Response("Channel succesfully edited!", delete_after=30)
        else:
            return Response("Nothing happend..", delete_after=30)


    async def cmd_edbitrate(self, message, name, value):
        """
        Usage:
            {command_prefix}edbitrate name bitrate

        Edits the bitrate of a channel
        Voice-only
        """
        chan = message.server.channels
        edited = False

        kind = discord.ChannelType.voice
        for element in chan:
            if element.name == name and element.type == kind:
                await self.edit_channel(element, bitrate=(int(value)*1000))
                edited = True

        if edited == True:
            return Response("Bitrate succesfully edited!", delete_after=30)
        else:
            return Response("Nothing happend..", delete_after=30)


    async def cmd_edtopic(self, message, name, leftover_args):
        """
        Usage:
            {command_prefix}edtopic name topic

        Edits the topic of a channel
        Text-only
        """
        chan = message.server.channels
        edited = False
        kind = discord.ChannelType.text

        for element in chan:
            if element.name == name and element.type == kind:
                dummy = ""
                for i in leftover_args:
                    dummy += i + " "
                await self.edit_channel(element, topic=dummy)
                edited = True

        if edited == True:
            return Response("Topic succesfully edited!", delete_after=30)
        else:
            return Response("Nothing happend..", delete_after=30)


    async def cmd_edvtopic(self, message, name, leftover_args):
        """
        Usage:
            {command_prefix}edvtopic name topic

        Edits the topic of a voice channel
        Voice-only
        """
        chan = message.server.channels
        edited = False
        kind = discord.ChannelType.voice

        for element in chan:
            if element.name == name and element.type == kind:
                dummy = ""
                for i in leftover_args:
                    dummy += i + " "
                await self.edit_channel(element, topic=dummy)
                edited = True

        if edited == True:
            return Response("Topic succesfully edited!", delete_after=30)
        else:
            return Response("Nothing happend..", delete_after=30)


    async def cmd_edlimit(self, message, name, value):
        """
        Usage:
            {command_prefix}edbitrate name userlimit

        Sets the max number of users in a voice-channel
        Voice-only
        """
        chan = message.server.channels
        edited = False

        kind = discord.ChannelType.voice
        for element in chan:
            if element.name == name and element.type == kind:
                await self.edit_channel(element, user_limit=int(value))
                edited = True

        if edited == True:
            return Response("User limit succesfully edited!", delete_after=30)
        else:
            return Response("Nothing happend..", delete_after=30)


    async def cmd_edname(self, message, name, value):
        """
        Usage:
            {command_prefix}edname name newname

        Edits the name of a channel
        Text-only
        """
        chan = message.server.channels
        edited = False
        kind = discord.ChannelType.text

        for element in chan:
            if element.name == name and element.type == kind:
                await self.edit_channel(element, name=value)
                edited = True

        if edited == True:
            return Response("Name succesfully edited!", delete_after=30)
        else:
            return Response("Nothing happend..", delete_after=30)


    async def cmd_edvname(self, message, name, value):
        """
        Usage:
            {command_prefix}edvtopic name newname

        Edits the name of a voice channel
        Voice-only
        """
        chan = message.server.channels
        edited = False
        kind = discord.ChannelType.voice

        for element in chan:
            if element.name == name and element.type == kind:
                await self.edit_channel(element, name=value)
                edited = True

        if edited == True:
            return Response("Name succesfully edited!", delete_after=30)
        else:
            return Response("Nothing happend..", delete_after=30)


    #######################################################Information###########################################################


    async def cmd_serverinfo(self, message):
        """
        Usage:
            {command_prefix}serverinfo

        Shows information about the current server.
        """

        #Personal
        server = message.server
        message = "Information about the server:"
        message += "\n\nName: " + str(server.name)
        message += "\nOwner: " + str(server.owner)
        message += "\nOwner ID: " + str(server.owner_id)
        message += "\nRegion: " + str(server.region)

        message += "\nCreated at: " + str(server.created_at)
        message += "\nDefault role: " + str(server.default_role)
        text = ""
        for role in server.roles:
            text += str(role.name) + ", "
        length = len(text)
        text = text[0:length-2]
        message += "\nRoles: " + text
        message += "\nIcon URL: " + str(server.icon_url)
        message += "\nServer ID: " + str(server.id)
        message += "\nLarge (over 250 members): " + str(server.large)
        message += "\nCount of members: " + str(server.member_count)
        message += "\nVerification level: " + str(server.verification_level)
        text = ""
        for channel in server.channels:
            text += str(channel) + ", "
        length = len(text)
        text = text[0:length-2]
        message += "\nChannels: " + text
        message += "\nDefault channel: " + str(server.default_channel)
        message += "\nAfk channel: " + str(server.afk_channel)
        message += "\nTimeout (in seconds): " + str(server.afk_timeout)


        return Response(message, delete_after=120)


    async def cmd_info(self, message, person):
        """
        Usage:
            {command_prefix}info name

        Prints information about the given user
        Don't use the nickname of a user
        """
        members = message.server.members
        for member in members:
            if member.name == person:
                #Personal
                message = "Information about user general:"
                message += "\n\nName: " + str(member.name)
                message += "\nNick: " + str(member.nick)
                message += "\nMention: " + str(member.mention)
                message += "\nDiscriminator: " + str(member.discriminator)
                message += "\nId: " + str(member.id)
                message += "\nAvatar URL: " + str(member.avatar_url)
                message += "\nBot: " + str(member.bot)
                message += "\nStatus: " + str(member.status)
                message += "\nAFK: " + str(member.is_afk)
                message += "\nGame: " + str(member.game)
                message += "\nCreated_at: " + str(member.created_at)

                #Server specific
                message += "\n\nInformation about the user at this server:"
                message += "\n\nServer: " + str(member.server)
                message += "\nJoined at: " + str(member.joined_at)
                message += "\nAdministrator: " + str(member.server_permissions.administrator)
                message += "\nTop role: " + str(member.top_role)
                message += "\nColor: " + str(member.color)


                #Voice specific
                message += "\n\nInformation about the voice state:"
                message += "\n\nVoice channel: " + str(member.voice_channel)
                message += "\nDeaf: " + str(member.deaf)
                message += "\nSelf deaf: " + str(member.self_deaf)
                message += "\nMute: " + str(member.mute)
                message += "\nSelf mute: " + str(member.self_mute)
                return Response(message)


    async def cmd_id(self, message, author, user_mentions):
        """
        Usage:
            {command_prefix}id [@user]

        Tells the user their id or the id of another user.
        """
        if message.channel.name == "bot-control":
            return

        if not user_mentions:
            return Response('your id is `%s`' % author.id, reply=True, delete_after=35)
        else:
            usr = user_mentions[0]
            return Response("%s's id is `%s`" % (usr.name, usr.id), reply=True, delete_after=35)


    async def cmd_listids(self, message, server, author, leftover_args, cat='all'):
        """
        Usage:
            {command_prefix}listids [categories]

        Lists the ids for various things.  Categories are:
           all, users, roles, channels
        """
        if message.channel.name == "bot-control":
            return

        cats = ['channels', 'roles', 'users']

        if cat not in cats and cat != 'all':
            return Response(
                "Valid categories: " + ' '.join(['`%s`' % c for c in cats]),
                reply=True,
                delete_after=25
            )

        if cat == 'all':
            requested_cats = cats
        else:
            requested_cats = [cat] + [c.strip(',') for c in leftover_args]

        data = ['Your ID: %s' % author.id]

        for cur_cat in requested_cats:
            rawudata = None

            if cur_cat == 'users':
                data.append("\nUser IDs:")
                rawudata = ['%s #%s: %s' % (m.name, m.discriminator, m.id) for m in server.members]

            elif cur_cat == 'roles':
                data.append("\nRole IDs:")
                rawudata = ['%s: %s' % (r.name, r.id) for r in server.roles]

            elif cur_cat == 'channels':
                data.append("\nText Channel IDs:")
                tchans = [c for c in server.channels if c.type == discord.ChannelType.text]
                rawudata = ['%s: %s' % (c.name, c.id) for c in tchans]

                rawudata.append("\nVoice Channel IDs:")
                vchans = [c for c in server.channels if c.type == discord.ChannelType.voice]
                rawudata.extend('%s: %s' % (c.name, c.id) for c in vchans)

            if rawudata:
                data.extend(rawudata)

        with BytesIO() as sdata:
            sdata.writelines(d.encode('utf8') + b'\n' for d in data)
            sdata.seek(0)

            await self.send_file(author, sdata, filename='%s-ids-%s.txt' % (server.name.replace(' ', ''), cat))

        return Response(":mailbox_with_mail:", delete_after=20)


    async def cmd_listusers(self, message):
        """
        Usage:
            {command_prefix}listusers

        Shows all usernames with discriminator.
        """
        response = ""
        for member in message.server.members:
            response += str(member) + "\n"
        return Response(response, delete_after=20)


    async def cmd_shortcuts(self, message):
        """
        Usage:
            {command_prefix}shortcuts

        Explains the meaning of shorted words in commands
        """
        string = "cr = create"
        string += "\nrm = remnove"
        string += "\ned = edit"
        string += "\nv = voice"
        string += "\np = private"
        string += "\nt = this"
        return Response(string, delete_after=30)


    async def cmd_count(self, message):
        """
        Usage:
            {command_prefix}count

        Used to calculate the number of the own messages in a channel
        """
        await self.send_message(message.channel, 'Calculate number of your sended messages...')
        mess = []
        async for log in self.logs_from(message.channel, limit=1000):
            mess.append(log)
        counter = -1
        for element in mess:
            if element.author == message.author:
                counter += 1
        if counter == 998 or counter == 1000:
            await self.send_message(message.channel, 'You have sended over 1000 messages.')
        else:
            await self.send_message(message.channel, 'You have sended %s messages.' % counter)

        await asyncio.sleep(20)
        await self.clear(message, 3)
        return


    async def cmd_countall(self, message):
        """
        Usage:
            {command_prefix}countall

        Used to calculate the number of all messages in a channel
        """
        await self.send_message(message.channel, 'Calculate number of messages in this channel...')
        mess = []
        async for log in self.logs_from(message.channel, limit=1000):
            mess.append(log)
        counter = -2
        for element in mess:
            counter += 1
        if counter == 998 or counter == 1000:
            await self.send_message(message.channel, 'This channel includes over 1000 messages.')
        else:
            await self.send_message(message.channel, 'This channel includes %s messages.' % counter)

        await asyncio.sleep(20)
        await self.clear(message, 3)
        return



    #########################################################Features############################################################


    async def cmd_sleep(self, message, time):
        """
        Usage:
            {command_prefix}sleep time

        Let the bot sleep for a moment
        """
        await asyncio.sleep(int(time))
        return Response("Good morning! I'm fit again! :D", delete_after=20)


    async def cmd_stopwatch(self, message, command):
        """
        Usage:
            {command_prefix}stopwatch start/stop/status

        Handles a stopwatch.
        Attention: Their can only be one stopwatch on all servers at the moment. It will be fixed later.
        """
        #FIXME More stopwatches

        if command == "start":
            if self.timer != 0:
                response = "The time of the timer was running for " + str(time.time() - self.timer) + " seconds. It has been deleted and the new timer started."
            else:
                response = "The timer has been started."
            self.timer = time.time()
            return Response(response, delete_after=60)

        elif command == "stop":
            value = round(time.time() - self.timer, 2)
            self.timer = 0
            return Response("The time was %s seconds." % value, delete_after=60)

        elif command == "status":
            if self.timer != 0:
                return Response("The stopwatch run since %s seconds." % str(round(time.time() - self.timer, 2)), delete_after=60)
            else:
                return Response("The stopwatch isn't running.", delete_after=60)
        else:
            return Response("Cannot recognize you're command. Use %sstopwatch start/stop/status or %shelp stopwatch to see the help." % (self.config.command_prefix,self.config.command_prefix), delete_after=30)


    async def cmd_blacklist(self, message, user_mentions, option, something): #TODO Replacing with database?
        """
        Usage:
            {command_prefix}blacklist [ + | - | add | remove ] @UserName [@UserName2 ...]

        Add or remove users to the blacklist.
        Blacklisted users are forbidden from using bot commands.
        """

        if message.channel.name == "bot-control":
            return

        if not user_mentions:
            raise exceptions.CommandError("No users listed.", expire_in=20)

        if option not in ['+', '-', 'add', 'remove']:
            raise exceptions.CommandError(
                'Invalid option "%s" specified, use +, -, add, or remove' % option, expire_in=20
            )

        for user in user_mentions.copy():
            if user.id == self.config.owner_id:
                print("[Commands:Blacklist] The owner cannot be blacklisted.")
                user_mentions.remove(user)

        old_len = len(self.blacklist)

        if option in ['+', 'add']:
            self.blacklist.update(user.id for user in user_mentions)

            write_file(self.config.blacklist_file, self.blacklist)

            return Response(
                '%s users have been added to the blacklist' % (len(self.blacklist) - old_len),
                reply=True, delete_after=10
            )

        else:
            if self.blacklist.isdisjoint(user.id for user in user_mentions):
                return Response('none of those users are in the blacklist.', reply=True, delete_after=10)

            else:
                self.blacklist.difference_update(user.id for user in user_mentions)
                write_file(self.config.blacklist_file, self.blacklist)

                return Response(
                    '%s users have been removed from the blacklist' % (old_len - len(self.blacklist)),
                    reply=True, delete_after=10
                )








    async def cmd_perms(self, message, author, channel, server, permissions):
        """
        Usage:
            {command_prefix}perms

        Sends the user a list of their permissions.
        """
        if message.channel.name == "bot-control":
            return

        lines = ['Command permissions in %s\n' % server.name, '```', '```']

        for perm in permissions.__dict__:
            if perm in ['user_list'] or permissions.__dict__[perm] == set():
                continue

            lines.insert(len(lines) - 1, "%s: %s" % (perm, permissions.__dict__[perm]))

        await self.send_message(author, '\n'.join(lines))
        return Response(":mailbox_with_mail:", delete_after=20)
        ####




    ######################################################Please insert here######################################################


    async def cmd_addgame(self, message, name):

        pass





    ##############################################################################################################################







    async def clear(self, message, number):
        mess2 = []
        async for log in self.logs_from(message.channel, limit=100):
            mess2.append(log)
        for j in range(number):
            try:
                await self.delete_message(mess2[j])
            except IndexError:
                pass
        return


    async def dump(self):

        for server in self.servers:
            channels = []
            for channel in server.channels:
                channels.append(channel)

            for channel in channels:
                if channel.type != discord.ChannelType.voice:
                    pass
                else:
                    length = len(channel.name)
                    if channel.name[length-3:length] == "(t)":
                        await self.delete_channel(channel)




    async def cmd_shutdownsurrogate(self, channel):
        await self.safe_send_message(channel, "Good bye :wave:")
        self.end = True
        await self.logout()
        await self.close()
        return




if __name__ == '__main__':
    bot = NextBot()
    bot.run()
