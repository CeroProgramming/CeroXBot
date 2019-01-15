import urllib.request

class Setup(object):

    def __init__(self):
        pass

    async def setup(self):

        try:

            owner = await self._get_owner_by_id()
            await self.send_typing(owner)
            await self.send_message(owner, content='Welcome. I am the CeroXBot aka CXBot. You or someone who knows your ID has set you as my owner. If you don\'t know about me, this is probably a mistake, simply ignore me in this case. Otherwise, can we start with the setup? If yes type \'start\'.')
            await self.wait_for_message(timeout=None, author=owner, content='start')
            await self.send_typing(owner)
            await self.send_message(owner, content='Do not use me on diffrent servers in this state of development. If you want to use me on diffrent servers, create multiple instances with a unique bot token per instance.')
            await self.send_typing(owner)
            await self.send_message(owner, content='Do you want to set my name? (This means the name that will be displayed in the developer settings and if you don\'t set a nickname.) (No/Yes)')
            b = await self._wait_for_bool(owner)
            if b:
                await self.send_typing(owner)
                await self.send_message(owner, content='Okay, which one?')
                message = await self.wait_for_message(timeout=None, author=owner)
                await self.edit_profile(username=message.content)
            await self.send_typing(owner)
            await self.send_message(owner, content='Do you like me to have a nickname? (No/Yes)')
            b = await self._wait_for_bool(owner)
            if b:
                await self.send_typing(owner)
                await self.send_message(owner, content='Okay, which one?')
                message = await self.wait_for_message(timeout=None, author=owner)
                self.c.nickname = message.content
                await self.send_typing(owner)
                await self.send_message(owner, content='Shall I try to set my nickname? (Never[0]/Always[1]/Only if added\
                    to a new server[2]')
                self.c.autoSetNickname = await self._wait_for_list(owner, ['0', '1', '2'])
            else:
                del self.c.nickname
            await self.send_typing(owner)
            await self.send_message(owner, content='Do you like to set my avatar now? (No/Yes)')
            b = await self._wait_for_bool(owner)
            if b:
                await self.send_typing(owner)
                await self.send_message(owner, content='Send the picture..')
                url = await self._wait_for_picture_url(owner)
                self.c.avatarUrl = "config/avatar.%s" % (url.split(".")[len(url.split("."))-1])
                user_agent = 'Mozilla/5.0 (Windows; U; Windows NT 5.1; en-US; rv:1.9.0.7) Gecko/2009021910 Firefox/3.0.7'
                headers={'User-Agent':user_agent,}
                request=urllib.request.Request(url,None,headers)
                response = urllib.request.urlopen(request)
                data = response.read()
                await self.edit_profile(avatar=data)
            await self.send_typing(owner)
            await self.send_message(owner, content='Do you want me to use a prefix that is needed to trigger commands? (No/Yes)')
            b = await self._wait_for_bool(owner)
            if b:
                await self.send_typing(owner)
                await self.send_message(owner, content='Which one? It can be a whole string, but I will cut all trailing whitspaces.')
                message = await self.wait_for_message(timeout=None, author=owner)
                while message.content.endswith(' '):
                    message.content = message.content[:-1]
                self.c.prefix = message.content
            else:
                del self.c.prefix
            await self.send_typing(owner)
            await self.send_message(owner, content="Shall I save logs? (No/Yes)")
            self.c.logging = await self._wait_for_bool(owner)
            if self.c.logging:
                await self.send_typing(owner)
                await self.send_message(owner, content='Okay, I log all basic stuff.')
                await self.send_message(owner, content='Shall I also log all messages? (No/Yes)')
                self.c.logMessages = await self._wait_for_bool(owner)
                await self.send_typing(owner)
                await self.send_message(owner, content='Shall I also log all interactions between me and everything else? (No/Yes)')
                self.c.logBotActivities = await self._wait_for_bool(owner)
                await self.send_typing(owner)
                await self.send_message(owner, content='Shall I log all public available user data like online time and played games? (this may or may not generate huge amounts of data) (No/Yes)')
                self.c.logUserActivities = await self._wait_for_bool(owner)
            else:
                self.c.logMessages = False
                self.c.logBotActivities = False
                self.c.logUserActivities = False
            await self.send_typing(owner)
            await self.send_message(owner, content='Do you want me to track all played games? (some functions will not work otherwise) (No/Yes)')
            self.c.trackGameHistory = await self._wait_for_bool(owner)
            await self.send_typing(owner)
            await self.send_message(owner, content='Do you want me to track statistics about how much games were played? (some functions will not work otherwise) (No/Yes)')
            self.c.trackGameStatistics = await self._wait_for_bool(owner)
            await self.send_typing(owner)
            await self.send_message(owner, content='Do you want me to automatically create permament roles for registered games? (No/Yes)')
            self.c.autoCreateGameRoles = await self._wait_for_bool(owner)
            if self.c.autoCreateGameRoles:
                await self.send_typing(owner)
                await self.send_message(owner, content='Do you want me to automatically register games that somebody played? (this may cause unwanted behavior if a game or process is recognized wrong or if someone renamed a game in his settings) (No/Yes)')
                self.c.autoAddGames = await self._wait_for_bool(owner)
                await self.send_typing(owner)
                await self.send_message(owner, content='Do you want me to automatically append roles to users that play the respective game? (No/Yes)')
                self.c.autoGiveGameRoles = await self._wait_for_bool(owner)
                self.c.autoCreateTemporaryGameRoles = False # TODO outsource into config,py
            else:
                await self.send_typing(owner)
                await self.send_message(owner, content='Do you want me to automatically create and append temporary roles for played games? (No/Yes)')
                self.c.autoCreateTemporaryGameRoles = await self._wait_for_bool(owner)
                self.c.autoAddGames = False
                self.c.autoGiveGameRoles = False
            await self.send_typing(owner)
            await self.send_message(owner, content='You can choose between several settings of default user persmissions. You can manually edit them later on.')
            await self.send_typing(owner)
            await self.send_message(owner, content='0: No one except you can use any command unless you explicit allow it later on.')
            await self.send_typing(owner)
            await self.send_message(owner, content='1: Users can per default use several harmless features like surveys and reminders. (suggested)')
            await self.send_typing(owner)
            await self.send_message(owner, content='2: Users can per default use the same as in 1 and have some special commands for temporary channels and such things.')
            await self.send_typing(owner)
            await self.send_message(owner, content='3: Users can per default administrate the complete server (THIS COULD BE DANGEROUS IF YOU DO NOT TRUST YOUR SERVER MEMBERS!!)')
            self.c.defaultCommandPermissions = await self._wait_for_number(owner, 0, 3)
            await self.send_typing(owner)
            await self.send_message(owner, content='.')
            await self.send_typing(owner)
            await self.send_message(owner, content='.')
            await self.send_typing(owner)
            await self.send_message(owner, content='.')
            await self.send_typing(owner)
            await self.send_message(owner, content='```This bot was written by CeroProgramming aka Simon Deckwert. \nIt is licensed under the MIT license. \nIf you want to see the source, visit https://github.com/CeroProgramming/CeroXBot \nIf you find any bugs or feature requests, you can open an issue at https://github.com/CeroProgramming/CeroXBot/issues \nTo see all commands, type %shelp . To see more information about a command, type %shelp \'command\' \nIf you havn\'t already done, you can apply this bot to a server here: https://discordapp.com/oauth2/authorize?client_id=%s&scope=bot&permissions=0```' % (self.c.prefix, self.c.prefix, self.c.clientID))


        except Exception as e:
            print(e)
