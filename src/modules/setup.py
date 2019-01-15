from modules.base import Base

import urllib.request
from discord import Color

class Setup(object):

    def __init__(self):
        pass

    @Base.excep
    async def setup(self):

        owner = await self._get_owner_by_id()
        await self.io_message(owner, 'Welcome. I am the CeroXBot aka CXBot. You or someone who knows your ID has set you as my owner. If you don\'t know about me, this is probably a mistake, simply ignore me in this case. Otherwise, can we start with the setup? If yes type \'start\'.')
        await self.wait_for_message(timeout=None, author=owner, content='start')
        await self.io_message(owner, 'Do not use me on diffrent servers in this state of development. If you want to use me on diffrent servers, create multiple instances with a unique bot token per instance.')
        await self.io_message(owner, 'Do you want to set my name? (This means the name that will be displayed in the developer settings and if you don\'t set a nickname.) (No/Yes)')
        b = await self._wait_for_bool(owner)
        if b:
            await self.io_message(owner, 'Okay, which one?')
            message = await self.wait_for_message(timeout=None, author=owner)
            await self.edit_profile(username=message.content)
        await self.io_message(owner, 'Do you like me to have a nickname? (No/Yes)')
        b = await self._wait_for_bool(owner)
        if b:
            await self.io_message(owner, 'Okay, which one?')
            message = await self.wait_for_message(timeout=None, author=owner)
            self.c.nickname = message.content
            await self.io_message(owner, 'Shall I try to set my nickname? (Never[0]/Always[1]/Only if added to a new server[2]')
            self.c.autoSetNickname = await self._wait_for_list(owner, ['0', '1', '2'])
        else:
            del self.c.nickname
        await self.io_message(owner, 'Do you like to set my avatar now? (No/Yes)')
        b = await self._wait_for_bool(owner)
        if b:
            await self.io_message(owner, 'Send the picture..')
            url = await self._wait_for_picture_url(owner)
            self.c.avatarUrl = "config/avatar.%s" % (url.split(".")[len(url.split("."))-1])
            user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
            headers={'User-Agent':user_agent,}
            request=urllib.request.Request(url,None,headers)
            response = urllib.request.urlopen(request)
            data = response.read()
            await self.edit_profile(avatar=data)
        await self.io_message(owner, 'Do you want me to use a prefix that is needed to trigger commands? (No/Yes)')
        b = await self._wait_for_bool(owner)
        if b:
            await self.io_message(owner, 'Which one? It can be a whole string, but I will cut all trailing whitspaces.')
            message = await self.wait_for_message(timeout=None, author=owner)
            while message.content.endswith(' '):
                message.content = message.content[:-1]
            self.c.prefix = message.content
        else:
            del self.c.prefix
        await self.send_message(owner, content="Shall I save logs? (No/Yes)")
        b = await self._wait_for_bool(owner)
        if b:
            self.c.logging = b
            await self.io_message(owner, 'Okay, I log all basic stuff.')
            await self.io_message(owner, 'Shall I also log all messages? (No/Yes)')
            self.c.logMessages = await self._wait_for_bool(owner)
            await self.io_message(owner, 'Shall I also log all interactions between me and everything else? (No/Yes)')
            self.c.logBotActivities = await self._wait_for_bool(owner)
            await self.io_message(owner, 'Shall I log all public available user data like online time and played games? (this may or may not generate huge amounts of data) (No/Yes)')
            self.c.logUserActivities = await self._wait_for_bool(owner)
        else:
            self.c.logMessages = False
            self.c.logBotActivities = False
            self.c.logUserActivities = False
        await self.io_message(owner, 'Do you want me to track all played games? (some functions will not work otherwise) (No/Yes)')
        self.c.trackGameHistory = await self._wait_for_bool(owner)
        await self.io_message(owner, 'Do you want me to track statistics about how much games were played? (some functions will not work otherwise) (No/Yes)')
        self.c.trackGameStatistics = await self._wait_for_bool(owner)
        await self.io_message(owner, 'Do you want me to automatically create permament roles for registered games? (No/Yes)')
        self.c.autoCreateGameRoles = await self._wait_for_bool(owner)
        if self.c.autoCreateGameRoles:
            await self.io_message(owner, 'Do you want me to automatically register games that somebody played? (this may cause unwanted behavior if a game or process is recognized wrong or if someone renamed a game in his settings) (No/Yes)')
            self.c.autoAddGames = await self._wait_for_bool(owner)
            await self.io_message(owner, 'Do you want me to automatically append roles to users that play the respective game? (No/Yes)')
            self.c.autoGiveGameRoles = await self._wait_for_bool(owner)
            self.c.autoCreateTemporaryGameRoles = False # TODO outsource into config,py
        else:
            await self.io_message(owner, 'Do you want me to automatically create and append temporary roles for played games? (No/Yes)')
            self.c.autoCreateTemporaryGameRoles = await self._wait_for_bool(owner)
            self.c.autoAddGames = False
            self.c.autoGiveGameRoles = False
        await self.io_message(owner, 'You can choose between several settings of default user persmissions. You can manually edit them later on.')
        await self.io_message(owner, '0: No one except you can use any command unless you explicit allow it later on.')
        await self.io_message(owner, '1: Users can per default use several harmless features like surveys and reminders. (suggested)')
        await self.io_message(owner, '2: Users can per default use the same as in 1 and have some special commands for temporary channels and such things.')
        await self.io_message(owner, '3: Users can per default administrate the complete server (THIS COULD BE DANGEROUS IF YOU DO NOT TRUST YOUR SERVER MEMBERS!!)')
        self.c.defaultCommandPermissions = await self._wait_for_number(owner, 0, 3)
        await self.io_message(owner, '...')
        await self.io_message(owner, '_**Welcome. You can now start to use me.**_')
        await self.io_message(owner, 'This bot was written by CeroProgramming.')
        e = await self.create_embed("Github CeroProgramming", "https://github.com/CeroProgramming", "GitHub Profile URL", Color.dark_purple(), "CeroProgramming", "https://github.com/CeroProgramming/", "https://avatars3.githubusercontent.com/u/22818389?s=460&v=4", "https://proxy.duckduckgo.com/iu/?u=https%3A%2F%2Fimage.freepik.com%2Ffree-icon%2Fgithub-logo_318-53553.jpg&f=1")
        await self.io_embed(message.channel, e)
        await self.io_message(owner, 'I\'m licensed under the MIT license.')
        await self.io_message(owner, '```MIT License \n\n Copyright (c) 2017 CeroProgramming\n\nPermission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:\n\nThe above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.\n\nTHE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.```')
        await self.io_message(owner, 'If you want to see the source, visit https://github.com/CeroProgramming/CeroXBot')
        await self.io_message(owner, 'If you find any bugs or if you have feature requests, you can open an issue at https://github.com/CeroProgramming/CeroXBot/issues')
        await self.io_message(owner, 'To see all commands, type %shelp . To see more information about a command, type %shelp \'command\' \nIf you havn\'t already done, you can apply this bot to a server here: https://discordapp.com/oauth2/authorize?client_id=%s&scope=bot&permissions=0' % (self.c.prefix if self.c.prefix else '', self.c.prefix if self.c.prefix else '', self.c.clientID))
        self.c.firstStart = False
